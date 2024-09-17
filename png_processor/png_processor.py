from PIL import Image
import sys

rune = sys.argv[1]
print(rune)

input = rune+'.png'
image = Image.open(input)
pixels = list(image.getdata())
output = open(rune+'.bin', mode='wb')

x = 0
y = 0

for alpha, pixel in pixels:

    if(pixel != 0):
        print("Found pixel at " + str(x) + ", " + str(y))
        output.write(x.to_bytes(1, 'big'))
        output.write(y.to_bytes(1, 'big'))
    if x == 240:
        x = 0
        y += 1
    x += 1
