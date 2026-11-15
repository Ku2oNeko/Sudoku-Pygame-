# Sudoku (pygame)

A Sudoku game for our OOP pygame project. It has three difficulties, lives, hints that cost time, a timer, a light and dark theme, and a top-3 leaderboard for each level.

Demo video: https://youtu.be/B93TJ0tpFjg

## Run it

1. Install Python 3.8 or newer, then pygame 2: `pip install pygame`
2. From this folder, run `python main.py`

## How to play

| Action | How |
|---|---|
| Select a cell | Click it. Click it again to unselect. |
| Draft a digit | Type 1–9 on the number row or the numpad. |
| Check the cell | Press Enter (either Enter key). |
| Erase | Backspace, Delete, 0 or numpad minus |

- **Drafts aren't checked.** A typed digit is only a note until you press Enter on that cell.
- **Right answer:** the cell turns green and locks.
- **Wrong answer:** the cell turns red and you lose a life. It stays red until you change or erase the digit, and pressing Enter again on the same red digit costs nothing.
- **3 lives.** The third mistake ends the game. Retry replays the same level from the start.
- **3 hints.** A hint fills a random empty cell and adds time: Easy +1:00, Normal +3:00, Hard +5:00.
- **Timer** starts when the puzzle appears and stops at the last correct cell.
- **After you solve it**, type your name (English letters only, up to 12; an empty name is saved as "Player"). Every solve is saved, and the right side of the screen shows the 3 fastest times for that level. A tie goes to whoever solved first.
- The number keys still work when the keyboard is set to Thai. The name box needs English.

## Add a level

Put two files in `levels/easy`, `levels/normal` or `levels/hard`:

- `<Name>_puzzle.txt`: 9 lines of 9 digits separated by commas, with `0` for an empty cell
- `<Name>_key.txt`: the full solution in the same format

Example line: `0,6,0,0,1,0,0,4,3`

When a difficulty has more than one level, the game picks one at random. The game checks each file's format and that the key matches the puzzle, and it skips a broken level with a message in the console. It doesn't check that a puzzle has only one solution, so make sure yours does. If a puzzle had two solutions, a correct digit could be marked wrong.

### Levels included

All three have exactly one solution.

| Level | Givens | Solving techniques needed |
|---|---|---|
| Easy | 38 | Naked singles only |
| Normal | 30 | Hidden singles |
| Hard | 25 | Locked candidates and a hidden pair |

## Files

| File | What it does |
|---|---|
| `main.py` | Starts the game |
| `settings.py` | Sizes, lives, hints, penalties, keys and file paths |
| `game.py` | `Game`: the window, the main loop and switching screens |
| `screens.py` | `Screen` and its 4 screens: menu, play, game over, win |
| `board.py` | `Board`: the 9×9 grid, checking answers, hints and the win check |
| `cell.py` | `Cell`, `GivenCell`, `PlayerCell` |
| `widgets.py` | `Clickable`, `Label`, `Button`, `NameBox` |
| `theme.py` | `Theme`, `LightTheme`, `DarkTheme` |
| `game_timer.py` | `GameTimer` |
| `level_reader.py` | `Level`, `LevelReader` |
| `leaderboard.py` | `Record`, `Leaderboard` |
| `levels/` | The puzzle and key files |
| `data/history.txt` | Every solve, one per line (`difficulty,level,name,seconds,date`). Created on the first save. |

## OOP concepts in the code

Each concept is tagged in the comments, so you can search for `[Composition]` and similar tags.

| Concept | Where |
|---|---|
| Class and object | Every file. `Board` creates 81 `Cell` objects. |
| `__init__` and `__str__` | For example `Cell`, `Board`, `Level`, `Record`, `GameTimer`, `Theme` |
| Inheritance | `GivenCell` and `PlayerCell` inherit from `Cell`, which inherits from `Clickable`. The 4 screens inherit from `Screen`. `LightTheme` and `DarkTheme` inherit from `Theme`. |
| Multiple inheritance | `Button(Label, Clickable)` |
| Polymorphism | `Board.draw()` calls `cell.draw()` on both cell types, and each type picks its own colors. `Game.run()` calls `handle_event()`, `update()` and `draw()` on whichever screen is active. `Button` overrides `Label.draw()`. |
| Composition | `Board` creates and owns its 81 cells. `PlayScreen` creates its own `Board` and `GameTimer`. |
| Aggregation | `Game` creates one `Leaderboard`, one `LevelReader` and the two themes, and the screens only keep references to them. `PlayScreen` uses a `Level` that belongs to `LevelReader`. |
| Encapsulation | Protected `_key` and `_digit` in `Cell`. Private `__state` in `PlayerCell`, and private `__lives`, `__hints_left` and methods like `__use_hint()` in `PlayScreen`. Also private data in `GameTimer`, `Leaderboard`, `LevelReader` and `NameBox`, read through `get_...()` methods. |
| Abstraction | `Screen` and `Cell` declare methods with `pass` that subclasses fill in. `Board` hides how cells are handled behind `submit_selected()`, `reveal_random()` and `is_solved()`. |
