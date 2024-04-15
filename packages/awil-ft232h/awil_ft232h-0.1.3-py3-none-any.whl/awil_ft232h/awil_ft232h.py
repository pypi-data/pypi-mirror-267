from pyftdi.spi import SpiController, SpiPort
from typing import List


class AwilFt232h:
    _ADBUS_COUNT = 5
    _ACBUS_COUNT = 10
    _GPIO_BASE_MASK = 0x0100  # GPIOの開始位置（8bit目から）

    def __init__(self) -> None:
        self._spi: SpiController = None
        self._is_open = False

    def __del__(self) -> None:
        if self._spi is not None:
            self.close()

    def open(self, serial_number: str) -> None:
        self._spi = SpiController()
        self._spi.configure(f'ftdi://ftdi:232h:{serial_number}/1')
        self._is_open = True
        self._spi.set_gpio_direction(0xFF00, 0xFF00)
        self._spi.write_gpio(0xFF00)

    def close(self) -> None:
        self._spi.close()
        self._spi.terminate()
        self._spi = None
        self._is_open = False

    def write(self, data: List[int], channel: int, frequency: int, mode: int) -> None:
        self._spi_operation('write', data, channel, frequency, mode)

    def read(self, length: int, channel: int, frequency: int, mode: int) -> List[int]:
        return self._spi_operation('read', [], channel, frequency, mode, length)

    def exchange(self, data: List[int], channel: int, frequency: int, mode: int) -> List[int]:
        return self._spi_operation('exchange', data, channel, frequency, mode)

    def _spi_operation(self, operation: str, data: List[int], channel: int, frequency: int, mode: int, length: int = None) -> List[int]:
        if not self._is_open:
            raise RuntimeError('SPI is not open')

        if channel < self._ADBUS_COUNT:
            spi_port = self._spi.get_port(channel, frequency, mode)
            if operation == 'write':
                spi_port.write(data)
            elif operation == 'read':
                return list(spi_port.read(length))
            elif operation == 'exchange':
                return list(spi_port.exchange(data, len(data)))
        else:
            # 対象のGPIOピンマスクを計算
            gpio_pin_mask = self._GPIO_BASE_MASK << (channel - self._ADBUS_COUNT)

            # 現在のGPIO状態を読み取る
            current_gpio_state = self._spi.read_gpio()

            # 対象のGPIOピンのみをLOWに設定
            new_gpio_state = current_gpio_state & ~gpio_pin_mask
            self._spi.write_gpio(new_gpio_state)

            # 命令を送信
            result = list(self._spi.exchange(frequency, data, readlen=length or len(data), duplex=True, cpol=bool(mode & 0x2), cpha=bool(mode & 0x1)))

            # 操作後に元のGPIO状態に戻す
            new_gpio_state = current_gpio_state | gpio_pin_mask
            self._spi.write_gpio(new_gpio_state)

            return result
