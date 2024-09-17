import math
from machine import Pin, Timer
from lcd import LCD_1inch3
import random
from futhark import Futhark
from futhark_render import FutharkRender
import png

futhark_bag = []
clean_futhark_bag = []
drawn_runes = []
selected_rune = 0
rune = None

draw_mode = 0 # 0 = Rune detail, 1 = Rune picker

# Colour Mixing Routine
def colour(R,G,B): # Compact method!
  mix1 = ((R&0xF8)*256) + ((G&0xFC)*8) + ((B&0xF8)>>3)
  return (mix1 & 0xFF) *256 + int((mix1 & 0xFF00) /256) # low nibble first

c = colour(255,255,255)               # Calculate 2-byte colour code
invc = colour(0,0,0)

green = colour(5,255,5)


def random_shuffle(seq):
    l = len(seq)
    for i in range(l):
        j = random.randrange(l)
        seq[i], seq[j] = seq[j], seq[i]

def chunk_rune_meaning(meaning, offset):
    '''A generator to divide a sequence into chunks of n units.'''
    while meaning:
        yield meaning[:offset]
        meaning = meaning[offset:]

def draw_current_rune():
    global rune
    global lcd
    global c
    global invc
    
    FutharkRender.draw(rune['name'].lower()+'.bin', lcd, c, invc)
    return    

def setup_futhark_bag():
    futhark_bag = [
        Futhark.FEHU,
        Futhark.URUZ,
        Futhark.THURISAZ,
        Futhark.ANSUZ,
        Futhark.RAIDHO,
        Futhark.KENNAZ,
        Futhark.GEBO,
        Futhark.WUNJO,
        Futhark.HAGALAZ,
        Futhark.NAUTHIZ,
        Futhark.ISA,
        Futhark.JERA,
        Futhark.EIHWAZ,
        Futhark.PERTHRO,
        Futhark.ALGIZ,
        Futhark.SOWILO,
        Futhark.TIWAZ,
        Futhark.BERKANA,
        Futhark.EHWAZ,
        Futhark.MANNAZ,
        Futhark.LAGUZ,
        Futhark.INGWAZ,
        Futhark.OTHALA, 
        Futhark.DAGAZ,
    ]
    return futhark_bag

def reset_futhark_bag():
    global futhark_bag
    futhark_bag = setup_futhark_bag()
    do_runes()
    return

def do_runes():

    global futhark_bag
    global lcd
    global c
    global invc
    
    if(len(futhark_bag) == 0):
        lcd.fill_rect(0, 200, 240, 240, invc)
        lcd.show()
        lcd.text("Rune bag empty!",20,200,c) # simple text (s,x,y,c)
        lcd.show()
        return
    else:        
        random_shuffle(futhark_bag)
        global rune
        rune = futhark_bag.pop()
        drawn_runes.append(rune)
        show_current_rune()
        return


def increment_selected_rune():
    global selected_rune
    if selected_rune < 24:    
        selected_rune += 1
    show_rune_list()
    return


def decrement_selected_rune():
    global selected_rune
    if selected_rune > 0:
        selected_rune -= 1
    show_rune_list()
    return

def select_rune_explain():
    global selected_rune
    global clean_futhark_bag
    global rune
    
    rune = clean_futhark_bag[selected_rune]
    
    show_current_rune(show_remaining=False)

def set_arrow_irqs():
    global up
    global down
    global ctrl
    
    down.irq(lambda p: increment_selected_rune(), trigger=Pin.IRQ_RISING)
    up.irq(lambda p: decrement_selected_rune(), trigger=Pin.IRQ_RISING)
    ctrl.irq(lambda p: select_rune_explain(), trigger=Pin.IRQ_RISING) 
    return

def clear_arrow_irqs():
    global up
    global down
    global ctrl
    
    down.irq(lambda p: None, trigger=Pin.IRQ_RISING)
    up.irq(lambda p: None, trigger=Pin.IRQ_RISING)
    ctrl.irq(lambda p: None, trigger=Pin.IRQ_RISING) 
    return

def toggle_rune_list():
    global draw_mode
    
    if(draw_mode == 0):
        draw_mode = 1
        set_arrow_irqs()
        show_rune_list()
    else:
        draw_mode = 0
        clear_arrow_irqs()
        show_current_rune()
    
    return

def show_current_rune(show_remaining = True):
    global rune
    global lcd
    global c
    global invc
    lcd.fill(invc)
    lcd.text("Rune: " + rune['name'],20,20,c) # simple text (s,x,y,c)
    lcd.text("Meaning: ", 20, 40, c) # simple text (s,x,y,c)
    offset = 0
    meanings = chunk_rune_meaning(rune['meaning'], 25)
    for meaning in meanings:
        lcd.text(meaning, 20, 60+offset, c) # simple text (s,x,y,c)
        offset = offset + 20
    
    if show_remaining:
        lcd.text("Runes remaining in bag: " + str(len(futhark_bag)), 20, 200, c)
    lcd.show()                            # Draw on the screen
    return

def show_rune_list():
    global lcd
    global selected_rune
    global clean_futhark_bag
    global c
    global green
    global invc
    
    lcd.fill(invc)
    offset = 0
    rune_chunk = math.floor(selected_rune / 10)
    for i, rune in enumerate(clean_futhark_bag):
        if rune_chunk * 10 <= i <= (rune_chunk + 1) * 10:
            if i == selected_rune:
                lcd.text(rune['name'], 20, 20+offset, green) # simple text (s,x,y,c)
            else:
                lcd.text(rune['name'], 20, 20+offset, c) # simple text (s,x,y,c)
            offset = offset + 20
        lcd.show()                            # Draw on the screen
    return

def show_drawn_runes(drawn_runes, lcd):
    return

keyA = Pin(15,Pin.IN,Pin.PULL_UP)
keyB = Pin(17,Pin.IN,Pin.PULL_UP)
keyX = Pin(19 ,Pin.IN,Pin.PULL_UP)
keyY= Pin(21 ,Pin.IN,Pin.PULL_UP)

up = Pin(2,Pin.IN,Pin.PULL_UP)
down = Pin(18,Pin.IN,Pin.PULL_UP)
left = Pin(16,Pin.IN,Pin.PULL_UP)
right = Pin(20,Pin.IN,Pin.PULL_UP)
ctrl = Pin(3,Pin.IN,Pin.PULL_UP)

lcd = LCD_1inch3() # Start screen 

futhark_bag = setup_futhark_bag()
clean_futhark_bag = setup_futhark_bag()
draw_mode = 0
do_runes()
keyA.irq(lambda p:do_runes(), trigger=Pin.IRQ_RISING)
keyB.irq(lambda p:toggle_rune_list(), trigger=Pin.IRQ_RISING)
keyX.irq(lambda p:draw_current_rune(), trigger=Pin.IRQ_RISING)
keyY.irq(lambda p:reset_futhark_bag(), trigger=Pin.IRQ_RISING)