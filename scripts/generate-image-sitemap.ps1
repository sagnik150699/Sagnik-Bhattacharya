$blogDir = Join-Path $PSScriptRoot "..\public\blog"
$publicDir = Join-Path $PSScriptRoot "..\public"

$results = @()

# Process each blog HTML file
Get-ChildItem (Join-Path $blogDir "*.html") | ForEach-Object {
    $content = [System.IO.File]::ReadAllText($_.FullName)
    $slug = $_.BaseName
    
    # Extract title
    $title = ""
    if ($content -match '<title>([^<]+)</title>') { $title = $matches[1] }
    
    # Extract og:image:alt
    $alt = ""
    if ($content -match 'property="og:image:alt"\s+content="([^"]+)"') { $alt = $matches[1] }
    
    $results += [PSCustomObject]@{
        Slug = $slug
        Title = $title
        Alt = $alt
    }
}

# Output as JSON
$results | ConvertTo-Json | Out-File (Join-Path $PSScriptRoot "blog-metadata.json") -Encoding utf8
Write-Host "Extracted metadata for $($results.Count) posts"
$results | Format-Table -AutoSize
