Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$utf8 = [System.Text.UTF8Encoding]::new($false)

$siteUrl = 'https://sagnikbhattacharya.com'
$organizationUrl = 'https://codingliquids.com'
$organizationLogoUrl = 'https://www.codingliquids.com/logo.png?v=13'
$personImageUrl = "$siteUrl/sagnik-bhattacharya.png"
$sameAsProfiles = @(
  'https://www.linkedin.com/in/sagnik-bhattacharya-916b9463/',
  'https://github.com/sagnik150699',
  'https://www.udemy.com/user/sagnik-bhattacharya-5/'
)

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..')
$publicDir = Join-Path $repoRoot 'public'
$blogDir = Join-Path $publicDir 'blog'

function Read-Html {
  param([string]$Path)

  return [System.IO.File]::ReadAllText($Path, [System.Text.Encoding]::UTF8)
}

function Write-Html {
  param(
    [string]$Path,
    [string]$Content
  )

  [System.IO.File]::WriteAllText($Path, $Content, $utf8)
}

function Decode-Html {
  param([string]$Value)

  return [System.Net.WebUtility]::HtmlDecode($Value)
}

function Get-HeadValue {
  param(
    [string]$Html,
    [string]$Pattern
  )

  $match = [regex]::Match($Html, $Pattern, [System.Text.RegularExpressions.RegexOptions]::IgnoreCase)
  if (-not $match.Success) {
    return $null
  }

  return (Decode-Html $match.Groups[1].Value.Trim())
}

function Get-Title {
  param([string]$Html)

  return (Get-HeadValue $Html '<title>\s*(.*?)\s*</title>')
}

function Get-Canonical {
  param([string]$Html)

  return (Get-HeadValue $Html '<link(?=[^>]+\brel="canonical")(?=[^>]+\bhref="([^"]+)")[^>]*>')
}

function Get-MetaContent {
  param(
    [string]$Html,
    [string]$Key
  )

  $escapedKey = [regex]::Escape($Key)
  return (Get-HeadValue $Html "<meta(?=[^>]+\b(?:name|property)=""$escapedKey"")(?=[^>]+\bcontent=""([^""]+)"")[^>]*>")
}

function ConvertTo-JsonLd {
  param([object]$Data)

  return ($Data | ConvertTo-Json -Depth 20)
}

