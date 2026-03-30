from machine import Pin, PWM
import time

class ServoPTK:
    def __init__(
        self,
        pin,
        freq=50,
        min_us=500,
        max_us=2500,
        max_angle=180
    ):
        """
        Classe para controle de servo motor em MicroPython.

        pin       -> pino GPIO
        freq      -> frequência PWM do servo (geralmente 50 Hz)
        min_us    -> pulso mínimo em microssegundos
        max_us    -> pulso máximo em microssegundos
        max_angle -> ângulo máximo do servo
        """
        self.freq = freq
        self.min_us = min_us
        self.max_us = max_us
        self.max_angle = max_angle

        self.pwm = PWM(Pin(pin), freq=self.freq)

        # Período do PWM em microssegundos
        self.period_us = int(1_000_000 / self.freq)

    def _clamp(self, value, vmin, vmax):
        if value < vmin:
            return vmin
        if value > vmax:
            return vmax
        return value

    def _write_pulse_us(self, pulse_us):
        pulse_us = self._clamp(pulse_us, self.min_us, self.max_us)

        # 1) Porta com duty_u16()
        if hasattr(self.pwm, "duty_u16"):
            duty = int((pulse_us / self.period_us) * 65535)
            self.pwm.duty_u16(duty)

        # 2) Porta com duty_ns()
        elif hasattr(self.pwm, "duty_ns"):
            self.pwm.duty_ns(pulse_us * 1000)

        # 3) Porta com duty() (ex.: algumas versões ESP8266/ESP32)
        elif hasattr(self.pwm, "duty"):
            # duty de 0 a 1023
            duty = int((pulse_us / self.period_us) * 1023)
            self.pwm.duty(duty)

        else:
            raise NotImplementedError("Método PWM não suportado nesta porta do MicroPython.")

    def write_angle(self, angle):
        """
        Move o servo para um ângulo entre 0 e max_angle.
        """
        angle = self._clamp(angle, 0, self.max_angle)
        pulse_us = self.min_us + (self.max_us - self.min_us) * (angle / self.max_angle)
        self._write_pulse_us(int(pulse_us))

    def write_us(self, pulse_us):
        """
        Move o servo usando largura de pulso em microssegundos.
        """
        self._write_pulse_us(int(pulse_us))

    def center(self):
        """
        Centraliza o servo.
        """
        self.write_angle(self.max_angle / 2)

    def release(self):
        """
        Desliga o sinal PWM.
        """
        self.pwm.deinit()