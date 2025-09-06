import pygame
import sys
import json
import constants as SOKOBAN
from pygame.locals import *
from copy import deepcopy


class Level:
    def __init__(self, level_to_load):
        self.last_structure_state = None
        self.load(level_to_load)

    def load(self, level):
        self.structure = []
        max_width = 0
        with open("assets/levels/level_" + str(level) + ".txt") as level_file:
            rows = level_file.read().split('\n')

            for y in range(len(rows)):
                level_row = []
                if len(rows[y]) > max_width:
                    max_width = len(rows[y])

                for x in range(len(rows[y])):
                    if rows[y][x] == ' ':
                        level_row.append(SOKOBAN.AIR)
                    elif rows[y][x] == 'X':
                        level_row.append(SOKOBAN.WALL)
                    elif rows[y][x] == '*':
                        level_row.append(SOKOBAN.BOX)
                    elif rows[y][x] == '.':
                        level_row.append(SOKOBAN.TARGET)
                    elif rows[y][x] == '@':
                        level_row.append(SOKOBAN.AIR)
                        self.position_player = [x, y]
                self.structure.append(level_row)

        self.width = max_width * SOKOBAN.SPRITESIZE
        self.height = (len(rows) - 1) * SOKOBAN.SPRITESIZE

    def cancel_last_move(self, player, interface):
        if self.last_structure_state:
            self.structure = self.last_structure_state
            player.pos = self.last_player_pos
            interface.colorTxtCancel = SOKOBAN.GREY
            self.last_structure_state = None
        else:
            print("No previous state")

    def render(self, window, textures):
        for y in range(len(self.structure)):
            for x in range(len(self.structure[y])):
                case = self.structure[y][x]
                if case in textures:
                    texture = textures[case]
                else:
                    texture = None

                if texture:
                    window.blit(texture, (x * SOKOBAN.SPRITESIZE, y * SOKOBAN.SPRITESIZE))


