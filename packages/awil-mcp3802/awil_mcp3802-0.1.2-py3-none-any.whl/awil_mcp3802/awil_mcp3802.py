from typing import List

from awil_ft232h import AwilFt232h

# データシート
# https://ww1.microchip.com/downloads/aemDocuments/documents/APID/ProductDocuments/DataSheets/21298e.pdf


class ControlBit:
    START = 0b00000100
    SINGLE_ENDED = 0b00000010
    DIFFERENTIAL = 0b00000000


class Channel:
    CH0 = 0b000
    CH1 = 0b001
    CH2 = 0b010
    CH3 = 0b011
    CH4 = 0b100
    CH5 = 0b101
    CH6 = 0b110
    CH7 = 0b111


class AwilMcp3802:
    AMOUNT_OF_CHANNELS = 8
    _RESOLUTION_BIT = 12
    _RESOLUTION_STEP = 2 ** _RESOLUTION_BIT
    _SPI_MODE = 0b00

    def __init__(self, awil_ft232h: AwilFt232h, supply_voltage: float = 3.3, spi_channel: int = 0, spi_requency: int = 1E6) -> None:
        self._awil_ft232h = awil_ft232h

        self._supply_voltage = supply_voltage
        self._spi_channel = spi_channel
        self._spi_frequency = spi_requency

    def read_voltage(self, channel: Channel) -> float:
        send_data = [
            ControlBit.START |  # Start bit
            ControlBit.SINGLE_ENDED |  # Single/Diff
            channel >> 2,  # Channel (MSB)
            (channel << 6 & 0b11000000),  # Channel (LSB)
            0b00000000
        ]
        received_data = self._awil_ft232h.exchange(send_data, self._spi_channel, self._spi_frequency, self._SPI_MODE)
        voltage = self._received_data_to_voltage(received_data)
        return voltage

    def read_all_voltages(self) -> List[float]:
        voltages = []
        for channel in range(self.AMOUNT_OF_CHANNELS):
            voltage = self.read_voltage(channel)
            voltages.append(voltage)
        return voltages

    def _received_data_to_voltage(self, data: List[int]) -> float:
        value = ((data[1] & 0x0F) << 8) | data[2]
        voltage = (value / self._RESOLUTION_STEP) * self._supply_voltage
        return voltage
