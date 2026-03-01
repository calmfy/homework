# AI Assistant Guidelines for `homework` repository

This repository currently consists of a single Python script (`hw_1.py`) implementing root-\ finding algorithms and a small "sphere immersion" problem. It's a student exercise rather than a multi‑module project, so there are only a few patterns to be aware of.

## Big picture

- `hw_1.py` is the only source file.  There is no package structure, no tests, no build system.  The program is driven by `main()` which presents a Russian‑language text menu and reads from `input()`.
- Two distinct problems are implemented:
  1. A general root‑finding toolkit: functions `f`, `df`, `d2f` along with `separate_roots` and four numerical methods (`bisection`, `newton`, `modified_newton`, `secant`).  The main loop lets a user choose an interval produced by `separate_roots` and compare methods.
  2. `sphere_problem()` calculates immersion depths for a sphere made of various materials using a simple bisection loop inside a dictionary of densities.
- The code is mostly self‑contained; there are no external dependencies beyond the standard `math` module and built‑in `input`/`print`.
- All user‑facing text (menu items, prompts, table headers) is written in Russian.  When extending or refactoring, preserve the language or be explicit about translations.

## Developer workflows

- Run the program with `python hw_1.py` from the workspace root.  It is interactive – tests are manual and based on reading console output.
- There are no automation scripts, so any additional tooling (e.g. formatting with `black` or adding unit tests) should be added explicitly in future commits.

## Patterns and conventions

- Numerical methods return a tuple `(root, steps, residual)` and the calling code in `main()` prints them in a fixed table format.  New methods should follow the same signature for interoperability with the menu code.
- The `separate_roots` function divides an interval `[A,B]` into `N` subintervals and checks for sign changes; it prints the found intervals before returning them.  The interactive flow expects results to be indexed starting at 1.
- The sphere problem creates its own internal function `g(d)` inside the loop and then applies a simple bisection.  Replicating this pattern is fine for similar physics tasks.
- Russian comments (e.g. `# ПРОЦЕДУРА ОТДЕЛЕНИЯ КОРНЕЙ`) are used as section separators; maintain this style when adding sections.

## External integration

- There are no external APIs, libraries, or configuration files.  The only import is `math`.

## When updating this file

- Merge intelligently if future students add more assignments.  Keep this section short and focused on the mechanics of the repo rather than general Python advice.
- If additional modules, tests, or workflows appear, update the Big picture/workflows sections accordingly.

> _Tip:_ since this repo is simple, most agent tasks will be small edits or educational explanations rather than architectural changes.  Aim for clarity and consistency with existing naming and comments.