# ==============================
# หน้าจอทั้งหมดของเกม: เมนู / เล่น / แพ้ / ชนะ
# ==============================
import pygame
from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, BOARD_X, BOARD_Y, BOARD_SIZE, PANEL_X, PANEL_WIDTH,
                      MAX_LIVES, MAX_HINTS, DIFFICULTIES, HINT_PENALTY, NAME_MAX_LENGTH, DEFAULT_NAME,
                      TOP_COUNT, DIGIT_KEYS, DIGIT_SCANCODES, CLEAR_KEYS, CLEAR_SCANCODES, ENTER_KEYS)
from board import Board
from game_timer import GameTimer
from leaderboard import Record
from widgets import Label, Button, NameBox


class Screen:
    """คลาสแม่ของทุกหน้าจอ"""
    # [Abstraction] บอกแค่ว่าทุกหน้าจอต้อง รับ event / อัปเดต / วาด ได้
    #               รายละเอียดจริงให้คลาสลูกเขียนเอง

    def __init__(self, game):
        self.game = game                # [Aggregation] อ้างถึงเกมหลัก (หน้าจอไม่ได้เป็นเจ้าของเกม)

    def handle_event(self, event):
        pass

    def update(self):
        pass

    def draw(self, screen):
        pass

    def _draw_card(self, screen, theme, rect):
        """ม่านโปร่งแสงทับทั้งจอ + การ์ดตรงกลาง (คลาสลูกเรียกใช้ได้)"""
        shade = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        shade.fill(theme.overlay)
        screen.blit(shade, (0, 0))
        pygame.draw.rect(screen, theme.card, rect, border_radius=14)
        pygame.draw.rect(screen, theme.card_border, rect, 2, border_radius=14)

    def __str__(self):
        return type(self).__name__


class MenuScreen(Screen):
    """หน้าเมนู: เลือกความยาก สลับธีม หรือออกจากเกม"""
    # [Inheritance] สืบทอดจาก Screen

    def __init__(self, game):
        super().__init__(game)
        fonts = game.fonts
        cx = SCREEN_WIDTH // 2
        self.title = Label("SUDOKU", fonts["title"], (cx, 112), "center")
        self.subtitle = Label("Choose a difficulty", fonts["body"], (cx, 180), "center", "muted")
        self.level_buttons = {}
        for index, difficulty in enumerate(DIFFICULTIES):
            button = Button(difficulty, fonts["big"], (cx - 130, 216 + index * 66, 260, 52))
            if not game.level_reader.has_levels(difficulty):
                button.enabled = False                      # ไม่มีด่านที่ใช้ได้
                button.set_text(f"{difficulty} (no level)")
            self.level_buttons[difficulty] = button
        self.theme_button = Button("", fonts["body"], (cx - 100, 440, 200, 42))
        self.quit_button = Button("Quit", fonts["body"], (cx - 100, 494, 200, 42))
        penalties = []
        for difficulty in DIFFICULTIES:
            penalties.append(f"{difficulty} {GameTimer.format_added(HINT_PENALTY[difficulty])}")
        self.footer = Label("Each hint adds time:   " + "  ·  ".join(penalties),
                            fonts["small"], (cx, 568), "center", "muted")

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:      # คลิกซ้ายเท่านั้น
            for difficulty in DIFFICULTIES:
                if self.level_buttons[difficulty].is_clicked(event.pos):
                    level = self.game.level_reader.random_level(difficulty)
                    self.game.change_screen(PlayScreen(self.game, level))
                    return
            if self.theme_button.is_clicked(event.pos):
                self.game.toggle_theme()
            elif self.quit_button.is_clicked(event.pos):
                self.game.quit()

    def draw(self, screen):
        theme = self.game.theme
        screen.fill(theme.background)
        self.theme_button.set_text(theme.switch_label())    # [Polymorphism] ธีมไหนก็ตอบเองว่าปุ่มต้องเขียนอะไร
        items = [self.title, self.subtitle, self.theme_button, self.quit_button, self.footer]
        items += list(self.level_buttons.values())
        for item in items:
            item.draw(screen, theme)                         # [Polymorphism] Label กับ Button ต่างมี draw() ของตัวเอง


