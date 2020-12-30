from random import choice
from collections import deque
from Levels.Blocks import Block
from Mobs.GameCharacters import Mob
from pygame.sprite import Group


LEVELS = [
    [['.', '.', '.', '.', '.', '.', ',', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '-', '-', '-', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.']],

    [['.', '.', '.', '.', '.', '.', ',', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['-', '-', '-', '-', '-', '-', '-', '-']],

    [['.', '.', '-', '-', '-', '-', ',', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '-', '-', '.', '.', '.'],
     ['-', '-', '-', '-', '-', '-', '-', '-']],

    [['.', '.', '.', '.', '.', '.', '+', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '-', '-', '-', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['.', '.', '.', '.', '.', '+', '.', '.'],
     ['.', '.', '.', '.', '.', '.', '.', '.'],
     ['-', '-', '-', '-', '-', '-', '-', '-']]
]
ANIMATION_DELAY = 0.1
PATH_TO_IMAGE_GRASS = 'Gamedata/Blocks/grass.png'
PATH_TO_IMAGE_WORM = 'Gamedata/Mobs/Worms/wormGreen.png'
ANIMATIONS_WORMS = [('Gamedata/Mobs/Worms/wormGreen.png', ANIMATION_DELAY),
                    ('Gamedata/Mobs/Worms/wormGreen_move.png', ANIMATION_DELAY),
                    ('Gamedata/Mobs/Worms/wormGreen_dead.png', ANIMATION_DELAY)]
BLOCK_WIDTH = 128
BLOCK_HEIGHT = 108
WORM_WIDTH = 128
WORM_HEIGHT = 128
SCREEN_RESOLUTION = 1024
AMOUNT_REGIONS_TO_DRAW = 4


class LevelGenerator:
    """
       Class for generation levels from LEVELS constant.

       self.level_blocks: (deque) - array with block level from LEVELS. len(level_blocks) == 4;
       self.is_start: (bool) - determines the start of the game;
       self.next_region: (int) - number of the next region (0, 1, 2, 3);
    """
    def __init__(self, play_sounds):
        self.string_level_blocks = deque([])
        self.sprite_level_blocks = deque([])
        self.is_start = True
        self.next_region = 0
        self.play_sounds = play_sounds

        self.generate_level()

    def _generate_next_blocks(self):
        """
        Generate next blocks from LEVELS and change self.next_region attribute
        :return: None
        """
        next_block = choice(LEVELS)
        if self.is_start is False and self.next_region == 0:
            last = self.string_level_blocks[-1][1]
            self.string_level_blocks.append((self.next_region, last))
            self._get_sprites_block(last, self.next_region)
        else:
            if self.next_region != 0:
                self.string_level_blocks.append((self.next_region, next_block))
                self._get_sprites_block(next_block, self.next_region)
            else:
                if len(self.string_level_blocks) > 0:
                    last = self.string_level_blocks[-1][1]
                    self.string_level_blocks.append((self.next_region, last))
                    self._get_sprites_block(last, self.next_region)
                else:
                    self.string_level_blocks.append((self.next_region, next_block))
                    self._get_sprites_block(next_block, self.next_region)
        self.next_region += 1
        self.next_region %= AMOUNT_REGIONS_TO_DRAW

    def draw_blocks(self, screen, camera, region, return_blocks=True):
        """
        Method for drawing level blocks
        :param screen: (pygame.Surface) - screen where objects will be drawn;
        :param camera: (Camera) -  big rect that follows for player;
        :param region: (int) - current region of player;
        :param return_blocks (bool) if True returns dict with level_blocks and mobs sprites.
        :return: None
        """
        if self.is_start and region == 2:
            self._get_next_state()
        else:
            if (self.get_left_region() + 1) % AMOUNT_REGIONS_TO_DRAW == (region - 1) % AMOUNT_REGIONS_TO_DRAW:
                self._get_next_state()

        for level_region in self.sprite_level_blocks:
            for level_object in level_region:
                if str(level_object) == 'Block':
                    screen.blit(level_object.image, camera.apply(level_object))

        if return_blocks:
            return self._get_all_objects()

    def _get_sprites_block(self, block, region):
        """
           Method for getting sprites from str chars
           (+) - worm;
           (-) - platform object;
           (.) - nothing;
        :param block: arr[arr[str]] level region that need to draw
        :param region: (int) - current region
        :return: None
        """
        level_data = Group()
        for idx_row, row in enumerate(block):
            for idx_elem, elem in enumerate(row):
                if elem == '-':
                    x = idx_elem * BLOCK_WIDTH + SCREEN_RESOLUTION * region
                    y = idx_row * BLOCK_HEIGHT
                    block = Block(PATH_TO_IMAGE_GRASS, (x, y))
                    level_data.add(block)
                elif elem == '+':
                    x = idx_elem * WORM_WIDTH + SCREEN_RESOLUTION * region
                    y = idx_row * WORM_HEIGHT
                    worm = Mob(PATH_TO_IMAGE_WORM, ANIMATIONS_WORMS, (x, y), self.play_sounds)
                    level_data.add(worm)
        self.sprite_level_blocks.append(level_data)

    def generate_level(self):
        """
        Method for starting level generation
        :return: None
        """
        for _ in range(AMOUNT_REGIONS_TO_DRAW):
            self._generate_next_blocks()

    def _get_next_state(self):
        """
        Method for generate next level blocks from LEVELS
        :return: None
        """
        self.string_level_blocks.popleft()
        self.sprite_level_blocks.popleft()
        self._generate_next_blocks()
        self.is_start = False

    def _get_all_objects(self):
        """
         Method for getting all sprite objects at the moment
        :return: dict with level blocks and mobs sprites
        """
        level_objects = Group()
        mobs_objects = Group()
        for sprite_group in self.sprite_level_blocks:
            for object_ in sprite_group:
                if str(object_) == 'Mob':
                    mobs_objects.add(object_)
                elif str(object_) == 'Block':
                    level_objects.add(object_)
        return {'level_blocks': level_objects,
                'mobs': mobs_objects}

    def get_left_region(self):
        """
        Get the leftmost region
        :return: None
        """
        return self.string_level_blocks[0][0]

    def remove_objects(self, objects):
        """
           Delete sprite objects from level objects
        :param objects: (pygame.sprite.Group) - removing objects
        :return:
        """
        for sprite_group in self.sprite_level_blocks:
            sprite_group.remove(objects)
