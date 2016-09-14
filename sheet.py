from PIL import Image
import os


class Sheet:
    """
    create a contact sheet of avatars starting from an unsized image
    """
    def __init__(self, image_filename, sheet_width=1200, sheet_height=900, margin=50,
                 avatar_width=150, space_between=10):
        """
        :param image_filename: full filename of unsized image to use. Parent directory is used for storing output
        :param sheet_width: (in px)
        :param sheet_height: (in px)
        :param margin: used for all 4 margins (in px)
        :param avatar_width: specify width of avatar on the contact sheet. Avatar height is
          calculated from aspect ratio
        :param space_between: space between avatars on the contact sheet (in px)
        :return:
        """
        A4 = (sheet_width, sheet_height)
        white = 0xFFFFFFFF
        self.sheet = Image.new(mode="RGBA", size=A4, color=white)
        self.margin = margin
        self.space_between = space_between
        self.avatar_width = avatar_width
        self.avatar_height = None  # set later
        self.avatar = self.get_avatar(image_filename)
        self.image_location = os.path.dirname(image_filename)
        self.image_filename = image_filename
        self.avatars_across = int(float(sheet_width - margin * 2) / (self.avatar_width + self.space_between))
        self.avatars_down = int(float(sheet_height - margin * 2) / (self.avatar_height + self.space_between))
        # TODO: this will fail if multiple Sheet objects are in process simultaneously
        self.thumbnail_filename = os.path.join(self.image_location, 'thumbnail.png')
        self.avatar.save(self.thumbnail_filename)

    def get_avatar(self, image_filename):
        original_image = Image.open(image_filename)
        width, height = original_image.size
        asp_ratio = float(height) / float(width)
        self.avatar_height = int(self.avatar_width * asp_ratio)
        return original_image.resize((self.avatar_width, self.avatar_height), Image.ANTIALIAS)

    def place_avatars(self):
        ypos = 0
        while ypos < self.avatars_down:
            xpos = 0
            while xpos < self.avatars_across:
                self.sheet.paste(self.avatar, self.coordinates(ypos, xpos))
                xpos += 1
            ypos += 1
        return self

    def coordinates(self, ypos, xpos):
        y_coord = self.margin + ypos * (self.avatar_height + self.space_between)
        x_coord = self.margin + xpos * (self.avatar_width + self.space_between)
        return x_coord, y_coord

    def save_sheet(self):
        """
        save sheet (lossless) with name based on original image filename
        """
        sheet_filename = '{0}_sheet.png'.format(os.path.splitext(os.path.basename(self.image_filename))[0])
        sheet_filename = os.path.join(self.image_location, sheet_filename)
        self.sheet.save(sheet_filename, 'png')
        os.unlink(self.thumbnail_filename)

if __name__ == '__main__':
    Sheet(r'C:\Users\m45914\Code\commoncode\images\Kingfisher.jpg').place_avatars().save_sheet()
