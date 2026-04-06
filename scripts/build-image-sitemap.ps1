$blogDir = Join-Path $PSScriptRoot "..\public\blog"
$metaFile = Join-Path $PSScriptRoot "blog-metadata.json"
$outFile = Join-Path $PSScriptRoot "..\public\sitemap.xml"

$meta = Get-Content $metaFile -Raw | ConvertFrom-Json
$base = "https://sagnikbhattacharya.com"

# Build a slug->metadata lookup
$lookup = @{}
foreach ($m in $meta) { $lookup[$m.Slug] = $m }

# Read existing sitemap to preserve lastmod/changefreq/priority
[xml]$oldSitemap = Get-Content (Join-Path $PSScriptRoot "..\public\sitemap.xml") -Raw
$oldUrls = @{}
foreach ($u in $oldSitemap.urlset.url) {
    $oldUrls[$u.loc] = @{
        lastmod = $u.lastmod
        changefreq = $u.changefreq
        priority = $u.priority
    }
}

$sb = [System.Text.StringBuilder]::new()
[void]$sb.AppendLine('<?xml version="1.0" encoding="UTF-8"?>')
[void]$sb.AppendLine('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
[void]$sb.AppendLine('        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">')

# Helper to write a URL entry
function Add-UrlEntry($loc, $lastmod, $changefreq, $priority, $images) {
    [void]$sb.AppendLine("  <url>")
    [void]$sb.AppendLine("    <loc>$loc</loc>")
    [void]$sb.AppendLine("    <lastmod>$lastmod</lastmod>")
    [void]$sb.AppendLine("    <changefreq>$changefreq</changefreq>")
    [void]$sb.AppendLine("    <priority>$priority</priority>")
    foreach ($img in $images) {
        [void]$sb.AppendLine("    <image:image>")
        [void]$sb.AppendLine("      <image:loc>$($img.loc)</image:loc>")
        if ($img.title) {
            $t = [System.Security.SecurityElement]::Escape($img.title)
            [void]$sb.AppendLine("      <image:title>$t</image:title>")
        }
        if ($img.caption) {
            $c = [System.Security.SecurityElement]::Escape($img.caption)
            [void]$sb.AppendLine("      <image:caption>$c</image:caption>")
        }
        [void]$sb.AppendLine("    </image:image>")
    }
    [void]$sb.AppendLine("  </url>")
}

# Static pages with profile image
$profileImg = @{ loc = "$base/sagnik-bhattacharya.png"; title = "Sagnik Bhattacharya"; caption = "Sagnik Bhattacharya - Tech Educator, Flutter and Excel Instructor, Founder of Coding Liquids" }
$flutterCourseImg = @{
    loc = "$base/images/the-complete-flutter-guide-build-android-ios-and-web-apps.jpg"
    title = "The Complete Flutter Guide: Build Android, iOS and Web apps"
    caption = "The Complete Flutter Guide: Build Android, iOS and Web apps course thumbnail featuring the Flutter logo, Virginia Thorn, and Sagnik Bhattacharya."
}

$staticPages = @(
    @{ loc = "$base/"; lastmod = "2026-04-01"; changefreq = "weekly"; priority = "1.0"; images = @($profileImg) },
    @{ loc = "$base/about"; lastmod = "2026-04-01"; changefreq = "monthly"; priority = "0.8"; images = @($profileImg) },
    @{ loc = "$base/courses"; lastmod = "2026-04-06"; changefreq = "monthly"; priority = "0.9"; images = @($profileImg, $flutterCourseImg) },
    @{ loc = "$base/services"; lastmod = "2026-04-01"; changefreq = "monthly"; priority = "0.8"; images = @($profileImg) },
    @{ loc = "$base/contact"; lastmod = "2026-04-01"; changefreq = "monthly"; priority = "0.7"; images = @($profileImg) },
    @{ loc = "$base/blog"; lastmod = "2026-04-01"; changefreq = "daily"; priority = "0.9"; images = @($profileImg) }
)

foreach ($p in $staticPages) {
    $info = $oldUrls[$p.loc]
    $lm = if ($info -and $info.lastmod -and ([datetime]$info.lastmod -ge [datetime]$p.lastmod)) { $info.lastmod } else { $p.lastmod }
    $cf = if ($info) { $info.changefreq } else { $p.changefreq }
    $pr = if ($info) { $info.priority } else { $p.priority }
    $images = if ($p.images) { $p.images } else { @($profileImg) }
    Add-UrlEntry $p.loc $lm $cf $pr $images
}

# Blog posts - iterate through the old sitemap order to preserve ordering
foreach ($u in $oldSitemap.urlset.url) {
    $loc = $u.loc
    if ($loc -notmatch '/blog/[^/]+$' -or $loc -eq "$base/blog") { continue }
    
    $slug = $loc -replace '.*/blog/', ''
    $m = $lookup[$slug]
    if (-not $m) { 
        # No metadata found, just add without image
        Add-UrlEntry $loc $u.lastmod $u.changefreq $u.priority @()
        continue
    }
    
    $imgLoc = "$base/blog/images/$slug-sagnik-bhattacharya-coding-liquids.jpg"
    $img = @{
        loc = $imgLoc
        title = $m.Title
        caption = $m.Alt
    }
    Add-UrlEntry $loc $u.lastmod $u.changefreq $u.priority @($img)
}

[void]$sb.AppendLine("</urlset>")

$sb.ToString() | Out-File $outFile -Encoding utf8 -NoNewline
Write-Host "Sitemap written to $outFile with image entries for $($meta.Count) blog posts + 6 static pages"
