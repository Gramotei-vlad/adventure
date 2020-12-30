from pyganim import PygAnimation
from pygame.sprite import Sprite
from pygame.mixer import Sound
from time import time
import pygame

STOP_MOVEMENT = 300
STOP_FALLING = 2000
GRAVITY_POWER = 15
TIME_TO_SHOW_DEATH_ANIMATION = 10
PUSH_SOUND = 'Gamedata/Sounds/push.wav'


class Mob(Sprite):
    """
       Class for creating game mobs
       Args:
           path_to_image (str) - path to image mob;
           animations (list) - list with paths to animations mobs;
           coords (tuple) - start coordinates of mob
           play_sounds (bool) - if True there will be certain sounds
    """
    def __init__(self, path_to_image, animations, coords, play_sounds):
        super().__init__()

        self.health = 100
        self.path_to_image = path_to_image
        self.stay_animation = PygAnimation([animations[0]])
        self.move_animation = PygAnimation(animations[:2])
        self.dead_animation = PygAnimation([animations[2]])
        self.rect = self.image.get_rect()
        self.rect.x = coords[0]
        self.rect.y = coords[1]
        self.play_sounds = play_sounds
        self.direction = 1
        self.dead_time = 0
        self.distance = 0
        self.speed = 10
        self.damage = 10
        self.push = 30
        self.push_sound = Sound(PUSH_SOUND)
        self.on_ground = True

        self._play_animations()

    @property
    def image(self):
        return pygame.image.load(self.path_to_image)

    @property
    def coordinates(self):
        return self.rect.x, self.rect.y

    def _play_animations(self):
        """
        Method for loading and playing animations It is enough to call method once
        :return: None
        """

        self.stay_animation.play()
        self.move_animation.play()
        self.dead_animation.play()

    def push_object(self, object_):
        """
        If has collision between mob and object_ (for example, player), mob will pushes object by self.push
        :param object_: pygame.sprite object
        :return: None
        """
        object_.health -= self.damage
        check = False
        if self.direction == 1 and object_.rect.x > self.rect.x:
            object_.rect.x += self.push
            check = True
        elif self.direction == -1 and object_.rect.x < self.rect.x:
            object_.rect.x -= self.push
            check = True

        if check and self.play_sounds:
            self.push_sound.play()

    def live(self, screen, camera, level_objects):
        """
        Life cycle of mob. If mod is dead it will returns True
        :param screen: (pygame.Surface) - screen where image will be drew
        :param camera: (Camera) - big rect that follows for player
        :param level_objects: (pygame.sprite.Group) - Group with level blocks sprites or mobs
        :return: (bool)
        """
        permissions = self._check_collision(level_objects)

        if permissions['is_dead']:
            self.dead_time = time()
            return True

        curr_distance = self.direction * self.speed

        if self.direction == 1 and permissions['right']:
            self.rect.x += curr_distance
        elif self.direction == -1 and permissions['left']:
            self.rect.x += curr_distance
        else:
            curr_distance = 0

        self.distance += abs(curr_distance)
        if self.distance >= STOP_MOVEMENT:
            self.direction *= -1
            self.distance = 0

        if curr_distance != 0:
            self.move_animation.blit(screen, camera.apply(self))
        else:
            self.stay_animation.blit(screen, camera.apply(self))

        self._gravity()

        if self.coordinates[1] >= STOP_FALLING:
            self.dead_time = time()
            return True
        return False

    def _gravity(self):
        """
        If there is no surface it means that mob is falling
        :return: None
        """
        if not self.on_ground:
            self.rect.y += GRAVITY_POWER

    def _check_collision(self, level_objects):
        """
           Checks collision with mob and finds side of collision
        :param level_objects: (pygame.sprite.Group) - Group with level blocks sprites
        :return: (dict) - dict with permissions to moves.
        """
        moves = {'right': True,
                 'left': True,
                 'up': False,
                 'is_dead': False}
        self.on_ground = False
        for object_ in level_objects:
            if self != object_ and object_.rect.colliderect(self.rect):
                # 100
                if object_.rect.centerx > self.rect.centerx and object_.rect.centery - self.rect.centery < 30:
                    moves['right'] = False
                    if str(object_) == 'Mob':
                        self.push_object(object_)
                elif object_.rect.centerx < self.rect.centerx and object_.rect.centery - self.rect.centery < 30:
                    moves['left'] = False
                    if str(object_) == 'Mob':
                        self.push_object(object_)

                if object_.rect.centery > self.rect.centery:
                    moves['up'] = True
                    self.on_ground = True
                else:
                    if str(object_) == 'Mob':
                        moves['is_dead'] = True
        return moves

    def __str__(self):
        return 'Mob'

    def die(self, screen, camera):
        """
        If mob is dead this method will be called. 10 seconds for showing death animations
        :param screen: (pygame.Surface) - screen where image will be drew
        :param camera: (Camera) - big rect that follows for player
        :return: (bool)
        """
        self.damage = 0
        self.push = 0
        self.health = 0

        self.dead_animation.blit(screen, camera.apply(self))

        curr_time = time()
        if curr_time - self.dead_time >= TIME_TO_SHOW_DEATH_ANIMATION:
            return True
        return False
