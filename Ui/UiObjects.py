import pygame
import time


class UiObject:
    """
     Interface object (Icons sound, pause and etc)
     :arg:
        :image (pygame.image) - icon for Ui Object;
        :x (int) - x coordinate of top left corner;
        :y (int) - y coordinate of top left corner;
        :width (int) - width of icon;
        :height (int) - height of icon;
        :sound_path (str) - path to sound of icon;
    """
    def __init__(self, images, name, x, y, width, height, sound_path):
        self.main_image = images[0]
        self.images = images
        self.name = name
        self.left_up_corner = x, y
        self.right_down_corner = x + width, y + height
        self.sound_path = sound_path
        self.curr_idx = 0

    @property
    def sound(self):
        return pygame.mixer.Sound(self.sound_path)

    def check_collision(self, pos, sound=True):
        """
        Method for check collision between mouse click and ui icon
        :param pos: (tuple) - tuple of x, y coordinate of left mouse click
        :param sound: (bool) if True there will be a certain sound
        :return: (bool) if there is a collision - True, else False
        """
        x, y = pos
        if self.left_up_corner[0] <= x <= self.right_down_corner[0] and (
            self.left_up_corner[1] <= y <= self.right_down_corner[1]
        ):
            if sound:
                self.sound.play()

            # Сон нужен, чтобы звук не отставал.
            # Для пользователя задержка будет не сильно заметна
            # И при этом звук проиграется именно в момент клика
            time.sleep(0.5)
            return True
        return False

    def _get_next_img_idx(self):
        """
           Method for getting next index of image
        :return: (int) current image from ui object
        """
        self.curr_idx = (self.curr_idx + 1) % len(self.images)
        return self.curr_idx

    def change_state(self):
        """
           Method for getting next image in ui structure
        :return: None
        """
        self._get_next_img_idx()
        self.main_image = self.images[self.curr_idx]