class Player:
    def __init__(self, level):
        self.pos = level.position_player
        self.direction = SOKOBAN.DOWN

    def move(self, direction, level, interface):
        x = self.pos[0]
        y = self.pos[1]

        levelHasChanged = False
        previous_level_structure = deepcopy(level.structure)
        previous_player_pos = [x, y]

        if direction == K_LEFT or direction == K_q:
            self.direction = SOKOBAN.LEFT
            if x > 0 and level.structure[y][x - 1] in [SOKOBAN.AIR, SOKOBAN.TARGET]:
                # Player just move on an empty case to the left
                self.pos[0] -= 1
            elif x > 1 and level.structure[y][x - 1] in [SOKOBAN.BOX, SOKOBAN.TARGET_FILLED] and level.structure[y][
                x - 2] in [SOKOBAN.AIR, SOKOBAN.TARGET]:
                # Player is trying to push a box to the left
                levelHasChanged = True
                if level.structure[y][x - 1] == SOKOBAN.TARGET_FILLED:
                    level.structure[y][x - 1] = SOKOBAN.TARGET
                else:
                    level.structure[y][x - 1] = SOKOBAN.AIR

                if level.structure[y][x - 2] == SOKOBAN.TARGET_FILLED:
                    level.structure[y][x - 2] = SOKOBAN.TARGET
                elif level.structure[y][x - 2] == SOKOBAN.TARGET:
                    level.structure[y][x - 2] = SOKOBAN.TARGET_FILLED
                else:
                    level.structure[y][x - 2] = SOKOBAN.BOX

                self.pos[0] -= 1

        if direction == K_RIGHT or direction == K_d:
            self.direction = SOKOBAN.RIGHT
            if level.structure[y][x + 1] in [SOKOBAN.AIR, SOKOBAN.TARGET]:
                self.pos[0] += 1
            elif level.structure[y][x + 1] in [SOKOBAN.BOX, SOKOBAN.TARGET_FILLED] and level.structure[y][x + 2] in [
                SOKOBAN.AIR, SOKOBAN.TARGET]:
                # Player is trying to push a box to the right
                levelHasChanged = True
                if level.structure[y][x + 1] == SOKOBAN.TARGET_FILLED:
                    level.structure[y][x + 1] = SOKOBAN.TARGET
                else:
                    level.structure[y][x + 1] = SOKOBAN.AIR

                if level.structure[y][x + 2] == SOKOBAN.TARGET_FILLED:
                    level.structure[y][x + 2] = SOKOBAN.TARGET
                elif level.structure[y][x + 2] == SOKOBAN.TARGET:
                    level.structure[y][x + 2] = SOKOBAN.TARGET_FILLED
                else:
                    level.structure[y][x + 2] = SOKOBAN.BOX

                self.pos[0] += 1

        if direction == K_UP or direction == K_z:
            self.direction = SOKOBAN.UP
            if y > 0 and level.structure[y - 1][x] in [SOKOBAN.AIR, SOKOBAN.TARGET]:
                self.pos[1] -= 1
            elif y > 1 and level.structure[y - 1][x] in [SOKOBAN.BOX, SOKOBAN.TARGET_FILLED] and level.structure[y - 2][
                x] in [SOKOBAN.AIR, SOKOBAN.TARGET]:
                # Player is trying to push a box to the left
                levelHasChanged = True
                if level.structure[y - 1][x] == SOKOBAN.TARGET_FILLED:
                    level.structure[y - 1][x] = SOKOBAN.TARGET
                else:
                    level.structure[y - 1][x] = SOKOBAN.AIR

                if level.structure[y - 2][x] == SOKOBAN.TARGET_FILLED:
                    level.structure[y - 2][x] = SOKOBAN.TARGET
                elif level.structure[y - 2][x] == SOKOBAN.TARGET:
                    level.structure[y - 2][x] = SOKOBAN.TARGET_FILLED
                else:
                    level.structure[y - 2][x] = SOKOBAN.BOX

                self.pos[1] -= 1

        if direction == K_DOWN or direction == K_s:
            self.direction = SOKOBAN.DOWN
            if level.structure[y + 1][x] in [SOKOBAN.AIR, SOKOBAN.TARGET]:
                self.pos[1] += 1
            elif level.structure[y + 1][x] in [SOKOBAN.BOX, SOKOBAN.TARGET_FILLED] and level.structure[y + 2][x] in [
                SOKOBAN.AIR, SOKOBAN.TARGET]:
                # Player is trying to push a box to the left
                levelHasChanged = True
                if level.structure[y + 1][x] == SOKOBAN.TARGET_FILLED:
                    level.structure[y + 1][x] = SOKOBAN.TARGET
                else:
                    level.structure[y + 1][x] = SOKOBAN.AIR

                if level.structure[y + 2][x] == SOKOBAN.TARGET_FILLED:
                    level.structure[y + 2][x] = SOKOBAN.TARGET
                elif level.structure[y + 2][x] == SOKOBAN.TARGET:
                    level.structure[y + 2][x] = SOKOBAN.TARGET_FILLED
                else:
                    level.structure[y + 2][x] = SOKOBAN.BOX

                self.pos[1] += 1

        if levelHasChanged:
            level.last_structure_state = previous_level_structure
            level.last_player_pos = previous_player_pos
            interface.colorTxtCancel = SOKOBAN.BLACK

    def render(self, window, textures):
        if self.direction == SOKOBAN.DOWN:
            top = 0
        elif self.direction == SOKOBAN.LEFT:
            top = SOKOBAN.SPRITESIZE
        elif self.direction == SOKOBAN.RIGHT:
            top = SOKOBAN.SPRITESIZE * 2
        elif self.direction == SOKOBAN.UP:
            top = SOKOBAN.SPRITESIZE * 3

        areaPlayer = pygame.Rect((0, top), (32, 32))
        window.blit(textures[SOKOBAN.PLAYER], (self.pos[0] * SOKOBAN.SPRITESIZE, self.pos[1] * SOKOBAN.SPRITESIZE),
                    area=areaPlayer)


class Scores:
    def __init__(self, game):
        self.game = game

    def load(self):
        try:
            with open("scores", "r") as data:
                scores = json.load(data)
                self.game.index_level = scores["level"]
            self.game.load_level()
            self.game.start()
        except FileNotFoundError:
            print("No saved data")

    def save(self):
        # Saving score in file only when current level > saved level
        try:
            with open("scores", "r") as data:
                scores = json.load(data)
                saved_level = scores["level"]
        except FileNotFoundError:
            saved_level = 0

        if saved_level < self.game.index_level:
            data = {
                "level": self.game.index_level
            }
            with open("scores", "w") as scores:
                json.dump(data, scores, ensure_ascii=False, indent=4)


