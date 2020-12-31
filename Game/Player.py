import pygame
from pygame.locals import *
from pyganim import PygAnimation
from pygame.sprite import Sprite

GRAVITY_POWER = 5
ENERGY_RECOVERY = 5
STOP_FALLING = 2000
JUMP_POWER = 65
START_PLAYER_POSITION_X = 512
START_PLAYER_POSITION_Y = 0
PLAYER_IMAGE = 'Gamedata/Players/yellow_front.png'
PLAYER_FALLING_IMAGE = 'GameData/Players/yellow_fall.png'
PLAYER_RIGHT_IMAGE = 'GameData/Players/yellow_right.png'
HEALTH_IMAGE = 'GameData/UI/hudHeart_full.png'
ANIMATION_DELAY = 0.1


class MainCharacter(Sprite):
    """
       Class with player characteristics, animations and etc
       :self.image_path (str) - path to image sprite;
       :self.stay_and_left_animation (PygAnimation) - animations of stay and left movement;
       :self.fall_animation (PygAnimation) - animations of falling player
       :self.right_animation (PygAnimation) - animations of right movement;
       :self.rect (pygame.Rect) - rect of player (player is a rect with point of view of game)
       :self.on_ground (bool) - Is player on ground?
       :self.jump_power (int) - amount of pixels that character will move by
       :self.down_speed (int) - speed of falling;
       :self.image (pygame.image) - image of player;
       :self.coordinates (tuple) - coordinate of player on xy-axis

    """
    def __init__(self):
        super().__init__()

        self.image_path = PLAYER_IMAGE
        self.stay_and_left_animation = PygAnimation([(PLAYER_IMAGE, ANIMATION_DELAY)])
        self.fall_animation = PygAnimation([(PLAYER_FALLING_IMAGE, ANIMATION_DELAY)])
        self.right_animation = PygAnimation([(PLAYER_RIGHT_IMAGE, ANIMATION_DELAY)])
        self.health_image = pygame.image.load(HEALTH_IMAGE)
        self.rect = self.image.get_rect()
        self.on_ground = True
        self.is_jumping = False
        self.jump_power = JUMP_POWER
        self.speed = 30
        self.health = 100
        self.max_distance = 0
        self.down_speed = 25

        self.set_start_coords(START_PLAYER_POSITION_X, START_PLAYER_POSITION_Y)
        self._play_animations()

    @property
    def image(self):
        return pygame.image.load(self.image_path)

    @property
    def coordinates(self):
        return self.rect.x, self.rect.y

    @property
    def region(self):
        return self.coordinates[0] // 1000

    @property
    def is_dead(self):
        return self.health <= 0 or self.coordinates[1] >= STOP_FALLING

    def set_start_coords(self, x, y):
        """
        Set start coords
        :param x: (int) - x-axis;
        :param y: (int) - y-axis;
        :return: None
        """

        self.rect.x = x
        self.rect.y = y

    def move(self, screen, camera, left_stop, level_objects):
        """
          Method for processing player movements
        :param screen: (pygame.Surface) - screen where image will be drew
        :param camera: (Camera) - big rect that follows for player
        :param left_stop (int) - the leftmost region (as a rule it equals curr_region - 1)
        :param level_objects (pygame.sprite.Group) - Group with level blocks sprites
        :return: None
        """
        permissions = self._check_collision(level_objects)
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_UP] and permissions['up']:
            self.is_jumping = True
        elif pressed_keys[K_RIGHT] and permissions['right']:
            if self.on_ground is True:
                self.right_animation.blit(screen, camera.apply(self))
            self.rect.x += self.speed
            self.max_distance += self.speed
            self.rect.x = max(self.rect.x % 3584, 512)
        elif pressed_keys[K_LEFT] and permissions['left']:
            if self.on_ground is True:
                self.stay_and_left_animation.blit(screen, camera.apply(self))
            if self.rect.x >= left_stop * 1024 + 150:
                self.rect.x -= self.speed
                self.max_distance -= self.speed
        else:
            if self.on_ground:
                self.stay_and_left_animation.blit(screen, camera.apply(self))

        if self.is_jumping:
            self._jumping(screen, camera, permissions['top_collision'])
        else:
            self._gravity(screen, camera)

    def _check_collision(self, level_objects):
        """
           Check collision with player and its side
        :param level_objects: (pygame.sprite.Group) - Group with level blocks sprites
        :return: (dict) - dict with permissions to moves.
        """
        moves = {'right': True,
                 'left': True,
                 'up': False,
                 'top_collision': False}
        self.on_ground = False
        for object_ in level_objects:
            if object_.rect.colliderect(self.rect):
                if object_.rect.centerx > self.rect.centerx and object_.rect.centery - self.rect.centery < 100:
                    moves['right'] = False
                    if str(object_) == 'Mob':
                        object_.push_object(self)
                elif object_.rect.centerx < self.rect.centerx and object_.rect.centery - self.rect.centery < 100:
                    moves['left'] = False
                    if str(object_) == 'Mob':
                        object_.push_object(self)
                if object_.rect.centery > self.rect.centery:
                    moves['up'] = True
                    self.on_ground = True
                else:
                    moves['top_collision'] = True
        return moves

    def _jumping(self, screen, camera, top_collision):
        """
           If this method was called it means that player is flying (self.on_ground = False)
        :param screen: (pygame.Surface) - screen where image will be drew
        :param camera: (Camera) - big rect that follows for player
        :param top_collision (bool) - if True player collides with top block
        :return: None
        """
        if self.jump_power > 0 and top_collision is False:
            self.fall_animation.blit(screen, camera.apply(self))
            self.rect.y -= self.jump_power
            self.jump_power -= GRAVITY_POWER
        else:
            self.is_jumping = False

    def _gravity(self, screen, camera):
        """
            Check if the character is on the ground or not. If false it means that character is falling
        :param screen: (pygame.Surface) - screen where image will be drew
        :param camera: (Camera) - big rect that follows for player
        :return: None
        """

        if not self.on_ground:
            self.fall_animation.blit(screen, camera.apply(self))
            self.rect.y += self.down_speed
        else:
            self.jump_power = min(JUMP_POWER, self.jump_power + ENERGY_RECOVERY)

    def _play_animations(self):
        """
        Method for loading and playing animations It is enough to call method once
        :return: None
        """

        self.stay_and_left_animation.play()
        self.right_animation.play()
        self.fall_animation.play()
