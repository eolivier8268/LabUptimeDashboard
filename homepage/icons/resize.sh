# to .ico file
convert -resize x16 -gravity center -crop 16x16+0+0 ./input -flatten -colors 256 -background transparent ./output    
# to other image for homepage logos
convert input.jpg -resize "267x267^" -gravity center -crop 267x267+0+0 output.jpg
