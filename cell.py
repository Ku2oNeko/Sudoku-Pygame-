# ==============================
# ช่องในตาราง
# ==============================
import pygame
from settings import BOARD_X, BOARD_Y, CELL_SIZE, THIN_LINE, THICK_LINE
from widgets import Clickable


class Cell(Clickable):
    """คลาสแม่ของช่องทุกแบบ"""
    # [Inheritance] ได้ sensor (กล่องตรวจจับการคลิก) มาจาก Clickable
    # [Abstraction] คลาสแม่บอกแค่ว่าช่องต้องทำอะไรได้บ้าง คลาสลูกเป็นคนเขียนจริง

    def __init__(self, row, col, key, digit):
        super().__init__(Cell.rect_of(row, col))
        self.row = row                  # แถว 1-9
        self.col = col                  # หลัก 1-9
        self._key = key                 # [Encapsulation] protected: เลขเฉลย
        self._digit = digit             # [Encapsulation] protected: เลขในช่อง (0 = ว่าง)
        self.is_selected = False        # กำลังถูกเลือกอยู่หรือไม่

    @staticmethod
    def rect_of(row, col):
        """คำนวณกล่องของช่องจากแถว/หลัก (ขอบกล่อง 3x3 กว้างกว่าเส้นปกติ)"""
        extra = THICK_LINE - THIN_LINE
        x = BOARD_X + THICK_LINE + (col - 1) * (CELL_SIZE + THIN_LINE) + ((col - 1) // 3) * extra
        y = BOARD_Y + THICK_LINE + (row - 1) * (CELL_SIZE + THIN_LINE) + ((row - 1) // 3) * extra
        return pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

    def get_digit(self):
        return self._digit

    def select(self):
        self.is_selected = True

    def deselect(self):
        self.is_selected = False

    # ----- เมธอดที่คลาสลูกต้องเขียนทับ -----
    def input_digit(self, digit):
        """ใส่เลข 1-9 หรือ 0 เพื่อลบ"""
        pass

    def check(self):
        """ตรวจคำตอบ: True = ถูก, False = ผิด, None = ไม่มีอะไรให้ตรวจ"""
        pass

    def is_editable(self):
        pass

    def is_correct(self):
        pass

    def _fill_color(self, theme):
        pass

    def _digit_color(self, theme):
        pass

    # ----- วาดช่อง -----
    def draw(self, screen, theme, font):
        # พื้นช่อง: สีขึ้นกับชนิดและสถานะของช่อง (คลาสลูกเป็นคนเลือก)
        pygame.draw.rect(screen, self._fill_color(theme), self.sensor)
        # ตัวเลข
        if self._digit != 0:
            image, _ = font.render(str(self._digit), self._digit_color(theme))
            screen.blit(image, image.get_rect(center=self.sensor.center))
        # กรอบช่องที่เลือก (เป็นกรอบ ไม่ทับสีพื้น ช่องแดง/เขียวจึงยังเห็นสีอยู่)
        if self.is_selected:
            pygame.draw.rect(screen, theme.selected_frame, self.sensor, 4)

    def __str__(self):
        return f"{type(self).__name__}(row={self.row}, col={self.col}, digit={self._digit})"


class GivenCell(Cell):
    """ช่องที่โจทย์ให้มา: ล็อกไว้ แก้ไม่ได้"""
    # [Inheritance] สืบทอดจาก Cell
    # [Polymorphism] เขียนทับเมธอดของ Cell ให้เป็นแบบ "ช่องโจทย์"

    def __init__(self, row, col, key):
        super().__init__(row, col, key, key)   # เลขในช่อง = เลขเฉลย

    def input_digit(self, digit):
        pass                                   # แก้ไม่ได้

    def check(self):
        return None                            # ไม่มีอะไรให้ตรวจ

    def is_editable(self):
        return False

    def is_correct(self):
        return True

    def _fill_color(self, theme):
        return theme.given_cell

    def _digit_color(self, theme):
        return theme.given_digit


class PlayerCell(Cell):
    """ช่องที่ผู้เล่นเติม: ว่าง -> ทดเลข -> (กด Enter) -> ถูก หรือ ผิด"""
    # [Inheritance] สืบทอดจาก Cell
    # [Polymorphism] เขียนทับเมธอดของ Cell ให้เป็นแบบ "ช่องผู้เล่น"

    # สถานะของช่อง
    EMPTY = "empty"       # ว่าง
    DRAFT = "draft"       # ทดเลขไว้ ยังไม่ได้ส่ง
    CORRECT = "correct"   # ส่งแล้ว ถูก (ล็อก)
    WRONG = "wrong"       # ส่งแล้ว ผิด (แดงค้างจนกว่าจะแก้หรือลบเลข)

    def __init__(self, row, col, key):
        super().__init__(row, col, key, 0)
        self.__state = PlayerCell.EMPTY        # [Encapsulation] private

    def get_state(self):
        return self.__state

    def input_digit(self, digit):
        if self.__state == PlayerCell.CORRECT:
            return                             # ตอบถูกแล้ว ล็อก
        if digit == self._digit:
            return                             # เลขเดิม: ไม่เปลี่ยนอะไร (ถ้าแดงอยู่ก็ยังแดง)
        self._digit = digit
        if digit == 0:
            self.__state = PlayerCell.EMPTY
        else:
            self.__state = PlayerCell.DRAFT

    def check(self):
        if self.__state != PlayerCell.DRAFT:
            return None                        # ว่าง หรือส่งไปแล้ว: ไม่ตรวจซ้ำ ไม่เสียชีวิต
        if self._digit == self._key:
            self.__state = PlayerCell.CORRECT
            return True
        self.__state = PlayerCell.WRONG
        return False

    def reveal(self):
        """ตัวช่วย: เปิดเลขเฉลยในช่องนี้"""
        self._digit = self._key
        self.__state = PlayerCell.CORRECT

    def is_editable(self):
        return self.__state != PlayerCell.CORRECT

    def is_correct(self):
        return self.__state == PlayerCell.CORRECT

    def _fill_color(self, theme):
        if self.__state == PlayerCell.CORRECT:
            return theme.correct_cell
        if self.__state == PlayerCell.WRONG:
            return theme.wrong_cell
        return theme.cell

    def _digit_color(self, theme):
        if self.__state == PlayerCell.CORRECT:
            return theme.correct_digit
        if self.__state == PlayerCell.WRONG:
            return theme.wrong_digit
        return theme.draft_digit
