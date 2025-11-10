# Contributing Guidelines

Thank you for your interest in contributing to this project!  
This repository aims to demonstrate high-quality data engineering, analytics, and reporting practices.  
To keep the codebase clean, consistent, and efficient, please follow the guidelines below.

---

##  Repository Structure

project-root/
│
├─ src/ # Core scripts and modules
├─ data/ # Input data (exclude sensitive information)
│ ├─ raw/
│ └─ processed/
├─ notebooks/ # Exploratory or analytical notebooks
├─ reports/ # Generated reports, KPIs, QC outputs
├─ tools/ # Utility scripts (synthetic data, SQL runners, etc.)
└─ tests/ # Unit tests


---

##  Development Workflow

1. **Fork the repo** and create a feature branch:
git checkout -b feature/your-feature-name

2. **Run linting and tests locally** before committing:
ruff check .
black .
mypy src
pytest

3. **Ensure your code is typed** (PEP 484 type hints).

4. **Write or update tests** for any new functionality.

5. **Document your changes** in:
- Docstrings (`"""Description..."""`)
- README or dedicated markdown files if needed

6. **Submit a pull request**:
- Provide a clear description of the change
- Link to issues (if applicable)
- Include sample output or screenshots for visible components

---

## Testing Requirements

- Use `pytest`
- Keep tests in the `tests/` directory
- Aim for **80%+ coverage**
- Add tests for:
- edge cases
- invalid inputs
- expected outputs

---

## Code Style

This project follows:

- `ruff` for linting
- `black` for formatting (line length = 88)
- `mypy` for static type checking

Please ensure your code passes all checks before making a pull request.

---

##  Data Management Rules

- **Do NOT commit sensitive data**
- Use synthetic data for demos (`make synth`)
- Large files should be excluded using `.gitignore`

---

##  Contribution Philosophy

This project values:

- Clarity
- Modularity
- Reproducibility
- Automation
- Professional engineering standards

If your contribution improves any of these, it is welcome.

---

##  Questions

If you have questions about contributing or want to discuss an idea, please open an issue using the following template:

[Proposal] Brief title

Summary:

Use case:

Proposed approach:

---

Thank you for helping improve this project and making it more useful, expressive, and professional.