function New-JsonLdScript {
  param([object]$Data)

  $json = ConvertTo-JsonLd $Data
  return "  <script type=`"application/ld+json`">`r`n$json`r`n  </script>"
}

function Remove-JsonLdTypes {
  param(
    [string]$Html,
    [string[]]$Types
  )

  $pattern = '<script\b[^>]*type="application/ld\+json"[^>]*>\s*(.*?)\s*</script>\s*'
  return [regex]::Replace(
    $Html,
    $pattern,
    {
      param($match)

      $jsonText = $match.Groups[1].Value.Trim()
      try {
        $jsonObject = $jsonText | ConvertFrom-Json
      } catch {
        return $match.Value
      }

      $typeProperty = $jsonObject.PSObject.Properties['@type']
      if ($null -eq $typeProperty) {
        return $match.Value
      }

      $topLevelTypes = @($typeProperty.Value)
      foreach ($topLevelType in $topLevelTypes) {
        if ($Types -contains [string]$topLevelType) {
          return ''
        }
      }

      return $match.Value
    },
    [System.Text.RegularExpressions.RegexOptions]::IgnoreCase -bor [System.Text.RegularExpressions.RegexOptions]::Singleline
  )
}

function Insert-ManagedScripts {
  param(
    [string]$Html,
    [string[]]$Scripts
  )

  $block = (($Scripts -join "`r`n") + "`r`n")
  return ($Html -replace '<link rel="stylesheet" href="/style\.css">', ($block + '  <link rel="stylesheet" href="/style.css">'))
}

function New-OrganizationReference {
  return [ordered]@{
    '@type' = 'Organization'
    name = 'Coding Liquids'
    url = $organizationUrl
    logo = [ordered]@{
      '@type' = 'ImageObject'
      url = $organizationLogoUrl
    }
  }
}

function New-OrganizationSchema {
  return [ordered]@{
    '@context' = 'https://schema.org'
    '@type' = 'Organization'
    name = 'Coding Liquids'
    url = $organizationUrl
    logo = [ordered]@{
      '@type' = 'ImageObject'
      url = $organizationLogoUrl
    }
    founder = [ordered]@{
      '@type' = 'Person'
      name = 'Sagnik Bhattacharya'
      url = $siteUrl
    }
  }
}

function New-PersonSchema {
  return [ordered]@{
    '@context' = 'https://schema.org'
    '@type' = 'Person'
    name = 'Sagnik Bhattacharya'
    jobTitle = 'CEO & Founder'
    worksFor = [ordered]@{
      '@type' = 'Organization'
      name = 'Coding Liquids'
      url = $organizationUrl
    }
    url = $siteUrl
    image = $personImageUrl
    sameAs = $sameAsProfiles
  }
}

function New-WebsiteSchema {
  return [ordered]@{
    '@context' = 'https://schema.org'
    '@type' = 'WebSite'
    name = 'Sagnik Bhattacharya'
    url = "$siteUrl/"
  }
}

function New-BreadcrumbSchema {
  param([object[]]$Items)

  $position = 1
  $listItems = foreach ($item in $Items) {
    [ordered]@{
      '@type' = 'ListItem'
      position = $position
      name = $item.Name
      item = $item.Item
    }
    $position += 1
  }

  return [ordered]@{
    '@context' = 'https://schema.org'
    '@type' = 'BreadcrumbList'
    itemListElement = @($listItems)
  }
}

function New-BlogPostingSchema {
  param(
    [string]$Headline,
    [string]$Description,
    [string]$CanonicalUrl,
    [string]$ImageUrl,
    [string]$PublishedDate,
    [string]$ModifiedDate
  )

  return [ordered]@{
    '@context' = 'https://schema.org'
    '@type' = 'BlogPosting'
    headline = $Headline
    author = [ordered]@{
      '@type' = 'Person'
      name = 'Sagnik Bhattacharya'
      url = $siteUrl
    }
    datePublished = $PublishedDate
    dateModified = $ModifiedDate
    description = $Description
    publisher = (New-OrganizationReference)
    image = [ordered]@{
      '@type' = 'ImageObject'
      url = $ImageUrl
    }
    mainEntityOfPage = [ordered]@{
      '@type' = 'WebPage'
      '@id' = $CanonicalUrl
    }
  }
}

function Update-Page {
  param(
    [string]$Path,
    [switch]$IncludePerson,
    [switch]$IncludeWebsite,
    [object[]]$BreadcrumbItems,
    [object[]]$AdditionalSchemas,
    [string[]]$ManagedTypes
  )

  $html = Read-Html $Path
  $html = Remove-JsonLdTypes $html $ManagedTypes

  $scripts = New-Object System.Collections.Generic.List[string]
  foreach ($schema in $AdditionalSchemas) {
    $scripts.Add((New-JsonLdScript $schema))
  }
  if ($IncludePerson) {
    $scripts.Add((New-JsonLdScript (New-PersonSchema)))
  }
  $scripts.Add((New-JsonLdScript (New-OrganizationSchema)))
  $scripts.Add((New-JsonLdScript (New-BreadcrumbSchema $BreadcrumbItems)))
  if ($IncludeWebsite) {
    $scripts.Add((New-JsonLdScript (New-WebsiteSchema)))
  }

  $html = Insert-ManagedScripts $html ($scripts.ToArray())
  Write-Html $Path $html
}

$defaultManagedTypes = @('Person', 'Organization', 'BreadcrumbList', 'WebSite', 'FAQPage')
$blogManagedTypes = @('BlogPosting', 'Organization', 'BreadcrumbList', 'FAQPage')

$rootPages = @(
  [ordered]@{
    Path = Join-Path $publicDir 'index.html'
    IncludePerson = $true
    IncludeWebsite = $true
    BreadcrumbItems = @(
      [ordered]@{ Name = 'Home'; Item = "$siteUrl/" }
    )
    AdditionalSchemas = @()
    ManagedTypes = $defaultManagedTypes
  },
  [ordered]@{
    Path = Join-Path $publicDir 'about.html'
    IncludePerson = $true
    IncludeWebsite = $false
    BreadcrumbItems = @(
      [ordered]@{ Name = 'Home'; Item = "$siteUrl/" },
      [ordered]@{ Name = 'About'; Item = "$siteUrl/about" }
    )
    AdditionalSchemas = @()
    ManagedTypes = $defaultManagedTypes
  },
  [ordered]@{
    Path = Join-Path $publicDir 'blog.html'
    IncludePerson = $false
    IncludeWebsite = $false
    BreadcrumbItems = @(
      [ordered]@{ Name = 'Home'; Item = "$siteUrl/" },
      [ordered]@{ Name = 'Blog'; Item = "$siteUrl/blog" }
    )
    AdditionalSchemas = @()
    ManagedTypes = $defaultManagedTypes
  },
  [ordered]@{
    Path = Join-Path $publicDir 'courses.html'
    IncludePerson = $false
    IncludeWebsite = $false
    BreadcrumbItems = @(
      [ordered]@{ Name = 'Home'; Item = "$siteUrl/" },
      [ordered]@{ Name = 'Courses'; Item = "$siteUrl/courses" }
    )
    AdditionalSchemas = @()
    ManagedTypes = $defaultManagedTypes
  },
  [ordered]@{
    Path = Join-Path $publicDir 'services.html'
    IncludePerson = $false
    IncludeWebsite = $false
    BreadcrumbItems = @(
      [ordered]@{ Name = 'Home'; Item = "$siteUrl/" },
      [ordered]@{ Name = 'Services'; Item = "$siteUrl/services" }
    )
    AdditionalSchemas = @()
    ManagedTypes = $defaultManagedTypes
  },
  [ordered]@{
    Path = Join-Path $publicDir 'contact.html'
    IncludePerson = $false
    IncludeWebsite = $false
    BreadcrumbItems = @(
      [ordered]@{ Name = 'Home'; Item = "$siteUrl/" },
      [ordered]@{ Name = 'Contact'; Item = "$siteUrl/contact" }
    )
    AdditionalSchemas = @()
    ManagedTypes = $defaultManagedTypes
  }
)

foreach ($page in $rootPages) {
  Update-Page `
    -Path $page.Path `
    -IncludePerson:$page.IncludePerson `
    -IncludeWebsite:$page.IncludeWebsite `
    -BreadcrumbItems $page.BreadcrumbItems `
    -AdditionalSchemas $page.AdditionalSchemas `
    -ManagedTypes $page.ManagedTypes
}

Get-ChildItem $blogDir -Filter '*.html' | ForEach-Object {
  $path = $_.FullName
  $html = Read-Html $path

  $headline = Get-MetaContent $html 'og:title'
  if (-not $headline) {
    $headline = Get-Title $html
  }

  $description = Get-MetaContent $html 'description'
  $canonicalUrl = Get-Canonical $html
  $imageUrl = Get-MetaContent $html 'og:image'
  $publishedDate = Get-MetaContent $html 'article:published_time'
  $modifiedDate = Get-MetaContent $html 'article:modified_time'
  if (-not $modifiedDate) {
    $modifiedDate = $publishedDate
  }

  if (-not $headline -or -not $description -or -not $canonicalUrl -or -not $imageUrl -or -not $publishedDate -or -not $modifiedDate) {
    throw "Missing blog metadata in $path"
  }

  $blogPosting = New-BlogPostingSchema `
    -Headline $headline `
    -Description $description `
    -CanonicalUrl $canonicalUrl `
    -ImageUrl $imageUrl `
    -PublishedDate $publishedDate `
    -ModifiedDate $modifiedDate

  Update-Page `
    -Path $path `
    -BreadcrumbItems @(
      [ordered]@{ Name = 'Home'; Item = "$siteUrl/" },
      [ordered]@{ Name = 'Blog'; Item = "$siteUrl/blog" },
      [ordered]@{ Name = $headline; Item = $canonicalUrl }
    ) `
    -AdditionalSchemas @($blogPosting) `
    -ManagedTypes $blogManagedTypes
}
