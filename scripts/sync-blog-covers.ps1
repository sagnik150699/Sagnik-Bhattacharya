Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing

function C($hex,[int]$a=255){
  $h=$hex.TrimStart('#')
  [Drawing.Color]::FromArgb($a,[Convert]::ToInt32($h.Substring(0,2),16),[Convert]::ToInt32($h.Substring(2,2),16),[Convert]::ToInt32($h.Substring(4,2),16))
}
function PathRR([float]$x,[float]$y,[float]$w,[float]$h,[float]$r){
  $d=$r*2
  $p=New-Object Drawing.Drawing2D.GraphicsPath
  $p.AddArc($x,$y,$d,$d,180,90)
  $p.AddArc($x+$w-$d,$y,$d,$d,270,90)
  $p.AddArc($x+$w-$d,$y+$h-$d,$d,$d,0,90)
  $p.AddArc($x,$y+$h-$d,$d,$d,90,90)
  $p.CloseFigure()
  $p
}
function FillRR($g,$b,[float]$x,[float]$y,[float]$w,[float]$h,[float]$r){
  $p=PathRR $x $y $w $h $r
  try{$g.FillPath($b,$p)}finally{$p.Dispose()}
}
function StrokeRR($g,$pen,[float]$x,[float]$y,[float]$w,[float]$h,[float]$r){
  $p=PathRR $x $y $w $h $r
  try{$g.DrawPath($pen,$p)}finally{$p.Dispose()}
}
function Glow($g,[float]$cx,[float]$cy,[float]$r,[string]$hex,[int]$strength=18){
  for($i=7;$i-ge 1;$i--){
    $size=$r+(30*$i)
    $alpha=[Math]::Max(8,[int]($strength*$i))
    $b=New-Object Drawing.SolidBrush (C $hex $alpha)
    try{$g.FillEllipse($b,$cx-($size/2),$cy-($size/2),$size,$size)}finally{$b.Dispose()}
  }
}
function NewTextFormat([Drawing.StringTrimming]$trimming=[Drawing.StringTrimming]::EllipsisWord){
  $sf=New-Object Drawing.StringFormat
  $sf.Alignment=[Drawing.StringAlignment]::Near
  $sf.LineAlignment=[Drawing.StringAlignment]::Near
  $sf.Trimming=$trimming
  $sf.FormatFlags=[Drawing.StringFormatFlags]::LineLimit
  $sf
}
function WrapTextBlock($g,[string]$text,[float]$x,[float]$y,[float]$w,[float]$h,[float]$size,[string]$hex,[string]$fontName='Segoe UI',[Drawing.FontStyle]$style=[Drawing.FontStyle]::Bold,[int]$alpha=255){
  $font=New-Object Drawing.Font($fontName,$size,$style,[Drawing.GraphicsUnit]::Pixel)
  $brush=New-Object Drawing.SolidBrush (C $hex $alpha)
  $sf=NewTextFormat
  try{$g.DrawString($text,$font,$brush,[Drawing.RectangleF]::new($x,$y,$w,$h),$sf)}finally{$font.Dispose();$brush.Dispose();$sf.Dispose()}
}
function MeasureTextBlockHeight($g,[string]$text,[float]$w,[float]$size,[string]$fontName='Segoe UI',[Drawing.FontStyle]$style=[Drawing.FontStyle]::Bold){
  $font=New-Object Drawing.Font($fontName,$size,$style,[Drawing.GraphicsUnit]::Pixel)
  $sf=NewTextFormat
  try{
    $measured=$g.MeasureString($text,$font,[Drawing.SizeF]::new($w,2000),$sf)
    return [float][Math]::Ceiling($measured.Height)
  }finally{$font.Dispose();$sf.Dispose()}
}
function Tag($g,[string]$text,[float]$x,[float]$y,[string]$fill,[string]$fg,[float]$fontSize=18,[float]$padX=16,[float]$height=34){
  $font=New-Object Drawing.Font('Segoe UI',$fontSize,[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
  $size=$g.MeasureString($text,$font)
  $width=[Math]::Ceiling($size.Width + ($padX * 2))
  $fillBrush=New-Object Drawing.SolidBrush (C $fill 235)
  $strokePen=New-Object Drawing.Pen (C $fg 28),1
  $textBrush=New-Object Drawing.SolidBrush (C $fg 248)
  try{
    FillRR $g $fillBrush $x $y $width $height 16
    StrokeRR $g $strokePen $x $y $width $height 16
    $g.DrawString($text,$font,$textBrush,$x + $padX - 1,$y + 5)
  }finally{$font.Dispose();$fillBrush.Dispose();$strokePen.Dispose();$textBrush.Dispose()}
  return $width
}
function TagRow($g,[string[]]$items,[float]$x,[float]$y,[string]$fill,[string]$fg,[float]$fontSize=16,[float]$padX=14,[float]$height=30){
  $cursor=$x
  foreach($item in $items){
    $w=Tag $g $item $cursor $y $fill $fg $fontSize $padX $height
    $cursor += $w + 10
  }
}
function GlassPanel($g,[float]$x,[float]$y,[float]$w,[float]$h,[float]$r,[string]$fill,[int]$fillA,[string]$line,[int]$lineA){
  $shadow=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(34,0,8,14))
  $body=New-Object Drawing.SolidBrush (C $fill $fillA)
  $pen=New-Object Drawing.Pen (C $line $lineA),1.2
  try{
    FillRR $g $shadow ($x+12) ($y+16) $w $h $r
    FillRR $g $body $x $y $w $h $r
    StrokeRR $g $pen $x $y $w $h $r
  }finally{$shadow.Dispose();$body.Dispose();$pen.Dispose()}
}
function SaveJ($img,[string]$path){
  $enc=[Drawing.Imaging.ImageCodecInfo]::GetImageEncoders()|Where-Object{$_.MimeType-eq 'image/jpeg'}|Select-Object -First 1
  $ep=New-Object Drawing.Imaging.EncoderParameters 1
  $ep.Param[0]=New-Object Drawing.Imaging.EncoderParameter([Drawing.Imaging.Encoder]::Quality,[long]98)
  try{$img.Save($path,$enc,$ep)}finally{$ep.Dispose()}
}
function ExcelLogo($g,[float]$x,[float]$y,[float]$size){
  $shadow=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(26,20,16,10))
  try{FillRR $g $shadow ($x+8) ($y+10) $size $size 36}finally{$shadow.Dispose()}

  $bg=New-Object Drawing.Drawing2D.LinearGradientBrush([Drawing.PointF]::new($x,$y),[Drawing.PointF]::new($x+$size,$y+$size),(C '#34D399'),(C '#166534'))
  try{FillRR $g $bg $x $y $size $size 36}finally{$bg.Dispose()}

  $sheetBrush=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(246,255,255,255))
  $sheetPen=New-Object Drawing.Pen (C '#D1FAE5' 240),1.2
  try{
    FillRR $g $sheetBrush ($x+54) ($y+22) ($size-74) ($size-44) 22
    StrokeRR $g $sheetPen ($x+54) ($y+22) ($size-74) ($size-44) 22
  }finally{$sheetBrush.Dispose();$sheetPen.Dispose()}

  $gridPen=New-Object Drawing.Pen (C '#BBF7D0' 170),1
  try{
    for($gx=$x+74;$gx-lt($x+$size-28);$gx+=22){$g.DrawLine($gridPen,$gx,$y+34,$gx,$y+$size-34)}
    for($gy=$y+42;$gy-lt($y+$size-26);$gy+=22){$g.DrawLine($gridPen,$x+66,$gy,$x+$size-24,$gy)}
  }finally{$gridPen.Dispose()}

  $frontBrush=New-Object Drawing.SolidBrush (C '#0F5132' 245)
  try{FillRR $g $frontBrush ($x+12) ($y+34) 78 ($size-68) 20}finally{$frontBrush.Dispose()}

  $font=New-Object Drawing.Font('Segoe UI',($size*0.34),[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
  $brush=New-Object Drawing.SolidBrush ([Drawing.Color]::White)
  $sf=NewTextFormat
  $sf.Alignment='Center'
  $sf.LineAlignment='Center'
  try{$g.DrawString('X',$font,$brush,[Drawing.RectangleF]::new($x+8,$y+30,86,$size-60),$sf)}finally{$font.Dispose();$brush.Dispose();$sf.Dispose()}
}
function GetPortraitSourceRect($img,[float]$dstW,[float]$dstH){
  $dstAspect=$dstW / $dstH
  $cropHeight=[float][Math]::Round([Math]::Min($img.Height * 0.84,$img.Width / $dstAspect))
  if($cropHeight -le 0){$cropHeight=[float]$img.Height}
  $cropWidth=[float][Math]::Round($cropHeight * $dstAspect)
  if($cropWidth -gt $img.Width){
    $cropWidth=[float]$img.Width
    $cropHeight=[float][Math]::Round($cropWidth / $dstAspect)
  }
  $srcX=[float][Math]::Round(($img.Width - $cropWidth) / 2)
  [Drawing.RectangleF]::new($srcX,0,$cropWidth,$cropHeight)
}
function PortraitFrame($g,$img,$p){
  Glow $g 246 228 190 $p.P 16
  Glow $g 186 470 120 $p.S 16

  $frame=New-Object Drawing.Drawing2D.LinearGradientBrush([Drawing.PointF]::new(28,70),[Drawing.PointF]::new(500,592),(C $p.P 240),(C $p.S 238))
  try{FillRR $g $frame 30 72 470 520 54}finally{$frame.Dispose()}

  $cardShadow=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(24,4,10,16))
  $cardBrush=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(250,255,255,255))
  $cardPen=New-Object Drawing.Pen (C '#E5E7EB' 180),1.3
  try{
    FillRR $g $cardShadow 60 104 404 456 40
    FillRR $g $cardBrush 46 92 426 476 42
    StrokeRR $g $cardPen 46 92 426 476 42
  }finally{$cardShadow.Dispose();$cardBrush.Dispose();$cardPen.Dispose()}

  $clip=PathRR 60 106 398 448 34
  try{
    $old=$g.Clip
    $g.SetClip($clip)
    $dst=[Drawing.RectangleF]::new(60,106,398,448)
    $src=GetPortraitSourceRect $img $dst.Width $dst.Height
    $g.DrawImage($img,$dst,$src,[Drawing.GraphicsUnit]::Pixel)
    $fade=[Drawing.RectangleF]::new(376,106,82,448)
    $fb=New-Object Drawing.Drawing2D.LinearGradientBrush([Drawing.PointF]::new($fade.Left,$fade.Top),[Drawing.PointF]::new($fade.Right,$fade.Top),[Drawing.Color]::FromArgb(0,255,255,255),[Drawing.Color]::FromArgb(175,255,255,255))
    try{$g.FillRectangle($fb,$fade)}finally{$fb.Dispose()}
    $g.Clip=$old
  }finally{$clip.Dispose()}

  Tag $g 'Sagnik Bhattacharya' 82 520 '#FFFFFF' '#0F172A' 18 18 36 | Out-Null
}
function BackdropScene($g,$p){
  GlassPanel $g 870 86 258 170 32 '#0F1D28' 212 '#BFE8D4' 24
  $grid=New-Object Drawing.Pen (C '#FFFFFF' 18),1
  $cell=New-Object Drawing.SolidBrush (C '#FFFFFF' 10)
  $hi1=New-Object Drawing.SolidBrush (C $p.P 220)
  $hi2=New-Object Drawing.SolidBrush (C $p.S 215)
  try{
    for($gx=892;$gx-lt1112;$gx+=42){$g.DrawLine($grid,$gx,108,$gx,234)}
    for($gy=114;$gy-lt236;$gy+=28){$g.DrawLine($grid,892,$gy,1108,$gy)}
    for($r=0;$r-lt4;$r++){
      for($c=0;$c-lt5;$c++){
        FillRR $g $cell (890+($c*42)) (108+($r*28)) 34 20 6
      }
    }
    FillRR $g $hi1 932 136 34 20 6
    FillRR $g $hi2 974 164 34 20 6
    FillRR $g $hi1 1016 192 34 20 6
    FillRR $g $hi2 1058 136 34 20 6
  }finally{$grid.Dispose();$cell.Dispose();$hi1.Dispose();$hi2.Dispose()}

  GlassPanel $g 900 330 198 128 28 '#0F1D28' 212 '#BFE8D4' 22
  $axis=New-Object Drawing.Pen (C '#FFFFFF' 60),2
  $bar1=New-Object Drawing.SolidBrush (C $p.P 220)
  $bar2=New-Object Drawing.SolidBrush (C $p.S 220)
  $linePen=New-Object Drawing.Pen (C '#FFFFFF' 190),3
  $linePen.StartCap='Round'
  $linePen.EndCap='Round'
  try{
    $g.DrawLine($axis,924,430,1076,430)
    $g.DrawLine($axis,924,356,924,430)
    FillRR $g $bar1 946 394 22 36 6
    FillRR $g $bar2 978 380 22 50 6
    FillRR $g $bar1 1010 366 22 64 6
    FillRR $g $bar2 1042 386 22 44 6
    $pts=[Drawing.PointF[]]@([Drawing.PointF]::new(946,408),[Drawing.PointF]::new(989,392),[Drawing.PointF]::new(1021,376),[Drawing.PointF]::new(1054,386))
    $g.DrawLines($linePen,$pts)
  }finally{$axis.Dispose();$bar1.Dispose();$bar2.Dispose();$linePen.Dispose()}

  GlassPanel $g 862 490 224 66 22 $p.P 226 '#FFFFFF' 28
  $line=New-Object Drawing.SolidBrush (C '#FFFFFF' 56)
  try{
    FillRR $g $line 888 508 164 10 5
    FillRR $g $line 888 528 122 10 5
  }finally{$line.Dispose()}

  Glow $g 1126 320 52 $p.S 12
  Glow $g 838 300 40 $p.P 12
}
function TitleSize([string]$title){
  $len=$title.Length
  if($len -gt 80){32}
  elseif($len -gt 68){35}
  elseif($len -gt 58){38}
  elseif($len -gt 48){41}
  else{45}
}
function FitTitleLayout($g,[string]$title,[string]$hook){
  $titleY=[float]164
  $titleW=[float]428
  $titleMaxHeight=[float]226
  $hookW=[float]416
  $hookSize=[float]21
  $hookGap=[float]18
  $tagsGap=[float]24
  $buttonGap=[float]18
  $buttonYMax=[float]520
  $fontSize=[float](TitleSize $title)
  $minSize=[float]31
  do{
    $titleHeight=MeasureTextBlockHeight $g $title $titleW $fontSize 'Segoe UI' ([Drawing.FontStyle]::Bold)
    $hookHeight=[Math]::Max(66,[float](MeasureTextBlockHeight $g $hook $hookW $hookSize 'Segoe UI' ([Drawing.FontStyle]::Regular)))
    $hookY=$titleY + $titleHeight + $hookGap
    $tagsY=$hookY + $hookHeight + $tagsGap
    $ctaY=$tagsY + 30 + $buttonGap
    if($titleHeight -le $titleMaxHeight -and $ctaY -le $buttonYMax){break}
    $fontSize -= 1
  }while($fontSize -gt $minSize)

  [pscustomobject]@{
    TitleWidth=$titleW
    TitleHeight=$titleMaxHeight
    TitleSize=$fontSize
    HookY=$hookY
    HookHeight=$hookHeight
    TagsY=$tagsY
    CtaY=$ctaY
  }
}
function NewCover($p,$img,[string]$title,[string]$tag,[string]$path){
  $bmp=New-Object Drawing.Bitmap 1200,630
  $g=[Drawing.Graphics]::FromImage($bmp)
  try{
    $g.SmoothingMode='AntiAlias'
    $g.InterpolationMode='HighQualityBicubic'
    $g.PixelOffsetMode='HighQuality'
    $g.CompositingQuality='HighQuality'
    $g.TextRenderingHint=[Drawing.Text.TextRenderingHint]::ClearTypeGridFit

    $bg=New-Object Drawing.Drawing2D.LinearGradientBrush([Drawing.PointF]::new(0,0),[Drawing.PointF]::new(1200,630),(C '#06131D'),(C '#0E2230'))
    try{$g.FillRectangle($bg,0,0,1200,630)}finally{$bg.Dispose()}

    Glow $g 140 96 220 $p.P 14
    Glow $g 1080 134 240 $p.S 12
    Glow $g 1000 590 220 $p.P 10

    $wash=New-Object Drawing.SolidBrush (C '#FFFFFF' 10)
    try{
      $g.FillEllipse($wash,-120,-80,320,320)
      $g.FillEllipse($wash,1010,-120,260,260)
      $g.FillPolygon($wash,[Drawing.PointF[]]@([Drawing.PointF]::new(0,630),[Drawing.PointF]::new(0,430),[Drawing.PointF]::new(260,630)))
    }finally{$wash.Dispose()}

    $grid=New-Object Drawing.Pen (C '#FFFFFF' 10),1
    try{
      for($gx=520;$gx-lt1180;$gx+=28){$g.DrawLine($grid,$gx,0,$gx,630)}
      for($gy=0;$gy-lt630;$gy+=28){$g.DrawLine($grid,520,$gy,1200,$gy)}
    }finally{$grid.Dispose()}

    PortraitFrame $g $img $p
    BackdropScene $g $p
    ExcelLogo $g 1034 26 132
    GlassPanel $g 520 84 498 470 38 '#07131B' 210 '#D8F7E5' 26
    $titleLayout=FitTitleLayout $g $title $p.Hook

    Tag $g $tag 548 110 '#FFFFFF' '#0F172A' 18 16 36 | Out-Null
    WrapTextBlock $g $title 548 164 $titleLayout.TitleWidth $titleLayout.TitleHeight $titleLayout.TitleSize '#F8FAFC' 'Segoe UI' ([Drawing.FontStyle]::Bold) 248
    WrapTextBlock $g $p.Hook 548 $titleLayout.HookY 416 $titleLayout.HookHeight 21 '#DCEFE6' 'Segoe UI' ([Drawing.FontStyle]::Regular) 224
    TagRow $g $p.K 548 $titleLayout.TagsY '#163645' '#E5FAEF' 16 14 30
    Tag $g $p.CTA 548 $titleLayout.CtaY $p.P '#FFFFFF' 22 22 48 | Out-Null

    SaveJ $bmp $path
  }finally{$g.Dispose();$bmp.Dispose()}
}
function SetImageMeta([string]$html,[string]$url,[string]$alt){
  $ea=[Net.WebUtility]::HtmlEncode($alt)
  $meta=@"
<meta property="og:image" content="$url">
  <meta property="og:image:secure_url" content="$url">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="$ea">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="$url">
  <meta name="twitter:image:alt" content="$ea">
"@
  $html=[regex]::Replace($html,'\s*<meta property="og:image(?::secure_url|:type|:width|:height|:alt)?"[^>]*>','','Singleline')
  $html=[regex]::Replace($html,'\s*<meta name="twitter:(?:card|image|image:alt)"[^>]*>','','Singleline')
  $html -replace '<meta property="og:url" content="[^"]*">',('$0'+"`r`n  "+$meta)
}
function SetJsonImage([string]$html,[string]$url,[string]$title){
  $m=[regex]::Match($html,'<script[^>]*application/ld\+json[^>]*>(.*?)</script>','Singleline')
  if(-not $m.Success){return $html}
  $obj=($m.Groups[1].Value.Trim()|ConvertFrom-Json)
  $obj|Add-Member -NotePropertyName image -NotePropertyValue ([ordered]@{
    '@type'='ImageObject'
    url=$url
    contentUrl=$url
    width=1200
    height=630
    caption="$title by Sagnik Bhattacharya for Coding Liquids"
    creditText='Sagnik Bhattacharya for Coding Liquids'
    creator=[ordered]@{'@type'='Person';name='Sagnik Bhattacharya';url='https://sagnikbhattacharya.com'}
    publisher=[ordered]@{'@type'='Organization';name='Coding Liquids';url='https://codingliquids.com'}
    copyrightHolder=[ordered]@{'@type'='Organization';name='Coding Liquids';url='https://codingliquids.com'}
  }) -Force
  $json=$obj|ConvertTo-Json -Compress -Depth 10
  $html.Substring(0,$m.Groups[1].Index)+$json+$html.Substring($m.Groups[1].Index+$m.Groups[1].Length)
}
function SetCoverHtml([string]$html,[string]$src,[string]$alt){
  $ea=[Net.WebUtility]::HtmlEncode($alt)
  $html=[regex]::Replace($html,'\s*<figure class="blog-cover">.*?</figure>','','Singleline')
  $fig=@"
<figure class="blog-cover">
          <img src="$src" alt="$ea" width="1200" height="630" loading="eager" fetchpriority="high" decoding="async">
          <figcaption class="sr-only">$ea</figcaption>
        </figure>
        <div class="blog-post-content">
"@
  $html -replace '<div class="blog-post-content">',$fig
}
$posts=@(
@{Slug='advanced-formulas';P='#0F766E';S='#34D399';Hook='Move beyond basic formulas and start solving real spreadsheet problems faster.';CTA='Master These 15 Formulas';K=@('LET','LAMBDA','SUMPRODUCT');Cue='formula blocks, dynamic arrays, and advanced spreadsheet logic'},
@{Slug='charts-visualisations';P='#1D4ED8';S='#F97316';Hook='Build charts that tell a clear story instead of just filling space.';CTA='Create Better Excel Charts';K=@('Line','Bar','Story');Cue='bold charts, trend lines, and presentation-ready visuals'},
@{Slug='claude-ai-excel-formulas';P='#4338CA';S='#14B8A6';Hook='Turn plain English prompts into ready-to-use Excel formulas in minutes.';CTA='Write Smarter Formulas';K=@('Prompts','Formula','AI');Cue='AI prompt styling, formulas, and spreadsheet visuals'},
@{Slug='claude-ai-excel-macros';P='#4F46E5';S='#F59E0B';Hook='Use AI to turn repetitive spreadsheet work into reusable VBA automation.';CTA='Generate Better Macros';K=@('VBA','Macros','Automation');Cue='macro automation cues, code blocks, and workflow visuals'},
@{Slug='claude-debug-formulas';P='#0F766E';S='#EF4444';Hook='Catch broken formulas quickly and understand exactly how to fix them.';CTA='Fix Formula Errors Fast';K=@('Errors','Fixes','Explain');Cue='formula debugging cues, alerts, and clean fixes'},
@{Slug='clean-messy-data';P='#047857';S='#F59E0B';Hook='Clean duplicates, spacing, and broken columns without wasting hours.';CTA='Clean Data Much Faster';K=@('Trim','Split','Clean');Cue='messy spreadsheet elements transforming into organised rows'},
@{Slug='conditional-formatting-tips';P='#B45309';S='#EC4899';Hook='Make important numbers jump out instantly with smarter formatting rules.';CTA='Highlight What Matters';K=@('Heatmaps','Icons','Rules');Cue='highlighted cells, colour scales, and formatting triggers'},
@{Slug='copilot-automate-tasks';P='#2563EB';S='#22C55E';Hook='Let Copilot handle sorting, formatting, and repeat work for you.';CTA='Automate The Busywork';K=@('Sort','Format','Repeat');Cue='automation loops, task cards, and spreadsheet workflow elements'},
@{Slug='copilot-data-analysis';P='#1D4ED8';S='#06B6D4';Hook='Use AI to surface insights, trends, and summaries from messy data.';CTA='Analyse Data With AI';K=@('Insights','Charts','Trends');Cue='data analysis cards, charts, and insight panels'},
@{Slug='data-validation';P='#0F766E';S='#22C55E';Hook='Stop bad inputs before they break your spreadsheet or your reports.';CTA='Prevent Spreadsheet Errors';K=@('Dropdowns','Checks','Rules');Cue='validation controls, dropdowns, and error-prevention signals'},
@{Slug='dynamic-dashboards';P='#059669';S='#0EA5E9';Hook='Create interactive dashboards that stakeholders can understand at a glance.';CTA='Build Dynamic Dashboards';K=@('KPI','Slicers','Charts');Cue='dashboard cards, KPIs, and interactive chart elements'},
@{Slug='excel-vs-google-sheets';P='#166534';S='#2563EB';Hook='Choose the spreadsheet tool that actually fits the way you work.';CTA='Pick The Right Tool';K=@('Offline','Collab','AI');Cue='side-by-side spreadsheet comparison panels and decision cues'},
@{Slug='financial-modelling';P='#0F172A';S='#10B981';Hook='Build cleaner forecasts, cash flow models, and scenario analysis in Excel.';CTA='Build Your First Model';K=@('Revenue','Cash Flow','Scenario');Cue='forecast visuals, tables, and financial model elements'},
@{Slug='getting-started-copilot-excel';P='#2563EB';S='#14B8A6';Hook='Get comfortable with Copilot fast and start using it inside real sheets.';CTA='Start Using Copilot';K=@('Prompt','Analyse','Formula');Cue='AI assistant styling, onboarding cues, and spreadsheet cards'},
@{Slug='index-match-guide';P='#166534';S='#F59E0B';Hook='Replace brittle lookups with a more flexible and reliable formula setup.';CTA='Upgrade Your Lookups';K=@('INDEX','MATCH','Lookup');Cue='lookup references, match arrows, and formula comparison cues'},
@{Slug='keyboard-shortcuts';P='#1F2937';S='#10B981';Hook='Memorise the shortcuts that save time every single day in Excel.';CTA='Save Hours Every Week';K=@('Ctrl','Navigate','Format');Cue='keyboard cues, fast actions, and productivity shortcuts'},
@{Slug='mastering-pivot-tables';P='#0F766E';S='#F59E0B';Hook='Summarise large data sets quickly and turn rows into useful answers.';CTA='Master Pivot Tables';K=@('Rows','Values','Groups');Cue='pivot layouts, summary visuals, and grouped data blocks'},
@{Slug='power-pivot-guide';P='#1E3A8A';S='#10B981';Hook='Handle massive datasets with better relationships, DAX, and data models.';CTA='Scale Beyond 1M Rows';K=@('DAX','Relations','Models');Cue='connected data tables, model relationships, and scale cues'},
@{Slug='power-query-guide';P='#047857';S='#06B6D4';Hook='Automate data cleaning and transformation instead of repeating manual prep.';CTA='Automate Data Prep';K=@('Source','Transform','Load');Cue='data pipelines, transformation steps, and import flow elements'},
@{Slug='what-if-analysis';P='#1D4ED8';S='#F59E0B';Hook='Compare outcomes, test assumptions, and make better Excel decisions.';CTA='Run Better Scenarios';K=@('Goal Seek','Scenarios','Solver');Cue='spreadsheet visuals and scenario comparison elements'},
@{Slug='vlookup-vs-xlookup';P='#166534';S='#EA580C';Hook='See when the legacy lookup still works and when the modern one wins.';CTA='Choose The Better Lookup';K=@('VLOOKUP','XLOOKUP','Compare');Cue='lookup comparisons, arrows, and side-by-side formula cues'}
)

