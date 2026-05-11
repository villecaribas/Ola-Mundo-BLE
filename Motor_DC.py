from machine import Pin, PWM

class MotorDC:
    def __init__(self, pin_pwm=4, pin_dir=27):
        self.pwm = PWM(Pin(pin_pwm))
        self.pwm.freq(1000)
        try:
            self.max_duty = 1023
            self.pwm.duty(0)
            self.use_u16 = False
        except:
            self.max_duty = 65535
            self.use_u16 = True
        self.dir = Pin(pin_dir, Pin.OUT)

    def set_vel(self, v):
        v = max(0, min(self.max_duty, v))
        self.pwm.duty_u16(v) if self.use_u16 else self.pwm.duty(v)

    def frente(self): self.dir.value(1)
    def tras(self): self.dir.value(0)
    def parar(self): self.set_vel(0)