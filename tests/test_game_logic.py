from logic_utils import check_guess, parse_guess, update_score, get_range_for_difficulty


# --- check_guess ---

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, outcome should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, outcome should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"

def test_check_guess_never_returns_tuple():
    # FIX verification: check_guess must return a plain string, not a (outcome, message) tuple
    result = check_guess(30, 50)
    assert isinstance(result, str)

def test_check_guess_integer_comparison_consistency():
    # FIX verification: result must be the same on "odd" and "even" attempt numbers
    # (the old bug depended on attempt parity in the caller — now check_guess is pure)
    assert check_guess(99, 42) == "Too High"
    assert check_guess(1, 42) == "Too Low"
    assert check_guess(42, 42) == "Win"


# --- parse_guess ---

def test_parse_guess_valid_integer():
    ok, value, err = parse_guess("42", 1, 100)
    assert ok is True
    assert value == 42
    assert err is None

def test_parse_guess_empty_string():
    ok, value, err = parse_guess("", 1, 100)
    assert ok is False
    assert value is None

def test_parse_guess_float_string():
    ok, value, err = parse_guess("7.9", 1, 100)
    assert ok is True
    assert value == 7

def test_parse_guess_non_numeric():
    ok, value, err = parse_guess("abc", 1, 100)
    assert ok is False

def test_parse_guess_negative_number_rejected():
    # FIX verification: negative numbers must be rejected as out of range
    ok, value, err = parse_guess("-5", 1, 100)
    assert ok is False
    assert err is not None

def test_parse_guess_above_range_rejected():
    # FIX verification: numbers above high must be rejected
    ok, value, err = parse_guess("101", 1, 100)
    assert ok is False
    assert err is not None

def test_parse_guess_boundary_low_accepted():
    ok, value, err = parse_guess("1", 1, 100)
    assert ok is True
    assert value == 1

def test_parse_guess_boundary_high_accepted():
    ok, value, err = parse_guess("100", 1, 100)
    assert ok is True
    assert value == 100

def test_parse_guess_easy_range_rejects_above_20():
    # Easy mode range is 1-20; guessing 50 should be rejected
    ok, value, err = parse_guess("50", 1, 20)
    assert ok is False


# --- update_score ---

def test_update_score_win_first_attempt():
    # Win on attempt 1: 100 - 10*1 = 90 points added
    score = update_score(0, "Win", 1)
    assert score == 90

def test_update_score_wrong_guess_always_subtracts():
    # FIX verification: "Too High" must always subtract, never add
    score_odd = update_score(100, "Too High", 1)
    score_even = update_score(100, "Too High", 2)
    assert score_odd == 95
    assert score_even == 95  # old bug: this would have been 105

def test_update_score_too_low_subtracts():
    score = update_score(100, "Too Low", 3)
    assert score == 95


# --- get_range_for_difficulty ---

def test_easy_range():
    assert get_range_for_difficulty("Easy") == (1, 20)

def test_normal_range():
    assert get_range_for_difficulty("Normal") == (1, 100)

def test_hard_range():
    assert get_range_for_difficulty("Hard") == (1, 50)
