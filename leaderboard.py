# ==============================
# ประวัติการเล่นและอันดับเวลา
# ==============================
import os
from datetime import datetime
from game_timer import GameTimer


class Record:
    """ผลการแก้สำเร็จ 1 ครั้ง"""

    def __init__(self, difficulty, level_name, player_name, seconds, finished_at=None):
        self.difficulty = difficulty
        self.level_name = level_name
        self.player_name = player_name
        self.seconds = seconds          # เวลาที่ใช้ (รวมเวลาที่ถูกบวกจากตัวช่วยแล้ว)
        if finished_at is None:
            finished_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.finished_at = finished_at

    def to_line(self):
        """แปลงเป็น 1 บรรทัดในไฟล์ history.txt"""
        return f"{self.difficulty},{self.level_name},{self.player_name},{self.seconds},{self.finished_at}"

    @staticmethod
    def from_line(line):
        """สร้าง Record จาก 1 บรรทัดในไฟล์"""
        parts = line.strip().split(",")
        if len(parts) != 5:
            raise ValueError("expected 5 values")
        return Record(parts[0], parts[1], parts[2], int(parts[3]), parts[4])

    def is_for(self, difficulty, level_name):
        return self.difficulty == difficulty and self.level_name == level_name

    def __str__(self):
        return f"{self.player_name} {GameTimer.format(self.seconds)}"


class Leaderboard:
    """เก็บประวัติการเล่นทั้งหมด (data/history.txt) และหาอันดับเวลาของแต่ละด่าน"""

    def __init__(self, history_file):
        self.__history_file = history_file
        self.__records = []             # [Encapsulation] private: เพิ่มได้ผ่าน add() เท่านั้น
        self.__load()

    def __load(self):
        if not os.path.isfile(self.__history_file):
            return                      # ยังไม่เคยมีใครเล่นจบ
        with open(self.__history_file, encoding="utf-8") as file:
            for number, line in enumerate(file.readlines(), start=1):
                if line.strip() == "":
                    continue
                try:
                    self.__records.append(Record.from_line(line))
                except ValueError:
                    print(f"[Leaderboard] Skipped broken line {number} in history.txt")

    def add(self, record):
        """บันทึกผลใหม่ ทั้งในรายการและต่อท้ายไฟล์"""
        self.__records.append(record)
        try:
            os.makedirs(os.path.dirname(self.__history_file), exist_ok=True)
            with open(self.__history_file, "a", encoding="utf-8") as file:
                file.write(record.to_line() + "\n")
        except OSError as error:
            print(f"[Leaderboard] Couldn't save history: {error}")

    def ranking(self, difficulty, level_name):
        """ผลทั้งหมดของด่านนี้ เรียงจากเร็วสุด
        (เวลาเท่ากัน คนที่แก้ได้ก่อนอยู่อันดับดีกว่า เพราะ sort ของ Python คงลำดับเดิมไว้)"""
        records = []
        for record in self.__records:
            if record.is_for(difficulty, level_name):
                records.append(record)
        records.sort(key=lambda record: record.seconds)
        return records

    def top(self, difficulty, level_name, count):
        return self.ranking(difficulty, level_name)[:count]

    def rank_of(self, record):
        """อันดับของผลนี้ในด่านของมัน (เริ่มที่ 1)"""
        return self.ranking(record.difficulty, record.level_name).index(record) + 1
