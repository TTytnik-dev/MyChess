# MyChess

MyChess is a fully functional chess application developed as a semester project. It features a graphical user interface, game history tracking, timers, support for FEN (Forsyth-Edwards Notation) input, board manipulation, and an AI opponent integrated via the Stockfish engine.

## Key Features

* **Graphical User Interface:** Built with `pygame`, providing an intuitive chess board experience.
* **AI Opponent:** Integrated with the Stockfish engine with adjustable difficulty levels.
* **FEN Support:** Load board positions from FEN strings, including clipboard integration for easy pasting.
* **Game History:** Navigate through your moves forward and backward.
* **Game Mechanics:** Move undo, move validation, pawn promotion, and move timers for both players.
* **Board Manipulation:** Ability to flip the board view.
* **Move Hinting:** Visual cues for valid moves.

## Prerequisites & Dependencies

The project requires Python 3. The necessary dependencies are listed in the `requirements.txt` file.

Required Python packages:
- pygame
- stockfish
- pytest

### Virtual Environment (optional)

```bash
python3 -m venv venv
source venv/bin/activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Installing Stockfish

Ubuntu/Debian:

```bash
sudo apt install stockfish
```

Fedora:

```bash
sudo dnf install stockfish
```

Arch Linux:

```bash
sudo pacman -S stockfish
```

## Usage

Run the application from the project root directory.

### Standard Game (Player vs Player)

```bash
python3 -m app.gui.window
```

### Play Against AI (Bot plays as Black)

```bash
python3 -m app.gui.window --bot
```

### Play Against AI (Bot plays as White)

```bash
python3 -m app.gui.window --bot --bot_color white
```

## Running Tests

The project includes unit and integration tests to ensure code stability.

Run tests using:

```bash
pytest tests/
```

## AI Annotation (Anotace)

Při vývoji projektu byl využit generativní nástroj (LLM - Gemini) pro účely konzultací, řešení problémů s knihovnou Pygame (clipboard, event handling, board flipping) a implementace integrace s enginem Stockfish.