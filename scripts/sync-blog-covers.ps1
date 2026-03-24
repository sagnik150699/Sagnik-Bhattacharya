Set-StrictMode -Version Latest
$ErrorActionPreference='Stop'
Add-Type -AssemblyName System.Drawing

function C($hex,[int]$a=255){$h=$hex.TrimStart('#');[Drawing.Color]::FromArgb($a,[Convert]::ToInt32($h.Substring(0,2),16),[Convert]::ToInt32($h.Substring(2,2),16),[Convert]::ToInt32($h.Substring(4,2),16))}
function PathRR([float]$x,[float]$y,[float]$w,[float]$h,[float]$r){$d=$r*2;$p=New-Object Drawing.Drawing2D.GraphicsPath;$p.AddArc($x,$y,$d,$d,180,90);$p.AddArc($x+$w-$d,$y,$d,$d,270,90);$p.AddArc($x+$w-$d,$y+$h-$d,$d,$d,0,90);$p.AddArc($x,$y+$h-$d,$d,$d,90,90);$p.CloseFigure();$p}
function FillRR($g,$b,[float]$x,[float]$y,[float]$w,[float]$h,[float]$r){$p=PathRR $x $y $w $h $r; try{$g.FillPath($b,$p)}finally{$p.Dispose()}}
function StrokeRR($g,$pen,[float]$x,[float]$y,[float]$w,[float]$h,[float]$r){$p=PathRR $x $y $w $h $r; try{$g.DrawPath($pen,$p)}finally{$p.Dispose()}}
function Glow($g,[float]$cx,[float]$cy,[float]$r,[string]$hex){for($i=7;$i-ge 1;$i--){$size=$r+(28*$i);$b=New-Object Drawing.SolidBrush (C $hex ([Math]::Max(8,[int](18*$i)))); try{$g.FillEllipse($b,$cx-($size/2),$cy-($size/2),$size,$size)}finally{$b.Dispose()}}}
function Panel($g,[float]$x,[float]$y,[float]$w,[float]$h,[float]$r,[string]$fill,[string]$line){$sb=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(24,20,16,10));$fb=New-Object Drawing.SolidBrush (C $fill 228);$pen=New-Object Drawing.Pen (C $line 140),1.5; try{FillRR $g $sb $x ($y+16) $w $h $r;FillRR $g $fb $x $y $w $h $r;StrokeRR $g $pen $x $y $w $h $r}finally{$sb.Dispose();$fb.Dispose();$pen.Dispose()}}
function Arrow($g,[string]$hex,[float]$x1,[float]$y1,[float]$x2,[float]$y2,[float]$t=4){$pen=New-Object Drawing.Pen (C $hex 220),$t;$pen.StartCap='Round';$pen.EndCap='Round'; try{$g.DrawLine($pen,$x1,$y1,$x2,$y2);$dx=$x2-$x1;$dy=$y2-$y1;$len=[Math]::Sqrt(($dx*$dx)+($dy*$dy));if($len-gt 0){$ux=$dx/$len;$uy=$dy/$len;$size=12;$l=[Drawing.PointF]::new($x2-($ux*$size)-($uy*($size*.7)),$y2-($uy*$size)+($ux*($size*.7)));$r=[Drawing.PointF]::new($x2-($ux*$size)+($uy*($size*.7)),$y2-($uy*$size)-($ux*($size*.7)));$b=New-Object Drawing.SolidBrush (C $hex 220); try{$g.FillPolygon($b,[Drawing.PointF[]]@([Drawing.PointF]::new($x2,$y2),$l,$r))}finally{$b.Dispose()}}}finally{$pen.Dispose()}}
function Check($g,[string]$hex,[float]$x,[float]$y){$p=New-Object Drawing.Pen (C $hex 235),4;$p.StartCap='Round';$p.EndCap='Round'; try{$g.DrawLines($p,[Drawing.PointF[]]@([Drawing.PointF]::new($x,$y+8),[Drawing.PointF]::new($x+10,$y+18),[Drawing.PointF]::new($x+28,$y)))}finally{$p.Dispose()}}
function Chevron($g,[string]$hex,[float]$x,[float]$y){$p=New-Object Drawing.Pen (C $hex 220),3;$p.StartCap='Round';$p.EndCap='Round'; try{$g.DrawLines($p,[Drawing.PointF[]]@([Drawing.PointF]::new($x,$y),[Drawing.PointF]::new($x+8,$y+8),[Drawing.PointF]::new($x+16,$y)))}finally{$p.Dispose()}}
function Spark($g,[string]$hex,[float]$x,[float]$y,[float]$s){$p=New-Object Drawing.Pen (C $hex 220),3;$p.StartCap='Round';$p.EndCap='Round'; try{$g.DrawLine($p,$x,$y-$s,$x,$y+$s);$g.DrawLine($p,$x-$s,$y,$x+$s,$y);$g.DrawLine($p,$x-($s*.66),$y-($s*.66),$x+($s*.66),$y+($s*.66));$g.DrawLine($p,$x-($s*.66),$y+($s*.66),$x+($s*.66),$y-($s*.66))}finally{$p.Dispose()}}
function GridPanel($g,[float]$x,[float]$y,[float]$w,[float]$h,$p,[string[]]$hi){Panel $g $x $y $w $h 24 $p.F $p.L;$cell=New-Object Drawing.SolidBrush (C $p.F 198);$hl=New-Object Drawing.SolidBrush (C $p.P 210);$pen=New-Object Drawing.Pen (C $p.L 120),1; try{$cols=5;$rows=4;$pad=18;$gap=8;$cw=($w-(2*$pad)-(($cols-1)*$gap))/$cols;$ch=($h-(2*$pad)-(($rows-1)*$gap))/$rows;for($r=0;$r-lt$rows;$r++){for($c=0;$c-lt$cols;$c++){$cx=$x+$pad+($c*($cw+$gap));$cy=$y+$pad+($r*($ch+$gap));$brush=if($hi-contains "$r-$c"){$hl}else{$cell};FillRR $g $brush $cx $cy $cw $ch 10;StrokeRR $g $pen $cx $cy $cw $ch 10}}}finally{$cell.Dispose();$hl.Dispose();$pen.Dispose()}}
function ChartPanel($g,[float]$x,[float]$y,[float]$w,[float]$h,$p){Panel $g $x $y $w $h 24 $p.F $p.L;$axis=New-Object Drawing.Pen (C $p.L 130),2;$b1=New-Object Drawing.SolidBrush (C $p.P 220);$b2=New-Object Drawing.SolidBrush (C $p.S 220);$lp=New-Object Drawing.Pen (C $p.S 240),4;$lp.StartCap='Round';$lp.EndCap='Round'; try{$left=$x+22;$bottom=$y+$h-22;$top=$y+22;$right=$x+$w-20;$g.DrawLine($axis,$left,$top+14,$left,$bottom);$g.DrawLine($axis,$left,$bottom,$right,$bottom);$bw=24;$gap=20;$bars=@(54,96,74,128,110);for($i=0;$i-lt$bars.Count;$i++){$bh=$bars[$i];$bx=$left+24+($i*($bw+$gap));$by=$bottom-$bh;$br=if($i%2-eq 0){$b1}else{$b2};FillRR $g $br $bx $by $bw $bh 8}$pts=[Drawing.PointF[]]@([Drawing.PointF]::new($left+36,$bottom-44),[Drawing.PointF]::new($left+80,$bottom-88),[Drawing.PointF]::new($left+124,$bottom-70),[Drawing.PointF]::new($left+168,$bottom-136),[Drawing.PointF]::new($left+212,$bottom-104));$g.DrawLines($lp,$pts);foreach($pt in $pts){$m=New-Object Drawing.SolidBrush (C $p.S 250); try{$g.FillEllipse($m,$pt.X-6,$pt.Y-6,12,12)}finally{$m.Dispose()}}}finally{$axis.Dispose();$b1.Dispose();$b2.Dispose();$lp.Dispose()}}
function Subject($g,$img){Glow $g 260 140 110 '#FFFFFF';$sb=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(30,18,14,12));$cb=New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(245,255,255,255));$op=New-Object Drawing.Pen ([Drawing.Color]::FromArgb(40,44,24,16)),1.5; try{FillRR $g $sb 54 56 490 542 42;FillRR $g $cb 40 40 490 542 42;StrokeRR $g $op 40 40 490 542 42;$clip=PathRR 52 52 466 518 34; try{$old=$g.Clip;$g.SetClip($clip);$dst=[Drawing.RectangleF]::new(52,52,466,518);$src=[Drawing.RectangleF]::new(166,18,690,760);$g.DrawImage($img,$dst,$src,[Drawing.GraphicsUnit]::Pixel);$fade=[Drawing.RectangleF]::new(410,52,108,518);$fb=New-Object Drawing.Drawing2D.LinearGradientBrush([Drawing.PointF]::new($fade.Left,$fade.Top),[Drawing.PointF]::new($fade.Right,$fade.Top),[Drawing.Color]::FromArgb(0,255,255,255),[Drawing.Color]::FromArgb(165,255,255,255)); try{$g.FillRectangle($fb,$fade)}finally{$fb.Dispose()};$g.Clip=$old}finally{$clip.Dispose()}}finally{$sb.Dispose();$cb.Dispose();$op.Dispose()}}
function Motif($g,$p){switch($p.M){
'formula' {GridPanel $g 620 92 500 202 $p @('0-2','1-1','2-3','3-4');Panel $g 710 334 320 130 24 $p.F $p.L;Arrow $g $p.P 710 524 1018 486;$a=New-Object Drawing.SolidBrush (C $p.S 205);$b=New-Object Drawing.SolidBrush (C $p.P 225);try{FillRR $g $a 744 364 188 24 10;FillRR $g $b 744 400 120 18 9;FillRR $g $a 744 430 236 18 9;FillRR $g $a 744 462 164 18 9}finally{$a.Dispose();$b.Dispose()}}
'charts' {ChartPanel $g 648 104 462 232 $p;Panel $g 748 372 236 160 28 $p.F $p.L;$p1=New-Object Drawing.Pen (C $p.P 230),18;$p2=New-Object Drawing.Pen (C $p.S 230),18;try{$p1.StartCap='Round';$p1.EndCap='Round';$p2.StartCap='Round';$p2.EndCap='Round';$g.DrawArc($p1,790,404,146,100,180,150);$g.DrawArc($p2,790,404,146,100,332,160)}finally{$p1.Dispose();$p2.Dispose()}}
'ai' {GridPanel $g 700 138 386 196 $p @('0-1','1-2','2-2','3-3');Panel $g 612 348 224 136 26 $p.F $p.L;Arrow $g $p.P 820 416 700 416;$bb=New-Object Drawing.SolidBrush (C $p.P 220);try{FillRR $g $bb 640 376 150 58 18;FillRR $g $bb 664 446 92 12 6}finally{$bb.Dispose()};Spark $g $p.S 1042 108 12;Spark $g $p.S 1082 168 9}
'macros' {Panel $g 636 126 454 154 28 $p.F $p.L;Panel $g 690 332 346 162 28 $p.F $p.L;$s1=New-Object Drawing.SolidBrush (C $p.P 220);$s2=New-Object Drawing.SolidBrush (C $p.S 220);try{FillRR $g $s1 676 168 96 52 16;FillRR $g $s2 814 168 96 52 16;FillRR $g $s1 952 168 96 52 16;Arrow $g $p.S 772 194 814 194;Arrow $g $p.S 910 194 952 194;FillRR $g $s2 722 362 122 18 8;FillRR $g $s1 722 394 184 18 8;FillRR $g $s2 722 426 224 18 8;FillRR $g $s1 722 458 154 18 8}finally{$s1.Dispose();$s2.Dispose()}}
'debug' {Panel $g 658 120 424 160 28 $p.F $p.L;Panel $g 726 328 288 176 28 $p.F $p.L;$bad=New-Object Drawing.SolidBrush (C $p.S 210);$good=New-Object Drawing.SolidBrush (C $p.P 220);try{FillRR $g $bad 696 154 264 18 8;FillRR $g $bad 696 188 204 18 8;FillRR $g $good 762 366 214 18 8;FillRR $g $good 762 398 166 18 8;$tb=New-Object Drawing.SolidBrush (C $p.S 235);try{$g.FillPolygon($tb,[Drawing.PointF[]]@([Drawing.PointF]::new(1004,156),[Drawing.PointF]::new(1024,196),[Drawing.PointF]::new(984,196)))}finally{$tb.Dispose()};$cb=New-Object Drawing.SolidBrush (C $p.P 230);try{$g.FillEllipse($cb,934,444,44,44)}finally{$cb.Dispose()};Check $g '#FFFFFF' 944 454}finally{$bad.Dispose();$good.Dispose()}}
'clean' {Panel $g 666 112 432 208 28 $p.F $p.L;Panel $g 740 350 284 152 28 $p.F $p.L;$m=New-Object Drawing.SolidBrush (C $p.S 170);$c=New-Object Drawing.SolidBrush (C $p.P 220);try{for($i=0;$i-lt14;$i++){$mx=700+((13*$i)%130);$my=150+((29*$i)%110);$size=10+(($i*3)%18);FillRR $g $m $mx $my $size (8+(($i*5)%20)) 6};Arrow $g $p.P 846 214 944 214 5;for($r=0;$r-lt3;$r++){for($col=0;$col-lt4;$col++){$cx=964+($col*26);$cy=176+($r*34);FillRR $g $c $cx $cy 20 18 5}};for($r=0;$r-lt3;$r++){FillRR $g $c 774 (380+($r*34)) 216 16 8}}finally{$m.Dispose();$c.Dispose()}}
'conditional' {GridPanel $g 648 100 466 242 $p @('0-0','0-1','1-2','2-3','3-1','3-4');$w=New-Object Drawing.SolidBrush (C $p.P 210);$q=New-Object Drawing.SolidBrush (C $p.S 210);try{FillRR $g $w 724 384 120 74 18;FillRR $g $q 866 384 180 74 18;FillRR $g $w 760 482 238 22 11}finally{$w.Dispose();$q.Dispose()}}
'automation' {Panel $g 654 124 438 170 30 $p.F $p.L;GridPanel $g 756 338 254 156 $p @('0-1','1-2','2-1');$n1=New-Object Drawing.SolidBrush (C $p.P 220);$n2=New-Object Drawing.SolidBrush (C $p.S 220);try{$g.FillEllipse($n1,728,170,40,40);$g.FillEllipse($n2,868,146,40,40);$g.FillEllipse($n1,988,202,40,40);Arrow $g $p.S 768 190 868 166;Arrow $g $p.P 908 166 988 222;Arrow $g $p.S 1008 236 748 208}finally{$n1.Dispose();$n2.Dispose()}}
'validation' {Panel $g 664 112 436 208 30 $p.F $p.L;Panel $g 760 356 244 132 28 $p.F $p.L;$f=New-Object Drawing.SolidBrush (C $p.P 52);$a=New-Object Drawing.SolidBrush (C $p.P 220);try{for($i=0;$i-lt3;$i++){$fy=146+($i*46);FillRR $g $f 698 $fy 264 28 10;Chevron $g $p.P 970 ($fy+10)};$g.FillEllipse($a,856,392,54,54);Check $g '#FFFFFF' 868 406;FillRR $g $a 790 458 184 16 8}finally{$f.Dispose();$a.Dispose()}}
'dashboard' {Panel $g 640 108 468 188 30 $p.F $p.L;ChartPanel $g 748 330 252 176 $p;$k1=New-Object Drawing.SolidBrush (C $p.P 220);$k2=New-Object Drawing.SolidBrush (C $p.S 220);try{FillRR $g $k1 674 144 114 70 20;FillRR $g $k2 810 144 114 70 20;FillRR $g $k1 946 144 114 70 20}finally{$k1.Dispose();$k2.Dispose()}}
'versus' {GridPanel $g 630 116 202 256 $p @('0-1','1-3','3-1');$o=[ordered]@{F='#FFF7ED';L='#FDBA74';P='#F59E0B';S=$p.S};GridPanel $g 900 116 202 256 $o @('0-2','1-1','2-4');Arrow $g $p.S 842 244 894 244 6;Panel $g 732 408 268 90 24 $p.F $p.L}
'finance' {ChartPanel $g 650 106 454 214 $p;Panel $g 742 356 272 142 26 $p.F $p.L;$tb=New-Object Drawing.SolidBrush (C $p.P 200);try{for($r=0;$r-lt4;$r++){FillRR $g $tb 774 (388+($r*26)) 206 14 7}}finally{$tb.Dispose()}}
'lookup' {GridPanel $g 630 120 190 254 $p @('1-0','2-0','3-0');$o=[ordered]@{F=$p.F;L=$p.L;P=$p.S;S=$p.P};GridPanel $g 922 120 190 254 $o @('1-4','2-3','3-2');Arrow $g $p.P 820 170 922 170 5;Arrow $g $p.S 820 228 922 228 5;Arrow $g $p.P 820 286 922 286 5;Panel $g 736 408 270 92 24 $p.F $p.L}
'keyboard' {Panel $g 654 122 438 230 30 $p.F $p.L;$base=New-Object Drawing.SolidBrush (C $p.P 60);$acc=New-Object Drawing.SolidBrush (C $p.S 220);try{for($r=0;$r-lt3;$r++){for($c=0;$c-lt5;$c++){$x=688+($c*72);$y=156+($r*56);$b=if(($r-eq1-and $c-eq1)-or($r-eq1-and $c-eq2)-or($r-eq1-and $c-eq3)){$acc}else{$base};FillRR $g $b $x $y 52 38 12}};Arrow $g $p.S 776 408 972 408 5}finally{$base.Dispose();$acc.Dispose()}}
'pivot' {GridPanel $g 636 110 296 222 $p @('0-0','0-1','1-2','2-2');Panel $g 954 110 146 146 28 $p.F $p.L;Panel $g 756 370 264 126 24 $p.F $p.L;$p1=New-Object Drawing.Pen (C $p.P 230),16;$p2=New-Object Drawing.Pen (C $p.S 230),16;try{$p1.StartCap='Round';$p1.EndCap='Round';$p2.StartCap='Round';$p2.EndCap='Round';$g.DrawArc($p1,978,134,96,96,140,160);$g.DrawArc($p2,978,134,96,96,310,180)}finally{$p1.Dispose();$p2.Dispose()}}
'data-model' {GridPanel $g 640 114 186 186 $p @('0-1','2-2');$o=[ordered]@{F=$p.F;L=$p.L;P=$p.S;S=$p.P};GridPanel $g 862 114 186 186 $o @('1-2','3-3');GridPanel $g 750 336 186 186 $p @('0-0','2-4');Arrow $g $p.S 826 208 862 208 5;Arrow $g $p.P 918 300 842 336 5;Arrow $g $p.S 730 300 800 336 5}
'pipeline' {Panel $g 632 132 458 160 30 $p.F $p.L;$s1=New-Object Drawing.SolidBrush (C $p.P 220);$s2=New-Object Drawing.SolidBrush (C $p.S 220);try{FillRR $g $s1 668 182 100 52 16;FillRR $g $s2 810 182 100 52 16;FillRR $g $s1 952 182 100 52 16;Arrow $g $p.S 768 208 810 208 5;Arrow $g $p.P 910 208 952 208 5}finally{$s1.Dispose();$s2.Dispose()};GridPanel $g 744 340 236 156 $p @('0-2','1-1','2-3')}
}}
function Txt($g,[string]$text,[float]$x,[float]$y,[float]$size,[string]$hex,[string]$fontName='Segoe UI',[Drawing.FontStyle]$style=[Drawing.FontStyle]::Bold,[int]$alpha=235){
  $font = New-Object Drawing.Font($fontName,$size,$style,[Drawing.GraphicsUnit]::Pixel)
  $brush = New-Object Drawing.SolidBrush (C $hex $alpha)
  try { $g.DrawString($text,$font,$brush,$x,$y) } finally { $font.Dispose(); $brush.Dispose() }
}
function Tag($g,[string]$text,[float]$x,[float]$y,[string]$fill,[string]$fg,[float]$fontSize=18,[float]$padX=16,[float]$height=34){
  $font = New-Object Drawing.Font('Segoe UI',$fontSize,[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
  $size = $g.MeasureString($text,$font)
  $width = [Math]::Ceiling($size.Width + ($padX * 2))
  $fillBrush = New-Object Drawing.SolidBrush (C $fill 232)
  $strokePen = New-Object Drawing.Pen (C $fg 34),1
  $textBrush = New-Object Drawing.SolidBrush (C $fg 245)
  try {
    FillRR $g $fillBrush $x $y $width $height 16
    StrokeRR $g $strokePen $x $y $width $height 16
    $g.DrawString($text,$font,$textBrush,$x + $padX - 1,$y + 5)
  } finally {
    $font.Dispose(); $fillBrush.Dispose(); $strokePen.Dispose(); $textBrush.Dispose()
  }
  return $width
}
function TagRow($g,[string[]]$items,[float]$x,[float]$y,[string]$fill,[string]$fg){
  $cursor = $x
  foreach($item in $items){
    $w = Tag $g $item $cursor $y $fill $fg
    $cursor += $w + 12
  }
}
function TopicText($g,$p){
  switch($p.Slug){
    'advanced-formulas' { Tag $g 'Advanced Formulas' 588 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; Txt $g '=LET(total, SUM(...))' 740 360 20 '#0F766E' 'Consolas' ([Drawing.FontStyle]::Regular) 225; TagRow $g @('SUMPRODUCT','LET','LAMBDA') 684 506 '#FFFFFF' '#0F766E' }
    'charts-visualisations' { Tag $g 'Excel Charts' 620 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; TagRow $g @('Line','Bar','Pie') 754 506 '#FFFFFF' '#1D4ED8'; Txt $g 'Best chart for the story' 770 392 18 '#1D4ED8' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220 }
    'claude-ai-excel-formulas' { Tag $g 'AI Formula Prompt' 590 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; Txt $g 'Describe the spreadsheet...' 642 387 18 '#4338CA' 'Segoe UI' ([Drawing.FontStyle]::Regular) 220; TagRow $g @('Prompt','Formula','Excel') 700 506 '#FFFFFF' '#4338CA' }
    'claude-ai-excel-macros' { Tag $g 'AI VBA Macros' 612 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; Txt $g 'Sub FormatData()' 724 364 20 '#4F46E5' 'Consolas' ([Drawing.FontStyle]::Regular) 225; TagRow $g @('VBA','Macro','Automation') 676 506 '#FFFFFF' '#4F46E5' }
    'claude-debug-formulas' { Tag $g 'Debug Formulas' 606 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; Txt $g '#REF!  #VALUE!' 714 150 20 '#B91C1C' 'Consolas' ([Drawing.FontStyle]::Bold) 235; Txt $g 'IFERROR(...)' 786 366 20 '#0F766E' 'Consolas' ([Drawing.FontStyle]::Regular) 225; TagRow $g @('Error','Fix','Explain') 708 506 '#FFFFFF' '#0F766E' }
    'clean-messy-data' { Tag $g 'Clean Messy Data' 590 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; Txt $g 'Duplicates  ->  Clean Table' 720 210 18 '#047857' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220; TagRow $g @('Trim','Split','Remove') 706 506 '#FFFFFF' '#047857' }
    'conditional-formatting-tips' { Tag $g 'Conditional Formatting' 556 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; TagRow $g @('Heatmap','Data Bars','Icons') 658 506 '#FFFFFF' '#B45309'; Txt $g 'Highlight what matters' 754 398 18 '#B45309' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220 }
    'copilot-automate-tasks' { Tag $g 'Automate Tasks' 614 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; TagRow $g @('Sort','Filter','Format') 700 506 '#FFFFFF' '#2563EB'; Txt $g 'Prompt  ->  Action' 748 392 18 '#2563EB' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220 }
    'copilot-data-analysis' { Tag $g 'Data Analysis' 620 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; TagRow $g @('Insights','Charts','Trend') 690 506 '#FFFFFF' '#1D4ED8'; Txt $g 'Summarise the data' 734 392 18 '#1D4ED8' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220 }
    'data-validation' { Tag $g 'Data Validation' 604 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; Txt $g 'List' 720 149 18 '#0F766E' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220; Txt $g 'Date' 720 195 18 '#0F766E' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220; Txt $g 'Whole Number' 720 241 18 '#0F766E' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220; TagRow $g @('Dropdown','Rules','Valid') 702 506 '#FFFFFF' '#0F766E' }
    'dynamic-dashboards' { Tag $g 'Dynamic Dashboards' 582 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; TagRow $g @('KPI','Slicer','Chart') 732 506 '#FFFFFF' '#059669'; Txt $g 'Interactive view' 748 392 18 '#059669' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220 }
    'excel-vs-google-sheets' { Tag $g 'Excel vs Sheets' 600 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; Txt $g 'Excel' 686 386 20 '#166534' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220; Txt $g 'Sheets' 902 386 20 '#2563EB' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220; TagRow $g @('Offline','Cloud','Collab') 676 506 '#FFFFFF' '#166534' }
    'financial-modelling' { Tag $g 'Financial Modelling' 582 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; TagRow $g @('Revenue','Cash Flow','Scenario') 650 506 '#FFFFFF' '#0F172A'; Txt $g 'Forecast model' 790 392 18 '#0F172A' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220 }
    'getting-started-copilot-excel' { Tag $g 'Copilot in Excel' 596 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; Txt $g 'Ask a question about the sheet' 636 387 18 '#2563EB' 'Segoe UI' ([Drawing.FontStyle]::Regular) 220; TagRow $g @('Prompt','Analyse','Formula') 676 506 '#FFFFFF' '#2563EB' }
    'index-match-guide' { Tag $g 'INDEX + MATCH' 610 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; Txt $g 'INDEX(' 672 385 20 '#166534' 'Consolas' ([Drawing.FontStyle]::Regular) 225; Txt $g 'MATCH(' 908 385 20 '#F59E0B' 'Consolas' ([Drawing.FontStyle]::Regular) 225; TagRow $g @('Lookup','Row','Column') 706 506 '#FFFFFF' '#166534' }
    'keyboard-shortcuts' { Tag $g 'Keyboard Shortcuts' 586 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; Txt $g 'Ctrl' 699 163 18 '#1F2937' 'Segoe UI' ([Drawing.FontStyle]::Bold) 235; Txt $g 'Shift' 761 163 18 '#1F2937' 'Segoe UI' ([Drawing.FontStyle]::Bold) 235; Txt $g 'L' 848 163 18 '#1F2937' 'Segoe UI' ([Drawing.FontStyle]::Bold) 235; TagRow $g @('Navigate','Format','Filter') 672 506 '#FFFFFF' '#1F2937' }
    'mastering-pivot-tables' { Tag $g 'Pivot Tables' 622 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; Txt $g 'Rows' 808 392 18 '#0F766E' 'Segoe UI' ([Drawing.FontStyle]::Bold) 225; Txt $g 'Columns' 880 392 18 '#0F766E' 'Segoe UI' ([Drawing.FontStyle]::Bold) 225; Txt $g 'Values' 960 392 18 '#0F766E' 'Segoe UI' ([Drawing.FontStyle]::Bold) 225; TagRow $g @('Summarise','Group','Analyse') 664 506 '#FFFFFF' '#0F766E' }
    'power-pivot-guide' { Tag $g 'Power Pivot' 626 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; TagRow $g @('Tables','DAX','Relations') 698 506 '#FFFFFF' '#1E3A8A'; Txt $g 'Data model' 778 82 18 '#1E3A8A' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220 }
    'power-query-guide' { Tag $g 'Power Query' 620 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; Txt $g 'Extract  ->  Transform  ->  Load' 690 82 18 '#047857' 'Segoe UI' ([Drawing.FontStyle]::Bold) 220; TagRow $g @('Source','Transform','Load') 668 506 '#FFFFFF' '#047857' }
    'vlookup-vs-xlookup' { Tag $g 'VLOOKUP vs XLOOKUP' 558 42 '#FFFFFF' '#0F172A' 20 18 40 | Out-Null; Txt $g 'VLOOKUP' 680 385 18 '#166534' 'Consolas' ([Drawing.FontStyle]::Regular) 225; Txt $g 'XLOOKUP' 908 385 18 '#EA580C' 'Consolas' ([Drawing.FontStyle]::Regular) 225; TagRow $g @('Legacy','Modern','Lookup') 700 506 '#FFFFFF' '#166534' }
  }
}
function ExcelLogo($g,[float]$x,[float]$y,[float]$size){
  $shadow = New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(26,20,16,10))
  try { FillRR $g $shadow ($x+8) ($y+10) $size $size 36 } finally { $shadow.Dispose() }

  $bg = New-Object Drawing.Drawing2D.LinearGradientBrush([Drawing.PointF]::new($x,$y),[Drawing.PointF]::new($x+$size,$y+$size),(C '#34D399'),(C '#166534'))
  try { FillRR $g $bg $x $y $size $size 36 } finally { $bg.Dispose() }

  $sheetBrush = New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(246,255,255,255))
  $sheetPen = New-Object Drawing.Pen (C '#D1FAE5' 240),1.2
  try {
    FillRR $g $sheetBrush ($x+54) ($y+22) ($size-74) ($size-44) 22
    StrokeRR $g $sheetPen ($x+54) ($y+22) ($size-74) ($size-44) 22
  } finally { $sheetBrush.Dispose(); $sheetPen.Dispose() }

  $gridPen = New-Object Drawing.Pen (C '#BBF7D0' 170),1
  try {
    for($gx=$x+74;$gx-lt($x+$size-28);$gx+=22){ $g.DrawLine($gridPen,$gx,$y+34,$gx,$y+$size-34) }
    for($gy=$y+42;$gy-lt($y+$size-26);$gy+=22){ $g.DrawLine($gridPen,$x+66,$gy,$x+$size-24,$gy) }
  } finally { $gridPen.Dispose() }

  $frontBrush = New-Object Drawing.SolidBrush (C '#0F5132' 245)
  try { FillRR $g $frontBrush ($x+12) ($y+34) 78 ($size-68) 20 } finally { $frontBrush.Dispose() }

  $font = New-Object Drawing.Font('Segoe UI',($size*0.34),[Drawing.FontStyle]::Bold,[Drawing.GraphicsUnit]::Pixel)
  $brush = New-Object Drawing.SolidBrush ([Drawing.Color]::White)
  $sf = New-Object Drawing.StringFormat
  $sf.Alignment = 'Center'
  $sf.LineAlignment = 'Center'
  try { $g.DrawString('X',$font,$brush,[Drawing.RectangleF]::new($x+8,$y+30,86,$size-60),$sf) } finally { $font.Dispose(); $brush.Dispose(); $sf.Dispose() }
}

