# fontwriter.py Implements the FontWriter class.

# The MIT License (MIT)
#
# Copyright (c) 2016 Peter Hinch
# Copyright (c) 2017 Brian Cappello
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# A FontWriter supports rendering text to a Display instance in a given font.
# Multiple FontWriter instances may be created, each rendering a font to the
# same Display object.


def from_bytes(data, signed=False):
    return int.from_bytes(data, 'little', signed)


class FontWriter(object):
    # these attributes and set_position are common to all FontWriter instances
    x_pos = 0
    y_pos = 0

    @classmethod
    def set_position(cls, x, y):
        cls.x_pos = x
        cls.y_pos = y

    def __init__(self, display, font, color=1):
        super().__init__()
        self.set_display(display)
        self.set_font(font)
        self.set_color(color)

    def set_display(self, display):
        self.display = display

    def set_font(self, font):
        self.font = font

    def set_color(self, color):
        self.color = color

    def _newline(self):
        FontWriter.x_pos = 0
        FontWriter.y_pos += self.font.HEIGHT

    def draw_text(self, string, color=None):
        color = color if color is not None else self.color
        for char in string:
            self.draw_char(char, color)

    def draw_char(self, char, color):
        """
        Draw a line mapped character
        """
        if char == '\n':
            self._newline()
            return

        is_lhmap, data, char_height, char_width = self.font.get_char(char)

        if FontWriter.x_pos + char_width > self.display.screen_width:
            self._newline()

        if is_lhmap:
            self._draw_lhmap_char(data, color)
        else:
            self._draw_lvmap_char(data, color)

        FontWriter.x_pos += char_width

    def _draw_lhmap_char(self, data, color):
        """
        Draw a horizontally line mapped character
        """
        prev_lines = []
        y = 0
        data_i = 0
        while data_i < len(data):
            num_lines = data[data_i]
            if num_lines:
                prev_lines = []
                y = FontWriter.y_pos + data[data_i + 1]
                for i in range(num_lines):
                    lstart = data_i + 2 + (i * 2)
                    x = FontWriter.x_pos + data[lstart]
                    length = data[lstart + 1]
                    prev_lines.append((x, length))
                    self.display.hline(x, y, length, color)
                data_i = lstart + 2
            else:
                y += 1
                for line in prev_lines:
                    self.display.hline(line[0], y, line[1], color)
                data_i += 1

    def _draw_lvmap_char(self, data, color):
        """
        Draw a vertically line mapped character
        """
        prev_lines = []
        x = 0
        data_i = 0
        while data_i < len(data):
            num_lines = data[data_i]
            if num_lines:
                prev_lines = []
                x = FontWriter.x_pos + data[data_i + 1]
                for i in range(num_lines):
                    lstart = data_i + 2 + (i * 2)
                    y = FontWriter.y_pos + data[lstart]
                    length = data[lstart + 1]
                    prev_lines.append((y, length))
                    self.display.vline(x, y, length, color)
                data_i = lstart + 2
            else:
                x += 1
                for line in prev_lines:
                    self.display.vline(x, line[0], line[1], color)
                data_i += 1
