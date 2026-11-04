# ==============================
# อ่านด่านจากไฟล์ .txt
# ==============================
import os
import random


class Level:
    """ด่าน 1 ด่าน: โจทย์ + เฉลย"""

    def __init__(self, difficulty, name, puzzle, key):
        self.difficulty = difficulty    # "Easy" / "Normal" / "Hard"
        self.name = name                # ชื่อด่าน เช่น "Level1"
        self.puzzle = puzzle            # ตาราง 9x9 (0 = ช่องว่าง)
        self.key = key                  # เฉลย 9x9

    def count_givens(self):
        count = 0
        for row in self.puzzle:
            for digit in row:
                if digit != 0:
                    count += 1
        return count

    def __str__(self):
        return f"{self.difficulty} - {self.name} ({self.count_givens()} givens)"


class LevelReader:
    """หาและอ่านด่านทั้งหมดในโฟลเดอร์ levels/<ความยาก>/
    แต่ละด่านมี 2 ไฟล์: <ชื่อ>_puzzle.txt และ <ชื่อ>_key.txt"""

    PUZZLE_END = "_puzzle.txt"
    KEY_END = "_key.txt"

    def __init__(self, levels_dir, difficulties):
        self.__levels_dir = levels_dir
        self.__levels = {}              # [Encapsulation] private: {"Easy": [Level, ...], ...}
        for difficulty in difficulties:
            self.__levels[difficulty] = self.__read_folder(difficulty)

    # ----- ใช้จากข้างนอก -----
    def has_levels(self, difficulty):
        return len(self.__levels.get(difficulty, [])) > 0

    def get_levels(self, difficulty):
        return list(self.__levels.get(difficulty, []))

    def random_level(self, difficulty):
        """สุ่มด่านในความยากนั้น (ตอนนี้มีอย่างละ 1 ด่าน)"""
        return random.choice(self.__levels[difficulty])

    # ----- ภายในคลาส -----
    def __read_folder(self, difficulty):
        folder = os.path.join(self.__levels_dir, difficulty.lower())
        levels = []
        if not os.path.isdir(folder):
            print(f"[LevelReader] No folder for {difficulty}: {folder}")
            return levels
        for file_name in sorted(os.listdir(folder)):
            if not file_name.endswith(LevelReader.PUZZLE_END):
                continue
            name = file_name[:-len(LevelReader.PUZZLE_END)]
            try:
                levels.append(self.__read_level(folder, difficulty, name))
            except (ValueError, OSError) as error:
                print(f"[LevelReader] Skipped {difficulty}/{name}: {error}")
        if len(levels) == 0:
            print(f"[LevelReader] No playable level for {difficulty}")
        return levels

    def __read_level(self, folder, difficulty, name):
        if "," in name:
            raise ValueError("a level name can't contain a comma")
        key_file = name + LevelReader.KEY_END
        if not os.path.isfile(os.path.join(folder, key_file)):
            raise ValueError(f"missing {key_file}")
        puzzle = LevelReader.read_grid(os.path.join(folder, name + LevelReader.PUZZLE_END), 0)
        key = LevelReader.read_grid(os.path.join(folder, key_file), 1)
        LevelReader.check_key(key)
        LevelReader.check_match(puzzle, key)
        return Level(difficulty, name, puzzle, key)

    @staticmethod
    def read_grid(path, lowest):
        """อ่านไฟล์ตาราง: 9 บรรทัด บรรทัดละ 9 ตัวเลขคั่นด้วย ,
        lowest = 0 สำหรับโจทย์ (มีช่องว่าง), 1 สำหรับเฉลย (ต้องเต็ม)"""
        file_name = os.path.basename(path)
        grid = []
        # utf-8-sig: อ่านไฟล์ที่เซฟจาก Notepad (มี BOM) ได้ด้วย
        with open(path, encoding="utf-8-sig") as file:
            for line in file.readlines():
                if line.strip() == "":
                    continue                    # ข้ามบรรทัดว่าง
                row = []
                for item in line.strip().split(","):
                    try:
                        digit = int(item)
                    except ValueError:
                        raise ValueError(f"{file_name}: '{item.strip()}' is not a number")
                    if digit < lowest or digit > 9:
                        raise ValueError(f"{file_name}: {digit} is out of range")
                    row.append(digit)
                if len(row) != 9:
                    raise ValueError(f"{file_name}: a row has {len(row)} numbers instead of 9")
                grid.append(row)
        if len(grid) != 9:
            raise ValueError(f"{file_name}: {len(grid)} rows instead of 9")
        return grid

    @staticmethod
    def check_key(key):
        """เฉลยต้องถูกกติกา: ทุกแถว ทุกหลัก ทุกกล่อง 3x3 มีเลข 1-9 ครบ ไม่ซ้ำ"""
        full = set(range(1, 10))
        for i in range(9):
            row = set(key[i])
            col = set()
            box = set()
            for j in range(9):
                col.add(key[j][i])
                box.add(key[(i // 3) * 3 + j // 3][(i % 3) * 3 + j % 3])
            if row != full:
                raise ValueError(f"key row {i + 1} repeats a digit")
            if col != full:
                raise ValueError(f"key column {i + 1} repeats a digit")
            if box != full:
                raise ValueError(f"key box {i + 1} repeats a digit")

    @staticmethod
    def check_match(puzzle, key):
        """เลขที่โจทย์ให้มาต้องตรงกับเฉลย และต้องเหลือช่องว่างให้เล่น"""
        empty = 0
        for row in range(9):
            for col in range(9):
                digit = puzzle[row][col]
                if digit == 0:
                    empty += 1
                elif digit != key[row][col]:
                    raise ValueError(f"puzzle and key differ at row {row + 1}, column {col + 1}")
        if empty == 0:
            raise ValueError("the puzzle has no empty cells")
