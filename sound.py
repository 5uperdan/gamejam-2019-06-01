# Generate a 440 Hz square waveform in Pygame by building an array of samples and play
# it for 5 seconds.  Change the hard-coded 440 to another value to generate a different
# pitch.
#
# Run with the following command:
#   python pygame-play-tone.py

from array import array
from time import sleep

import pygame
from pygame.mixer import Sound, get_init, pre_init

class Note(Sound):

    def __init__(self, frequency, volume=.1):
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(get_init()[0] / self.frequency))
        samples = array("h", [0] * period)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in range(period):
            if time < period / 2:
                samples[time] = amplitude
            else:
                samples[time] = -amplitude
        return samples

class Tune():
    
    def __init__(self):
        self.notes = {'c0n' : 261.63, 'c0+' : 277.00,
                      'd0n' : 293.66, 'd0+' : 311.00,
                      'e0n' : 329.63,
                      'f0n' : 349.23, 'f0+' : 370.00,
                      'g0n' : 392.00, 'g0+' : 415.00,
                      'a1n' : 440.00, 'a1+' : 466.00,
                      'b1n' : 493.88,
                      'c1n' : 523.25, 'c1+' : 554.00,
                      'd1n' : 587.33, 'd1+' : 622.00,
                      'e1n' : 659.26,
                      'f1n' : 698.46, 'f1+' : 740.00,
                      'g1n' : 783.99, 'g1+' : 831.00,
                      'a2n' : 880.00, 'a2+' : 932.00,
                      'b2n' : 987.77,
                      'c2n' : 1046.50, 'c2+' : 1109.00}
        self.sequence = []
        self.lengths = [1.0]
        self.pauses = [0.1]
        self.speed = 1.0
    
    def play(self):
        while len(self.lengths) < len(self.sequence):
            self.lengths.append(self.lengths[-1])
        while len(self.pauses) < len(self.sequence):
            self.pauses.append(self.pauses[-1])
        for i, n in enumerate(self.sequence):
            freq = self.notes.get(n)
            Note(freq, 0.5).play(int((freq*self.lengths[i])/self.speed))
            sleep(self.pauses[i]/self.speed)

if __name__ == "__main__":
    pre_init(44100, -16, 1, 1024)
    pygame.init()
    tune = Tune()
    tune.sequence = ['c1n','e1n','g1n','g1n','e1n','c1n','e1n','g1n','c2n','c2n','g1n','e1n']
    tune.lengths = [0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5]
    tune.pauses = [0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6]
    tune.speed = 3.0
    tune.play()
    