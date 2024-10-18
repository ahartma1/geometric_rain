import pygame
from geometric_rain.classes.game import Game
from geometric_rain.classes.menu import Menu
from geometric_rain.classes.sound import Sound
from geometric_rain.classes.display import Display
from geometric_rain.classes.scores import Scorekeeper
import cv2
import base64
from flask_socketio import emit



class Engine:

    def __init__(self, game_name: str):
        self.game_choice = None
        self.scorekeeper = Scorekeeper(game_name)
        self.display = Display(self.scorekeeper)
        self.sound = Sound()
        self.menu = Menu(self.display)
        self.game = Game(self.display, self.sound, self.scorekeeper)
        self.loop = self.game
        self.state = 'game'
        self.running = True

    def set_state(self, new_state):
        self.state = new_state
        self.loop = self.game if new_state == 'game' else self.menu

    def run(self):
        while self.running:

            if self.loop.paused:
                self.loop.event_loop()
                self.loop.key_check()
                font = pygame.font.Font(None, 74)
                text = font.render('PAUSED', True, (255, 255, 255))
                self.display.frame.blit(text, (400 - text.get_width() // 2, 300 - text.get_height() // 2))
                pygame.display.flip()

                # Capture the screen and send it to the client
                frame = pygame.surfarray.array3d(self.display.frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                _, buffer = cv2.imencode('.jpg', frame)
                frame_data = base64.b64encode(buffer).decode('utf-8')
                emit('frame', frame_data)
            else:
                content = self.loop.iteration()
                self.display.render_frame(content,
                                          self.game.next_piece,
                                          self.game.pieces)
                
                # Capture the screen and send it to the client
                frame = pygame.surfarray.array3d(self.display.frame)
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                _, buffer = cv2.imencode('.jpg', frame)
                frame_data = base64.b64encode(buffer).decode('utf-8')
                emit('frame', frame_data)
            self.loop.clock.tick(60)

