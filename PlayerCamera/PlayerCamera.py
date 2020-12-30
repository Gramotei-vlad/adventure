from pygame.locals import *

CAMERA_X_RESOLUTION = 4096
CAMERA_Y_RESOLUTION = 1000  # 1000


class Camera(object):
    def __init__(self, camera_func, window_resolution):
        self.camera_func = camera_func
        self.window_resolution = window_resolution
        self.state = Rect(0, 0, CAMERA_X_RESOLUTION, CAMERA_Y_RESOLUTION)

    def apply(self, target):
        return target.rect.move(self.state.topleft)

    def update(self, target):
        self.state = self.camera_func(self.state, target.rect, *self.window_resolution)


def camera_configure(camera, target_rect, window_width, window_height):
    l, t, _, _ = target_rect
    _, _, w, h = camera
    l = -l + window_width / 2
    t = -t + window_height / 2 + 135  # Закомментить надо

    l = min(0, l)
    l = max(-(camera.width - window_width), l)
    t = max(-(camera.height - window_height), t)
    t = min(0, t)
    return Rect(l, t, w, h)
