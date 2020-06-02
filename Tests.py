import unittest
from Synthesizer.synthesizer import *


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.C = Note(name='C', key='a', midi_number=60)
        self.D = Note(name='D', key='s', midi_number=62)
        self.E = Note(name='E', key='d', midi_number=64)
        self.F = Note(name='F', key='f', midi_number=65)
        self.G = Note(name='G', key='g', midi_number=67)
        self.A = Note(name='A', key='h', midi_number=69)
        self.B = Note(name='B', key='j', midi_number=71)
        self.test_notes = Notes(self.C, self.D, self.E, self.F, self.G, self.A, self.B)
        pygame.midi.init()

    def test_getting(self):
        """
        Test for getting attributes by key and by name
        """
        self.assertEqual(self.test_notes['C'], self.C)

    def test_setting(self):
        """
        Test for KeyError raising if we try to change whole Note
        """
        with self.assertRaises(KeyError):
            self.test_notes['C'] = Note(name='Test', key='a', midi_number=0)  # Попытка присвоить новое значение

    def test_key_handling(self):
        with self.subTest('Key pressed'):
            self.test_notes.key_down('C')  # Нажатие
            self.assertTrue(self.test_notes['C'].pressed, self.test_notes['C'].duration != 0)
        with self.subTest('Key released'):
            self.test_notes.key_up('C')  # Отжатие
            self.assertFalse(self.test_notes['C'].pressed)


if __name__ == '__main__':
    unittest.main()
