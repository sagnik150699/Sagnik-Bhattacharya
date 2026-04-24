param(
  [string[]]$Slug,
  [switch]$ImageOnly
)
Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing

$codingLiquidsUrl='https://codingliquids.com'
$codingLiquidsTermsUrl='https://www.codingliquids.com/termsofuse'
$imageAcquireLicenseUrl='https://sagnikbhattacharya.com/contact'
$codingLiquidsCopyrightNotice=([string][char]0x00A9)+' Sagnik Bhattacharya and Coding Liquids. All rights reserved.'
$defaultPortraitFocus='headshot'

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
function FlutterGlyph($g,[float]$x,[float]$y,[float]$scale=1){
  $light=New-Object Drawing.SolidBrush (C '#93E6FF' 248)
  $mid=New-Object Drawing.SolidBrush (C '#38BDF8' 244)
  $dark=New-Object Drawing.SolidBrush (C '#2563EB' 242)
  try{
    $g.FillPolygon($light,[Drawing.PointF[]]@(
      [Drawing.PointF]::new($x + (12*$scale),$y + (16*$scale)),
      [Drawing.PointF]::new($x + (38*$scale),$y + (42*$scale)),
      [Drawing.PointF]::new($x + (54*$scale),$y + (26*$scale)),
      [Drawing.PointF]::new($x + (28*$scale),$y + (0*$scale))
    ))
    $g.FillPolygon($mid,[Drawing.PointF[]]@(
      [Drawing.PointF]::new($x + (12*$scale),$y + (54*$scale)),
      [Drawing.PointF]::new($x + (38*$scale),$y + (80*$scale)),
      [Drawing.PointF]::new($x + (92*$scale),$y + (26*$scale)),
      [Drawing.PointF]::new($x + (66*$scale),$y + (0*$scale))
    ))
    $g.FillPolygon($dark,[Drawing.PointF[]]@(
      [Drawing.PointF]::new($x + (40*$scale),$y + (54*$scale)),
      [Drawing.PointF]::new($x + (58*$scale),$y + (72*$scale)),
      [Drawing.PointF]::new($x + (92*$scale),$y + (38*$scale)),
      [Drawing.PointF]::new($x + (74*$scale),$y + (20*$scale))
    ))
  }finally{$light.Dispose();$mid.Dispose();$dark.Dispose()}
}
function ReactNativeGlyph($g,[float]$cx,[float]$cy,[float]$scale=1){
  $pen=New-Object Drawing.Pen (C '#61DAFB' 236),([Math]::Max(2.4,(3.2*$scale)))
  $pen.StartCap='Round'
  $pen.EndCap='Round'
  $core=New-Object Drawing.SolidBrush (C '#9BE7FF' 246)
  try{
    foreach($angle in @(0,60,-60)){
      $state=$g.Save()
      try{
        $g.TranslateTransform($cx,$cy)
        $g.RotateTransform($angle)
        $g.DrawEllipse($pen,(-30*$scale),(-12*$scale),(60*$scale),(24*$scale))
      }finally{$g.Restore($state)}
    }
    $g.FillEllipse($core,$cx-(7*$scale),$cy-(7*$scale),(14*$scale),(14*$scale))
  }finally{$pen.Dispose();$core.Dispose()}
}
function PhoneMockup($g,[float]$x,[float]$y,[float]$w,[float]$h,[string]$accent,[string]$accent2,[string]$mode){
  $shadow=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(22,0,10,18))
  $body=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(234,8,20,31))
  $screen=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(248,13,27,41))
  $stroke=New-Object Drawing.Pen (C '#D7F8FF' 34),1
  $speaker=New-Object Drawing.SolidBrush (C '#FFFFFF' 42)
  $accentBrush=New-Object Drawing.SolidBrush (C $accent 236)
  $accentBrush2=New-Object Drawing.SolidBrush (C $accent2 218)
  $muted=New-Object Drawing.SolidBrush (C '#FFFFFF' 26)
  try{
    FillRR $g $shadow ($x+6) ($y+10) $w $h 24
    FillRR $g $body $x $y $w $h 24
    StrokeRR $g $stroke $x $y $w $h 24
    FillRR $g $screen ($x+6) ($y+8) ($w-12) ($h-16) 20
    FillRR $g $speaker ($x+($w/2)-14) ($y+12) 28 4 2
    if($mode -eq 'flutter'){
      FillRR $g $accentBrush ($x+18) ($y+34) ($w-36) 24 10
      FillRR $g $muted ($x+18) ($y+70) ($w-36) 42 12
      FillRR $g $accentBrush2 ($x+28) ($y+84) ($w-56) 10 5
      FillRR $g $muted ($x+18) ($y+120) ($w-36) 18 9
      FillRR $g $accentBrush ($x+18) ($y+148) 44 10 5
      FillRR $g $accentBrush2 ($x+68) ($y+148) 22 10 5
    }else{
      FillRR $g $muted ($x+18) ($y+34) ($w-36) 32 14
      FillRR $g $accentBrush ($x+28) ($y+46) 30 8 4
      FillRR $g $accentBrush2 ($x+18) ($y+82) ($w-36) 20 10
      FillRR $g $muted ($x+18) ($y+114) ($w-36) 34 12
      FillRR $g $accentBrush ($x+26) ($y+128) 22 8 4
      FillRR $g $accentBrush2 ($x+54) ($y+128) 28 8 4
      FillRR $g $muted ($x+16) ($y+$h-34) ($w-32) 8 4
    }
  }finally{$shadow.Dispose();$body.Dispose();$screen.Dispose();$stroke.Dispose();$speaker.Dispose();$accentBrush.Dispose();$accentBrush2.Dispose();$muted.Dispose()}
}
function CompareRow($g,[float]$x,[float]$y,[string]$label,[float]$flutterWidth,[float]$reactWidth,[string]$flutterColor,[string]$reactColor){
  $font=New-Object Drawing.Font('Segoe UI',12,[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
  $textBrush=New-Object Drawing.SolidBrush (C '#ECFEFF' 232)
  $track=New-Object Drawing.SolidBrush (C '#FFFFFF' 14)
  $flutterBrush=New-Object Drawing.SolidBrush (C $flutterColor 236)
  $reactBrush=New-Object Drawing.SolidBrush (C $reactColor 220)
  try{
    $g.DrawString($label,$font,$textBrush,$x,$y-3)
    FillRR $g $track ($x+58) ($y+2) 118 8 4
    FillRR $g $track ($x+58) ($y+16) 118 8 4
    FillRR $g $flutterBrush ($x+58) ($y+2) $flutterWidth 8 4
    FillRR $g $reactBrush ($x+58) ($y+16) $reactWidth 8 4
  }finally{$font.Dispose();$textBrush.Dispose();$track.Dispose();$flutterBrush.Dispose();$reactBrush.Dispose()}
}
function FrameworkBadge($g,$p,[float]$x,[float]$y){
  GlassPanel $g $x $y 158 132 32 '#07131B' 222 '#D9F7FF' 26

  $left=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(236,15,36,58))
  $right=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(236,13,28,44))
  $label=New-Object Drawing.SolidBrush (C '#FFFFFF' 68)
  $vsBrush=New-Object Drawing.SolidBrush (C $p.P 240)
  $vsStroke=New-Object Drawing.Pen (C '#FFFFFF' 34),1
  $font=New-Object Drawing.Font('Segoe UI',13,[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
  $text=New-Object Drawing.SolidBrush (C '#F8FAFC' 246)
  try{
    FillRR $g $left ($x+16) ($y+18) 54 68 18
    FillRR $g $right ($x+88) ($y+18) 54 68 18
    FlutterGlyph $g ($x+20) ($y+26) 0.52
    ReactNativeGlyph $g ($x+115) ($y+52) 0.62
    $g.FillEllipse($vsBrush,$x+60,$y+42,38,38)
    $g.DrawEllipse($vsStroke,$x+60,$y+42,38,38)
    $sf=NewTextFormat
    $sf.Alignment='Center'
    $sf.LineAlignment='Center'
    try{$g.DrawString('VS',$font,$text,[Drawing.RectangleF]::new($x+60,$y+42,38,38),$sf)}finally{$sf.Dispose()}
    FillRR $g $label ($x+18) ($y+98) 122 12 6
  }finally{$left.Dispose();$right.Dispose();$label.Dispose();$vsBrush.Dispose();$vsStroke.Dispose();$font.Dispose();$text.Dispose()}
}
function GetPortraitSourceRect($img,[float]$dstW,[float]$dstH,[string]$focus=''){
  $dstAspect=$dstW / $dstH
  $cropHeightFactor=if($focus -eq 'headshot'){0.66}else{0.84}
  $cropHeight=[float][Math]::Round([Math]::Min($img.Height * $cropHeightFactor,$img.Width / $dstAspect))
  if($cropHeight -le 0){$cropHeight=[float]$img.Height}
  $cropWidth=[float][Math]::Round($cropHeight * $dstAspect)
  if($cropWidth -gt $img.Width){
    $cropWidth=[float]$img.Width
    $cropHeight=[float][Math]::Round($cropWidth / $dstAspect)
  }
  $srcX=[float][Math]::Round(($img.Width - $cropWidth) / 2)
  $srcY=if($focus -eq 'headshot'){
    [float][Math]::Round([Math]::Min(($img.Height - $cropHeight),[Math]::Max(22,($img.Height * 0.04))))
  }else{
    0
  }
  [Drawing.RectangleF]::new($srcX,$srcY,$cropWidth,$cropHeight)
}
function PortraitFrame($g,$img,$p){
  $portraitFocus=if($p.Contains('PortraitFocus') -and $p['PortraitFocus']){[string]$p['PortraitFocus']}else{$defaultPortraitFocus}
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
    $src=GetPortraitSourceRect $img $dst.Width $dst.Height $portraitFocus
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
function MobileBackdropScene($g,$p){
  GlassPanel $g 854 84 292 214 34 '#0F1D28' 214 '#C8F4FF' 24
  PhoneMockup $g 880 108 92 162 $p.P '#93E6FF' 'flutter'
  PhoneMockup $g 1006 120 92 162 $p.S '#1D4ED8' 'react'

  $vsShadow=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(26,0,12,24))
  $vsFill=New-Object Drawing.SolidBrush (C '#0F172A' 242)
  $vsStroke=New-Object Drawing.Pen (C '#D8F6FF' 42),1
  $vsFont=New-Object Drawing.Font('Segoe UI',14,[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
  $vsText=New-Object Drawing.SolidBrush (C '#F8FAFC' 248)
  try{
    $g.FillEllipse($vsShadow,967,170,44,44)
    $g.FillEllipse($vsFill,961,164,44,44)
    $g.DrawEllipse($vsStroke,961,164,44,44)
    $sf=NewTextFormat
    $sf.Alignment='Center'
    $sf.LineAlignment='Center'
    try{$g.DrawString('VS',$vsFont,$vsText,[Drawing.RectangleF]::new(961,164,44,44),$sf)}finally{$sf.Dispose()}
  }finally{$vsShadow.Dispose();$vsFill.Dispose();$vsStroke.Dispose();$vsFont.Dispose();$vsText.Dispose()}

  GlassPanel $g 898 326 224 146 28 '#0F1D28' 212 '#C8F4FF' 22
  $tagX=920
  $tagX += Tag $g 'Flutter' $tagX 346 '#0F2942' '#D8F6FF' 12 10 24
  $tagX += 8
  Tag $g 'React Native' $tagX 346 '#102734' '#D8F6FF' 12 10 24 | Out-Null
  CompareRow $g 922 386 'UI' 92 78 $p.P $p.S
  CompareRow $g 922 418 'DX' 82 96 $p.P $p.S
  CompareRow $g 922 450 'Jobs' 68 102 $p.P $p.S

  GlassPanel $g 852 494 248 68 24 $p.P 230 '#FFFFFF' 28
  $line=New-Object Drawing.SolidBrush (C '#FFFFFF' 62)
  $dot1=New-Object Drawing.SolidBrush (C '#93E6FF' 228)
  $dot2=New-Object Drawing.SolidBrush (C '#61DAFB' 228)
  try{
    FillRR $g $line 880 512 126 10 5
    FillRR $g $line 880 532 164 10 5
    $g.FillEllipse($dot1,1048,508,12,12)
    $g.FillEllipse($dot2,1066,522,12,12)
  }finally{$line.Dispose();$dot1.Dispose();$dot2.Dispose()}

  Glow $g 1122 318 54 $p.S 12
  Glow $g 842 294 42 $p.P 12
}
function BubbleBadge($g,[float]$x,[float]$y,[string]$letter,[string]$accent,[float]$size=56){
  $shell=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(224,10,24,36))
  $stroke=New-Object Drawing.Pen (C $accent 72),1.2
  $orb=New-Object Drawing.SolidBrush (C $accent 236)
  $glint=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(44,255,255,255))
  $font=New-Object Drawing.Font('Segoe UI',([Math]::Max(16,($size*0.34))),[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
  $text=New-Object Drawing.SolidBrush (C '#0F172A' 244)
  try{
    FillRR $g $shell $x $y $size $size 18
    StrokeRR $g $stroke $x $y $size $size 18
    $orbSize=$size-18
    $orbX=$x+9
    $orbY=$y+9
    $g.FillEllipse($orb,$orbX,$orbY,$orbSize,$orbSize)
    $g.FillEllipse($glint,$orbX+4,$orbY+4,($orbSize*0.42),($orbSize*0.28))
    $sf=NewTextFormat
    $sf.Alignment='Center'
    $sf.LineAlignment='Center'
    try{$g.DrawString($letter,$font,$text,[Drawing.RectangleF]::new($orbX,$orbY,$orbSize,$orbSize),$sf)}finally{$sf.Dispose()}
  }finally{$shell.Dispose();$stroke.Dispose();$orb.Dispose();$glint.Dispose();$font.Dispose();$text.Dispose()}
}
function StateSignalBars($g,[float]$x,[float]$y,[string]$accent,[float]$trackWidth=34){
  $track=New-Object Drawing.SolidBrush (C '#FFFFFF' 16)
  $fill=New-Object Drawing.SolidBrush (C $accent 214)
  try{
    FillRR $g $track $x $y $trackWidth 8 4
    FillRR $g $track $x ($y+16) $trackWidth 8 4
    FillRR $g $track $x ($y+32) $trackWidth 8 4
    FillRR $g $fill $x $y ([Math]::Max(16,($trackWidth*0.76))) 8 4
    FillRR $g $fill $x ($y+16) ([Math]::Max(12,($trackWidth*0.54))) 8 4
    FillRR $g $fill $x ($y+32) ([Math]::Max(18,($trackWidth*0.86))) 8 4
  }finally{$track.Dispose();$fill.Dispose()}
}
function StateCard($g,[float]$x,[float]$y,[float]$w,[float]$h,[string]$label,[string]$letter,[string]$accent){
  GlassPanel $g $x $y $w $h 24 '#0F1D28' 214 $accent 54

  BubbleBadge $g ($x+16) ($y+16) $letter $accent 42

  $font=New-Object Drawing.Font('Segoe UI',15,[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
  $text=New-Object Drawing.SolidBrush (C '#F8FAFC' 244)
  $muted=New-Object Drawing.SolidBrush (C '#FFFFFF' 24)
  $fill=New-Object Drawing.SolidBrush (C $accent 216)
  try{
    $g.DrawString($label,$font,$text,$x+66,$y+24)
    FillRR $g $muted ($x+18) ($y+76) ($w-36) 8 4
    FillRR $g $fill ($x+18) ($y+76) ([Math]::Max(32,($w-60))) 8 4
    FillRR $g $muted ($x+18) ($y+94) ($w-58) 8 4
    FillRR $g $fill ($x+18) ($y+94) ([Math]::Max(22,($w-94))) 8 4
    FillRR $g $muted ($x+18) ($y+$h-26) ($w-44) 8 4
    StateSignalBars $g ($x+$w-54) ($y+22) $accent 28
  }finally{$font.Dispose();$text.Dispose();$muted.Dispose();$fill.Dispose()}
}
function StateManagementScene($g,$p){
  $provider='#38BDF8'
  $riverpod='#2DD4BF'
  $bloc='#F59E0B'

  GlassPanel $g 882 86 250 216 34 '#0F1D28' 210 '#C8F4FF' 22
  Glow $g 1010 96 160 $riverpod 11
  Glow $g 1128 432 140 $p.P 10

  BubbleBadge $g 930 22 'P' $provider 56
  BubbleBadge $g 988 18 'R' $riverpod 60
  BubbleBadge $g 1052 22 'B' $bloc 56

  StateCard $g 984 152 144 176 'Riverpod' 'R' $riverpod
  StateCard $g 940 234 138 146 'Provider' 'P' $provider
  StateCard $g 1082 220 100 154 'BLoC' 'B' $bloc

  $footer=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(26,255,255,255))
  $line1=New-Object Drawing.SolidBrush (C '#FFFFFF' 40)
  $line2=New-Object Drawing.SolidBrush (C '#FFFFFF' 24)
  try{
    FillRR $g $footer 1014 474 140 74 24
    FillRR $g $line1 1036 496 80 10 5
    FillRR $g $line2 1036 516 96 10 5
    FillRR $g $line1 1036 536 62 10 5
  }finally{$footer.Dispose();$line1.Dispose();$line2.Dispose()}
}
function PromptStep($g,[float]$x,[float]$y,[float]$w,[string]$label,[string]$accent,[float]$fillRatio=0.7){
  GlassPanel $g $x $y $w 72 20 '#0E1B26' 214 '#FFE8CC' 18

  Tag $g $label ($x+16) ($y+12) '#132634' '#F8FAFC' 11 10 22 | Out-Null

  $track=New-Object Drawing.SolidBrush (C '#FFFFFF' 34)
  $subtrack=New-Object Drawing.SolidBrush (C '#FFFFFF' 18)
  $fill=New-Object Drawing.SolidBrush (C $accent 228)
  $dot=New-Object Drawing.SolidBrush (C $accent 196)
  try{
    FillRR $g $track ($x+18) ($y+43) ($w-62) 8 4
    FillRR $g $subtrack ($x+18) ($y+57) ($w-82) 6 3
    $fillWidth=[float][Math]::Max(48,[Math]::Round(($w-96) * $fillRatio))
    FillRR $g $fill ($x+18) ($y+57) $fillWidth 6 3
    $g.FillEllipse($dot,$x+$w-28,$y+24,10,10)
  }finally{$track.Dispose();$subtrack.Dispose();$fill.Dispose();$dot.Dispose()}
}
function NeuroPromptScene($g,$p){
  GlassPanel $g 846 82 300 238 34 '#101E2A' 216 '#FFE6C7' 24
  Tag $g 'PROMPT BLUEPRINT' 872 104 '#FFFFFF' '#0F172A' 12 10 26 | Out-Null
  Tag $g '60' 1072 104 $p.P '#FFFFFF' 12 12 26 | Out-Null

  PromptStep $g 874 144 228 'Specific goal' $p.P 0.94
  PromptStep $g 892 204 226 'Sheet context' $p.S 0.78
  PromptStep $g 910 264 208 'Desired output' $p.P 0.62

  $connector=New-Object Drawing.Pen (C '#FFFFFF' 50),2
  $connector.StartCap='Round'
  $connector.EndCap='Round'
  try{
    $g.DrawLine($connector,1092,180,1110,180)
    $g.DrawLine($connector,1092,240,1110,240)
  }finally{$connector.Dispose()}

  GlassPanel $g 894 344 228 126 28 '#101E2A' 214 '#D8F7E5' 22
  TagRow $g @('Copy','Paste','Results') 916 364 '#102734' '#ECFEFF' 12 10 24

  $axis=New-Object Drawing.Pen (C '#FFFFFF' 56),2
  $bar1=New-Object Drawing.SolidBrush (C $p.P 228)
  $bar2=New-Object Drawing.SolidBrush (C $p.S 220)
  $line=New-Object Drawing.Pen (C '#FFFFFF' 188),3
  $line.StartCap='Round'
  $line.EndCap='Round'
  try{
    $g.DrawLine($axis,920,442,1092,442)
    $g.DrawLine($axis,920,388,920,442)
    FillRR $g $bar1 944 416 22 26 6
    FillRR $g $bar2 978 404 22 38 6
    FillRR $g $bar1 1012 392 22 50 6
    FillRR $g $bar2 1046 378 22 64 6
    $pts=[Drawing.PointF[]]@(
      [Drawing.PointF]::new(944,420),
      [Drawing.PointF]::new(989,408),
      [Drawing.PointF]::new(1022,396),
      [Drawing.PointF]::new(1057,382)
    )
    $g.DrawLines($line,$pts)
  }finally{$axis.Dispose();$bar1.Dispose();$bar2.Dispose();$line.Dispose()}

  GlassPanel $g 852 494 266 68 24 $p.P 230 '#FFFFFF' 28
  $ctaLine=New-Object Drawing.SolidBrush (C '#FFFFFF' 66)
  $ctaAccent=New-Object Drawing.SolidBrush (C '#FFF7ED' 216)
  try{
    FillRR $g $ctaLine 880 512 150 10 5
    FillRR $g $ctaLine 880 532 114 10 5
    FillRR $g $ctaAccent 1042 510 42 12 6
    FillRR $g $ctaAccent 1090 526 16 16 8
  }finally{$ctaLine.Dispose();$ctaAccent.Dispose()}

  Glow $g 1128 322 56 $p.S 12
  Glow $g 840 304 44 $p.P 12
}
function AiModelNeuroScene($g,$p){
  $chips=@($p.K | Select-Object -First 2)
  if($chips.Count -eq 0){$chips=@('AI','Models')}

  GlassPanel $g 842 82 308 222 34 '#101E2A' 216 '#E7EDFF' 24
  Tag $g 'MODEL PLAYBOOK' 868 104 '#FFFFFF' '#0F172A' 12 10 26 | Out-Null
  TagRow $g $chips 868 142 '#102734' '#ECFEFF' 12 10 24

  $card=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(228,11,24,38))
  $cardStroke=New-Object Drawing.Pen (C '#FFFFFF' 26),1
  $muted=New-Object Drawing.SolidBrush (C '#FFFFFF' 22)
  $link=New-Object Drawing.Pen (C '#FFFFFF' 52),2
  $primary=New-Object Drawing.SolidBrush (C $p.P 230)
  $secondary=New-Object Drawing.SolidBrush (C $p.S 220)
  try{
    $link.StartCap='Round'
    $link.EndCap='Round'
    FillRR $g $card 872 188 78 72 18
    FillRR $g $card 958 174 78 88 18
    FillRR $g $card 1044 188 78 72 18
    StrokeRR $g $cardStroke 872 188 78 72 18
    StrokeRR $g $cardStroke 958 174 78 88 18
    StrokeRR $g $cardStroke 1044 188 78 72 18
    $g.DrawLine($link,950,224,958,218)
    $g.DrawLine($link,1036,218,1044,224)

    FillRR $g $primary 886 202 34 10 5
    FillRR $g $muted 886 220 46 8 4
    FillRR $g $muted 886 236 34 8 4
    FillRR $g $secondary 914 238 16 16 8

    FillRR $g $secondary 972 188 42 10 5
    FillRR $g $muted 972 208 50 8 4
    FillRR $g $muted 972 224 36 8 4
    FillRR $g $primary 972 240 22 10 5
    FillRR $g $secondary 1000 240 20 10 5

    FillRR $g $secondary 1058 202 34 10 5
    FillRR $g $muted 1058 220 46 8 4
    FillRR $g $muted 1058 236 34 8 4
    FillRR $g $primary 1086 238 16 16 8
  }finally{$card.Dispose();$cardStroke.Dispose();$muted.Dispose();$link.Dispose();$primary.Dispose();$secondary.Dispose()}

  GlassPanel $g 888 330 224 132 28 '#101E2A' 214 '#D8F7E5' 22
  Tag $g 'LOCAL WORKFLOW' 912 352 '#FFFFFF' '#0F172A' 11 10 24 | Out-Null

  $window=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(228,13,27,41))
  $chrome=New-Object Drawing.SolidBrush (C '#FFFFFF' 30)
  $lineA=New-Object Drawing.SolidBrush (C $p.P 224)
  $lineB=New-Object Drawing.SolidBrush (C $p.S 214)
  $lineMuted=New-Object Drawing.SolidBrush (C '#FFFFFF' 26)
  try{
    FillRR $g $window 912 380 176 60 16
    FillRR $g $chrome 926 392 10 10 5
    FillRR $g $chrome 942 392 10 10 5
    FillRR $g $chrome 958 392 10 10 5
    FillRR $g $lineA 926 414 70 8 4
    FillRR $g $lineMuted 926 430 124 6 3
    FillRR $g $lineB 926 442 54 6 3
    FillRR $g $lineA 998 414 28 8 4
    FillRR $g $lineB 1032 414 34 8 4
  }finally{$window.Dispose();$chrome.Dispose();$lineA.Dispose();$lineB.Dispose();$lineMuted.Dispose()}

  GlassPanel $g 848 494 270 68 24 $p.P 230 '#FFFFFF' 28
  $ctaLine=New-Object Drawing.SolidBrush (C '#FFFFFF' 64)
  $ctaAccent=New-Object Drawing.SolidBrush (C '#FFF7ED' 218)
  try{
    FillRR $g $ctaLine 878 512 144 10 5
    FillRR $g $ctaLine 878 532 106 10 5
    FillRR $g $ctaAccent 1036 510 40 12 6
    FillRR $g $ctaAccent 1082 526 16 16 8
  }finally{$ctaLine.Dispose();$ctaAccent.Dispose()}

  Glow $g 1128 326 58 $p.S 12
  Glow $g 842 308 46 $p.P 12
}
function AiWorkflowScene($g,$p){
  $chips=@($p.K | Select-Object -First 3)
  if($chips.Count -eq 0){$chips=@('AI','Workflow','Tools')}

  GlassPanel $g 842 82 308 222 34 '#101E2A' 216 '#E7EDFF' 24
  Tag $g 'AI WORKFLOW' 868 104 '#FFFFFF' '#0F172A' 12 10 26 | Out-Null
  TagRow $g $chips 868 142 '#102734' '#ECFEFF' 12 10 24

  $card=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(228,11,24,38))
  $cardStroke=New-Object Drawing.Pen (C '#FFFFFF' 26),1
  $muted=New-Object Drawing.SolidBrush (C '#FFFFFF' 22)
  $link=New-Object Drawing.Pen (C '#FFFFFF' 52),2
  $primary=New-Object Drawing.SolidBrush (C $p.P 230)
  $secondary=New-Object Drawing.SolidBrush (C $p.S 220)
  try{
    $link.StartCap='Round'
    $link.EndCap='Round'
    FillRR $g $card 872 188 78 72 18
    FillRR $g $card 958 174 78 88 18
    FillRR $g $card 1044 188 78 72 18
    StrokeRR $g $cardStroke 872 188 78 72 18
    StrokeRR $g $cardStroke 958 174 78 88 18
    StrokeRR $g $cardStroke 1044 188 78 72 18
    $g.DrawLine($link,950,224,958,218)
    $g.DrawLine($link,1036,218,1044,224)

    FillRR $g $primary 886 202 34 10 5
    FillRR $g $muted 886 220 46 8 4
    FillRR $g $muted 886 236 34 8 4
    FillRR $g $secondary 914 238 16 16 8

    FillRR $g $secondary 972 188 42 10 5
    FillRR $g $muted 972 208 50 8 4
    FillRR $g $muted 972 224 36 8 4
    FillRR $g $primary 972 240 22 10 5
    FillRR $g $secondary 1000 240 20 10 5

    FillRR $g $secondary 1058 202 34 10 5
    FillRR $g $muted 1058 220 46 8 4
    FillRR $g $muted 1058 236 34 8 4
    FillRR $g $primary 1086 238 16 16 8
  }finally{$card.Dispose();$cardStroke.Dispose();$muted.Dispose();$link.Dispose();$primary.Dispose();$secondary.Dispose()}

  GlassPanel $g 888 330 224 132 28 '#101E2A' 214 '#D8F7E5' 22
  Tag $g 'SYSTEM MAP' 912 352 '#FFFFFF' '#0F172A' 11 10 24 | Out-Null

  $window=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(228,13,27,41))
  $chrome=New-Object Drawing.SolidBrush (C '#FFFFFF' 30)
  $lineA=New-Object Drawing.SolidBrush (C $p.P 224)
  $lineB=New-Object Drawing.SolidBrush (C $p.S 214)
  $lineMuted=New-Object Drawing.SolidBrush (C '#FFFFFF' 26)
  $pulse=New-Object Drawing.SolidBrush (C '#FFFFFF' 42)
  try{
    FillRR $g $window 912 380 176 60 16
    FillRR $g $chrome 926 392 10 10 5
    FillRR $g $chrome 942 392 10 10 5
    FillRR $g $chrome 958 392 10 10 5
    FillRR $g $lineA 926 414 70 8 4
    FillRR $g $lineMuted 926 430 124 6 3
    FillRR $g $lineB 926 442 54 6 3
    FillRR $g $lineA 998 414 28 8 4
    FillRR $g $lineB 1032 414 34 8 4
    $g.FillEllipse($pulse,1062,392,10,10)
  }finally{$window.Dispose();$chrome.Dispose();$lineA.Dispose();$lineB.Dispose();$lineMuted.Dispose();$pulse.Dispose()}

  GlassPanel $g 848 494 270 68 24 $p.P 230 '#FFFFFF' 28
  $ctaLine=New-Object Drawing.SolidBrush (C '#FFFFFF' 64)
  $ctaAccent=New-Object Drawing.SolidBrush (C '#FFF7ED' 218)
  try{
    FillRR $g $ctaLine 878 512 144 10 5
    FillRR $g $ctaLine 878 532 106 10 5
    FillRR $g $ctaAccent 1036 510 40 12 6
    FillRR $g $ctaAccent 1082 526 16 16 8
  }finally{$ctaLine.Dispose();$ctaAccent.Dispose()}

  Glow $g 1128 326 58 $p.S 12
  Glow $g 842 308 46 $p.P 12
}
function PlayBadge($g,[float]$x,[float]$y,[string]$accent,[float]$size=56){
  $shadow=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(26,0,12,24))
  $orb=New-Object Drawing.SolidBrush (C $accent 234)
  $ring=New-Object Drawing.Pen (C '#FFFFFF' 44),1.2
  $icon=New-Object Drawing.SolidBrush ([Drawing.Color]::White)
  $glint=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(42,255,255,255))
  try{
    $g.FillEllipse($shadow,$x+6,$y+8,$size,$size)
    $g.FillEllipse($orb,$x,$y,$size,$size)
    $g.DrawEllipse($ring,$x,$y,$size,$size)
    $g.FillEllipse($glint,$x+8,$y+8,($size*0.34),($size*0.22))
    $g.FillPolygon($icon,[Drawing.PointF[]]@(
      [Drawing.PointF]::new($x + ($size*0.40),$y + ($size*0.30)),
      [Drawing.PointF]::new($x + ($size*0.40),$y + ($size*0.70)),
      [Drawing.PointF]::new($x + ($size*0.74),$y + ($size*0.50))
    ))
  }finally{$shadow.Dispose();$orb.Dispose();$ring.Dispose();$icon.Dispose();$glint.Dispose()}
}
function VideoScene($g,$p){
  $chips=@($p.K | Select-Object -First 3)
  if($chips.Count -eq 0){$chips=@('Video','Motion','Prompt')}

  GlassPanel $g 842 82 308 226 34 '#101E2A' 216 '#FFE7C2' 24
  Tag $g 'VIDEO FLOW' 868 104 '#FFFFFF' '#0F172A' 12 10 26 | Out-Null
  TagRow $g $chips 868 142 '#102734' '#ECFEFF' 12 10 24

  $frame=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(232,12,26,40))
  $frameStroke=New-Object Drawing.Pen (C '#FFFFFF' 24),1
  $track=New-Object Drawing.Pen (C '#FFFFFF' 54),2
  $waveA=New-Object Drawing.SolidBrush (C $p.P 224)
  $waveB=New-Object Drawing.SolidBrush (C $p.S 218)
  $ghost=New-Object Drawing.SolidBrush (C '#FFFFFF' 18)
  try{
    FillRR $g $frame 872 182 250 96 18
    StrokeRR $g $frameStroke 872 182 250 96 18
    FillRR $g $ghost 886 196 66 60 14
    FillRR $g $ghost 964 196 66 60 14
    FillRR $g $ghost 1042 196 66 60 14
    FillRR $g $waveA 900 242 38 8 4
    FillRR $g $waveB 978 242 38 8 4
    FillRR $g $waveA 1056 242 38 8 4
    $g.DrawLine($track,898,266,1092,266)
    FillRR $g $waveB 928 262 56 8 4
    FillRR $g $waveA 1002 262 38 8 4
    PlayBadge $g 968 202 $p.P 56
  }finally{$frame.Dispose();$frameStroke.Dispose();$track.Dispose();$waveA.Dispose();$waveB.Dispose();$ghost.Dispose()}

  GlassPanel $g 894 330 228 132 28 '#101E2A' 214 '#D8F7E5' 22
  Tag $g 'TIMELINE' 918 352 '#FFFFFF' '#0F172A' 11 10 24 | Out-Null

  $timeline=New-Object Drawing.Pen (C '#FFFFFF' 54),2
  $timeline.StartCap='Round'
  $timeline.EndCap='Round'
  $barA=New-Object Drawing.SolidBrush (C $p.P 226)
  $barB=New-Object Drawing.SolidBrush (C $p.S 220)
  $muted=New-Object Drawing.SolidBrush (C '#FFFFFF' 22)
  $playhead=New-Object Drawing.SolidBrush (C '#FFF7ED' 226)
  try{
    $g.DrawLine($timeline,920,440,1094,440)
    for($i=0;$i -lt 6;$i++){
      FillRR $g $muted (924+($i*28)) 392 18 40 6
    }
    FillRR $g $barA 924 404 18 28 6
    FillRR $g $barB 952 396 18 36 6
    FillRR $g $barA 980 386 18 46 6
    FillRR $g $barB 1008 400 18 32 6
    FillRR $g $barA 1036 394 18 38 6
    FillRR $g $barB 1064 406 18 26 6
    FillRR $g $playhead 1004 374 4 74 2
    FillRR $g $muted 922 448 132 8 4
    FillRR $g $barA 922 448 88 8 4
  }finally{$timeline.Dispose();$barA.Dispose();$barB.Dispose();$muted.Dispose();$playhead.Dispose()}

  GlassPanel $g 848 494 270 68 24 $p.P 230 '#FFFFFF' 28
  $ctaLine=New-Object Drawing.SolidBrush (C '#FFFFFF' 64)
  $ctaAccent=New-Object Drawing.SolidBrush (C '#FFF7ED' 218)
  try{
    FillRR $g $ctaLine 878 512 144 10 5
    FillRR $g $ctaLine 878 532 106 10 5
    FillRR $g $ctaAccent 1036 510 40 12 6
    FillRR $g $ctaAccent 1082 526 16 16 8
  }finally{$ctaLine.Dispose();$ctaAccent.Dispose()}

  Glow $g 1128 324 58 $p.S 12
  Glow $g 842 306 46 $p.P 12
}
function OfficeAppBadge($g,[float]$x,[float]$y,[string]$letter,[string]$color,[float]$size=66){
  $shadow=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(28,0,12,24))
  $shell=New-Object Drawing.SolidBrush (C '#07131B' 226)
  $panel=New-Object Drawing.SolidBrush (C $color 238)
  $shine=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(36,255,255,255))
  $font=New-Object Drawing.Font('Segoe UI',($size*0.42),[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
  $text=New-Object Drawing.SolidBrush ([Drawing.Color]::White)
  $stroke=New-Object Drawing.Pen (C '#FFFFFF' 28),1
  try{
    FillRR $g $shadow ($x+6) ($y+8) $size $size 18
    FillRR $g $shell $x $y $size $size 18
    StrokeRR $g $stroke $x $y $size $size 18
    FillRR $g $panel ($x+10) ($y+10) ($size-20) ($size-20) 14
    $g.FillEllipse($shine,$x+17,$y+16,($size*0.24),($size*0.16))
    $sf=NewTextFormat
    $sf.Alignment='Center'
    $sf.LineAlignment='Center'
    try{$g.DrawString($letter,$font,$text,[Drawing.RectangleF]::new($x+10,$y+7,$size-20,$size-16),$sf)}finally{$sf.Dispose()}
  }finally{$shadow.Dispose();$shell.Dispose();$panel.Dispose();$shine.Dispose();$font.Dispose();$text.Dispose();$stroke.Dispose()}
}
function OfficeAgentScene($g,$p){
  GlassPanel $g 842 82 308 226 34 '#101E2A' 216 '#D7ECFF' 24
  Tag $g 'MICROSOFT 365' 868 104 '#FFFFFF' '#0F172A' 12 10 26 | Out-Null
  TagRow $g @('Word','Excel','PowerPoint') 868 142 '#102734' '#ECFEFF' 12 10 24

  $card=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(228,11,24,38))
  $cardStroke=New-Object Drawing.Pen (C '#FFFFFF' 26),1
  $muted=New-Object Drawing.SolidBrush (C '#FFFFFF' 24)
  $word=New-Object Drawing.SolidBrush (C '#2563EB' 226)
  $excel=New-Object Drawing.SolidBrush (C '#22C55E' 224)
  $powerpoint=New-Object Drawing.SolidBrush (C '#F97316' 224)
  $link=New-Object Drawing.Pen (C '#FFFFFF' 54),2
  try{
    $link.StartCap='Round'
    $link.EndCap='Round'
    FillRR $g $card 872 188 70 76 18
    FillRR $g $card 968 174 84 98 20
    FillRR $g $card 1078 188 70 76 18
    StrokeRR $g $cardStroke 872 188 70 76 18
    StrokeRR $g $cardStroke 968 174 84 98 20
    StrokeRR $g $cardStroke 1078 188 70 76 18
    $g.DrawLine($link,942,226,968,220)
    $g.DrawLine($link,1052,220,1078,226)

    FillRR $g $word 886 204 42 10 5
    FillRR $g $muted 886 222 34 8 4
    FillRR $g $muted 886 238 44 8 4

    FillRR $g $excel 984 190 42 10 5
    FillRR $g $muted 984 210 50 8 4
    FillRR $g $muted 984 226 40 8 4
    FillRR $g $word 984 246 18 12 6
    FillRR $g $excel 1008 246 18 12 6
    FillRR $g $powerpoint 1032 246 18 12 6

    FillRR $g $powerpoint 1092 204 34 10 5
    FillRR $g $muted 1092 222 42 8 4
    FillRR $g $muted 1092 238 28 8 4
  }finally{$card.Dispose();$cardStroke.Dispose();$muted.Dispose();$word.Dispose();$excel.Dispose();$powerpoint.Dispose();$link.Dispose()}

  GlassPanel $g 886 330 236 132 28 '#101E2A' 214 '#D8F7E5' 22
  Tag $g 'AGENT MODE' 912 352 '#FFFFFF' '#0F172A' 11 10 24 | Out-Null

  $window=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(228,13,27,41))
  $chrome=New-Object Drawing.SolidBrush (C '#FFFFFF' 30)
  $lineA=New-Object Drawing.SolidBrush (C $p.P 224)
  $lineB=New-Object Drawing.SolidBrush (C $p.S 214)
  $lineC=New-Object Drawing.SolidBrush (C '#F97316' 214)
  $lineMuted=New-Object Drawing.SolidBrush (C '#FFFFFF' 26)
  try{
    FillRR $g $window 912 382 184 58 16
    FillRR $g $chrome 926 394 10 10 5
    FillRR $g $chrome 942 394 10 10 5
    FillRR $g $chrome 958 394 10 10 5
    FillRR $g $lineA 928 416 58 8 4
    FillRR $g $lineMuted 928 432 132 6 3
    FillRR $g $lineB 994 416 26 8 4
    FillRR $g $lineC 1028 416 34 8 4
  }finally{$window.Dispose();$chrome.Dispose();$lineA.Dispose();$lineB.Dispose();$lineC.Dispose();$lineMuted.Dispose()}

  GlassPanel $g 848 494 270 68 24 $p.P 230 '#FFFFFF' 28
  $ctaLine=New-Object Drawing.SolidBrush (C '#FFFFFF' 64)
  $ctaAccent=New-Object Drawing.SolidBrush (C '#FFF7ED' 218)
  try{
    FillRR $g $ctaLine 878 512 144 10 5
    FillRR $g $ctaLine 878 532 106 10 5
    FillRR $g $ctaAccent 1036 510 40 12 6
    FillRR $g $ctaAccent 1082 526 16 16 8
  }finally{$ctaLine.Dispose();$ctaAccent.Dispose()}

  OfficeAppBadge $g 1018 28 'W' '#2563EB' 64
  OfficeAppBadge $g 1088 58 'X' '#16A34A' 64
  OfficeAppBadge $g 1052 126 'P' '#EA580C' 64
  Glow $g 1128 326 58 $p.S 12
  Glow $g 842 308 46 $p.P 12
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
    $variant=if($p.Contains('Variant')){[string]$p['Variant']}else{''}

    $renderTitle=if($p.Contains('CoverTitle') -and $p['CoverTitle']){[string]$p['CoverTitle']}else{$title}

    $renderTag=if($p.Contains('CoverTag') -and $p['CoverTag']){[string]$p['CoverTag']}else{$tag}
    if($variant -eq 'mobile-compare'){
      MobileBackdropScene $g $p
      FrameworkBadge $g $p 1010 26
      GlassPanel $g 520 84 498 470 38 '#07131B' 210 '#D9F7FF' 26
    }elseif($variant -eq 'state-management'){
      StateManagementScene $g $p
      GlassPanel $g 520 84 498 470 38 '#07131B' 210 '#D9F7FF' 24
    }elseif($variant -eq 'flutter-general'){
      BackdropScene $g $p
      GlassPanel $g 520 84 498 470 38 '#07131B' 210 '#D9F7FF' 24
      FlutterGlyph $g 1040 32 1.9
    }elseif($variant -eq 'ai-model-neuro'){
      AiModelNeuroScene $g $p
      GlassPanel $g 520 84 498 470 38 '#07131B' 212 '#E6EDFF' 24
    }elseif($variant -eq 'ai-workflow'){
      AiWorkflowScene $g $p
      GlassPanel $g 520 84 498 470 38 '#07131B' 212 '#E6EDFF' 24
    }elseif($variant -eq 'office-agent'){
      OfficeAgentScene $g $p
      GlassPanel $g 520 84 498 470 38 '#07131B' 212 '#D7ECFF' 24
    }elseif($variant -eq 'video-scene'){
      VideoScene $g $p
      GlassPanel $g 520 84 498 470 38 '#07131B' 212 '#FFE7C2' 28
    }elseif($variant -eq 'neuro-prompts'){
      NeuroPromptScene $g $p
      ExcelLogo $g 1034 26 132
      GlassPanel $g 520 84 498 470 38 '#07131B' 212 '#FFE7C2' 28
    }else{
      BackdropScene $g $p
      ExcelLogo $g 1034 26 132
      GlassPanel $g 520 84 498 470 38 '#07131B' 210 '#D8F7E5' 26
    }
    $titleLayout=FitTitleLayout $g $renderTitle $p.Hook

    Tag $g $renderTag 548 110 '#FFFFFF' '#0F172A' 18 16 36 | Out-Null
    WrapTextBlock $g $renderTitle 548 164 $titleLayout.TitleWidth $titleLayout.TitleHeight $titleLayout.TitleSize '#F8FAFC' 'Segoe UI' ([Drawing.FontStyle]::Bold) 248
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
  $scriptPattern='<script[^>]*application/ld\+json[^>]*>(.*?)</script>'
  $m=$null
  foreach($candidate in [regex]::Matches($html,$scriptPattern,'Singleline')){
    $jsonText=$candidate.Groups[1].Value.Trim()
    try{$obj=$jsonText|ConvertFrom-Json}catch{continue}
    $typeProp=$obj.PSObject.Properties['@type']
    if($null -ne $typeProp -and @($typeProp.Value) -contains 'BlogPosting'){
      $m=$candidate
      break
    }
  }
  if($null -eq $m){return $html}
  $obj=($m.Groups[1].Value.Trim()|ConvertFrom-Json)
  $obj|Add-Member -NotePropertyName image -NotePropertyValue ([ordered]@{
    '@type'='ImageObject'
    url=$url
    contentUrl=$url
    license=$codingLiquidsTermsUrl
    acquireLicensePage=$imageAcquireLicenseUrl
    width=1200
    height=630
    caption="$title by Sagnik Bhattacharya for Coding Liquids"
    creditText='Sagnik Bhattacharya for Coding Liquids'
    copyrightNotice=$codingLiquidsCopyrightNotice
    creator=[ordered]@{'@type'='Person';name='Sagnik Bhattacharya';url='https://sagnikbhattacharya.com'}
    publisher=[ordered]@{'@type'='Organization';name='Coding Liquids';url=$codingLiquidsUrl}
    copyrightHolder=[ordered]@{'@type'='Organization';name='Coding Liquids';url=$codingLiquidsUrl}
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
function GetPostTitle([string]$html,[string]$slug){
  foreach($pattern in @(
    '<h1 class="blog-post-title">(.*?)</h1>',
    '<meta property="og:title" content="([^"]+)"',
    '<title>(.*?)</title>'
  )){
    $match=[regex]::Match($html,$pattern,'Singleline')
    if($match.Success){
      $title=[Net.WebUtility]::HtmlDecode($match.Groups[1].Value.Trim())
      $title=$title -replace '\s+\|\s+Sagnik Bhattacharya$',''
      if($title){return $title}
    }
  }
  return (($slug -replace '-',' ') -replace '\s+',' ').Trim()
}
$posts=@(
@{Slug='advanced-formulas';P='#0F766E';S='#34D399';Hook='Move beyond basic formulas and start solving real spreadsheet problems faster.';CTA='Master These 15 Formulas';K=@('LET','LAMBDA','SUMPRODUCT');Cue='formula blocks, dynamic arrays, and advanced spreadsheet logic'},
@{Slug='charts-visualisations';P='#1D4ED8';S='#F97316';Hook='Build charts that tell a clear story instead of just filling space.';CTA='Create Better Excel Charts';K=@('Line','Bar','Story');Cue='bold charts, trend lines, and presentation-ready visuals'},
@{Slug='chatgpt-excel-guide';P='#047857';S='#F59E0B';Hook='Turn plain-English prompts into formulas, macros, and cleaner analysis in minutes.';CTA='Use ChatGPT To Save Hours';K=@('Prompts','Formulas','Analysis');Cue='AI chat interface, spreadsheet grids, and formula visuals'},
@{Slug='claude-ai-excel-formulas';P='#4338CA';S='#14B8A6';Hook='Turn plain English prompts into ready-to-use Excel formulas in minutes.';CTA='Write Smarter Formulas';K=@('Prompts','Formula','AI');Cue='AI prompt styling, formulas, and spreadsheet visuals'},
@{Slug='claude-ai-excel-macros';P='#4F46E5';S='#F59E0B';Hook='Use AI to turn repetitive spreadsheet work into reusable VBA automation.';CTA='Generate Better Macros';K=@('VBA','Macros','Automation');Cue='macro automation cues, code blocks, and workflow visuals'},
@{Slug='claude-debug-formulas';P='#0F766E';S='#EF4444';Hook='Catch broken formulas quickly and understand exactly how to fix them.';CTA='Fix Formula Errors Fast';K=@('Errors','Fixes','Explain');Cue='formula debugging cues, alerts, and clean fixes'},
@{Slug='clean-messy-data';P='#047857';S='#F59E0B';Hook='Clean duplicates, spacing, and broken columns without wasting hours.';CTA='Clean Data Much Faster';K=@('Trim','Split','Clean');Cue='messy spreadsheet elements transforming into organised rows'},
@{Slug='conditional-formatting-tips';P='#B45309';S='#EC4899';Hook='Make important numbers jump out instantly with smarter formatting rules.';CTA='Highlight What Matters';K=@('Heatmaps','Icons','Rules');Cue='highlighted cells, colour scales, and formatting triggers'},
@{Slug='copilot-automate-tasks';P='#2563EB';S='#22C55E';Hook='Let Copilot handle sorting, formatting, and repeat work for you.';CTA='Automate The Busywork';K=@('Sort','Format','Repeat');Cue='automation loops, task cards, and spreadsheet workflow elements'},
@{Slug='copilot-data-analysis';P='#1D4ED8';S='#06B6D4';Hook='Use AI to surface insights, trends, and summaries from messy data.';CTA='Analyse Data With AI';K=@('Insights','Charts','Trends');Cue='data analysis cards, charts, and insight panels'},
@{Slug='data-validation';P='#0F766E';S='#22C55E';Hook='Stop bad inputs before they break your spreadsheet or your reports.';CTA='Prevent Spreadsheet Errors';K=@('Dropdowns','Checks','Rules');Cue='validation controls, dropdowns, and error-prevention signals'},
@{Slug='dynamic-dashboards';P='#059669';S='#0EA5E9';Hook='Create interactive dashboards that stakeholders can understand at a glance.';CTA='Build Dynamic Dashboards';K=@('KPI','Slicers','Charts');Cue='dashboard cards, KPIs, and interactive chart elements'},
@{Slug='excel-ai-prompts';P='#F97316';S='#22C55E';Hook='Use specificity, context, and output framing to get formulas, macros, and analysis that actually work.';CTA='Copy. Paste. Get Results.';K=@('Copy','Paste','Results');Cue='attention-driven prompt cards, conversion cues, and spreadsheet grids';Variant='neuro-prompts'},
@{Slug='excel-vs-google-sheets';P='#166534';S='#2563EB';Hook='Choose the spreadsheet tool that actually fits the way you work.';CTA='Pick The Right Tool';K=@('Offline','Collab','AI');Cue='side-by-side spreadsheet comparison panels and decision cues'},
@{Slug='financial-modelling';P='#0F172A';S='#10B981';Hook='Build cleaner forecasts, cash flow models, and scenario analysis in Excel.';CTA='Build Your First Model';K=@('Revenue','Cash Flow','Scenario');Cue='forecast visuals, tables, and financial model elements'},
@{Slug='flutter-state-management';P='#2563EB';S='#22D3EE';Hook='Use app size, async complexity, and team needs to choose the right state management pattern.';CTA='Pick The Right Pattern';K=@('Provider','Riverpod','BLoC');Cue='comparison cards, a dark grid background, and choice-focused messaging';Variant='state-management';CoverTag='Flutter 2026';CoverTitle='Provider vs Riverpod vs BLoC Best For Your App?'},
@{Slug='flutter-vs-react-native';P='#2563EB';S='#22D3EE';Hook='Compare performance, DX, hiring, and product fit before you commit.';CTA='Choose The Right Framework';K=@('Flutter','React Native','2026');Cue='Flutter and React Native logos, mobile UI cards, and a framework comparison visual';Variant='mobile-compare'},
@{Slug='gemini-ai-excel';P='#2563EB';S='#F97316';Hook='Use Gemini to solve formula blocks, data questions, and spreadsheet busywork faster.';CTA='Get Excel Answers Faster';K=@('Gemini','Excel','Speed');Cue='AI prompt styling and spreadsheet visuals'},
@{Slug='getting-started-copilot-excel';P='#2563EB';S='#14B8A6';Hook='Get comfortable with Copilot fast and start using it inside real sheets.';CTA='Start Using Copilot';K=@('Prompt','Analyse','Formula');Cue='AI assistant styling, onboarding cues, and spreadsheet cards'},
@{Slug='index-match-guide';P='#166534';S='#F59E0B';Hook='Replace brittle lookups with a more flexible and reliable formula setup.';CTA='Upgrade Your Lookups';K=@('INDEX','MATCH','Lookup');Cue='lookup references, match arrows, and formula comparison cues'},
@{Slug='keyboard-shortcuts';P='#1F2937';S='#10B981';Hook='Memorise the shortcuts that save time every single day in Excel.';CTA='Save Hours Every Week';K=@('Ctrl','Navigate','Format');Cue='keyboard cues, fast actions, and productivity shortcuts'},
@{Slug='mastering-pivot-tables';P='#0F766E';S='#F59E0B';Hook='Summarise large data sets quickly and turn rows into useful answers.';CTA='Master Pivot Tables';K=@('Rows','Values','Groups');Cue='pivot layouts, summary visuals, and grouped data blocks'},
@{Slug='power-pivot-guide';P='#1E3A8A';S='#10B981';Hook='Handle massive datasets with better relationships, DAX, and data models.';CTA='Scale Beyond 1M Rows';K=@('DAX','Relations','Models');Cue='connected data tables, model relationships, and scale cues'},
@{Slug='power-query-guide';P='#047857';S='#06B6D4';Hook='Automate data cleaning and transformation instead of repeating manual prep.';CTA='Automate Data Prep';K=@('Source','Transform','Load');Cue='data pipelines, transformation steps, and import flow elements'},
@{Slug='what-if-analysis';P='#1D4ED8';S='#F59E0B';Hook='Compare outcomes, test assumptions, and make better Excel decisions.';CTA='Run Better Scenarios';K=@('Goal Seek','Scenarios','Solver');Cue='spreadsheet visuals and scenario comparison elements'},
@{Slug='vlookup-vs-xlookup';P='#166534';S='#EA580C';Hook='See when the legacy lookup still works and when the modern one wins.';CTA='Choose The Better Lookup';K=@('VLOOKUP','XLOOKUP','Compare');Cue='lookup comparisons, arrows, and side-by-side formula cues'}
)

$manifestPath=Join-Path $PSScriptRoot 'blog_cluster_covers.json'
if(Test-Path $manifestPath){
  $manifestPosts=Get-Content $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
  foreach($item in $manifestPosts){
    if($item.slug -in $posts.Slug){continue}
    $palette=switch($item.category){
      'Flutter' { @{P='#2563EB';S='#22D3EE';Variant='flutter-general'} }
      'AI + Excel' { @{P='#2563EB';S='#22C55E';Variant=''} }
      'AI' { @{P='#7C3AED';S='#22C55E';Variant='ai-workflow'} }
      'Video' { @{P='#F97316';S='#14B8A6';Variant='video-scene'} }
      default { @{P='#0F766E';S='#34D399';Variant=''} }
    }
    $primary=if($item.PSObject.Properties['primaryColor'] -and $item.primaryColor){[string]$item.primaryColor}elseif($item.PSObject.Properties['primary'] -and $item.primary){[string]$item.primary}else{[string]$palette.P}
    $secondary=if($item.PSObject.Properties['secondaryColor'] -and $item.secondaryColor){[string]$item.secondaryColor}elseif($item.PSObject.Properties['secondary'] -and $item.secondary){[string]$item.secondary}else{[string]$palette.S}
    $variant=if($item.PSObject.Properties['variant'] -and $item.variant){[string]$item.variant}else{[string]$palette.Variant}
    $entry=[ordered]@{
      Slug=[string]$item.slug
      P=$primary
      S=$secondary
      Hook=[string]$item.hook
      CTA=[string]$item.cta
      K=@($item.keywords | ForEach-Object { [string]$_ })
      Cue=[string]$item.cue
    }
    if($variant){
      $entry.Variant=$variant
    }
    if($item.PSObject.Properties['coverTag'] -and $item.coverTag){
      $entry.CoverTag=[string]$item.coverTag
    }
    if($item.PSObject.Properties['coverTitle'] -and $item.coverTitle){
      $entry.CoverTitle=[string]$item.coverTitle
    }
    if($item.PSObject.Properties['portraitFocus'] -and $item.portraitFocus){
      $entry.PortraitFocus=[string]$item.portraitFocus
    }
    $posts+=,$entry
  }
}

$root=Resolve-Path (Join-Path $PSScriptRoot '..')
$public=Join-Path $root 'public'
$blog=Join-Path $public 'blog'
$imgDir=Join-Path $blog 'images'
$utf8=[Text.UTF8Encoding]::new($false)
if(-not(Test-Path $imgDir)){New-Item -ItemType Directory -Path $imgDir|Out-Null}
$selectedPosts=$posts
if($Slug){
  $missing=@($Slug | Where-Object { $_ -notin $posts.Slug })
  if($missing.Count){
    throw ('Unknown slug(s): ' + ($missing -join ', '))
  }
  $selectedPosts=@($posts | Where-Object { $Slug -contains $_.Slug })
}else{
  Get-ChildItem $imgDir -File -ErrorAction SilentlyContinue | Remove-Item -Force
}
$head=[Drawing.Image]::FromFile((Join-Path $public 'sagnik-bhattacharya.png'))
try{
  foreach($p in $selectedPosts){
    $htmlPath=Join-Path $blog ($p.Slug+'.html')
    if(-not(Test-Path $htmlPath)){continue}
    $html=[IO.File]::ReadAllText($htmlPath,[Text.Encoding]::UTF8)
    $title=GetPostTitle $html $p.Slug
    $tagMatch=[regex]::Match($html,'<span class="blog-post-tag">(.*?)</span>','Singleline')
    $tag=if($tagMatch.Success){[Net.WebUtility]::HtmlDecode($tagMatch.Groups[1].Value.Trim())}else{'Excel Guide'}
    $file=$p.Slug+'-sagnik-bhattacharya-coding-liquids.jpg'
    $src='/blog/images/'+$file
    $url='https://sagnikbhattacharya.com/blog/images/'+$file
    $alt='Coding Liquids blog cover featuring Sagnik Bhattacharya for '+$title+', with '+$p.Cue+'.'
    NewCover $p $head $title $tag (Join-Path $imgDir $file)
    if(-not $ImageOnly){
      $html=SetImageMeta $html $url $alt
      $html=SetJsonImage $html $url $title
      $html=SetCoverHtml $html $src $alt
      [IO.File]::WriteAllText($htmlPath,$html,$utf8)
    }
  }
}finally{$head.Dispose()}
