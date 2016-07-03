# References:
# http://www.itstactical.com/intellicom/tradecraft/how-to-become-a-morse-code-expert/
# http://en.wikipedia.org/wiki/Morse_code

from array import array
from time import sleep
import pygame
from pygame.mixer import Sound, get_init, pre_init

letterToMorse = {"a": ".-",
                 "b": "-...",
                 "c": "-.-.",
                 "d": "-..",
                 "e": ".",
                 "f": "..-.",
                 "g": "--.",
                 "h": "....",
                 "i": "..",
                 "j": ".---",
                 "k": "-.-",
                 "l": ".-..",
                 "m": "--",
                 "n": "-.",
                 "o": "---",
                 "p": ".--.",
                 "q": "--.-",
                 "r": ".-.",
                 "s": "...",
                 "t": "-",
                 "u": "..-",
                 "v": "...-",
                 "w": ".--",
                 "x": "-..-",
                 "y": "-.--",
                 "z": "--..",
                 "1": ".----",
                 "2": "..---",
                 "3": "...--",
                 "4": "....-",
                 "5": ".....",
                 "6": "-....",
                 "7": "--...",
                 "8": "---..",
                 "9": "----.",
                 "0": "-----",
                 " ": "/",
                 ".": ".-.-.-",
                 ",": "--..--",
                 "?": "..--..",
                 "'": ".----.",
                 "!": "-.-.--",
                 "/": "-..-.",
                 "(": "-.--.",
                 ")": "-.--.-",
                 "&": ".-...",
                 ":": "---...",
                 ";": "-.-.-.",
                 "=": "-...-",
                 "+": ".-.-.",
                 "-": "-....-",
                 "_": "..--.-",
                 '"': ".-..-.",
                 "$": "...-..-",
                 "@": ".--.-."}


morseToLetter = {v: k for k, v in letterToMorse.items()}


def string_to_morse(s):
    """ input: string of text
    output: translated morse code
    example: "hello" -> ".... . .-.. .-.. ---" """

    l = s.lower()
    for c in l:
        if c not in letterToMorse.keys():
            print "BAD CHARACTER!!!!!!!!!!!!!:", c
    try:
        return " ".join(map(letterToMorse.__getitem__, l))
    except KeyError:
        keys = "".join(sorted([str(x) for x in letterToMorse.keys()]))
        raise KeyError("Unknown letter in input string. " +
                       "Acceptable letters are: " + keys +
                       ". Your input was: " + l)


def morse_to_string(s):
    """ input: string of morse code
    output: translated text string
    example: ".... . .-.. .-.. ---" -> "hello" """

    try:
        gi = morseToLetter.__getitem__
        return " ".join("".join(map(gi, c.split(" "))) for c in s.split(" / "))
    except KeyError:
        keys = " ".join(sorted([str(x) for x in morseToLetter.keys()]))
        raise KeyError("Unknown morse in input string. " +
                       "Acceptable letters are: " + keys +
                       ". Your input was: " + s)


class Note(Sound):

    def __init__(self, frequency, volume=.1):
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in xrange(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples


def play_morse(s):
    pauseTime = 0.05

    def play(freq=400, length=50):
        n = Note(freq)
        n.play(-1)
        sleep(length / 1000.0)
        n.stop()
        sleep(pauseTime)

    def dot():
        play()

    def dash():
        play(length=100)

    def space():
        sleep(pauseTime * 3)

    def word():
        sleep(pauseTime * 7)

    mapping = {".": dot,
               "-": dash,
               " ": space,
               "/": word}
    map(lambda x: mapping[x](), "/".join(s.split(" / ")))

if __name__ == "__main__":
    pre_init(44100, -16, 1, 1024)
    pygame.init()

    import sys
    text = " ".join(sys.argv[1:])
    # text = "hello"
    morse = string_to_morse(text)
    print morse
    play_morse(morse)
