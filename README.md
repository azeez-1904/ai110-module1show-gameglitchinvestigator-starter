# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

### What the game does
A number-guessing game where the player picks a difficulty (Easy / Normal / Hard), receives a secret number drawn from that difficulty's range, and tries to guess it within a limited number of attempts. The game gives "Too High" or "Too Low" hints after each guess and tracks a running score.

### Bugs found in the original AI-generated code

| # | Bug | Location |
|---|-----|----------|
| 1 | Hint messages were **backwards** — "Go HIGHER!" when guess was too high | `check_guess` in `app.py` lines 37–40 |
| 2 | On **even-numbered attempts** the secret was cast to `str`, causing alphabetical comparison (e.g. `"9" > "42"` = True) and random wrong hints | `app.py` lines 158–163 |
| 3 | Wrong guesses on even attempts **added +5 to score** instead of subtracting | `update_score` in `app.py` lines 57–60 |
| 4 | Info banner was hardcoded `"1 and 100"` regardless of difficulty — Hard mode uses 1–50 | `app.py` line 110 |

### Fixes applied

- **Refactored** all game logic (`get_range_for_difficulty`, `parse_guess`, `check_guess`, `update_score`) out of `app.py` and into `logic_utils.py`, fixing every bug during the move.
- `check_guess` now always compares integers, returns just the outcome string (`"Win"`, `"Too High"`, `"Too Low"`), and the hint messages live in `app.py` as a lookup dict — correct and readable.
- `update_score` removes the even-attempt parity branch: wrong guesses always subtract 5.
- The info banner now reads `f"between {low} and {high}"` using the values from `get_range_for_difficulty`.
- Added 12 new pytest cases (15 total, all passing) that directly target each fixed bug.

## 📸 Demo

> **pytest results — all 15 tests passing after fixes:**
>
> ```
> tests/test_game_logic.py::test_winning_guess                              PASSED
> tests/test_game_logic.py::test_guess_too_high                             PASSED
> tests/test_game_logic.py::test_guess_too_low                              PASSED
> tests/test_game_logic.py::test_check_guess_never_returns_tuple            PASSED
> tests/test_game_logic.py::test_check_guess_integer_comparison_consistency PASSED
> tests/test_game_logic.py::test_parse_guess_valid_integer                  PASSED
> tests/test_game_logic.py::test_parse_guess_empty_string                   PASSED
> tests/test_game_logic.py::test_parse_guess_float_string                   PASSED
> tests/test_game_logic.py::test_parse_guess_non_numeric                    PASSED
> tests/test_game_logic.py::test_update_score_win_first_attempt             PASSED
> tests/test_game_logic.py::test_update_score_wrong_guess_always_subtracts  PASSED
> tests/test_game_logic.py::test_update_score_too_low_subtracts             PASSED
> tests/test_game_logic.py::test_easy_range                                 PASSED
> tests/test_game_logic.py::test_normal_range                               PASSED
> tests/test_game_logic.py::test_hard_range                                 PASSED
> ========================= 15 passed in 0.03s =========================
> ```
>
> *(Take a screenshot of your terminal running `pytest tests/ -v` and insert it here)*

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, insert a screenshot of your Enhanced Game UI here]
