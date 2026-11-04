# ==============================
# ค่าตั้งต้นของเกม (อยากปรับตัวเลขไหน แก้ที่ไฟล์นี้ที่เดียว)
# ==============================
import os
import pygame

# ---------- หน้าต่างเกม ----------
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
TITLE = "Sudoku"
FONT_FILE = None                 # None = ฟอนต์ freesansbold ที่ติดมากับ pygame

# ---------- ตาราง ----------
# ช่องละ 50 px, เส้นบาง 3 px, เส้นหนา (ขอบนอกและขอบกล่อง 3x3) 6 px
BOARD_X = 20                     # มุมซ้ายบนของตาราง
BOARD_Y = 54
CELL_SIZE = 50
THIN_LINE = 3
THICK_LINE = 6
BOARD_SIZE = 9 * CELL_SIZE + 6 * THIN_LINE + 4 * THICK_LINE   # = 492

# ---------- แถบข้อมูลด้านขวา ----------
PANEL_X = 540
PANEL_WIDTH = 240

# ---------- กติกา ----------
MAX_LIVES = 3                    # ตอบผิดได้ 3 ครั้ง
MAX_HINTS = 3                    # ใช้ตัวช่วยได้ 3 ครั้ง
DIFFICULTIES = ["Easy", "Normal", "Hard"]
HINT_PENALTY = {"Easy": 60, "Normal": 180, "Hard": 300}   # วินาทีที่บวกเพิ่มต่อการใช้ตัวช่วย 1 ครั้ง

# ---------- ชื่อผู้เล่นและอันดับ ----------
NAME_MAX_LENGTH = 12
DEFAULT_NAME = "Player"          # ใช้ชื่อนี้ถ้าไม่พิมพ์ชื่อ
TOP_COUNT = 3

# ---------- ไฟล์ ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))   # โฟลเดอร์ของเกม (รันจากที่ไหนก็หาไฟล์เจอ)
LEVELS_DIR = os.path.join(BASE_DIR, "levels")
HISTORY_FILE = os.path.join(BASE_DIR, "data", "history.txt")

# ---------- ปุ่มบนคีย์บอร์ด ----------
# ตัวเลข: เช็กทั้งรหัสปุ่ม (key) และตำแหน่งปุ่มจริง (scancode)
# เพราะถ้าคีย์บอร์ดเป็นภาษาไทย ปุ่มแถวบนจะส่งตัวอักษรไทยมาแทนตัวเลข
DIGIT_KEYS = {}
DIGIT_SCANCODES = {}
for _number in range(1, 10):
    DIGIT_KEYS[getattr(pygame, f"K_{_number}")] = _number          # แถวบน
    DIGIT_KEYS[getattr(pygame, f"K_KP{_number}")] = _number        # แป้นตัวเลขด้านขวา
    DIGIT_SCANCODES[getattr(pygame, f"KSCAN_{_number}")] = _number
    DIGIT_SCANCODES[getattr(pygame, f"KSCAN_KP{_number}")] = _number

# ลบเลข
CLEAR_KEYS = (pygame.K_BACKSPACE, pygame.K_DELETE, pygame.K_KP_MINUS, pygame.K_0, pygame.K_KP0)
CLEAR_SCANCODES = (pygame.KSCAN_0, pygame.KSCAN_KP0)

# ส่งคำตอบ (Enter ปกติ และ Enter ที่แป้นตัวเลข)
ENTER_KEYS = (pygame.K_RETURN, pygame.K_KP_ENTER)
