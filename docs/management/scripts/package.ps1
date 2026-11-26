param([string]$DestinationPath, [string]$PaperPdf, [string]$SlidesPdf)
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem
$docRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
if (-not $DestinationPath) { $DestinationPath=Join-Path $docRoot 'speccheck-management-2026-11-25.zip' }
$DestinationPath=[IO.Path]::GetFullPath($DestinationPath)
if ($SlidesPdf) {
    $SlidesPdf=(Resolve-Path -LiteralPath $SlidesPdf).Path
}
if ($PaperPdf) {
    $PaperPdf=(Resolve-Path -LiteralPath $PaperPdf).Path
}
foreach ($required in @('paper.pdf','slides.pdf','README.md','UPDATE.md','EDITION-2026-11-25.md','evidence/claims.json','evidence/metrics.json','evidence/validation.json','snapshot/2026-11-24-18752f2/source.zip','snapshot/2026-11-24-498dea0/source.zip')) {
    if (-not (Test-Path -LiteralPath (Join-Path $docRoot $required))) { throw "Missing deliverable: $required" }
}
$pending=New-Object 'System.Collections.Generic.Stack[string]'
$pending.Push($docRoot)
$files=New-Object 'System.Collections.Generic.List[System.IO.FileInfo]'
while ($pending.Count -gt 0) {
    foreach ($entry in Get-ChildItem -LiteralPath $pending.Pop() -Force) {
        if (($entry.Attributes -band [IO.FileAttributes]::ReparsePoint) -ne 0) { continue }
        if ($entry.PSIsContainer) {
            if ($entry.Name -notin @('build','.git','__pycache__')) { $pending.Push($entry.FullName) }
        } elseif ($entry.FullName -ne $DestinationPath -and $entry.Name -notlike 'speccheck-management-*.zip*' -and
                  $entry.Name -notmatch '^(paper|slides)-.+\.pdf$' -and
                  ($entry.FullName -ne $SlidesPdf -or $entry.FullName -eq (Join-Path $docRoot 'slides.pdf')) -and
                  ($entry.FullName -ne $PaperPdf -or $entry.FullName -eq (Join-Path $docRoot 'paper.pdf'))) {
            $files.Add($entry)
        }
    }
}
$temporary=Join-Path $docRoot 'build/package.tmp.zip'
New-Item -ItemType Directory -Force -Path (Split-Path $temporary -Parent) | Out-Null
$stream=[IO.File]::Open($temporary,[IO.FileMode]::Create,[IO.FileAccess]::ReadWrite)
$zip=New-Object IO.Compression.ZipArchive($stream,[IO.Compression.ZipArchiveMode]::Create)
try {
    foreach ($file in ($files | Sort-Object FullName)) {
        $relative=$file.FullName.Substring($docRoot.Length+1).Replace('\','/')
        # Package reviewed replacements under the normal names while leaving
        # earlier PDFs available to any open viewer in the working folder.
        $source=if ($SlidesPdf -and $relative -eq 'slides.pdf') { $SlidesPdf }
                elseif ($PaperPdf -and $relative -eq 'paper.pdf') { $PaperPdf }
                else { $file.FullName }
        [IO.Compression.ZipFileExtensions]::CreateEntryFromFile($zip,$source,$relative,[IO.Compression.CompressionLevel]::Optimal) | Out-Null
    }
} finally {$zip.Dispose();$stream.Dispose()}
Copy-Item -LiteralPath $temporary -Destination $DestinationPath -Force
$checksum=(Get-FileHash -LiteralPath $DestinationPath -Algorithm SHA256).Hash.ToLowerInvariant()
[IO.File]::WriteAllText(($DestinationPath+'.sha256'),$checksum+'  '+[IO.Path]::GetFileName($DestinationPath)+"`n",(New-Object Text.UTF8Encoding($false)))
[pscustomobject]@{Package=$DestinationPath; Files=$files.Count; Bytes=(Get-Item -LiteralPath $DestinationPath).Length; SHA256=$checksum} | Format-List
