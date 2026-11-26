[CmdletBinding()]
param(
    [string]$Revision = '498dea06df250964013b2abb2b06c94d341b223b',
    [string]$ProjectRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..')),
    [string]$SnapshotRoot = (Join-Path (Split-Path $PSScriptRoot -Parent) 'snapshot'),
    [string]$ExtractTo
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
Add-Type -AssemblyName System.IO.Compression.FileSystem
$utf8 = New-Object System.Text.UTF8Encoding($false, $true)

function Git-Value([string[]]$Arguments) {
    $value = & git -C $ProjectRoot @Arguments
    if ($LASTEXITCODE -ne 0) { throw "Git failed: $($Arguments -join ' ')" }
    return ($value -join "`n").Trim()
}

function Hash-Bytes([byte[]]$Bytes) {
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($hasher.ComputeHash($Bytes))).Replace('-', '').ToLowerInvariant() }
    finally { $hasher.Dispose() }
}

function Write-Json([string]$Path, $Value) {
    [IO.File]::WriteAllText($Path, ($Value | ConvertTo-Json -Depth 12) + "`n", $utf8)
}

function Read-ArchiveText($Archive, [string]$Name) {
    $entry = $Archive.GetEntry($Name)
    if ($null -eq $entry) { return '' }
    $reader = New-Object IO.StreamReader($entry.Open(), $utf8)
    try { return $reader.ReadToEnd() } finally { $reader.Dispose() }
}

function Match-Value([string]$Text, [string]$Pattern) {
    $match = [regex]::Match($Text, $Pattern)
    if ($match.Success) { return $match.Groups[1].Value }
    return $null
}

