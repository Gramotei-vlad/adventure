import pygame


class Block(pygame.sprite.Sprite):
    """
       Level object class
       :arg path_to_image (str) - path to image blocks
       :arg coords (tuple) - coordinates of place where block is.
    """
    def __init__(self, path_to_image, coords):
        super().__init__()
        self.path_to_image = path_to_image
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]

    @property
    def coordinates(self):
        return self.rect.x, self.rect.y

    @property
    def image(self):
        return pygame.image.load(self.path_to_image)

    def __str__(self):
        return 'Block'