class PlayScreen(Screen):
    """หน้าเล่นเกม: กระดานด้านซ้าย แถบข้อมูลด้านขวา"""
    # [Inheritance] สืบทอดจาก Screen

    def __init__(self, game, level):
        super().__init__(game)
        self.level = level                          # [Aggregation] ด่านเป็นของ LevelReader หน้าเล่นแค่อ้างถึง
        self.leaderboard = game.leaderboard         # [Aggregation] ตารางอันดับใช้ร่วมกันทั้งเกม
        self.board = Board(level.puzzle, level.key) # [Composition] หน้าเล่นสร้างกระดานเอง
        self.timer = GameTimer()                    # [Composition] และนาฬิกาเอง
        self.__lives = MAX_LIVES                    # [Encapsulation] private
        self.__hints_left = MAX_HINTS
        self.__penalty = HINT_PENALTY.get(level.difficulty, 60)   # วินาทีที่บวกต่อตัวช่วย 1 ครั้ง
        self.__penalty_shown_until = 0              # เวลาที่ข้อความ "+1:00" หายไป
        self.__hint_cell = None                     # ช่องที่เพิ่งเปิดด้วยตัวช่วย
        self.__hint_cell_until = 0                  # เวลาที่กรอบกะพริบหายไป

        # แถบข้อมูลด้านขวา
        fonts = game.fonts
        x = PANEL_X
        right = PANEL_X + PANEL_WIDTH
        self.difficulty_label = Label(level.difficulty, fonts["big"], (x, BOARD_Y))
        self.level_label = Label(level.name, fonts["small"], (x, BOARD_Y + 38), color_name="muted")
        self.time_title = Label("Time", fonts["body"], (x, BOARD_Y + 76), color_name="muted")
        self.time_value = Label("", fonts["body"], (x + 80, BOARD_Y + 76))
        self.penalty_label = Label("", fonts["body"], (right, BOARD_Y + 76), "topright", "penalty")
        self.lives_title = Label("Lives", fonts["body"], (x, BOARD_Y + 108), color_name="muted")
        self.lives_value = Label("", fonts["body"], (x + 80, BOARD_Y + 108))
        self.hint_button = Button("", fonts["body"], (x, BOARD_Y + 150, PANEL_WIDTH, 42))
        self.theme_button = Button("", fonts["body"], (x, BOARD_Y + 202, PANEL_WIDTH, 42))
        self.menu_button = Button("Menu", fonts["body"], (x, BOARD_Y + 254, PANEL_WIDTH, 42))
        self.top_title = Label(f"Top {TOP_COUNT}", fonts["body"], (x, BOARD_Y + 326))
        self.top_names = []
        self.top_times = []
        for index in range(TOP_COUNT):
            y = BOARD_Y + 360 + index * 30
            self.top_names.append(Label("", fonts["body"], (x, y)))
            self.top_times.append(Label("", fonts["body"], (right, y), "topright"))
        self.help_label = Label("Click a cell   ·   1-9: draft   ·   Enter: check   ·   Backspace/Delete: erase",
                                fonts["small"], (BOARD_X, BOARD_Y + BOARD_SIZE + 16), color_name="muted")

    # ----- [Encapsulation] อ่านค่าผ่านเมธอด -----
    def get_lives(self):
        return self.__lives

    def get_hints_left(self):
        return self.__hints_left

    def get_hints_used(self):
        return MAX_HINTS - self.__hints_left

    def get_penalty(self):
        return self.__penalty

    # ----- รับคำสั่งจากผู้เล่น -----
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:      # คลิกซ้ายเท่านั้น
            if self.hint_button.is_clicked(event.pos):
                self.__use_hint()
            elif self.theme_button.is_clicked(event.pos):
                self.game.toggle_theme()
            elif self.menu_button.is_clicked(event.pos):
                self.game.change_screen(MenuScreen(self.game))           # ออกกลางเกม: ไม่บันทึก
            else:
                self.board.select_at(event.pos)
        elif event.type == pygame.KEYDOWN:
            self.__handle_key(event)

    def __handle_key(self, event):
        scancode = getattr(event, "scancode", None)
        if event.key in ENTER_KEYS:
            self.__submit()
        elif event.key in DIGIT_KEYS:
            self.board.input_digit(DIGIT_KEYS[event.key])
        elif scancode in DIGIT_SCANCODES:
            self.board.input_digit(DIGIT_SCANCODES[scancode])    # คีย์บอร์ดภาษาไทย: ดูจากตำแหน่งปุ่มแทน
        elif event.key in CLEAR_KEYS or scancode in CLEAR_SCANCODES:
            self.board.input_digit(0)

    def __submit(self):
        result = self.board.submit_selected()
        if result is True:
            self.__check_win()
        elif result is False:
            self.__lose_life()

    def __lose_life(self):
        self.__lives -= 1
        if self.__lives <= 0:
            self.timer.stop()
            self.game.change_screen(GameOverScreen(self.game, self))

    def __use_hint(self):
        if self.__hints_left <= 0:
            return
        cell = self.board.reveal_random()
        if cell is None:
            return
        self.__hints_left -= 1
        self.timer.add_penalty(self.__penalty)
        now = pygame.time.get_ticks()
        self.__penalty_shown_until = now + 1500
        self.__hint_cell = cell
        self.__hint_cell_until = now + 1200
        self.__check_win()

    def __check_win(self):
        if self.board.is_solved():
            self.timer.stop()                   # หยุดเวลาที่ช่องสุดท้าย (ตอนพิมพ์ชื่อไม่นับเวลา)
            self.board.clear_selection()
            self.game.change_screen(WinScreen(self.game, self))

    # ----- อัปเดตและวาด -----
    def update(self):
        if not self.timer.is_started():
            self.timer.start()                  # เริ่มจับเวลาเมื่อโจทย์ขึ้นจอครั้งแรก

    def draw(self, screen):
        theme = self.game.theme
        screen.fill(theme.background)
        self.board.draw(screen, theme, self.game.fonts["digit"])
        if self.__hint_cell is not None and pygame.time.get_ticks() < self.__hint_cell_until:
            pygame.draw.rect(screen, theme.hint_frame, self.__hint_cell.sensor, 4)
        self.__draw_panel(screen, theme)
        self.help_label.draw(screen, theme)

    def __draw_panel(self, screen, theme):
        # อัปเดตข้อความตามสถานะล่าสุด
        self.time_value.set_text(str(self.timer))                # ใช้ __str__ ของ GameTimer
        self.lives_value.set_text(f"{self.__lives} / {MAX_LIVES}")
        if self.__hints_left > 0:
            self.hint_button.set_text(f"Hint ({self.__hints_left} left)")
        else:
            self.hint_button.set_text("No hints left")
            self.hint_button.enabled = False
        self.theme_button.set_text(theme.switch_label())         # [Polymorphism]
        if pygame.time.get_ticks() < self.__penalty_shown_until:
            self.penalty_label.set_text(GameTimer.format_added(self.__penalty))
        else:
            self.penalty_label.set_text("")
        top = self.leaderboard.top(self.level.difficulty, self.level.name, TOP_COUNT)
        for index in range(TOP_COUNT):
            if index < len(top):
                self.top_names[index].set_text(f"{index + 1}. {top[index].player_name}")
                self.top_times[index].set_text(GameTimer.format(top[index].seconds))
            else:
                self.top_names[index].set_text(f"{index + 1}. ---")
                self.top_times[index].set_text("")
        # วาดทุกชิ้น
        items = [self.difficulty_label, self.level_label, self.time_title, self.time_value,
                 self.penalty_label, self.lives_title, self.lives_value,
                 self.hint_button, self.theme_button, self.menu_button, self.top_title]
        items += self.top_names + self.top_times
        for item in items:
            item.draw(screen, theme)            # [Polymorphism] Label กับ Button ต่างมี draw() ของตัวเอง


