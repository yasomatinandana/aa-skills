<#
  Builds a claude.ai-uploadable plugin zip from this repo.

  Writes entries manually with forward-slash separators, since
  Compress-Archive / ZipFile.CreateFromDirectory under Windows PowerShell's
  .NET Framework runtime bake in backslash separators, which claude.ai's
  upload validator rejects as "invalid characters".

  Zips the whole repo root (so .claude-plugin/plugin.json lands at the
  archive's top level), excluding VCS and local-harness directories.
#>

Add-Type -AssemblyName System.IO.Compression
Add-Type -AssemblyName System.IO.Compression.FileSystem

$srcRoot = Join-Path $PSScriptRoot "../.."

$srcRootFull = (Resolve-Path $srcRoot).Path.TrimEnd('\')
$destZipFull = Join-Path (Split-Path $srcRootFull -Parent) "aa-skills-claude-skills.zip"

if (Test-Path $destZipFull) { Remove-Item $destZipFull -Force }

# Local harness state and VCS internals - not part of the plugin.
$excludeDirNames = @('.git', '.hermes', '.claude', '.codex', '.cursor', 'node_modules')

$files = Get-ChildItem -Path $srcRootFull -Recurse -File | Where-Object {
    $relative = $_.FullName.Substring($srcRootFull.Length + 1)
    $parts = $relative -split '\\'
    $excluded = $false
    foreach ($ex in $excludeDirNames) {
        if ($parts -contains $ex) { $excluded = $true; break }
    }
    -not $excluded
}

$fs = [System.IO.File]::Open($destZipFull, [System.IO.FileMode]::CreateNew)
$archive = New-Object System.IO.Compression.ZipArchive($fs, [System.IO.Compression.ZipArchiveMode]::Create)

foreach ($f in $files) {
    $relative = $f.FullName.Substring($srcRootFull.Length + 1)
    $entryName = $relative -replace '\\', '/'
    $entry = $archive.CreateEntry($entryName, [System.IO.Compression.CompressionLevel]::Optimal)
    $entryStream = $entry.Open()
    $fileStream = [System.IO.File]::OpenRead($f.FullName)
    $fileStream.CopyTo($entryStream)
    $fileStream.Close()
    $entryStream.Close()
}

$archive.Dispose()
$fs.Close()

Write-Output "Wrote $destZipFull ($($files.Count) entries)"
