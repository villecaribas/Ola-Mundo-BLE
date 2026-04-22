from machine import Pin, PWM
import time

class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)

    def set_angle(self, angle):
        # Limite do ângulo
        angle = max(0, min(180, angle))

        # Conversão (ajuste fino pode ser necessário)
        duty = int(40 + (angle / 180) * 115)
        self.pwm.duty(duty)

    def sweep(self, delay=0.5):
        for angle in range(0, 181, 10):
            self.set_angle(angle)
            time.sleep(delay)

        for angle in range(180, -1, -10):
            self.set_angle(angle)
            time.sleep(delay)


# ===== Programa principal =====
servo = Servo(pin=15)

while True:
    servo.sweep(0.3)