function Safe-Child([string]$Root, [string]$Relative) {
    $fullRoot = [IO.Path]::GetFullPath($Root).TrimEnd('\', '/')
    $candidate = [IO.Path]::GetFullPath((Join-Path $fullRoot $Relative))
    if (-not $candidate.StartsWith($fullRoot + [IO.Path]::DirectorySeparatorChar, [StringComparison]::OrdinalIgnoreCase)) {
        throw "Archive path escapes the destination: $Relative"
    }
    return $candidate
}

$ProjectRoot = (Resolve-Path -LiteralPath $ProjectRoot).Path
$commit = Git-Value @('rev-parse', '--verify', ($Revision + '^{commit}'))
$tree = Git-Value @('rev-parse', ($commit + '^{tree}'))
$commitDate = Git-Value @('show', '-s', '--format=%cI', $commit)
$commitSubject = Git-Value @('show', '-s', '--format=%s', $commit)
$gitBlobs = @{}
foreach ($line in ((Git-Value @('-c', 'core.quotepath=false', 'ls-tree', '-r', $commit)) -split "`n")) {
    if ($line -match '^\d+ blob ([a-f0-9]+)\t(.+)$') { $gitBlobs[$Matches[2]] = $Matches[1] }
}
$snapshotId = $commitDate.Substring(0, 10) + '-' + $commit.Substring(0, 7)
$destination = [IO.Path]::GetFullPath((Join-Path $SnapshotRoot $snapshotId))
$archivePath = Join-Path $destination 'source.zip'
$manifestPath = Join-Path $destination 'manifest.json'

if (Test-Path -LiteralPath $destination) {
    if (-not (Test-Path -LiteralPath $manifestPath) -or -not (Test-Path -LiteralPath $archivePath)) {
        throw "Incomplete snapshot exists at $destination. Preserve it for inspection; choose a different SnapshotRoot."
    }
    $manifest = Get-Content -LiteralPath $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($manifest.commit -ne $commit -or $manifest.tree -ne $tree) {
        throw 'Existing snapshot belongs to another revision; it will not be overwritten.'
    }
    $archiveHash = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()
    if ($archiveHash -ne $manifest.archive.sha256) { throw 'Existing snapshot archive failed its checksum.' }
} else {
    New-Item -ItemType Directory -Path $destination -Force | Out-Null
    & git -C $ProjectRoot -c core.autocrlf=false archive --format=zip --output=$archivePath $commit
    if ($LASTEXITCODE -ne 0) { throw 'git archive failed; no manifest has been published.' }
    $manifest = $null
}

$archive = [IO.Compression.ZipFile]::OpenRead($archivePath)
try {
    $files = @($archive.Entries | Where-Object { $_.Name -ne '' } | Sort-Object FullName | ForEach-Object {
        $entry = $_
        # Validate names even when we are only calculating hashes.
        $null = Safe-Child $destination ('contents/' + $entry.FullName)
        $stream = $entry.Open()
        $memory = New-Object IO.MemoryStream
        try {
            $stream.CopyTo($memory)
            $bytes = $memory.ToArray()
            $gitHasher = [Security.Cryptography.SHA1]::Create()
            try {
                $header = [Text.Encoding]::ASCII.GetBytes('blob ' + $bytes.Length + [char]0)
                $null = $gitHasher.TransformBlock($header, 0, $header.Length, $header, 0)
                $null = $gitHasher.TransformFinalBlock($bytes, 0, $bytes.Length)
                $blobHash = ([BitConverter]::ToString($gitHasher.Hash)).Replace('-', '').ToLowerInvariant()
            } finally { $gitHasher.Dispose() }
            if (-not $gitBlobs.ContainsKey($entry.FullName) -or $blobHash -ne $gitBlobs[$entry.FullName]) {
                throw "Archived bytes differ from the pinned Git blob: $($entry.FullName)"
            }
            $lfHash = $null
            try {
                $text = $utf8.GetString($bytes)
                if (-not $text.Contains([char]0)) {
                    $lfHash = Hash-Bytes ($utf8.GetBytes($text.Replace("`r`n", "`n")))
                }
            } catch [Text.DecoderFallbackException] { }
            [pscustomobject][ordered]@{
                path = $entry.FullName
                bytes = $entry.Length
                sha256 = Hash-Bytes $bytes
                sha256_lf = $lfHash
                git_blob_sha1 = $blobHash
            }
        } finally { $stream.Dispose(); $memory.Dispose() }
    })

    if ($null -ne $manifest) {
        if ($files.Count -ne $manifest.file_count) { throw 'Archive file count differs from the manifest.' }
        $expected = @{}
        foreach ($file in $manifest.files) { $expected[$file.path] = $file }
        foreach ($file in $files) {
            if (-not $expected.ContainsKey($file.path) -or $file.sha256 -ne $expected[$file.path].sha256) {
                throw "Archive content failed its manifest check: $($file.path)"
            }
        }
    } else {
        $trackedPaths = @((Git-Value @('-c', 'core.quotepath=false', 'ls-tree', '-r', '--name-only', $commit)) -split "`n")
        $archivedPaths = @($files | ForEach-Object { $_.path })
        $pathDifference = @(Compare-Object -ReferenceObject $trackedPaths -DifferenceObject $archivedPaths)
        if ($pathDifference.Count -ne 0) { throw 'Archive paths differ from tracked paths; inspect export-ignore or submodules.' }

        $lockText = Read-ArchiveText $archive 'uv.lock'
        $projectText = Read-ArchiveText $archive 'pyproject.toml'
        $primaryServer = Read-ArchiveText $archive 'experiments/slurm/serve.sbatch'
        $secondServer = Read-ArchiveText $archive 'experiments/slurm/serve_second.sbatch'
        $cliText = Read-ArchiveText $archive 'speccheck/cli.py'
        $reviewedRevision = $commit -in @('18752f24cbfd625d23d7ae5bd967af43ee7af718', '498dea06df250964013b2abb2b06c94d341b223b')
        $lockedPackages = @{}
        foreach ($match in [regex]::Matches($lockText, '(?m)^name = "([^"]+)"\r?\nversion = "([^"]+)"')) {
            $lockedPackages[$match.Groups[1].Value] = $match.Groups[2].Value
        }
        $manifest = [ordered]@{
            schema_version = 1
            snapshot_id = $snapshotId
            captured_at_utc = [DateTime]::UtcNow.ToString('o')
            commit = $commit
            tree = $tree
            commit_date = $commitDate
            commit_subject = $commitSubject
            content_basis = 'Exact tracked file contents at the Git revision, independent of the current working tree.'
            file_count = $files.Count
            uncompressed_bytes = ($files | Measure-Object -Property bytes -Sum).Sum
            archive = [ordered]@{
                file = 'source.zip'
                bytes = (Get-Item -LiteralPath $archivePath).Length
                sha256 = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()
            }
            configuration = [ordered]@{
                configuration_scope = 'Values extracted from this revision; individual historical runs retain their own recorded settings. Missing/unrecognized fields are null and require review.'
                behavior_defaults_manually_reviewed = $reviewedRevision
                python_requirement = Match-Value $projectText '(?m)^requires-python = "([^"]+)"'
                dependency_source = 'pyproject.toml and uv.lock'
                locked_packages = $lockedPackages
                primary_model = Match-Value $primaryServer '(?m)^MODEL=([^\r\n]+)'
                second_model = Match-Value $secondServer '(?m)^MODEL=([^\r\n]+)'
                primary_context_tokens = Match-Value $primaryServer '(?m)^\s*--max-model-len\s+(\d+)'
                second_context_tokens = Match-Value $secondServer '(?m)^\s*--max-model-len\s+(\d+)'
                samples_per_rule_default = Match-Value $cliText 'add_argument\("--samples"[^\r\n]*default=(\d+)'
                temperature_default = Match-Value $cliText 'add_argument\("--temperature"[^\r\n]*default=([\d.]+)'
                symbol_sets_default = Match-Value $cliText 'add_argument\("--symbol-sets"[^\r\n]*default=(\d+)'
                optional_second_reader_default = $(if ($reviewedRevision) { $false } else { $null })
                optional_incremental_default = $(if ($commit -eq '498dea06df250964013b2abb2b06c94d341b223b') { $false } else { $null })
                outcome_pair_questions_default = $(if ($reviewedRevision) { $true } else { $null })
                source_paths = @('speccheck/cli.py', 'speccheck/formalize.py', 'speccheck/probe.py', 'experiments/slurm/serve.sbatch', 'experiments/slurm/serve_second.sbatch')
            }
            provenance_limits = @(
                'This commit identifies the documentation baseline, not the code revision that generated every historical result.',
                'Historical experiment files generally do not record a source commit. Preserve their timestamps, configurations, inputs and raw samples without inventing missing provenance.',
                'Archive includes stored results and overlays together with their original result files. It excludes Git history, local untracked files, virtual environments, caches, model weights and external GPU/server state.',
                'Recorded model names and settings do not guarantee byte-identical regeneration of stochastic model outputs.',
                'sha256 is the exact archived byte hash. sha256_lf normalizes CRLF to LF only for valid UTF-8 text, to distinguish Windows checkout line endings from substantive changes.'
            )
            files = $files
        }
        Write-Json $manifestPath $manifest
        [IO.File]::WriteAllText((Join-Path $destination 'SHA256SUMS.txt'),
            $manifest.archive.sha256 + "  source.zip`n" +
            (Get-FileHash -LiteralPath $manifestPath -Algorithm SHA256).Hash.ToLowerInvariant() + "  manifest.json`n", $utf8)
    }

    if ($ExtractTo) {
        $ExtractTo = [IO.Path]::GetFullPath($ExtractTo)
        if (Test-Path -LiteralPath $ExtractTo) {
            foreach ($file in $files) {
                $target = Safe-Child $ExtractTo $file.path
                if (-not (Test-Path -LiteralPath $target -PathType Leaf) -or
                    (Get-FileHash -LiteralPath $target -Algorithm SHA256).Hash.ToLowerInvariant() -ne $file.sha256) {
                    throw "Existing extracted baseline differs at $($file.path); it will not be overwritten."
                }
            }
        } else {
            New-Item -ItemType Directory -Path $ExtractTo -Force | Out-Null
            foreach ($entry in $archive.Entries) {
                if ($entry.Name -eq '') { continue }
                $target = Safe-Child $ExtractTo $entry.FullName
                New-Item -ItemType Directory -Path (Split-Path $target -Parent) -Force | Out-Null
                [IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $target, $false)
            }
        }
    }
} finally { $archive.Dispose() }

[pscustomobject]@{
    Snapshot = $snapshotId
    Commit = $commit
    Files = $files.Count
    Archive = $archivePath
    ArchiveBytes = (Get-Item -LiteralPath $archivePath).Length
    SHA256 = (Get-FileHash -LiteralPath $archivePath -Algorithm SHA256).Hash.ToLowerInvariant()
    ExtractedBaseline = $ExtractTo
} | Format-List
