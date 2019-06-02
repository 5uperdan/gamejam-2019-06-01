from array import array
from time import sleep, time

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
    volume = 0.0
    tune_schedule = []
    notes = {'c0n' : 261.63, 'c0+' : 277.00,
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
    
    def __init__(self, volume=0.8):
        self.notes = Tune.notes
        self.sequence_a = []
        self.sequence_b = []
        self.lengths = [1.0]
        self.pauses = [0.1]
        self.speed = 1.0
        self.volume = Tune.volume
        self.volume = 0.8
        self.melody = 'a'
    
    def blocking_play(self):
        while len(self.lengths) < len(self.sequence):
            self.lengths.append(self.lengths[-1])
        while len(self.pauses) < len(self.sequence):
            self.pauses.append(self.pauses[-1])
        for i, n in enumerate(self.sequence):
            freq = self.notes.get(n)
            Note(freq, 0.5).play(int((freq*self.lengths[i])/self.speed))
            sleep(self.pauses[i]/self.speed)
    
    def play(self, new_melody=None):
        now = time()
        if new_melody is not None:
            if new_melody == 'a' or new_melody == 'b':
                self.melody = new_melody
        offset = 0
        if self.melody == 'a': seq = self.sequence_a 
        if self.melody == 'b': seq = self.sequence_b 
        for i, n in enumerate(seq):
            freq = self.notes.get(n)
            dur = self.lengths[i]
            spd = self.speed
            element = (now+offset, freq, dur, spd)
            Tune.tune_schedule.append(element)
            offset += self.pauses[i]/spd
    
    @classmethod
    def tick(self):
        """ this is called every game tick and sound.py decides if a new 
            beep needs to be pushed to the sound card """
        play_now = []
        if len(Tune.tune_schedule) > 0:
            now = time()
            for i, note in enumerate(Tune.tune_schedule):
                if note[0] <= now:
                    play_now.append(note)
            if len(play_now) > 0:
                for note_to_push in play_now:
                    _, freq, dur, spd = note_to_push
                    Note(freq, 0.5).play(int((freq*dur)/spd))
            for to_remove in play_now:
                Tune.tune_schedule.remove(to_remove)
            
    
if __name__ == "__main__":

    pre_init(44100, -16, 1, 1024)
    pygame.init()
    tune = Tune()
    tune.sequence_a = ['c1n','d1n','c1n','e1n','e1n','d1n','c1n',
                       'c1n','d1n','c1n','e1n','e1n','d1n','c1n',
                       'f1n','g1n','f1n','a2n','a2n','g1n','f1n',
                       'c1n','d1n','c1n','e1n','e1n','d1n','c1n',
                       'g1n','a2n','g1n','b2n','b2n','a2n','g1n',
                       'a2n','a2n','g1n','f1n','f1n','e1n','d1n','c1n']
    tune.sequence_b = ['c1n','d1n','c1n','d1+','d1+','d1n','c1n',
                       'c1n','d1n','c1n','d1+','d1+','d1n','c1n',
                       'f1n','g1n','f1n','g1+','g1+','g1n','f1n',
                       'c1n','d1n','c1n','d1+','d1+','d1n','c1n',
                       'g1n','a2n','g1n','a2+','a2+','a2n','g1n',
                       'g1+','g1+','g1n','f1n','f1n','d1+','d1n','c1n']
    tune.lengths = [0.6, 0.6, 0.6, 0.3, 1.2, 0.6, 5.4,
                    0.6, 0.6, 0.6, 0.3, 1.2, 0.6, 5.4,
                    0.6, 0.6, 0.6, 0.3, 1.2, 0.6, 5.4,
                    0.6, 0.6, 0.6, 0.3, 1.2, 0.6, 5.4,
                    0.6, 0.6, 0.6, 0.3, 1.2, 0.6, 5.4,
                    0.6, 0.6, 0.6, 0.3, 1.2, 0.6, 2.5, 2.5]
    tune.pauses = [0.8, 0.8, 0.8, 1.6, 1.6, 0.8, 6.0,
                   0.8, 0.8, 0.8, 1.6, 1.6, 0.8, 6.0,
                   0.8, 0.8, 0.8, 1.6, 1.6, 0.8, 6.0,
                   0.8, 0.8, 0.8, 1.6, 1.6, 0.8, 6.0,
                   0.8, 0.8, 0.8, 1.6, 1.6, 0.8, 6.0,
                   0.8, 0.8, 0.8, 1.6, 1.6, 0.8, 3.0, 3.0]
    tune.speed = 6.0
    
    beep = Tune()
    beep.sequence_a = ['c0n']
    beep.lengths = [1.0]
    beep.pauses = [0.0]
    beep.speed = 1.0
    
#    tune.blocking_play()
    
    tune.play()
    for loop in range(740):
        sleep(1/30)
        #if loop == 75:
        #    beep.play()
        if loop == 370:
            tune.play('b')
        Tune.tick()

