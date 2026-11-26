param([ValidateSet('paper','slides')][string]$Target='paper')
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing
$docRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$images=@(Get-ChildItem -LiteralPath (Join-Path $docRoot ('build/' + $Target + '-pages')) -Filter 'page-*.png' | Sort-Object Name)
if ($images.Count -eq 0) { throw 'Render PDF pages first with build.ps1 -Render.' }
$cellW=850
$cellH=if ($Target -eq 'paper') {1235} else {520}
$perSheet=4
for ($offset=0; $offset -lt $images.Count; $offset+=$perSheet) {
    $bitmap=New-Object Drawing.Bitmap (2*$cellW),(2*$cellH)
    $graphics=[Drawing.Graphics]::FromImage($bitmap)
    $graphics.Clear([Drawing.Color]::FromArgb(223,228,233))
    $graphics.InterpolationMode=[Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
    $font=New-Object Drawing.Font 'Arial',16
    try {
        for ($j=0; $j -lt $perSheet -and ($offset+$j) -lt $images.Count; $j++) {
            $img=[Drawing.Image]::FromFile($images[$offset+$j].FullName)
            try {
                $x=($j%2)*$cellW
                $y=[math]::Floor($j/2)*$cellH
                $scale=[math]::Min(($cellW-20)/$img.Width,($cellH-42)/$img.Height)
                $graphics.DrawString(($Target + ' PDF page ' + ($offset+$j+1)), $font, [Drawing.Brushes]::Black, [single]($x+10), [single]($y+5))
                $graphics.DrawImage($img,[int]($x+10),[int]($y+32),[int]($img.Width*$scale),[int]($img.Height*$scale))
            } finally {$img.Dispose()}
        }
        $sheetPath=Join-Path $docRoot ('build/' + $Target + '-sheet-' + ([int]($offset/$perSheet)+1) + '.png')
        $bitmap.Save($sheetPath,[Drawing.Imaging.ImageFormat]::Png)
        Write-Output $sheetPath
    } finally {$font.Dispose();$graphics.Dispose();$bitmap.Dispose()}
}
