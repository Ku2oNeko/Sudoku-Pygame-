# ==============================
# กระดาน 9x9
# ==============================
import random
import pygame
from settings import BOARD_X, BOARD_Y, BOARD_SIZE
from cell import GivenCell, PlayerCell


class Board:
    """กระดาน 9x9: เลือกช่อง ใส่เลข ตรวจคำตอบ ตัวช่วย และเช็กว่าชนะหรือยัง"""
    # [Composition] กระดานสร้างช่องทั้ง 81 ช่องเองใน __init__ และเป็นเจ้าของช่องเหล่านั้น
    #               กระดานหายไปเมื่อไร ช่องก็หายไปด้วย
    # [Abstraction] หน้าเล่นเรียกแค่ submit_selected() / reveal_random() / is_solved()
    #               ไม่ต้องรู้ว่าข้างในจัดการช่องยังไง

    def __init__(self, puzzle, key):
        self.grid = []                  # [[แถว1], [แถว2], ..., [แถว9]] (เดิมคือ ObjList)
        self.cells = []                 # [ช่อง11, ช่อง12, ..., ช่อง99] (เดิมคือ ObjBunch)
        self.selected = None            # ช่องที่กำลังเลือกอยู่ (เดิมคือ target)
        self.rect = pygame.Rect(BOARD_X, BOARD_Y, BOARD_SIZE, BOARD_SIZE)
        for row in range(1, 10):
            cells_in_row = []
            for col in range(1, 10):
                answer = key[row - 1][col - 1]
                if puzzle[row - 1][col - 1] != 0:
                    cell = GivenCell(row, col, answer)     # เลขที่โจทย์ให้มา
                else:
                    cell = PlayerCell(row, col, answer)    # ช่องว่างให้ผู้เล่นเติม
                cells_in_row.append(cell)
                self.cells.append(cell)
            self.grid.append(cells_in_row)

    def select_at(self, pos):
        """เลือกช่องที่คลิก (คลิกช่องเดิมซ้ำ = ยกเลิกการเลือก)"""
        for cell in self.cells:
            if cell.is_clicked(pos):
                if self.selected is not None:
                    self.selected.deselect()
                if cell is self.selected:
                    self.selected = None
                else:
                    cell.select()
                    self.selected = cell
                return

    def clear_selection(self):
        if self.selected is not None:
            self.selected.deselect()
            self.selected = None

    def input_digit(self, digit):
        """ใส่เลขทด (0 = ลบ) ในช่องที่เลือก"""
        if self.selected is not None:
            self.selected.input_digit(digit)           # [Polymorphism] ช่องแต่ละแบบจัดการเอง

    def submit_selected(self):
        """ส่งคำตอบช่องที่เลือก (กด Enter): True = ถูก, False = ผิด, None = ไม่มีอะไรให้ตรวจ"""
        if self.selected is None:
            return None
        return self.selected.check()                   # [Polymorphism]

    def reveal_random(self):
        """ตัวช่วย: สุ่มช่องว่าง 1 ช่องแล้วเปิดเฉลย
        (ถ้าไม่เหลือช่องว่าง สุ่มจากช่องที่ทดเลขไว้หรือช่องสีแดงแทน)"""
        choices = []
        for cell in self.cells:
            if cell.is_editable() and cell.get_digit() == 0:
                choices.append(cell)
        if len(choices) == 0:
            for cell in self.cells:
                if cell.is_editable():
                    choices.append(cell)
        if len(choices) == 0:
            return None
        cell = random.choice(choices)
        cell.reveal()
        return cell

    def is_solved(self):
        """ชนะเมื่อทุกช่องถูกหมด"""
        for cell in self.cells:
            if not cell.is_correct():
                return False
        return True

    def draw(self, screen, theme, font):
        pygame.draw.rect(screen, theme.board_lines, self.rect)   # พื้นที่โผล่ตามร่องคือเส้นตาราง
        for cell in self.cells:
            cell.draw(screen, theme, font)     # [Polymorphism] ไม่ต้องสนว่าเป็นช่องแบบไหน

    def __str__(self):
        lines = []
        for row in self.grid:
            digits = []
            for cell in row:
                digits.append(str(cell.get_digit()))
            lines.append(" ".join(digits))
        return "\n".join(lines)
