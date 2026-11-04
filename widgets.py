# ==============================
# ข้อความ ปุ่ม และช่องพิมพ์ชื่อ
# ==============================
import string
import pygame


class Clickable:
    """ความสามารถ "คลิกได้": มีกล่องล่องหนตรวจจับการคลิก"""

    def __init__(self, rect):
        self.sensor = pygame.Rect(rect)   # กล่องล่องหนตรวจจับการคลิก

    def is_clicked(self, pos):
        """True ถ้าตำแหน่งที่คลิกอยู่ในกล่อง"""
        return self.sensor.collidepoint(pos)


class Label:
    """ข้อความบนหน้าจอ (สีเปลี่ยนตามธีม)"""

    def __init__(self, text, font, pos, anchor="topleft", color_name="text"):
        self.text = text
        self.font = font
        self.pos = pos                  # จุดวางข้อความ
        self.anchor = anchor            # จุดนั้นคือมุมไหนของข้อความ เช่น "center", "topleft"
        self.color_name = color_name    # ชื่อสีในธีม เช่น "text", "muted"

    def set_text(self, text):
        self.text = text

    def draw(self, screen, theme):
        image, _ = self.font.render(self.text, getattr(theme, self.color_name))
        screen.blit(image, image.get_rect(**{self.anchor: self.pos}))

    def __str__(self):
        return f"Label('{self.text}')"


class Button(Label, Clickable):
    """ปุ่ม = ข้อความ (Label) + คลิกได้ (Clickable)"""
    # [Multiple Inheritance] สืบทอดจาก 2 คลาสพร้อมกัน

    def __init__(self, text, font, rect):
        rect = pygame.Rect(rect)
        Label.__init__(self, text, font, rect.center, "center", "button_text")
        Clickable.__init__(self, rect)
        self.enabled = True             # False = ปุ่มสีเทา กดไม่ได้

    def is_clicked(self, pos):
        # [Polymorphism] เขียนทับของ Clickable: ปุ่มที่ปิดอยู่กดไม่ได้
        return self.enabled and Clickable.is_clicked(self, pos)

    def draw(self, screen, theme):
        # [Polymorphism] เขียนทับของ Label: วาดกล่องปุ่มก่อน แล้วค่อยวาดข้อความ
        if not self.enabled:
            color = theme.button_disabled
            self.color_name = "muted"
        elif self.sensor.collidepoint(pygame.mouse.get_pos()):
            color = theme.button_hover
            self.color_name = "button_text"
        else:
            color = theme.button
            self.color_name = "button_text"
        pygame.draw.rect(screen, color, self.sensor, border_radius=8)
        Label.draw(self, screen, theme)

    def __str__(self):
        return f"Button('{self.text}')"


class NameBox:
    """ช่องพิมพ์ชื่อผู้เล่น: รับเฉพาะตัวอักษรภาษาอังกฤษ A-Z, a-z"""

    def __init__(self, font, rect, max_length):
        self.font = font
        self.rect = pygame.Rect(rect)
        self.max_length = max_length
        self.__text = ""                # [Encapsulation] private: แก้ได้ผ่านเมธอดเท่านั้น

    def get_text(self):
        return self.__text

    def add_text(self, text):
        """เติมตัวอักษรที่พิมพ์มา คืนข้อความเตือน ("" = ไม่มีปัญหา)"""
        warning = ""
        for char in text:
            if char in string.ascii_letters:
                if len(self.__text) < self.max_length:
                    self.__text += char
                else:
                    warning = f"Up to {self.max_length} letters"
            elif char.isascii():
                warning = "Letters A-Z only"                   # ตัวเลข เว้นวรรค สัญลักษณ์
            else:
                warning = "Switch your keyboard to English"    # เช่น ตัวอักษรไทย
        return warning

    def remove_last(self):
        self.__text = self.__text[:-1]

    def draw(self, screen, theme):
        pygame.draw.rect(screen, theme.input_box, self.rect, border_radius=6)
        pygame.draw.rect(screen, theme.input_border, self.rect, 2, border_radius=6)
        image, _ = self.font.render(self.__text, theme.text)
        text_rect = image.get_rect(midleft=(self.rect.x + 12, self.rect.centery))
        screen.blit(image, text_rect)
        # เคอร์เซอร์กะพริบทุกครึ่งวินาที
        if pygame.time.get_ticks() // 500 % 2 == 0:
            x = text_rect.right + 3
            pygame.draw.line(screen, theme.text, (x, self.rect.y + 10), (x, self.rect.bottom - 10), 2)

    def __str__(self):
        return f"NameBox('{self.__text}')"
