from Ui.UiObjects import UiObject
from Game.Player import MainCharacter
from Levels.Blocks import Block
from pygame.sprite import Group

import unittest


class UiObjectTest(unittest.TestCase):
    def test_check_collision(self):
        data = (['GameData/Menu/MainButton.png'], 'start', (450, 384), (90, 60), 'GameData/Sounds/MainButton.wav')
        object_1 = UiObject(data[0], data[1], *data[2], *data[3], data[4])
        pos = (30, 30)
        result_1 = object_1.check_collision(pos, sound=False)

        object_2 = UiObject(data[0], data[1], *data[2], *data[3], data[4])
        pos_2 = (450, 384)
        result_2 = object_2.check_collision(pos_2, sound=False)

        object_3 = UiObject(data[0], data[1], *data[2], *data[3], data[4])
        pos_3 = (540, 384)
        result_3 = object_3.check_collision(pos_3, sound=False)

        self.assertEqual(result_1, False)
        self.assertEqual(result_2, True)
        self.assertEqual(result_3, True)

    def test_get_next_img_idx(self):
        data = (['GameData/Menu/MainButton.png'], 'start', (450, 384), (90, 60), 'GameData/Sounds/MainButton.wav')
        object_1 = UiObject(data[0], data[1], *data[2], *data[3], data[4])
        result = object_1._get_next_img_idx()

        data = (['GameData/Menu/MainButton.png', 'Another_path'], 'start',
                (450, 384), (90, 60), 'GameData/Sounds/MainButton.wav')
        object_2 = UiObject(data[0], data[1], *data[2], *data[3], data[4])
        result_2 = object_2._get_next_img_idx()

        data = (['GameData/Menu/MainButton.png', 'Another_path'], 'start',
                (450, 384), (90, 60), 'GameData/Sounds/MainButton.wav')
        object_3 = UiObject(data[0], data[1], *data[2], *data[3], data[4])
        object_3._get_next_img_idx()
        result_3 = object_3._get_next_img_idx()

        self.assertEqual(result, 0)
        self.assertEqual(result_2, 1)
        self.assertEqual(result_3, 0)


class PlayerTestCase(unittest.TestCase):
    def test_check_collision(self):
        player = MainCharacter()
        level_objects = Block('Gamedata/Blocks/grass.png', (20, 20))
        result_1 = player._check_collision(Group(level_objects))
        ans_1 = {'up': False, 'top_collision': False, 'right': True, 'left': True}

        level_objects_2 = Block('Gamedata/Blocks/grass.png', (520, 20))
        result_2 = player._check_collision(Group(level_objects_2))
        ans_2 = {'top_collision': False, 'right': False, 'left': True, 'up': True}

        level_objects_3 = Block('Gamedata/Blocks/grass.png', (520, 520))
        result_3 = player._check_collision(Group(level_objects_3))
        ans_3 = {'top_collision': False, 'right': True, 'left': True, 'up': False}

        self.assertEqual(result_1, ans_1)
        self.assertEqual(result_2, ans_2)
        self.assertEqual(result_3, ans_3)

if __name__ == '__main__':
    unittest.main()