$root=Resolve-Path (Join-Path $PSScriptRoot '..')
$public=Join-Path $root 'public'
$blog=Join-Path $public 'blog'
$imgDir=Join-Path $blog 'images'
$utf8=[Text.UTF8Encoding]::new($false)
if(-not(Test-Path $imgDir)){New-Item -ItemType Directory -Path $imgDir|Out-Null}
Get-ChildItem $imgDir -File -ErrorAction SilentlyContinue | Remove-Item -Force
$head=[Drawing.Image]::FromFile((Join-Path $public 'sagnik-bhattacharya.png'))
try{
  foreach($p in $posts){
    $htmlPath=Join-Path $blog ($p.Slug+'.html')
    if(-not(Test-Path $htmlPath)){continue}
    $html=[IO.File]::ReadAllText($htmlPath)
    $title=[regex]::Match($html,'<title>(.*?) \| Sagnik Bhattacharya</title>','Singleline').Groups[1].Value.Trim()
    $tagMatch=[regex]::Match($html,'<span class="blog-post-tag">(.*?)</span>','Singleline')
    $tag=if($tagMatch.Success){[Net.WebUtility]::HtmlDecode($tagMatch.Groups[1].Value.Trim())}else{'Excel Guide'}
    $file=$p.Slug+'-sagnik-bhattacharya-coding-liquids.jpg'
    $src='/blog/images/'+$file
    $url='https://sagnikbhattacharya.com/blog/images/'+$file
    $alt='Blog cover featuring Sagnik Bhattacharya for '+$title+', with '+$p.Cue+'.'
    NewCover $p $head $title $tag (Join-Path $imgDir $file)
    $html=SetImageMeta $html $url $alt
    $html=SetJsonImage $html $url $title
    $html=SetCoverHtml $html $src $alt
    [IO.File]::WriteAllText($htmlPath,$html,$utf8)
  }
}finally{$head.Dispose()}


