from machine import Pin, PWM
import bluetooth
import time
from ble_simple_peripheral import BLESimplePeripheral

class MotorDC:
    def __init__(self, pin_pwm=4, pin_dir=27, freq=1000):
        # PWM (velocidade)
        self.pwm = PWM(Pin(pin_pwm))
        self.pwm.freq(freq)

        # Detecta tipo de duty
        try:
            self.max_duty = 1023
            self.pwm.duty(0)
            self.use_u16 = False
        except:
            self.max_duty = 65535
            self.use_u16 = True

        # Direção
        self.dir = Pin(pin_dir, Pin.OUT)

        print("Motor inicializado")

    def set_velocidade(self, valor):
        valor = max(0, min(self.max_duty, valor))

        if self.use_u16:
            self.pwm.duty_u16(valor)
        else:
            self.pwm.duty(valor)

        print("Velocidade:", valor)

    def frente(self):
        self.dir.value(1)
        print("Direção: Frente")

    def tras(self):
        self.dir.value(0)
        print("Direção: Trás")

    def parar(self):
        self.set_velocidade(0)
        print("Motor parado")


class MotorBLE:
    def __init__(self, motor):
        self.motor = motor

        # BLE
        self.ble = bluetooth.BLE()
        self.sp = BLESimplePeripheral(self.ble)

        print("Bluetooth ativo! Nome: ESP32_MOTOR")

    def processar_comando(self, comando):
        try:
            if comando.startswith("F"):
                valor = int(comando.split()[1])
                self.motor.frente()
                self.motor.set_velocidade(valor)
                self.sp.send("OK Frente {}\n".format(valor))

            elif comando.startswith("T"):
                valor = int(comando.split()[1])
                self.motor.tras()
                self.motor.set_velocidade(valor)
                self.sp.send("OK Tras {}\n".format(valor))

            elif comando == "S":
                self.motor.parar()
                self.sp.send("OK Parado\n")

            else:
                self.sp.send("Comando inválido\n")

        except Exception as e:
            self.sp.send("Erro\n")

    def loop(self):
        if self.sp.is_connected():
            if self.sp.any():
                comando = self.sp.read().decode().strip()
                print("Recebido:", comando)
                self.processar_comando(comando)