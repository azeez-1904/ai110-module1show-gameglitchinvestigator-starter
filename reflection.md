# 💭 Reflection: Game Glitch Investigator

Answer each question in 3 to 5 sentences. Be specific and honest about what actually happened while you worked. This is about your process, not trying to sound perfect.

## 1. What was broken when you started?

When I first ran the game it looked normal on the surface — there was a text input, a submit button, and a score counter. But after a few guesses it became clear that something was very wrong with the feedback and scoring.

**Bug 1 — Hints are backwards (`check_guess`, lines 37–40)**
- **Expected:** If my guess is too high, the game should tell me to go *lower*. If too low, go *higher*.
- **What actually happened:** The messages were swapped. Guessing too high showed "Go HIGHER!" and guessing too low showed "Go LOWER!" — the exact opposite of correct. Following the hints made it impossible to find the number.

**Bug 2 — String comparison breaks hints on even attempts (lines 158–163)**
- **Expected:** Every guess should be compared to the secret number as an integer, giving consistent feedback every turn.
- **What actually happened:** On every even-numbered attempt, the secret was secretly converted to a string (`secret = str(st.session_state.secret)`). Python then did alphabetical comparison instead of numeric — for example, `"9" > "42"` is `True` because `"9" > "4"` alphabetically. The hint flipped to the wrong direction on alternating turns, making the game feel completely random.

**Bug 3 — Score increases for wrong guesses on even attempts (lines 57–60)**
- **Expected:** Every wrong guess should reduce (or at least not increase) my score.
- **What actually happened:** Whenever a "Too High" outcome landed on an even attempt number, the code ran `return current_score + 5`, rewarding an incorrect guess with +5 points. My score would go *up* after a bad guess, making the score meaningless.

**Bug 4 — Hard mode range is wrong but the hint text is hardcoded**
- **Expected:** The displayed range should match the actual range the secret number is drawn from.
- **What actually happened:** Hard mode draws from 1–50, but the info banner always says "Guess a number between 1 and 100" regardless of difficulty. Players in Hard mode are told the wrong range the entire game.

---

## 2. How did you use AI as a teammate?

I used Claude Code (Anthropic) and GitHub Copilot to investigate and repair the bugs. Claude Code helped me read and analyze `app.py` before touching any code, and Copilot's inline chat helped me plan the refactor into `logic_utils.py`.

**Correct AI suggestion — fixing the backwards hints:**
When I described the hint bug, the AI correctly identified that lines 37–40 had the messages swapped: `"📈 Go HIGHER!"` was returned when `guess > secret` (too high), but it should say go lower. The AI suggested simply swapping the two message strings. I verified this by running `check_guess(60, 50)` in the test suite and confirming it returned `"Too High"`, then playing the live game and confirming the hint now pointed me in the right direction.

**Incorrect/misleading AI suggestion — the string comparison bug:**
When I first asked the AI to explain the even-attempt string conversion (lines 158–163), it initially suggested keeping the `str()` conversion but adding an `int()` cast inside `check_guess` to "handle both types." That would have papered over the root cause rather than removing the broken branch. I rejected this after reading the code more carefully — the entire `if st.session_state.attempts % 2 == 0` block was purposeless and wrong, so the correct fix was to delete it entirely and always pass the integer secret. I verified by adding `test_check_guess_integer_comparison_consistency` which confirms consistent results regardless of how many times it is called.

---

## 3. Debugging and testing your fixes

A bug was only considered fixed when two things were both true: a targeted pytest test passed AND the live game in the browser behaved correctly. Passing tests alone aren't enough — Streamlit state and reruns can introduce problems that pure unit tests don't catch.

**Test that caught the score bug:** `test_update_score_wrong_guess_always_subtracts` calls `update_score(100, "Too High", 2)` (an even attempt) and asserts the result is `95`, not `105`. Before the fix, this test would have failed because the original code added `+5` on even attempts. After moving the corrected logic to `logic_utils.py` (removing the `if attempt_number % 2 == 0` branch), the test passed. Running `pytest tests/ -v` showed all 15 tests green.

**Test that caught the string-comparison bug:** `test_check_guess_never_returns_tuple` asserts `isinstance(result, str)`. This would have failed against the original `app.py` version of `check_guess` which returned a `(outcome, message)` tuple. It confirmed that the new `logic_utils.py` version returns a plain string as the tests and `app.py` both expect.

The AI helped me think of the parity edge-case test (`test_update_score_wrong_guess_always_subtracts`) — I described the bug and asked "what test would have caught this from the start?" and it pointed me straight to testing the even-attempt case explicitly.

---

## 4. What did you learn about Streamlit and state?

- In your own words, explain why the secret number kept changing in the original app.
- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?
- What change did you make that finally gave the game a stable secret number?

---

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.
- What is one thing you would do differently next time you work with AI on a coding task?
- In one or two sentences, describe how this project changed the way you think about AI generated code.
