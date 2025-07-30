Project: Catchery

General Instructions:

- Follow existing Python coding conventions and structure.
- All public functions and classes must have clear docstrings using Google-style or PEP 257 format.
- Prefer clean, idiomatic Python using list comprehensions, generators, and context managers where appropriate.
- Ensure compatibility with Python 3.11+.
- Code should be readable and robust, prioritizing clarity over cleverness.

Coding Style:

- Use 4 spaces for indentation.
- Function and variable names should use `snake_case`.
- Class names should use `PascalCase`.
- Constant names should be in `UPPER_CASE`.
- Always use absolute imports where possible.
- Avoid side effects at import time.
- Avoid unnecessary comments — code should be self-explanatory. Where comments are needed, place them **above** the relevant code (never inline).

Error Handling:

- Use built-in exceptions where applicable (e.g. `ValueError`, `KeyError`, `FileNotFoundError`).
- Avoid blanket `except:` blocks — catch specific exceptions.
- Log all errors using the `logging` module, not `print`.
- When raising custom exceptions, define them in a dedicated `exceptions.py` module.

Project Structure:

- Follow the `src/` layout:

```bash
project_root/
├── src/
│ └── catchery/
├── tests/
├── pyproject.toml
├── requirements.txt
├── README.md
```

- Keep utility functions in `utils.py` or separate helpers modules.
- Do not mix test code with production code.

Regarding Dependencies:

- Use only well-maintained and widely adopted libraries.
- Prefer standard library modules where feasible.
- If adding a new dependency:
- Justify the addition in the commit message.
- Add the package to `requirements.txt` and lock file if used.
- Update related documentation or usage examples.

Testing:

- Use `pytest` as the test runner.
- Name test files with `test_*.py`.
- Each test function should cover one logical case.
- Use `mypy` to check types; use `coverage` or `pytest-cov` to measure test coverage.

Commits:

- Use the Conventional Commits format: `<type>(scope): short summary`
Examples:
- `feat(config): support dynamic environment loading`
- `fix(core): handle missing config file gracefully`
- `test(utils): add unit tests for retry logic`

Allowed types (use these as `<type>` in your commit messages):

- `feature` – New features
- `fix` – Bug fixes
- `documentation` – Documentation changes only
- `style` – Code style, formatting, missing semi-colons, etc. (no code meaning changes)
- `refactor` – Code changes that neither fix a bug nor add a feature
- `performance` – Code changes that improve performance
- `test` – Adding or correcting tests
- `build` – Changes to build system or external dependencies
- `ci` – Changes to CI configuration files and scripts
- `chore` – Maintenance tasks (e.g., updating dependencies, minor tooling)
- `revert` – Reverting previous commits
- `security` – Security-related improvements or fixes
- `ux` – User experience or UI improvements

Other Notes:

- Prefer simple, linear Git history. Use rebase over merge where possible.
- Use `pre-commit` hooks to enforce formatting, linting, and checks before commits.
- If unsure about a change, open a draft PR with a summary and rationale.