class PlayerInterface:
    def __init__(self, player, level):
        self.player = player
        self.level = level
        self.mouse_pos = (-1, -1)
        self.font_menu = pygame.font.Font('assets/fonts/chinese rocks rg.ttf', 20)
        self.txtLevel = "Niveau 1"
        self.colorTxtLevel = SOKOBAN.BLACK
        self.txtCancel = "Annuler le dernier coup"
        self.colorTxtCancel = SOKOBAN.GREY
        self.txtReset = "Recommencer le niveau"
        self.colorTxtReset = SOKOBAN.BLACK
        self.txtBoxHelp = "Caisse la plus proche"
        self.colortxtBoxHelp = SOKOBAN.BLACK
        self.caisseproche = True
        self.soundchoice = 'on'
        self.soundicon = pygame.image.load(f'assets/images/ui/{self.soundchoice}.png').convert_alpha()

    def click(self, pos_click, level, game):
        x = pos_click[0]
        y = pos_click[1]

        # Cancel last move
        if x > self.posTxtCancel[0] and x < self.posTxtCancel[0] + self.txtCancelSurface.get_width() \
                and y > self.posTxtCancel[1] and y < self.posTxtCancel[1] + self.txtCancelSurface.get_height():
            level.cancel_last_move(self.player, self)
            self.colorTxtCancel = SOKOBAN.GREY

        # caisse plus proche
        if x > self.postxtBoxHelp[0] and x < self.postxtBoxHelp[0] + self.txtBoxHelpSurface.get_width() \
                and y > self.postxtBoxHelp[1] and y < self.postxtBoxHelp[1] + self.txtBoxHelpSurface.get_height():
            game.afficherchemin = not game.afficherchemin
            self.colortxtBoxHelp = SOKOBAN.GREY if game.afficherchemin else SOKOBAN.BLACK

        # Reset level
        if x > self.posTxtReset[0] and x < self.posTxtReset[0] + self.txtResetSurface.get_width() \
                and y > self.posTxtReset[1] and y < self.posTxtReset[1] + self.txtResetSurface.get_height():
            game.load_level()

        icon_width, icon_height = self.soundicon.get_size()
        if self.possoundicon[0] < x < self.possoundicon[0] + icon_width and \
                self.possoundicon[1] < y < self.possoundicon[1] + icon_height:
            if self.soundchoice == 'on':
                self.soundchoice = "off"
                game.musicisplaying = False
            else:
                self.soundchoice = "on"
                game.musicisplaying = True
                pygame.mixer.music.unpause()

        self.soundicon = pygame.image.load(f'assets/images/ui/{self.soundchoice}.png').convert_alpha()

    def setTxtColors(self):
        pass

    def render(self, window, level):
        self.txtLevel = "Niveau " + str(level)
        self.txtLevelSurface = self.font_menu.render(self.txtLevel, True, self.colorTxtLevel, SOKOBAN.WHITE)
        window.blit(self.txtLevelSurface, (10, 10))

        self.txtCancelSurface = self.font_menu.render(self.txtCancel, True, self.colorTxtCancel, SOKOBAN.WHITE)
        self.posTxtCancel = (SOKOBAN.WINDOW_WIDTH - self.txtCancelSurface.get_width() - 10, 10)
        window.blit(self.txtCancelSurface, self.posTxtCancel)

        self.txtResetSurface = self.font_menu.render(self.txtReset, True, self.colorTxtReset, SOKOBAN.WHITE)
        self.posTxtReset = ((SOKOBAN.WINDOW_WIDTH / 2) - (self.txtResetSurface.get_width() / 2), 10)
        window.blit(self.txtResetSurface, self.posTxtReset)

        self.txtBoxHelpSurface = self.font_menu.render(self.txtBoxHelp, True, self.colortxtBoxHelp, SOKOBAN.WHITE)
        self.postxtBoxHelp = ((SOKOBAN.WINDOW_WIDTH - self.txtBoxHelpSurface.get_width() - 10), 50)
        window.blit(self.txtBoxHelpSurface, self.postxtBoxHelp)

        self.possoundicon = (15, 50)
        window.blit(self.soundicon, self.possoundicon)


class File:
    def __init__(self):
        self.elements = []

    def enfile(self, element):
        self.elements.append(element)

    def defile(self):
        if not self.est_vide():
            return self.elements.pop(0)
        return None

    def est_vide(self):
        return len(self.elements) == 0


