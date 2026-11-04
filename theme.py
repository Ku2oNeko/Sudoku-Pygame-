# ==============================
# ธีมสี (สว่าง / มืด)
# ==============================


class Theme:
    """คลาสแม่ของธีม: ชื่อธีม และสีที่ทั้งสองธีมใช้เหมือนกัน"""

    def __init__(self, name):
        self.name = name
        self.selected_frame = (40, 110, 255)   # กรอบช่องที่กำลังเลือก
        self.hint_frame = (255, 185, 0)        # กรอบกะพริบของช่องที่เพิ่งใช้ตัวช่วย
        self.penalty = (235, 125, 20)          # ข้อความเวลาที่ถูกบวกเพิ่ม
        self.button_text = (255, 255, 255)

    def switch_label(self):
        """ข้อความบนปุ่มสลับธีม (คลาสลูกเขียนทับ)"""
        pass

    def __str__(self):
        return f"{self.name} theme"


class LightTheme(Theme):
    """ธีมสว่าง"""
    # [Inheritance] สืบทอดจาก Theme แล้วเติมสีของตัวเอง

    def __init__(self):
        super().__init__("Light")
        self.background = (233, 235, 239)
        self.text = (28, 30, 36)
        self.muted = (105, 110, 120)
        self.board_lines = (25, 25, 30)
        self.cell = (250, 250, 252)
        self.given_cell = (222, 225, 232)
        self.given_digit = (20, 20, 25)
        self.draft_digit = (50, 50, 255)
        self.correct_cell = (170, 235, 175)
        self.correct_digit = (20, 95, 35)
        self.wrong_cell = (250, 170, 170)
        self.wrong_digit = (175, 20, 30)
        self.button = (52, 98, 214)
        self.button_hover = (75, 122, 236)
        self.button_disabled = (196, 200, 208)
        self.card = (250, 250, 252)
        self.card_border = (200, 204, 212)
        self.overlay = (20, 22, 28, 150)       # ม่านโปร่งแสงตอนแพ้/ชนะ
        self.highlight = (255, 236, 160)       # แถบเน้นชื่อเราในตารางอันดับ
        self.success = (30, 150, 60)
        self.danger = (205, 40, 50)
        self.input_box = (255, 255, 255)
        self.input_border = (52, 98, 214)

    def switch_label(self):
        # [Polymorphism] เขียนทับเมธอดของ Theme
        return "Dark mode"


class DarkTheme(Theme):
    """ธีมมืด"""
    # [Inheritance] สืบทอดจาก Theme แล้วเติมสีของตัวเอง

    def __init__(self):
        super().__init__("Dark")
        self.background = (22, 24, 29)
        self.text = (232, 234, 238)
        self.muted = (150, 156, 168)
        self.board_lines = (120, 126, 138)
        self.cell = (46, 50, 58)
        self.given_cell = (33, 36, 43)
        self.given_digit = (236, 238, 242)
        self.draft_digit = (125, 165, 255)
        self.correct_cell = (36, 92, 52)
        self.correct_digit = (205, 245, 210)
        self.wrong_cell = (125, 40, 46)
        self.wrong_digit = (255, 205, 205)
        self.button = (60, 105, 220)
        self.button_hover = (88, 132, 242)
        self.button_disabled = (60, 64, 74)
        self.card = (36, 39, 46)
        self.card_border = (72, 77, 88)
        self.overlay = (0, 0, 0, 165)
        self.highlight = (95, 80, 25)
        self.success = (90, 210, 120)
        self.danger = (255, 95, 100)
        self.input_box = (28, 30, 36)
        self.input_border = (95, 140, 255)

    def switch_label(self):
        # [Polymorphism] เขียนทับเมธอดของ Theme
        return "Light mode"
