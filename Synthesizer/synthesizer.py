"""Синтезатор."""
# Импорты сторонних библиотек

import pygame.midi


class Synthesizer:
    """Класс пианино."""

    def __init__(self):
        """Конструктор класса."""
        # Подготовка окна
        self.window_size = (320, 240)
        self._screen = pygame.display.set_mode(self.window_size)

        # Подготовка миди плеера
        pygame.midi.init()
        self._player = pygame.midi.Output(
            device_id=pygame.midi.get_default_output_id()
        )
        # Установка инструмента
        self._player.set_instrument(
            instrument_id=1
        )
        self._data = []

        # Настройка состояний клавиш
        self._key_state = {
            'a': {
                'keyCode': ord('a'),
                'note': 'C',
                'midiNumber': 60,
                'pressed': False,
                'duration': 0
            },
            's': {
                'keyCode': ord('s'),
                'note': 'D',
                'midiNumber': 62,
                'pressed': False,
                'duration': 0
            },
            'd': {
                'keyCode': ord('d'),
                'note': 'E',
                'midiNumber': 64,
                'pressed': False,
                'duration': 0
            },
            'f': {
                'keyCode': ord('f'),
                'note': 'F',
                'midiNumber': 65,
                'pressed': False,
                'duration': 0
            },
            'g': {
                'keyCode': ord('g'),
                'note': 'G',
                'midiNumber': 67,
                'pressed': False,
                'duration': 0
            },
            'h': {
                'keyCode': ord('h'),
                'note': 'A',
                'midiNumber': 69,
                'pressed': False,
                'duration': 0
            },
            'j': {
                'keyCode': ord('j'),
                'note': 'B',
                'midiNumber': 71,
                'pressed': False,
                'duration': 0
            }
        }
        self.running = False

    def start(self):
        """Старт синтезатора."""
        self.running = True
        self._loop()
        self.quit()
        return None

    def quit(self):
        """Отключение синтезатора."""
        self.running = False

        self._player.close()

        pygame.quit()
        return None

    def _loop(self):
        while self.running:
            for event in pygame.event.get():
                # Обработка выхода
                if event.type == pygame.QUIT:
                    self.running = False

                # Обработка нажатий и отпускания
                if event.type == pygame.KEYDOWN:
                    self._handle_key_down(event)
                elif event.type == pygame.KEYUP:
                    self._handle_key_up(event)

                # Обработка музыки
            self._play_music()

        return None

    def _handle_key_down(self, event):
        for key in self._key_state:
            if event.dict['unicode'] == key:
                self._key_state[key]['pressed'] = True
                self._key_state[key]['duration'] = pygame.midi.time()

        return None

    def _handle_key_up(self, event):
        for key in self._key_state:
            if event.key == self._key_state[key]['keyCode']:
                self._key_state[key]['pressed'] = False

                self._key_state[key]['duration'] = (
                    pygame.midi.time() - self._key_state[key]['duration'])

                if self._key_state[key]['duration'] > 127:
                    self._key_state[key]['duration'] = 127
        return None

    def _play_music(self):
        music_playable = True

        # for key in self._key_state.values():
        # if key['playable'] == True:
        #     music_playable = False
        # Формирование пакета для воспроизведения
        for key in self._key_state.values():
            if not key['pressed'] and key['duration'] != 0:
                self._data.append(
                    (
                        (
                            0x90,
                            key['midiNumber'],
                            64
                            # key['duration']
                        ),
                        0
                        # pygame.midi.time()
                    )
                )

        self._player.write(self._data)
        self._data = []

        for key in self._key_state.values():
            key['duration'] = 0
            key['pressed'] = False
        return None


if __name__ == '__main__':

    piano = Synthesizer()
    piano.start()