class GameOverScreen(Screen):
    """หน้าแพ้ (ผิดครบ 3 ครั้ง): เล่นด่านเดิมใหม่ หรือกลับเมนู"""
    # [Inheritance] สืบทอดจาก Screen

    def __init__(self, game, play_screen):
        super().__init__(game)
        self.play_screen = play_screen          # [Aggregation] หน้าเล่นที่จบแล้ว ใช้วาดเป็นพื้นหลัง
        fonts = game.fonts
        cx = SCREEN_WIDTH // 2
        self.title = Label("GAME OVER", fonts["huge"], (cx, 228), "center", "danger")
        self.message = Label(f"You made {MAX_LIVES} mistakes.", fonts["body"], (cx, 280), "center")
        self.retry_button = Button("Retry", fonts["body"], (cx - 150, 322, 140, 46))
        self.menu_button = Button("Menu", fonts["body"], (cx + 10, 322, 140, 46))

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.retry_button.is_clicked(event.pos):
                # ด่านเดิม เริ่มใหม่หมด: ชีวิต ตัวช่วย และเวลา
                self.game.change_screen(PlayScreen(self.game, self.play_screen.level))
            elif self.menu_button.is_clicked(event.pos):
                self.game.change_screen(MenuScreen(self.game))

    def draw(self, screen):
        theme = self.game.theme
        self.play_screen.draw(screen)
        self._draw_card(screen, theme, pygame.Rect(210, 170, 380, 230))
        for item in [self.title, self.message, self.retry_button, self.menu_button]:
            item.draw(screen, theme)


