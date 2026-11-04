# ==============================
# ตัวเกมหลัก: หน้าต่าง ลูปหลัก และการสลับหน้าจอ
# ==============================
import pygame
import pygame.freetype
from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, FPS, TITLE, FONT_FILE,
                      DIFFICULTIES, LEVELS_DIR, HISTORY_FILE)
from theme import LightTheme, DarkTheme
from level_reader import LevelReader
from leaderboard import Leaderboard
from screens import MenuScreen


class Game:
    """เกมหลัก: เปิดหน้าต่าง วนลูป และสลับหน้าจอ"""
    # [Aggregation] เกมสร้างธีม ตัวอ่านด่าน และตารางอันดับไว้ชุดเดียว
    #               หน้าจอต่าง ๆ แค่อ้างถึง (หน้าจอถูกสร้างใหม่ไปเรื่อย ๆ แต่ของพวกนี้อยู่ตลอดเกม)

    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(Game.__make_icon())
        self.window = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.fonts = {
            "title": Game.__make_font(84),
            "huge": Game.__make_font(52),
            "big": Game.__make_font(30),
            "digit": Game.__make_font(36, pad=False),
            "body": Game.__make_font(22),
            "small": Game.__make_font(16),
        }
        self.light_theme = LightTheme()
        self.dark_theme = DarkTheme()
        self.theme = self.light_theme                  # เริ่มที่ธีมสว่างทุกครั้ง
        self.level_reader = LevelReader(LEVELS_DIR, DIFFICULTIES)
        self.leaderboard = Leaderboard(HISTORY_FILE)
        self.current_screen = MenuScreen(self)
        self.running = True

    @staticmethod
    def __make_font(size, pad=True):
        """สร้างฟอนต์ (ใช้ pygame.freetype เพราะ pygame.font เว้นช่องไฟเพี้ยน เช่น "Backs pace")
        pad=True: ข้อความทุกอันสูงเท่ากัน วางเรียงแนวเดียวกันได้
        pad=False: กล่องพอดีตัวอักษร ใช้กับตัวเลขในช่องให้อยู่กลางพอดี"""
        font = pygame.freetype.Font(FONT_FILE, size)
        font.pad = pad
        return font

    @staticmethod
    def __make_icon():
        """ไอคอนหน้าต่าง: ตาราง 3x3 เล็ก ๆ"""
        icon = pygame.Surface((32, 32))
        icon.fill((28, 30, 36))
        for row in range(3):
            for col in range(3):
                color = (250, 250, 252)
                if row == col:
                    color = (170, 235, 175)
                pygame.draw.rect(icon, color, (2 + col * 10, 2 + row * 10, 8, 8))
        return icon

    def change_screen(self, new_screen):
        self.current_screen = new_screen

    def toggle_theme(self):
        if self.theme is self.light_theme:
            self.theme = self.dark_theme
        else:
            self.theme = self.light_theme

    def quit(self):
        self.running = False

    def run(self):
        """ลูปหลัก: รับ event -> อัปเดต -> วาด (60 ครั้งต่อวินาที)"""
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                else:
                    self.current_screen.handle_event(event)   # [Polymorphism] หน้าจอไหนก็รับ event ได้
            self.current_screen.update()
            self.current_screen.draw(self.window)
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()
