def get_range_for_difficulty(difficulty: str):
    """Return (low, high) inclusive range for a given difficulty."""
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str, low: int = 1, high: int = 100):
    """
    Parse user input into an int guess and validate it is within [low, high].

    Returns: (ok: bool, guess_int: int | None, error_message: str | None)

    FIX: added low/high range validation so out-of-range and negative inputs
    are rejected before they reach check_guess.
    """
    if raw is None or raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    if value < low or value > high:
        return False, None, f"Please enter a number between {low} and {high}."

    return True, value, None


def check_guess(guess, secret):
    """
    Compare guess to secret and return the outcome string.

    Returns: "Win", "Too High", or "Too Low"

    FIXME was here: original code had swapped hint messages AND a branch that
    converted secret to str on even attempts, causing alphabetical comparison.
    FIX: always compare integers, return just the outcome string (no message),
    and correct the direction labels.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        # FIXME was here: original said "Go HIGHER!" when guess was too high — backwards.
        # FIX: guess is above the secret, so player should go lower.
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """
    Update score based on outcome and attempt number.

    FIXME was here: "Too High" on even attempt numbers added +5 (rewarded wrong guesses).
    FIX: wrong guesses always subtract 5, regardless of attempt parity.
    """
    if outcome == "Win":
        points = 100 - 10 * attempt_number
        if points < 10:
            points = 10
        return current_score + points

    if outcome in ("Too High", "Too Low"):
        # FIXME was here: original added +5 on even attempts for "Too High".
        # FIX: always subtract 5 for any wrong guess.
        return current_score - 5

    return current_score
