import math

from awil_ft232h import AwilFt232h


class AwilAd9833:
    """
    Note:
        AD9833のSPI通信を行うクラス

    Datasheet:
        https://www.analog.com/media/jp/technical-documentation/data-sheets/AD9833_JP.pdf
    """

    _SQUARE_WAVE_VOLTAGE = 5.0
    _OTHER_WAVE_VOLTAGE = 0.6
    _FREQ_MCLK = 25000000.0
    _MAX_FREQUENCY = 12500000.0
    _RESET = [0x01, 0x00]
    _SINE = [0x00, 0x00]
    _TRIANGLE = [0x00, 0x02]
    _SQUARE = [0x00, 0x28]
    _FREQUENCY = [0x20, 0x00]

    _SPI_MODE = 2

    def __init__(self, awil_ft232h: AwilFt232h, spi_channel: int = 0, spi_frequency: int = 1E6) -> None:
        self._awil_ft232h = awil_ft232h
        self._spi_channel = spi_channel
        self._spi_frequency = spi_frequency

    def reset(self) -> None:
        data = self._RESET
        self._awil_ft232h.write(data, self._spi_channel, self._spi_frequency, self._SPI_MODE)

    def set_wave_type(self, wave_type: int) -> None:
        """
        Args:
            wave_type (int): 0 = サイン波、1 = 三角波、2 = 方形波
        Note:
            周波数を設定すると波形が正弦波にリセットされるので毎回波形コマンドも送ること
        """

        data = []
        if wave_type == 0:
            data = self._SINE
        elif wave_type == 1:
            data = self._TRIANGLE
        elif wave_type == 2:
            data = self._SQUARE
        else:
            raise ValueError("wave_type must be 1, 2 or 3")

        self._awil_ft232h.write(data, self._spi_channel, self._spi_frequency, self._SPI_MODE)

    def set_frequency(self, frequency: float) -> None:  #
        """
        Args:
            frequency (float): 波形の周波数 [Hz]
        """

        freq_reg: int = int(round(frequency, 1) * math.pow(2, 28) / self._FREQ_MCLK)
        msb: int = (freq_reg & 0xFFFC000) >> 14
        lsb: int = freq_reg & 0x3FFF
        msb |= 0x4000
        lsb |= 0x4000
        lsb_data = [(lsb & 0xff00) >> 8, (lsb & 0x00ff)]
        msb_data = [(msb & 0xff00) >> 8, (msb & 0x00ff)]
        data = self._FREQUENCY + lsb_data + msb_data

        self._awil_ft232h.write(data, self._spi_channel, self._spi_frequency, self._SPI_MODE)
