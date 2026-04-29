from machine import Pin, PWM
import time

class EurekaServo:
    def __init__(self, pin=26, min_us=500, max_us=2500, freq=50):
        self.pin = pin
        self.min_us = min_us      # pulso para 0 graus
        self.max_us = max_us      # pulso para 180 graus
        self.freq = freq

        self.pwm = PWM(Pin(self.pin))
        self.pwm.freq(self.freq)

    def set_angle(self, angle):
        # Garante que o ângulo fique entre 0 e 180
        angle = max(0, min(180, angle))

        # Converte ângulo para pulso em microssegundos
        pulse_us = self.min_us + (angle / 180) * (self.max_us - self.min_us)

        # MicroPython usa nanossegundos no duty_ns
        self.pwm.duty_ns(int(pulse_us * 1000))

        return pulse_us  # útil para calibração

    def sweep(self, delay=0.5):
        for angle in range(0, 181, 10):
            self.set_angle(angle)
            time.sleep(delay)

        for angle in range(180, -1, -10):
            self.set_angle(angle)
            time.sleep(delay)

    def center(self):
        self.set_angle(90)

    def deinit(self):
        self.pwm.deinit()
