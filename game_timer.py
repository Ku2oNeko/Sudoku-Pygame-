# ==============================
# นาฬิกาจับเวลา
# ==============================
import pygame


class GameTimer:
    """จับเวลาตั้งแต่โจทย์ขึ้นจอจนแก้เสร็จ (รวมเวลาที่ถูกบวกจากตัวช่วย)"""
    # [Encapsulation] ค่าภายในเป็น private ทั้งหมด ข้างนอกใช้ผ่านเมธอดเท่านั้น

    def __init__(self):
        self.__start_ms = None          # เวลาที่เริ่ม (มิลลิวินาที)
        self.__stop_ms = None           # เวลาที่หยุด (None = ยังเดินอยู่)
        self.__penalty_ms = 0           # เวลาที่ถูกบวกเพิ่มจากตัวช่วย

    def start(self):
        self.__start_ms = pygame.time.get_ticks()
        self.__stop_ms = None
        self.__penalty_ms = 0

    def stop(self):
        if self.is_running():
            self.__stop_ms = pygame.time.get_ticks()

    def is_started(self):
        return self.__start_ms is not None

    def is_running(self):
        return self.__start_ms is not None and self.__stop_ms is None

    def add_penalty(self, seconds):
        self.__penalty_ms += seconds * 1000

    def get_seconds(self):
        """เวลาทั้งหมดเป็นวินาทีเต็ม (รวมเวลาที่ถูกบวก)"""
        if self.__start_ms is None:
            return 0
        if self.__stop_ms is None:
            end = pygame.time.get_ticks()
        else:
            end = self.__stop_ms
        return (end - self.__start_ms + self.__penalty_ms) // 1000

    @staticmethod
    def format(seconds):
        """แปลงวินาทีเป็น mm:ss เช่น 75 -> 01:15"""
        return f"{seconds // 60:02d}:{seconds % 60:02d}"

    @staticmethod
    def format_added(seconds):
        """เวลาที่ถูกบวกเพิ่ม เช่น 60 -> +1:00"""
        return f"+{seconds // 60}:{seconds % 60:02d}"

    def __str__(self):
        return GameTimer.format(self.get_seconds())
