# Copilot Instructions for text_games

This repository contains simple text-based games. The main game implemented is Rock-Paper-Scissors-Lizard-Spock (RPSLS), located in `rpsls/rpsls.py`.

## Architecture Overview
- All game logic for RPSLS is in a single file: `rpsls/rpsls.py`.
- The game uses a dictionary (`RULES`) to encode win/loss relationships and reasons.
- User and computer choices are managed via the `CHOICES` list and helper functions.
- The game is interactive, using `input()` for user selection.

## Developer Workflows
- **Run the game:** Execute `python3 rpsls/rpsls.py` from the project root.
- **No build system or tests** are present; all logic is directly runnable.
- **No external dependencies** beyond Python's standard library.

## Project-Specific Patterns
- Game rules are encoded as a dictionary mapping `(winner, loser)` tuples to a reason string.
- Functions are used for user input, computer choice, and winner determination.
- The code expects integer input (1-5) for user selection, mapped to choices.
- All output is printed to the console; there is no file or network I/O.

## Conventions
- All game logic is kept in a single file per game.
- Use clear, descriptive function names (`get_user_choice`, `get_computer_choice`, `determine_winner`).
- Error handling for user input is done via a loop and exception catching.

## Key Files
- `rpsls/rpsls.py`: Main game logic and entry point.
- `README.md`: Project overview (minimal).

## Example: Adding a New Game
- Create a new subdirectory and place the main game file there (e.g., `newgame/newgame.py`).
- Follow the pattern of keeping all logic in one file and using simple input/output.

---
For questions or improvements, follow the conventions above and keep new games self-contained and simple.
