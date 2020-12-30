from pygame.locals import *
from Game.Player import MainCharacter
from Ui.UiObjects import UiObject
from Levels.LevelGenerator import LevelGenerator
from PlayerCamera.PlayerCamera import Camera, camera_configure
from pygame.sprite import Group
from pygame.sysfont import SysFont

import pygame

GAME_OVER_CAPTION = 'You were killed. Press any mouse key to continue...'
GAME_OVER_CAPTION_X = 150
GAME_OVER_CAPTION_Y = 100
THE_LONGEST_DISTANCE_CAPTION = 'The longest distance that you have run: '
DISTANCE_CAPTION_X = 200
DISTANCE_CAPTION_Y = 200
ALL_DISTANCE_CAPTION = 'All distance that you have run: '
ALL_DISTANCE_CAPTION_X = 200
ALL_DISTANCE_CAPTION_Y = 300
HEALTH_IMAGE_X = 100
HEALTH_IMAGE_Y = 0
HEALTH_X = 150
HEALTH_Y = 0
GREEN = (0, 255, 0)


class Game:
    """
       Class with game settings/level loaders/game rules
          :self.width (int) width of game window;
          :self.height (int) - height of game window;
          :self.full_screen (int) - FULLSCREEN or 0;
          :self.fps (int) - frame per second;
          :self.caption (str) - window name;
          :self.active_game (bool) - if false - quit from game else game is running
          :self.background_path (str) - path to image background
          :self._screen (pygame.Surface) - screen where image will be drew
          :self.background_image (pygame.image) - background image
    """

    def __init__(self):
        self.width = 0
        self.height = 0
        self.full_screen = True
        self.fps = 0
        self.caption = 'Adventure'
        self.active_game = True
        self.statistics = False
        self.background_path = 'Gamedata/Backgrounds/fon.png'
        self.max_distance = 0
        self.total_distance = 0
        self.sound = True
        self.font = SysFont(None, 45)
        self._screen = None
        self._camera = None

    @staticmethod
    def _get_settings():
        """
        Method for getting game settings from file
        :return: settings_data (dict) - dict with game settings
        """
        settings_data = dict()
        with open('Gamedata/settings.txt', mode='r') as f:
            for line in f:
                line = line.split(':')
                parameter, value = line[0], int(line[-1])
                settings_data[parameter] = value
        return settings_data

    @property
    def background_image(self):
        return pygame.image.load(self.background_path)

    @property
    def clock_(self):
        return pygame.time.Clock()

    def set_screen(self):
        """
        Set screen with self.width, self.height and self.full_screen
        :return: None
        """

        self._screen = pygame.display.set_mode((self.width, self.height), self.full_screen)

    def set_camera(self):
        self._camera = Camera(camera_configure, (self.width, self.height))

    @staticmethod
    def _get_save_data():
        """
        Method for getting game saves from file
        :return: save_data (dict) - dict with save data
        """
        save_data = dict()
        with open('GameData/saves.txt', mode='r') as f:
            for line in f:
                line = line.split(':')
                save_data[line[0]] = int(line[-1])
        return save_data

    def _menu(self):
        """
        Menu level where player may choose settings/levels and etc.
        If self.active_game is True it means that game is running else
        exiting the game
        :return: None
        """

        ui_elems = self._load_menudata()
        while self.active_game:

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    for obj in ui_elems:
                        if obj.name == 'start' and obj.check_collision(pos, self.sound):
                            self._game_loop()
                        if obj.name == 'music' and obj.check_collision(pos, self.sound):
                            self.sound = not self.sound
                            obj.change_state()
                        if obj.name == 'trophy' and obj.check_collision(pos, self.sound):
                            self._get_statistics(obj)
                        if obj.name == 'quit' and obj.check_collision(pos, self.sound):
                            self.active_game = False

                if event.type == QUIT:
                    self.active_game = False

            self._screen.blit(self.background_image, (0, 0))
            for obj in ui_elems:
                self._screen.blit(obj.main_image, obj.left_up_corner)
            pygame.display.update()
            self.clock_.tick(self.fps)

        self._save_game()
        pygame.quit()

    def _load_game(self):
        """
        Load game with saved game settings and game status
        :return: None
        """

        settings = self._get_settings()
        for parameter, value in settings.items():
            if parameter == 'width':
                self.width = value
            elif parameter == 'height':
                self.height = value
            elif parameter == 'full_screen':
                self.full_screen = FULLSCREEN if value == 1 else 0
            elif parameter == 'fps':
                self.fps = value
            elif parameter == 'sound':
                self.sound = True if value == 1 else False
            else:
                raise('Undefined parameter ' + str(parameter) + ' in settings.txt')

        saves = self._get_save_data()
        for parameter, value in saves.items():
            if parameter == 'max_distance':
                self.max_distance = value
            elif parameter == 'total_distance':
                self.total_distance = value
            else:
                raise ('Undefined parameter ' + str(parameter) + 'in saves.txt')

        self.set_screen()

    @staticmethod
    def _load_menudata():
        """
        Load icons and its sounds for menu game
        :return: (arr) - ui_elems
        """

        data = [(['GameData/Menu/buttonStart.png'], 'start', (450, 384), (90, 60), 'GameData/Sounds/MainButton.wav'),
                (['GameData/Menu/trophy.png'], 'trophy', (900, 50), (50, 50), 'GameData/Sounds/click.wav'),
                (['GameData/Menu/musicOn.png', 'GameData/Menu/musicOff.png'], 'music', (900, 100), (50, 50),
                 'GameData/Sounds/click.wav'),
                (['GameData/Menu/quit.png'], 'quit', (900, 150), (50, 50), 'GameData/Sounds/click.wav')]
        ui_elems = []
        for img_paths, name, coords, shape, sound_path in data:
            imgs = []
            for img_path in img_paths:
                img = pygame.image.load(img_path)
                imgs.append(img)
            ui_obj = UiObject(imgs, name, *coords, *shape, sound_path)
            ui_elems.append(ui_obj)
        return ui_elems

    def _game_loop(self):
        """
        Main loop with game where will be load main character, game mobs, ui levels and etc
        During the game all game objects will be drawn in self._screen
        Self.clock_ supports current self.fps
        :return: None
        """

        player = MainCharacter()
        level_generator = LevelGenerator(play_sounds=self.sound)
        dead_mobs = Group()
        self.set_camera()
        active_level = True
        result_session_was_saved = False
        while active_level:

            for event in pygame.event.get():
                if event.type == QUIT or (event.type == MOUSEBUTTONUP and player.is_dead):
                    active_level = False

            self._screen.blit(self.background_image, (0, 0))
            level_data = level_generator.draw_blocks(self._screen, self._camera, player.region)
            left_region = level_generator.get_left_region()

            level_blocks = level_data['level_blocks'].copy()
            level_blocks.add(level_data['mobs'])

            if not player.is_dead:
                player.move(self._screen, self._camera, left_region, level_blocks)
            else:
                if not result_session_was_saved:
                    self._save_session_result(player)
                    result_session_was_saved = True
                self._get_end_game_caption()

            for entity in level_data['mobs']:
                if entity.live(self._screen, self._camera, level_blocks):
                    dead_mobs.add(entity)
                    level_generator.remove_objects(entity)

            for dead_entity in dead_mobs:
                if dead_entity.die(self._screen, self._camera):
                    dead_mobs.remove(dead_entity)

            self._draw_ui_elem(player)
            pygame.display.update()
            self._camera.update(player)
            self.clock_.tick(self.fps)

    def start_game(self):
        """
        Public method for starting the game
        :return: None
        """

        self._load_game()
        pygame.display.set_caption(self.caption)
        self._menu()

    def _get_end_game_caption(self):
        """
            Method for drawing end game caption
        :return: None
        """
        curr_font = self.font.render(GAME_OVER_CAPTION, 0, GREEN)
        self._screen.blit(curr_font, (GAME_OVER_CAPTION_X, GAME_OVER_CAPTION_Y))

    def _save_session_result(self, player):
        """
            Method for saving session data
        :param player: (Player) - player object
        :return: None
        """
        self.max_distance = max(self.max_distance, player.max_distance)
        self.total_distance += player.max_distance

    def _draw_ui_elem(self, player):
        """
           Method for drawing ui elems in during the game (health and etc.)
        :param player: (Player) - player object
        :return: None
        """
        health_font = self.font.render(str(player.health), 0, GREEN)
        self._screen.blit(player.health_image, (HEALTH_IMAGE_X, HEALTH_IMAGE_Y))
        self._screen.blit(health_font, (HEALTH_X, HEALTH_Y))

    def _get_statistics(self, trophy_obj):
        """
           Method for showing statistics to player
        :param trophy_obj: (UiObject)
        :return: None
        """
        self.statistics = True
        curr_font = self.font.render(THE_LONGEST_DISTANCE_CAPTION + str(self.max_distance), 0, GREEN)
        curr_font_2 = self.font.render(ALL_DISTANCE_CAPTION + str(self.total_distance), 0, GREEN)

        while self.statistics:

            for event in pygame.event.get():
                if event.type == MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if trophy_obj.check_collision(pos, self.sound):
                        self.statistics = False

                if event.type == QUIT:
                    self.statistics = False

            self._screen.blit(self.background_image, (0, 0))

            self._screen.blit(curr_font, (DISTANCE_CAPTION_X, DISTANCE_CAPTION_Y))
            self._screen.blit(curr_font_2, (ALL_DISTANCE_CAPTION_X, ALL_DISTANCE_CAPTION_Y))
            self._screen.blit(trophy_obj.main_image, trophy_obj.left_up_corner)

            pygame.display.update()
            self.clock_.tick(self.fps)

    def _save_game(self):
        """
           Save statistics data and settings in the end of game.
        :return: None
        """
        settings = {'width': self.width,
                    'height': self.height,
                    'full_screen': self.full_screen,
                    'fps': self.fps,
                    'sound': self.sound
                    }
        statistics = {'max_distance': self.max_distance,
                      'total_distance': self.total_distance}

        with open('GameData/settings.txt', 'w') as f:
            for parameter, value in settings.items():
                if isinstance(value, bool):
                    value = 1 if value is True else 0
                if parameter == 'full_screen' and value != 0:
                    value = 1
                f.write(parameter + ': ' + str(value) + '\n')

        with open('GameData/saves.txt', 'w') as f:
            for parameter, value in statistics.items():
                f.write(parameter + ': ' + str(value) + '\n')