class Graphe:
    def __init__(self, niveau):
        self.niveau = niveau
        self.noeuds = {}
        self.construire_graphe()

    def construire_graphe(self):
        for y in range(len(self.niveau.structure)):
            for x in range(len(self.niveau.structure[y])):
                if self.niveau.structure[y][x] != SOKOBAN.WALL:
                    self.noeuds[(x, y)] = []
                    print(x, y)
                    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                        nx, ny = x + dx, y + dy
                        if 0 <= ny < len(self.niveau.structure) and 0 <= nx < len(self.niveau.structure[ny]):
                            if self.niveau.structure[ny][nx] != SOKOBAN.WALL:
                                self.noeuds[(x, y)].append((nx, ny))

    def plus_court_chemin(self, depart, arrivee):
        file = File()
        file.enfile((depart, [depart]))
        visites = {}

        while not file.est_vide():
            position, chemin = file.defile()
            if position == arrivee:
                return chemin

            if position not in visites:  # case visité
                visites[position] = True
                for voisin in self.noeuds[position]:  # visité case accesible
                    if voisin not in visites:
                        file.enfile((voisin, chemin + [voisin]))

        return None


class Game:
    def __init__(self, window):
        self.image = pygame.image.load(f'assets/images/niveau/{SOKOBAN.BIOME}.png').convert_alpha()
        self.window = window
        self.load_textures()
        self.player = None
        self.index_level = 1
        self.load_level()
        self.play = True
        self.scores = Scores(self)
        self.player_interface = PlayerInterface(self.player, self.level)
        self.afficherchemin = False

        self.chemin = []
        self.musicisplaying = True
        pygame.mixer.init()
        pygame.mixer.music.load(SOKOBAN.MUSIC)
        pygame.mixer.music.play(-1)

    def load_textures(self):
        self.textures = {
            SOKOBAN.WALL: pygame.image.load('assets/images/wall.png').convert_alpha(),
            SOKOBAN.BOX: pygame.image.load('assets/images/box.png').convert_alpha(),
            SOKOBAN.TARGET: pygame.image.load('assets/images/target.png').convert_alpha(),
            SOKOBAN.TARGET_FILLED: pygame.image.load('assets/images/valid_box.png').convert_alpha(),
            SOKOBAN.PLAYER: pygame.image.load('assets/images/player_sprites.png').convert_alpha(),

        }

    def load_level(self):
        self.level = Level(self.index_level)
        self.board = pygame.Surface((self.level.width, self.level.height))
        if self.player:
            self.player.pos = self.level.position_player
            self.player_interface.level = self.level
        else:
            self.player = Player(self.level)
        self.graphe = Graphe(self.level)

    def start(self):
        while self.play:
            if not self.musicisplaying:
                pygame.mixer.music.pause()
            for event in pygame.event.get():
                self.process_event(event)
                self.update_screen()

    def process_event(self, event):
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                # Quit game
                self.play = False
            if event.key in [K_UP, K_DOWN, K_LEFT, K_RIGHT, K_z, K_s, K_q, K_d]:
                # Move player
                self.player.move(event.key, self.level, self.player_interface)
                if self.has_win():
                    self.index_level += 1
                    self.scores.save()
                    self.load_level()
            if event.key == K_r:
                # Restart current level
                self.load_level()
            if event.key == K_l:
                # Cancel last move
                self.level.cancel_last_move(self.player, self.player_interface)
        if event.type == MOUSEBUTTONUP:
            self.player_interface.click(event.pos, self.level, self)
        if event.type == MOUSEMOTION:
            self.player_interface.mouse_pos = event.pos

    def chercher_chemin(self):
        joueur = tuple(self.player.pos)
        caisses = []

        for y in range(len(self.level.structure)):
            for x in range(len(self.level.structure[y])):
                if self.level.structure[y][x] == SOKOBAN.BOX:
                    caisses.append((x, y))

        if caisses:
            chemin_le_plus_court = None
            for caisse in caisses:
                chemin = self.graphe.plus_court_chemin(joueur, caisse)
                if chemin and (chemin_le_plus_court is None or len(chemin) < len(chemin_le_plus_court)):
                    chemin_le_plus_court = chemin
                if chemin_le_plus_court:
                    self.chemin = chemin_le_plus_court

    def rendu_chemin(self):
        if self.afficherchemin:
            pox_x_board = (SOKOBAN.WINDOW_WIDTH / 2) - (self.board.get_width() / 2)
            pos_y_board = (SOKOBAN.WINDOW_HEIGHT / 2) - (self.board.get_height() / 2)
            self.chercher_chemin()
            for (x, y) in self.chemin:
                pygame.draw.circle(self.window, (238, 130, 238),
                                   (pox_x_board + x * SOKOBAN.SPRITESIZE + SOKOBAN.SPRITESIZE // 2,
                                    pos_y_board + y * SOKOBAN.SPRITESIZE + SOKOBAN.SPRITESIZE // 2),
                                   SOKOBAN.SPRITESIZE // 4)

    def update_screen(self):
        self.board.blit(self.image, (0, 0))
        self.window.blit(self.image, (0, 0))
        self.level.render(self.board, self.textures)
        self.player.render(self.board, self.textures)
        pox_x_board = (SOKOBAN.WINDOW_WIDTH / 2) - (self.board.get_width() / 2)
        pos_y_board = (SOKOBAN.WINDOW_HEIGHT / 2) - (self.board.get_height() / 2)
        self.window.blit(self.board, (pox_x_board, pos_y_board))
        self.rendu_chemin()

        self.player_interface.render(self.window, self.index_level)

        pygame.display.flip()

    def has_win(self):
        nb_missing_target = 0
        for y in range(len(self.level.structure)):
            for x in range(len(self.level.structure[y])):
                if self.level.structure[y][x] == SOKOBAN.TARGET:
                    nb_missing_target += 1

        return nb_missing_target == 0


class Menu:
    def __init__(self):
        self.image = pygame.image.load('assets/images/menu/menu.png').convert_alpha()
        self.new_game_txt = "Nouvelle partie"
        self.load_game_txt = "Continuer"
        self.quit_game_txt = "Quitter"
        self.font = pygame.font.Font('assets/fonts/chinese rocks rg.ttf', 30)
        self.biome_menu_image = pygame.image.load(f'assets/images/menu/{SOKOBAN.BIOME}.png').convert_alpha()


    def click(self, click_pos, window):
        x = click_pos[0]
        y = click_pos[1]

        if x > self.new_game_txt_position[0] and x < self.new_game_txt_position[0] + self.new_game_txt_surface.get_width() \
        and y > 700 and y < 700 + self.new_game_txt_surface.get_height():
            sokoban = Game(window)
            sokoban.start()

        elif x > self.load_game_txt_position[0] and x < self.load_game_txt_position[0] + self.load_game_txt_surface.get_width() \
        and y > 700 and y < 700 + self.load_game_txt_surface.get_height():
            sokoban = Game(window)
            sokoban.scores.load()
        elif x > self.quit_game_txt_position[0] and x < self.quit_game_txt_position[0] + self.quit_game_txt_surface.get_width() \
        and y > 700 and y < 700 + self.quit_game_txt_surface.get_height():
            return False

        return True

    def render(self, window):
        window.blit(self.image, (0,0))

        self.new_game_txt_surface = self.font.render(self.new_game_txt, True, SOKOBAN.BLACK, SOKOBAN.WHITE)
        self.new_game_txt_position = ((SOKOBAN.WINDOW_WIDTH / 6) - (self.new_game_txt_surface.get_width() / 2), 700)
        window.blit(self.new_game_txt_surface, self.new_game_txt_position)

        self.load_game_txt_surface = self.font.render(self.load_game_txt, True, SOKOBAN.BLACK, SOKOBAN.WHITE)
        self.load_game_txt_position = ((SOKOBAN.WINDOW_WIDTH / 1.88) - (self.load_game_txt_surface.get_width() / 2), 700)
        window.blit(self.load_game_txt_surface, self.load_game_txt_position)

        self.quit_game_txt_surface = self.font.render(self.quit_game_txt, True, SOKOBAN.BLACK, SOKOBAN.WHITE)
        self.quit_game_txt_position = ((SOKOBAN.WINDOW_WIDTH / 1.10) - (self.quit_game_txt_surface.get_width() / 2), 700)
        window.blit(self.quit_game_txt_surface, self.quit_game_txt_position)

        window.blit(self.biome_menu_image, (0,350))


def main():
    pygame.init()
    pygame.key.set_repeat(100, 100)
    pygame.display.set_caption("Sokoban Game")
    window = pygame.display.set_mode((SOKOBAN.WINDOW_WIDTH, SOKOBAN.WINDOW_HEIGHT))
    menu = Menu()


    run = True
    while run:
        for event in pygame.event.get():
            if event.type == QUIT:
                run = False
            if event.type == KEYDOWN:
                if event.key == K_j:
                    sokoban = Game(window)
                    sokoban.start()
                elif event.key == K_c:
                    sokoban = Game(window)
                    sokoban.scores.load()
                elif event.key == K_ESCAPE:
                    run = False
            if event.type == MOUSEBUTTONUP:
                run = menu.click(event.pos, window)
        pygame.draw.rect(window, SOKOBAN.WHITE, (0,0,SOKOBAN.WINDOW_WIDTH,SOKOBAN.WINDOW_HEIGHT))
        menu.render(window)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
