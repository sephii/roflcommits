from PIL import Image, ImageDraw, ImageFont

class ImageManipulator:
    POSITION_TOPLEFT = 0
    POSITION_TOPRIGHT = 1
    POSITION_BOTTOMRIGHT = 2
    POSITION_BOTTOMLEFT = 3

    def __init__(self, image_path):
        self.image = Image.open(image_path)
        self.image_path = image_path

    def _cut_text(self, text, font):
        max_width = self.image.size[0]

        if font.getsize(text)[0] < max_width:
            return [text]

        words = text.split(' ')
        text_array = []
        start = 0

        for i, word in enumerate(words, 1):
            if font.getsize(' '.join(words[start:i]))[0] > max_width:
                text_array.append(' '.join(words[start:i - 1]))
                start = i - 1

        if i > start:
            text_array.append(' '.join(words[start:]))

        return text_array

    def add_text(self, text, position, font_file, font_size, 
                 padding=(10,10,10,10)):
        font = ImageFont.truetype(font_file, font_size)
        id = ImageDraw.Draw(self.image)
        image_width, image_height = self.image.size
        text_width, text_height = font.getsize(text)
        lines = self._cut_text(text, font)
        outline = 1
        outline_colour = 'black'

        positions = {
            self.POSITION_TOPLEFT: (
                padding[3], padding[0],
            ),
            self.POSITION_TOPRIGHT: (
                image_width - text_width - padding[1], padding[0],
            ),
            self.POSITION_BOTTOMRIGHT: (
                image_width - text_width - padding[1],
                self.image.size[1] - text_height * len(lines) - padding[2],
            ),
            self.POSITION_BOTTOMLEFT: (
                padding[3],
                self.image.size[1] - text_height * len(lines) - padding[2],
            ),
        }

        p = positions[position]
        offset_top = 0

        p_y = lambda t: p[1] + t

        for line in lines:
            id.text((p[0] + outline, p_y(offset_top)), line, font=font,
                    fill=outline_colour)
            id.text((p[0] - outline, p_y(offset_top)), line, font=font,
                    fill=outline_colour)
            id.text((p[0], p_y(offset_top) + outline), line, font=font,
                    fill=outline_colour)
            id.text((p[0], p_y(offset_top) - outline), line, font=font,
                    fill=outline_colour)
            id.text((p[0], p_y(offset_top)), line, font=font)
            offset_top += text_height

    def save(self, file):
        self.image.save(file)
