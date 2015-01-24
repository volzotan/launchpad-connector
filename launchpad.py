from pygame import midi
from pygame import time

import sys
import logging as logger

# logger = logging.getLogger(__name__)

class Launchpad(object):    

    BUTTON_PRESSED = 0
    BUTTON_RELEASED = 127

    def __init__(self):
        midi.init()

        try:
            if (midi.get_count() < 1):
                logger.error("no MIDI device connected")
                sys.exit(-1)
        except SystemExit:
            raise
        except:
            logger.error("MIDI not available")
            sys.exit(-2)

        self.name = midi.get_device_info(0)[0]
        self.input_stream = midi.Input(0, 16)
        self.output_stream = midi.Output(1, 128)


    def encodeLedColor(self, green, red):
        """Calculate LED colors

        GREEN | GREEN | CLEAR | COPY | RED | RED
        5     | 4     | 3     | 2    | 1   | 0
        """

        tmp = green << 4
        tmp |= (3 << 2)  # 0b11 -> CLEAR set and COPY set, as advised in manual
        tmp |= red

        return tmp


    def decodeButton(self, number):
        return [number % 16, number / 16]


    def encodeButton(self, coords):
        return coords[1] * 16 + coords[0]


    def lightButton(self, coords, green, red):
        self.send([144, self.encodeButton(coords), self.encodeLedColor(green, red)])


    def reset(self):
        self.send([176, 0, 0])


    def turnOnAllLEDs(self, brightness):
        """Turns all LEDs on

        Brightness:
        125 - low
        126 - medium
        127 - full
        """

        if brightness not in range(0,3):
            raise ValueError("mapping value not in range 0 .. 2")

        self.send([176, 0, 125 + brightness])


    def selectMapping(self, mapping):
        """Switch between button mappings

        1 - default X-Y layout
        2 - drum rack layout
        """

        if mapping not in range(1,3):
            raise ValueError("mapping value not in range 1 .. 2")

        self.send([176, 0, mapping])


    def doubleBuffer(self, copy, flash, update, display):
        """Control the double buffer

        0 | 1 | COPY | FLASH | UPDATE | 1 | DISPLAY
        6 | 5 | 4    | 3     | 2      | 1 | 0
        """

        msg = 01 << 5
        msg |= 0 << 1

        msg |= copy << 4
        msg |= flash << 3
        msg |= update << 2
        msg |= display

        self.send([176, 0, msg])


    def receive(self):
        if (self.input_stream.poll()):
            inp = self.input_stream.read(1)

            # [[[144, 98, 127, 0], 19491]]
            return [inp[0][0][0], self.decodeButton(inp[0][0][1]), inp[0][0][2]]

        return None


    def send(self, msg):
        self.output_stream.write_short(msg[0], msg[1], msg[2])


    def close(self):
        self.input_stream.close()
        self.output_stream.abort()
        midi.close()
