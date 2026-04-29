from machine import Pin, PWM
import time

musicas = {
    "megalovania": "Megalovania:d=4,o=5,b=120:\
d,d,d6,p,a,8p,g#,p,g,p,f,p,d,f,g,\
c,c,d6,p,a,8p,g#,p,g,p,f,p,d,f,g,\
b4,b4,d6,p,a,8p,g#,p,g,p,f,p,d,f,g,\
a#4,a#4,d6,p,a,8p,g#,p,g,p,f,p,d,f,g",
    "starwars": "StarWars:d=4,o=5,b=45:\
32p,32f#,32f#,32f#,8b.,8f#6.,32e6,32d#6,32c#6,8b6.,16f#6.,\
32e6,32d#6,32c#6,8b6.,16f#6.,32e6,32d#6,32e6,8c#6.,\
32f#,32f#,32f#,8b.,8f#6.,32e6,32d#6,32c#6,8b6.,16f#6.,\
32e6,32d#6,32c#6,8b6.,16f#6.,32e6,32d#6,32e6,8c#6",
    "impossiblemission": "ImpossibleMission:d=16,o=6,b=95:\
32d,32d#,32d,32d#,32d,32d#,32d,32d#,32d,32d,32d#,32e,32f,32f#,32g,\
g,8p,g,8p,a#,p,c7,p,g,8p,g,8p,f,p,f#,p,g,8p,g,8p,a#,p,c7,p,g,8p,g,8p,\
f,p,f#,p,a#,g,2d,32p,a#,g,2c#,32p,a#,g,2c,a#5,8c,2p,32p,a#5,g5,2f#,\
32p,a#5,g5,2f,32p,a#5,g5,2e,d#,8d"
}
class BuzzerPTK:
    def __init__(self, pin):
        self.buzzer = PWM(Pin(pin))
        self.buzzer.duty_u16(0)
        self._parar = False

        # Frequências base (oitava 4)
        self.NOTES = {
            "c": 262, "d": 294, "e": 330, "f": 349,
            "g": 392, "a": 440, "b": 494,
            "c#": 277, "d#": 311, "f#": 370,
            "g#": 415, "a#": 466
        }

    def stop(self):
        self._parar = True
        self.buzzer.duty_u16(0)

    def _freq_com_oitava(self, freq, octave):
        return int(freq * (2 ** (octave - 4)))

    def _play_tone(self, freq, duration):
        if self._parar:
            return

        if freq == 0:
            time.sleep(duration)
            return

        self.buzzer.freq(freq)
        self.buzzer.duty_u16(30000)
        time.sleep(duration)
        self.buzzer.duty_u16(0)

    def toque(self, song):
        self._parar = False  # reset

        name, settings, notes = song.split(":")
        settings = settings.split(",")

        default_duration = 4
        default_octave = 5
        bpm = 120

        for s in settings:
            if s.startswith("d="):
                default_duration = int(s[2:])
            elif s.startswith("o="):
                default_octave = int(s[2:])
            elif s.startswith("b="):
                bpm = int(s[2:])

        whole_note = (60 / bpm) * 4
        notes = notes.replace("\n", "").split(",")

        for note in notes:
            if self._parar:
                break

            note = note.strip()
            if not note:
                continue

            duration = default_duration
            octave = default_octave
            dotted = False
            freq = 0

            i = 0

            # duração (ex: 8d, 16c)
            num = ""
            while i < len(note) and note[i].isdigit():
                num += note[i]
                i += 1
            if num:
                duration = int(num)

            # pausa
            if i < len(note) and note[i] == 'p':
                freq = 0
                i += 1
            else:
                # nota
                if i < len(note):
                    if i+1 < len(note) and note[i+1] == '#':
                        key = note[i:i+2]
                        i += 2
                    else:
                        key = note[i]
                        i += 1

                    base_freq = self.NOTES.get(key, 0)
                    freq = self._freq_com_oitava(base_freq, octave)

            # oitava explícita (ex: d6)
            if i < len(note) and note[i].isdigit():
                octave = int(note[i])
                freq = self._freq_com_oitava(self.NOTES.get(key, 0), octave)
                i += 1

            # ponto (d.)
            if i < len(note) and note[i] == '.':
                dotted = True

            note_duration = whole_note / duration
            if dotted:
                note_duration *= 1.5

            self._play_tone(freq, note_duration)