"""CircuitPython Synthesia KeyLights"""
import time
import board
import neopixel
import adafruit_midi
import usb_midi

from adafruit_midi.note_on import NoteOn
from adafruit_midi.note_off import NoteOff
from adafruit_midi.control_change import ControlChange

MIDI = adafruit_midi.MIDI(midi_in=usb_midi.ports[0], midi_out=usb_midi.ports[1])

LED_PIN = board.D5
LED_COUNT = 144

KeyStrip = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness=0.3, auto_write=False)

LEFTMOST_KEY_NOTE = 21
BLUE = 0x0000FF
GREEN = 0x00FF00
RED = 0xFF0000
TEAL = 0x00FFFF

FingerHandColor = [
    GREEN,
    BLUE,
    BLUE,
    BLUE,
    BLUE,
    BLUE,
    GREEN,
    GREEN,
    GREEN,
    GREEN,
    GREEN,
    BLUE,
    GREEN,
]

def mapPitch2LEDIndex(note):
    if note < LEFTMOST_KEY_NOTE:
        return 0
    ledindex = note - LEFTMOST_KEY_NOTE
    if ledindex > (LED_COUNT - 1):
        return LED_COUNT - 1
    return ledindex

KeyStrip.fill(0)
KeyStrip.show()

while True:
    msg = MIDI.receive()
    if msg is not None:
        if isinstance(msg, NoteOn):
            print(time.monotonic(), 'Note-On', msg.channel, msg.note, msg.velocity)
            led_index = mapPitch2LEDIndex(msg.note)
            if msg.velocity > 0:
                if msg.channel < len(FingerHandColor):
                    color = FingerHandColor[msg.channel]
                    print(time.monotonic(), 'LED-on[', led_index, '] =', hex(color))
                    KeyStrip[led_index] = color
                    KeyStrip.show()
            else:
                KeyStrip[led_index] = 0
                KeyStrip.show()
        elif isinstance(msg, NoteOff):
            print(time.monotonic(), 'Note-Off', msg.channel, msg.note, msg._velocity)
            KeyStrip[mapPitch2LEDIndex(msg.note)] = 0
            KeyStrip.show()
        elif isinstance(msg, ControlChange):
            print(time.monotonic(), 'Control-Change', msg.channel, msg.control, msg.value)
            if msg.control == 16:
                KeyStrip.fill(0)
                KeyStrip.show()