class WinScreen(Screen):
    """หน้าชนะ: พิมพ์ชื่อ -> บันทึก -> ดูอันดับ"""
    # [Inheritance] สืบทอดจาก Screen

    def __init__(self, game, play_screen):
        super().__init__(game)
        self.play_screen = play_screen          # [Aggregation] หน้าเล่นที่จบแล้ว ใช้วาดเป็นพื้นหลัง
        self.level = play_screen.level
        self.seconds = play_screen.timer.get_seconds()
        self.__record = None                    # ผลที่บันทึกแล้ว (None = ยังไม่ได้บันทึก)
        self.__warning_until = 0                # เวลาที่ข้อความเตือนหายไป
        fonts = game.fonts
        cx = SCREEN_WIDTH // 2

        # ----- ช่วงพิมพ์ชื่อ -----
        self.title = Label("CLEARED!", fonts["huge"], (cx, 160), "center", "success")
        self.time_label = Label(f"Time {GameTimer.format(self.seconds)}", fonts["big"], (cx, 210), "center")
        hints_used = play_screen.get_hints_used()
        note = ""
        if hints_used == 1:
            note = f"includes {GameTimer.format_added(play_screen.get_penalty())} from 1 hint"
        elif hints_used > 1:
            note = f"includes {GameTimer.format_added(hints_used * play_screen.get_penalty())} from {hints_used} hints"
        self.note_label = Label(note, fonts["small"], (cx, 240), "center", "muted")
        self.prompt = Label("Enter your name", fonts["body"], (cx, 278), "center")
        self.name_box = NameBox(fonts["big"], (cx - 150, 296, 300, 48), NAME_MAX_LENGTH)
        self.rule_label = Label(f"English letters only (A-Z, a-z), up to {NAME_MAX_LENGTH}",
                                fonts["small"], (cx, 362), "center", "muted")
        self.warning_label = Label("", fonts["small"], (cx, 386), "center", "danger")
        self.save_button = Button("Save", fonts["body"], (cx - 80, 412, 160, 46))

        # ----- หลังบันทึก -----
        self.saved_title = Label("Saved!", fonts["huge"], (cx, 160), "center", "success")
        self.rank_label = Label("", fonts["body"], (cx, 208), "center")
        self.top_header = Label(f"Top {TOP_COUNT}   ·   {self.level.difficulty}   ·   {self.level.name}",
                                fonts["small"], (cx, 246), "center", "muted")
        self.row_tops = []                      # ตำแหน่ง y ของแต่ละแถว
        self.top_names = []
        self.top_times = []
        for index in range(TOP_COUNT):
            y = 272 + index * 36
            self.row_tops.append(y)
            self.top_names.append(Label("", fonts["body"], (cx - 130, y)))
            self.top_times.append(Label("", fonts["body"], (cx + 130, y), "topright"))
        self.again_button = Button("Play again", fonts["body"], (cx - 160, 412, 150, 46))
        self.menu_button = Button("Menu", fonts["body"], (cx + 10, 412, 150, 46))

    def handle_event(self, event):
        if self.__record is None:
            self.__handle_name_input(event)
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.again_button.is_clicked(event.pos):
                self.game.change_screen(PlayScreen(self.game, self.level))   # เล่นด่านเดิมอีกรอบ
            elif self.menu_button.is_clicked(event.pos):
                self.game.change_screen(MenuScreen(self.game))

    def __handle_name_input(self, event):
        if event.type == pygame.TEXTINPUT:                 # ตัวอักษรที่พิมพ์ (ตามภาษาของคีย์บอร์ด)
            warning = self.name_box.add_text(event.text)
            if warning != "":
                self.warning_label.set_text(warning)
                self.__warning_until = pygame.time.get_ticks() + 2500
        elif event.type == pygame.KEYDOWN:
            if event.key in ENTER_KEYS:
                self.__save()
            elif event.key == pygame.K_BACKSPACE:
                self.name_box.remove_last()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.save_button.is_clicked(event.pos):
                self.__save()

    def __save(self):
        name = self.name_box.get_text()
        if name == "":
            name = DEFAULT_NAME
        self.__record = Record(self.level.difficulty, self.level.name, name, self.seconds)
        self.game.leaderboard.add(self.__record)
        rank = self.game.leaderboard.rank_of(self.__record)
        if rank <= TOP_COUNT:
            self.rank_label.set_text(f"You placed #{rank}!")
        else:
            self.rank_label.set_text(f"You placed #{rank} (not in the top {TOP_COUNT})")

    def draw(self, screen):
        theme = self.game.theme
        self.play_screen.draw(screen)
        self._draw_card(screen, theme, pygame.Rect(170, 115, 460, 370))
        if self.__record is None:
            self.__draw_name_entry(screen, theme)
        else:
            self.__draw_ranking(screen, theme)

    def __draw_name_entry(self, screen, theme):
        if pygame.time.get_ticks() > self.__warning_until:
            self.warning_label.set_text("")
        for item in [self.title, self.time_label, self.note_label, self.prompt,
                     self.name_box, self.rule_label, self.warning_label, self.save_button]:
            item.draw(screen, theme)

    def __draw_ranking(self, screen, theme):
        top = self.game.leaderboard.top(self.level.difficulty, self.level.name, TOP_COUNT)
        cx = SCREEN_WIDTH // 2
        for index in range(TOP_COUNT):
            if index < len(top):
                if top[index] is self.__record:            # เน้นแถวของเรา
                    pygame.draw.rect(screen, theme.highlight,
                                     (cx - 142, self.row_tops[index] - 6, 284, 34), border_radius=6)
                self.top_names[index].set_text(f"{index + 1}. {top[index].player_name}")
                self.top_times[index].set_text(GameTimer.format(top[index].seconds))
            else:
                self.top_names[index].set_text(f"{index + 1}. ---")
                self.top_times[index].set_text("")
        items = [self.saved_title, self.rank_label, self.top_header, self.again_button, self.menu_button]
        items += self.top_names + self.top_times
        for item in items:
            item.draw(screen, theme)
