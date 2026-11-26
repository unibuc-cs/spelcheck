[CmdletBinding()]
param(
    [Parameter(Mandatory = $true)][string]$NewProjectDirectory,
    [string]$ManifestPath = (Join-Path (Split-Path $PSScriptRoot -Parent) 'snapshot/2026-11-24-498dea0/manifest.json'),
    [string]$OutputPath = (Join-Path (Split-Path $PSScriptRoot -Parent) 'build/snapshot-diff.json')
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version Latest
$utf8 = New-Object System.Text.UTF8Encoding($false, $true)
$root = (Resolve-Path -LiteralPath $NewProjectDirectory).Path.TrimEnd('\', '/')
$manifest = Get-Content -LiteralPath $ManifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
$baseline = @{}
foreach ($file in $manifest.files) { $baseline[$file.path] = $file }

function Hash-Bytes([byte[]]$Bytes) {
    $hasher = [Security.Cryptography.SHA256]::Create()
    try { return ([BitConverter]::ToString($hasher.ComputeHash($Bytes))).Replace('-', '').ToLowerInvariant() }
    finally { $hasher.Dispose() }
}

function File-Hashes([string]$Path) {
    $bytes = [IO.File]::ReadAllBytes($Path)
    $lfHash = $null
    try {
        $text = $utf8.GetString($bytes)
        if (-not $text.Contains([char]0)) {
            $lfHash = Hash-Bytes ($utf8.GetBytes($text.Replace("`r`n", "`n")))
        }
    } catch [Text.DecoderFallbackException] { }
    return [pscustomobject]@{ sha256 = Hash-Bytes $bytes; sha256_lf = $lfHash; bytes = $bytes.Length }
}

function Affected-Sections([string]$Path) {
    switch -Regex ($Path) {
        '^speccheck/(formalize|probe|llm|logic)\.py$' { 'Formal model and seven formalization steps'; 'Formal guarantees and limitations'; break }
        '^speccheck/checks\.py$' { 'Solver algorithms and finding semantics'; 'Formal guarantees and limitations'; break }
        '^speccheck/change\.py$' { 'OpenSpec merge, provenance and change attribution'; break }
        '^speccheck/(explain|refine|cli)\.py$' { 'Pipeline interfaces, reporting and optional branches'; break }
        '^tests/' { 'Engineering verification and worked-example checks'; break }
        '^experiments/results/' { 'Evaluation tables, charts and claims'; 'Saved example outputs'; break }
        '^experiments/sets/|^specs/' { 'Running examples'; 'Benchmark inventory and expected defects'; break }
        '^experiments/slurm/' { 'Deployment, models and scale limits'; break }
        '^experiments/' { 'Evaluation methodology and scoring'; break }
        '^(pyproject\.toml|uv\.lock)$' { 'Build and reproduction environment'; break }
        '^(research(_log)?|plan|README|GUIDE)\.md$' { 'Project status, design decisions and evidence reconciliation'; break }
        default { 'Review against the evidence index before deciding whether the paper or slides change' }
    }
}

$skipDirectories = @('.git', '.venv', 'venv', '__pycache__', '.pytest_cache', '.mypy_cache', '.ruff_cache', '.idea', '.jbeval', '.scratch', 'node_modules', 'out', 'build', 'dist', '.cache', '.speccheck')
$pending = New-Object 'System.Collections.Generic.Stack[string]'
$pending.Push($root)
$current = @{}
$skippedLinks = New-Object 'System.Collections.Generic.List[string]'
while ($pending.Count -gt 0) {
    $directory = $pending.Pop()
    foreach ($item in Get-ChildItem -LiteralPath $directory -Force) {
        $relative = $item.FullName.Substring($root.Length + 1).Replace('\', '/')
        if (($item.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) {
            $skippedLinks.Add($relative)
            continue
        }
        if ($item.PSIsContainer) {
            if ($skipDirectories -contains $item.Name -or $relative -eq 'docs/management') { continue }
            $pending.Push($item.FullName)
        } else {
            if (($item.Name -like '.env*' -or $item.Name -like 'api_key*') -and -not $baseline.ContainsKey($relative)) { continue }
            if ($item.Extension -eq '.pyc') { continue }
            $current[$relative] = $item.FullName
        }
    }
}

$changes = New-Object 'System.Collections.Generic.List[object]'
$lineEndings = New-Object 'System.Collections.Generic.List[string]'
$unchanged = 0
foreach ($path in @($baseline.Keys | Sort-Object)) {
    if (-not $current.ContainsKey($path)) {
        $changes.Add([pscustomobject]@{ kind = 'removed'; path = $path; before_sha256 = $baseline[$path].sha256; after_sha256 = $null; affected_sections = @(Affected-Sections $path) })
        continue
    }
    $hashes = File-Hashes $current[$path]
    if ($hashes.sha256 -eq $baseline[$path].sha256) { $unchanged++ }
    elseif ($null -ne $baseline[$path].sha256_lf -and $hashes.sha256_lf -eq $baseline[$path].sha256_lf) {
        $lineEndings.Add($path)
    } else {
        $changes.Add([pscustomobject]@{ kind = 'changed'; path = $path; before_sha256 = $baseline[$path].sha256; after_sha256 = $hashes.sha256; affected_sections = @(Affected-Sections $path) })
    }
}
foreach ($path in @($current.Keys | Sort-Object)) {
    if ($baseline.ContainsKey($path)) { continue }
    $hashes = File-Hashes $current[$path]
    $changes.Add([pscustomobject]@{ kind = 'added'; path = $path; before_sha256 = $null; after_sha256 = $hashes.sha256; affected_sections = @(Affected-Sections $path) })
}

$report = [ordered]@{
    schema_version = 1
    baseline_snapshot = $manifest.snapshot_id
    baseline_commit = $manifest.commit
    compared_at_utc = [DateTime]::UtcNow.ToString('o')
    new_project_directory = $root
    counts = [ordered]@{
        added = @($changes | Where-Object { $_.kind -eq 'added' }).Count
        changed = @($changes | Where-Object { $_.kind -eq 'changed' }).Count
        removed = @($changes | Where-Object { $_.kind -eq 'removed' }).Count
        unchanged_bytes = $unchanged
        line_endings_only = $lineEndings.Count
    }
    affected_sections = @($changes | ForEach-Object { $_.affected_sections } | Sort-Object -Unique)
    changes = @($changes.ToArray())
    line_endings_only = @($lineEndings.ToArray())
    skipped_reparse_points = @($skippedLinks.ToArray())
    comparison_policy = @(
        'Compare all baseline paths and new project files, excluding documentation deliverables under docs/management, runtime caches, virtual environments, build output and untracked local credentials.',
        'CRLF-versus-LF differences in valid UTF-8 text are listed separately. Exact archived SHA256 values remain unchanged in the manifest.',
        'No Git repository is required. No source files are modified. New result files are evidence candidates, not permission to pool incompatible experiments.',
        'Affected sections are review suggestions; consult the evidence index for the exact claims, figures and algorithms to update.'
    )
}
$OutputPath = [IO.Path]::GetFullPath($OutputPath)
New-Item -ItemType Directory -Path (Split-Path $OutputPath -Parent) -Force | Out-Null
[IO.File]::WriteAllText($OutputPath, ($report | ConvertTo-Json -Depth 10) + "`n", $utf8)
[pscustomobject]@{
    Baseline = $manifest.snapshot_id
    Added = $report.counts.added
    Changed = $report.counts.changed
    Removed = $report.counts.removed
    LineEndingsOnly = $report.counts.line_endings_only
    Report = $OutputPath
} | Format-List
