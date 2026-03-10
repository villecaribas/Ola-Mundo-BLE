from time import sleep, sleep_ms
import bluetooth
from machine import Pin
from micropython import const


# UUIDs para o serviço e característica (use UUIDs personalizados ou padrões)
_IRQ_CENTRAL_CONNECT = const(1)
_IRQ_CENTRAL_DISCONNECT = const(2)
_IRQ_GATT_WRITE = const(3)

# Flag para habilitar o BLE
_FLAG_READ = const(0x0002)
_FLAG_WRITE_NO_RESPONSE = const(0x0004)
_FLAG_WRITE = const(0x0008)
_FLAG_NOTIFY = const(0x0010)

# Defina o serviço e característica
_LED_UUID = bluetooth.UUID('12345678-1234-5678-1234-56789ABCDEF0')  # Serviço UUID personalizado
_LED_CHAR = (bluetooth.UUID('12345678-1234-5678-1234-56789ABCDEF1'),  # Característica UUID
             _FLAG_READ | _FLAG_WRITE | _FLAG_NOTIFY,)
_LED_SERVICE = (_LED_UUID, (_LED_CHAR,),)


class BLEServer:
    def __init__(self, name):
        self._ble = bluetooth.BLE()
        self._ble.active(True)
        self._ble.irq(self._irq)
        ((self._handle,),) = self._ble.gatts_register_services((_LED_SERVICE,))
        self._connections = set()
        self._advertise(name)

    def _irq(self, event, data):
        if event == _IRQ_CENTRAL_CONNECT:
            conn_handle, _, _ = data
            self._connections.add(conn_handle)
            print("\033[1;33mConexao OK!!\33[0m")
            
        elif event == _IRQ_CENTRAL_DISCONNECT:
            conn_handle, _, _ = data
            self._connections.remove(conn_handle)            
            print("\033[1;31mConexao FECHADA!!\33[0m")
            self._advertise(nomeDoLino)  # Reanuncia
            print("\033[1;34m"+nomeDoLino+"\033[0m está pronto para missão.")

        elif event == _IRQ_GATT_WRITE:
            conn_handle, value_handle = data
            value = self._ble.gatts_read(self._handle)
            cmd = value.decode('utf-8').strip()
            if cmd == "l11":
                print(f"(← {cmd}) LIGA LED1")
            elif cmd == "l10":
                print(f"(← {cmd}) DESLIGA LED1")
            else:
                print(f"(← {cmd}) não reconhecido)")

    def _advertise(self, name):
        name = bytes(name, 'utf-8')
        self._ble.gap_advertise(100, adv_data=b'\x02\x01\x06' + chr(len(name) + 1) + '\x09' + name)

# Inicia o servidor
ble_server = BLEServer(nomeDoLino)