function PortraitFrame($g,$img,$p){
  Glow $g 244 260 160 '#34D399'
  Glow $g 206 460 110 $p.P
  $bg = New-Object Drawing.Drawing2D.LinearGradientBrush([Drawing.PointF]::new(34,70),[Drawing.PointF]::new(460,590),(C $p.P 240),(C '#0B3D2E'))
  try { FillRR $g $bg 28 70 470 520 54 } finally { $bg.Dispose() }

  $stripe = New-Object Drawing.SolidBrush (C '#FFFFFF' 28)
  try {
    FillRR $g $stripe 52 92 22 476 18
    FillRR $g $stripe 434 92 22 476 18
  } finally { $stripe.Dispose() }

  $cardShadow = New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(24,20,16,10))
  $cardBrush = New-Object Drawing.SolidBrush ([Drawing.Color]::FromArgb(248,255,255,255))
  $cardPen = New-Object Drawing.Pen (C '#E5E7EB' 180),1.3
  try {
    FillRR $g $cardShadow 58 104 404 456 40
    FillRR $g $cardBrush 46 92 426 476 42
    StrokeRR $g $cardPen 46 92 426 476 42
  } finally { $cardShadow.Dispose(); $cardBrush.Dispose(); $cardPen.Dispose() }

  $clip = PathRR 60 106 398 448 34
  try {
    $old = $g.Clip
    $g.SetClip($clip)
    $dst = [Drawing.RectangleF]::new(60,106,398,448)
    $src = [Drawing.RectangleF]::new(148,0,730,860)
    $g.DrawImage($img,$dst,$src,[Drawing.GraphicsUnit]::Pixel)
    $fade = [Drawing.RectangleF]::new(376,106,82,448)
    $fb = New-Object Drawing.Drawing2D.LinearGradientBrush([Drawing.PointF]::new($fade.Left,$fade.Top),[Drawing.PointF]::new($fade.Right,$fade.Top),[Drawing.Color]::FromArgb(0,255,255,255),[Drawing.Color]::FromArgb(175,255,255,255))
    try { $g.FillRectangle($fb,$fade) } finally { $fb.Dispose() }
    $g.Clip = $old
  } finally { $clip.Dispose() }
}
function SaveJ($img,[string]$path){$enc=[Drawing.Imaging.ImageCodecInfo]::GetImageEncoders()|Where-Object{$_.MimeType-eq 'image/jpeg'}|Select-Object -First 1;$ep=New-Object Drawing.Imaging.EncoderParameters 1;$ep.Param[0]=New-Object Drawing.Imaging.EncoderParameter([Drawing.Imaging.Encoder]::Quality,[long]92);try{$img.Save($path,$enc,$ep)}finally{$ep.Dispose()}}
function NewCover($p,$img,[string]$path){
  $bmp=New-Object Drawing.Bitmap 1200,630
  $g=[Drawing.Graphics]::FromImage($bmp)
  try{
    $g.SmoothingMode='AntiAlias'
    $g.InterpolationMode='HighQualityBicubic'
    $g.PixelOffsetMode='HighQuality'
    $g.CompositingQuality='HighQuality'

    $bg=New-Object Drawing.Drawing2D.LinearGradientBrush([Drawing.PointF]::new(0,0),[Drawing.PointF]::new(1200,630),(C '#F8FBF8'),(C '#E7F7EC'))
    try{$g.FillRectangle($bg,0,0,1200,630)}finally{$bg.Dispose()}

    $wash=New-Object Drawing.SolidBrush (C '#166534' 18)
    try{
      $g.FillPolygon($wash,[Drawing.PointF[]]@([Drawing.PointF]::new(0,630),[Drawing.PointF]::new(0,388),[Drawing.PointF]::new(312,630)))
      $g.FillEllipse($wash,780,-40,360,360)
      $g.FillEllipse($wash,780,360,320,320)
    }finally{$wash.Dispose()}

    Panel $g 540 54 620 522 40 '#FFFFFF' '#BBF7D0'
    $gridPen=New-Object Drawing.Pen (C '#166534' 18),1
    try{
      for($gx=570;$gx-lt1130;$gx+=28){$g.DrawLine($gridPen,$gx,84,$gx,548)}
      for($gy=86;$gy-lt552;$gy+=28){$g.DrawLine($gridPen,570,$gy,1130,$gy)}
    }finally{$gridPen.Dispose()}

    PortraitFrame $g $img $p
    ExcelLogo $g 962 18 170
    Motif $g $p
    TopicText $g $p
    SaveJ $bmp $path
  }finally{$g.Dispose();$bmp.Dispose()}
}
function SetImageMeta([string]$html,[string]$url,[string]$alt){$ea=[Net.WebUtility]::HtmlEncode($alt);$meta=@"
<meta property="og:image" content="$url">
  <meta property="og:image:secure_url" content="$url">
  <meta property="og:image:type" content="image/jpeg">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="$ea">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="$url">
  <meta name="twitter:image:alt" content="$ea">
"@;$html=[regex]::Replace($html,'\s*<meta property="og:image(?::secure_url|:type|:width|:height|:alt)?"[^>]*>','','Singleline');$html=[regex]::Replace($html,'\s*<meta name="twitter:(?:card|image|image:alt)"[^>]*>','','Singleline');$html -replace '<meta property="og:url" content="[^"]*">',('$0'+"`r`n  "+$meta)}
function SetJsonImage([string]$html,[string]$url,[string]$title){$m=[regex]::Match($html,'<script[^>]*application/ld\+json[^>]*>(.*?)</script>','Singleline');if(-not $m.Success){return $html};$obj=($m.Groups[1].Value.Trim()|ConvertFrom-Json);$obj|Add-Member -NotePropertyName image -NotePropertyValue ([ordered]@{'@type'='ImageObject';url=$url;width=1200;height=630;caption="$title by Sagnik Bhattacharya for Coding Liquids"}) -Force;$json=$obj|ConvertTo-Json -Compress -Depth 10;$html.Substring(0,$m.Groups[1].Index)+$json+$html.Substring($m.Groups[1].Index+$m.Groups[1].Length)}
function SetCoverHtml([string]$html,[string]$src,[string]$alt){$ea=[Net.WebUtility]::HtmlEncode($alt);$html=[regex]::Replace($html,'\s*<figure class="blog-cover">.*?</figure>','','Singleline');$fig=@"
<figure class="blog-cover">
          <img src="$src" alt="$ea" width="1200" height="630" loading="eager" fetchpriority="high" decoding="async">
          <figcaption class="sr-only">$ea</figcaption>
        </figure>
        <div class="blog-post-content">
"@;$html -replace '<div class="blog-post-content">',$fig}
$posts=@(
@{Slug='advanced-formulas';M='formula';P='#0F766E';S='#34D399';F='#ECFDF5';L='#99F6E4';Cue='spreadsheet formulas, dynamic arrays, and highlighted function blocks'},
@{Slug='charts-visualisations';M='charts';P='#1D4ED8';S='#F97316';F='#EFF6FF';L='#93C5FD';Cue='professional Excel charts, trend lines, and polished data visualisation elements'},
@{Slug='claude-ai-excel-formulas';M='ai';P='#4338CA';S='#14B8A6';F='#EEF2FF';L='#C7D2FE';Cue='AI prompt bubbles, formula flows, and spreadsheet visuals'},
@{Slug='claude-ai-excel-macros';M='macros';P='#4F46E5';S='#F59E0B';F='#EEF2FF';L='#C7D2FE';Cue='automation flows, macro blocks, and spreadsheet controls'},
@{Slug='claude-debug-formulas';M='debug';P='#0F766E';S='#EF4444';F='#ECFDF5';L='#A7F3D0';Cue='formula diagnostics, alert markers, and clean fix indicators'},
@{Slug='clean-messy-data';M='clean';P='#047857';S='#F59E0B';F='#ECFDF5';L='#6EE7B7';Cue='messy spreadsheet elements transforming into clean organised rows'},
@{Slug='conditional-formatting-tips';M='conditional';P='#B45309';S='#EC4899';F='#FFF7ED';L='#FED7AA';Cue='colour-scaled cells, status blocks, and highlighted spreadsheet ranges'},
@{Slug='copilot-automate-tasks';M='automation';P='#2563EB';S='#22C55E';F='#EFF6FF';L='#93C5FD';Cue='automation loops, workflow arrows, and spreadsheet task cards'},
@{Slug='copilot-data-analysis';M='dashboard';P='#1D4ED8';S='#06B6D4';F='#EFF6FF';L='#BFDBFE';Cue='insight cards, charts, and data-analysis panels'},
@{Slug='data-validation';M='validation';P='#0F766E';S='#22C55E';F='#F0FDF4';L='#86EFAC';Cue='dropdown fields, validation checks, and structured spreadsheet forms'},
@{Slug='dynamic-dashboards';M='dashboard';P='#059669';S='#0EA5E9';F='#ECFDF5';L='#A7F3D0';Cue='interactive dashboard cards, charts, and KPI panels'},
@{Slug='excel-vs-google-sheets';M='versus';P='#166534';S='#2563EB';F='#F0FDF4';L='#BBF7D0';Cue='side-by-side spreadsheet panels comparing two working styles'},
@{Slug='financial-modelling';M='finance';P='#0F172A';S='#10B981';F='#F8FAFC';L='#CBD5E1';Cue='forecast curves, financial tables, and scenario-analysis chart elements'},
@{Slug='getting-started-copilot-excel';M='ai';P='#2563EB';S='#14B8A6';F='#EFF6FF';L='#93C5FD';Cue='AI assistant cues, spreadsheet cards, and onboarding workspace visuals'},
@{Slug='index-match-guide';M='lookup';P='#166534';S='#F59E0B';F='#F0FDF4';L='#86EFAC';Cue='lookup tables, matching arrows, and spreadsheet reference cues'},
@{Slug='keyboard-shortcuts';M='keyboard';P='#1F2937';S='#10B981';F='#F9FAFB';L='#D1D5DB';Cue='keyboard keycaps, navigation arrows, and productivity cues'},
@{Slug='mastering-pivot-tables';M='pivot';P='#0F766E';S='#F59E0B';F='#ECFDF5';L='#99F6E4';Cue='pivot layouts, summary rings, and grouped table blocks'},
@{Slug='power-pivot-guide';M='data-model';P='#1E3A8A';S='#10B981';F='#EFF6FF';L='#BFDBFE';Cue='connected data tables, model relationships, and large-scale analysis cues'},
@{Slug='power-query-guide';M='pipeline';P='#047857';S='#06B6D4';F='#ECFDF5';L='#A7F3D0';Cue='data pipelines, transformation steps, and imported table blocks'},
@{Slug='vlookup-vs-xlookup';M='lookup';P='#166534';S='#EA580C';F='#F0FDF4';L='#BBF7D0';Cue='contrasting lookup tables, arrows, and side-by-side formula comparison cues'}
)
$root=Resolve-Path (Join-Path $PSScriptRoot '..')
$public=Join-Path $root 'public'
$blog=Join-Path $public 'blog'
$imgDir=Join-Path $blog 'images'
$utf8=[Text.UTF8Encoding]::new($false)
if(-not(Test-Path $imgDir)){New-Item -ItemType Directory -Path $imgDir|Out-Null}
$head=[Drawing.Image]::FromFile((Join-Path $public 'sagnik-bhattacharya.png'))
try{foreach($p in $posts){$htmlPath=Join-Path $blog ($p.Slug+'.html');$html=[IO.File]::ReadAllText($htmlPath);$title=[regex]::Match($html,'<title>(.*?) \| Sagnik Bhattacharya</title>','Singleline').Groups[1].Value.Trim();$file=$p.Slug+'-sagnik-bhattacharya-coding-liquids.jpg';$src='/blog/images/'+$file;$url='https://sagnikbhattacharya.com/blog/images/'+$file;$alt='Sagnik Bhattacharya from Coding Liquids in a premium blog hero image for '+$title+', with '+$p.Cue+'.';NewCover $p $head (Join-Path $imgDir $file);$html=SetImageMeta $html $url $alt;$html=SetJsonImage $html $url $title;$html=SetCoverHtml $html $src $alt;[IO.File]::WriteAllText($htmlPath,$html,$utf8)}}finally{$head.Dispose()}