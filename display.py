import ssd1306

from fontwriter import FontWriter


class Display(ssd1306.SSD1306_I2C):
    screen_height = 0
    screen_width = 0

    def __init__(self, width, height, i2c, addr=0x3c, external_vcc=False,
                 default_font_writer=None, rotation=None):
        super().__init__(width, height, i2c, addr, external_vcc)
        self.set_default_font_writer(default_font_writer)
        self.set_rotation(rotation)

    def set_default_font_writer(self, default_font_writer):
        self.default_font_writer = default_font_writer

    def set_position(self, x, y):
        x = x if x is not None else FontWriter.x_pos
        y = y if y is not None else FontWriter.y_pos
        FontWriter.set_position(x, y)

    def draw_text(self, text, *, x=None, y=None, font_writer=None, color=None):
        self.set_position(x, y)
        if font_writer:
            font_writer.draw_text(text, color)
        else:
            self.default_font_writer.draw_text(text, color)

    def clear(self):
        self.fill(0)
        self.show()

    def set_rotation(self, rotation=None):
        rotation = 0 if not rotation else rotation % 360
        if not rotation:
            self.pixel = self._pixel
            self.hline = self._hline
            self.vline = self._vline
        elif rotation == 90:
            self.pixel = self._pixel_90
            self.hline = self._hline_90
            self.vline = self._vline_90
        elif rotation == 180:
            self.pixel = self._pixel_180
            self.hline = self._hline_180
            self.vline = self._vline_180
        elif rotation == 270:
            self.pixel = self._pixel_270
            self.hline = self._hline_270
            self.vline = self._vline_270
        else:
            raise ValueError('rotation must be falsy or one of 90, 180 or 270')

        if not rotation or rotation == 180:
            self.screen_width = self.width
            self.screen_height = self.height
        else:
            self.screen_width = self.height
            self.screen_height = self.width

    def _pixel(self, x, y, color=1):
        self.framebuf.pixel(x, y, color)

    def _hline(self, x, y, length, color=1):
        self.framebuf.hline(x, y, length, color)

    def _vline(self, x, y, length, color=1):
        self.framebuf.vline(x, y, length, color)

    def _pixel_90(self, x, y, color=1):
        self.framebuf.pixel(self.width - y, x, color)

    def _hline_90(self, x, y, length, color=1):
        self.framebuf.vline(self.width - y - 1, x, length, color)

    def _vline_90(self, x, y, length, color=1):
        self.framebuf.hline(self.width - y - length, x, length, color)

    def _pixel_180(self, x, y, color=1):
        self.framebuf.pixel(self.width - x, self.height - y, color)

    def _hline_180(self, x, y, length, color=1):
        self.framebuf.hline(self.width - x - length, self.height - y - 1, length, color)

    def _vline_180(self, x, y, length, color=1):
        self.framebuf.vline(self.width - x - 1, self.height - y - length, length, color)

    def _pixel_270(self, x, y, color=1):
        self.framebuf.pixel(y, self.height - x, color)

    def _hline_270(self, x, y, length, color=1):
        self.framebuf.vline(y, self.height - x - length, length, color)

    def _vline_270(self, x, y, length, color=1):
        self.framebuf.hline(y, self.height - x - 1, length, color)
