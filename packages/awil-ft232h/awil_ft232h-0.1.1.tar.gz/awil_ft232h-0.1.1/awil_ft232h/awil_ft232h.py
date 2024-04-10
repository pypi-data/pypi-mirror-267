from pyftdi.spi import SpiController, SpiPort
from typing import List
import time


class AwilFt232h:
    _ACBUS_COUNT = 10
    _ADBUS_COUNT = 5

    def __init__(self, serial_number: str) -> None:
        self._url = f'ftdi://ftdi:232h:{serial_number}/1'
        self._spi: SpiController = None
        self._spi_port: SpiPort = None

        self._cs = 0 # 0-4: ADBUS, 5-14: ACBUS
        self._freq = 1E6
        self._mode = 0

        self._is_open = False

    def __def__(self) -> None:
        if self._spi is not None:
            self.close()

    def open(self, cs: int = None, freq: int = None, mode: int = None) -> None:
        self._spi = SpiController(self._ADBUS_COUNT)
        self._spi.configure(self._url)

        self._is_open = True

        self._update(cs=cs, freq=freq, mode=mode)
        self._spi.set_gpio_direction(0xFF00, 0xFF00)
        self._spi.write_gpio(0xFF00)

    def close(self) -> None:
        self._spi.close()
        self._spi.terminate()
        self._spi = None
        self._spi_port = None
        self._is_open = False

    def write(self, data: List[int], cs: int = None, freq: int = None, mode: int = None) -> None:
        if self._is_open == False:
            raise Exception('SPI is not open')

        self._update(cs=cs, freq=freq, mode=mode)

        if self._cs < self._ADBUS_COUNT:
            self._spi_port.write(data)
        else:
            self._spi.write_gpio(0x0000)
            self._spi.exchange(self._freq, data, readlen=0, duplex=True, cpol=bool(self._mode & 0x2), cpha=bool(self._mode & 0x1))
            self._spi.write_gpio(0xFF00)

    def read(self, lenght: int, cs: int = None, freq: int = None, mode: int = None) -> List[int]:
        if self._is_open == False:
            raise Exception('SPI is not open')

        self._update(cs=cs, freq=freq, mode=mode)

        result = []
        if self._cs < self._ADBUS_COUNT:
            result = list(self._spi_port.read(lenght))
        else:
            self._spi.write_gpio(0x0000)
            result = self._spi.exchange(self._freq, [], readlen=lenght, duplex=True, cpol=bool(self._mode & 0x2), cpha=bool(self._mode & 0x1))
            self._spi.write_gpio(0xFF00)

        return result

    def exchange(self, data: List[int], cs: int = None, freq: int = None, mode: int = None) -> bytes:
        if self._is_open == False:
            raise Exception('SPI is not open')

        self._update(cs=cs, freq=freq, mode=mode)

        result = []
        if self._cs < self._ADBUS_COUNT:
            result = list(self._spi_port.exchange(data, len(data), duplex=True))
        else:
            self._spi.write_gpio(0x0000)
            result = self._spi.exchange(self._freq, data, readlen=len(data), duplex=True, cpol=bool(self._mode & 0x2), cpha=bool(self._mode & 0x1))
            self._spi.write_gpio(0xFF00)

        return result

    def _update(self, cs: int = None, freq: int = None, mode: int = None) -> None:
        if self._is_open == False:
            raise Exception('SPI is not open')
        if cs is None and freq is None and mode is None:
            return

        if cs is not None:
            self._cs = cs
        if freq is not None:
            self._freq = freq
        if mode is not None:
            self._mode = mode

        if self._cs < self._ADBUS_COUNT:
            self._spi_port = self._spi.get_port(cs=self._cs, freq=self._freq, mode=self._mode)
        else:
            self._spi_port = None
