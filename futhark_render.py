import random
# Colour Mixing Routine
def colour(R,G,B): # Compact method!
  mix1 = ((R&0xF8)*256) + ((G&0xFC)*8) + ((B&0xF8)>>3)
  return (mix1 & 0xFF) *256 + int((mix1 & 0xFF00) /256) # low nibble first

class FutharkRender:
    
    def draw(filename, lcd, c, invc):
        lcd.fill(invc)
        lcd.show()
        bin_file = open(filename, "rb")
        xByte = bin_file.read(1)
        yByte = bin_file.read(1)
        
        while xByte:            
            xVal = int.from_bytes(xByte, "big")
            yVal = int.from_bytes(yByte, "big")
            lcd.pixel(xVal, yVal, c)

            # Do stuff with byte.
            xByte = bin_file.read(1)
            yByte = bin_file.read(1)

        lcd.show()
        return
