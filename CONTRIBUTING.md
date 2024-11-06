# Contributing to the DGT-ZK Protocol

Thank you for your interest in contributing to the DGT-ZK Protocol! We welcome contributions from the community to improve the protocol, fix issues, add features, or enhance documentation. This guide outlines the steps to contribute effectively.

## Table of Contents

1. [Code of Conduct](#code-of-conduct)
2. [How to Contribute](#how-to-contribute)
3. [Development Setup](#development-setup)
4. [Coding Guidelines](#coding-guidelines)
5. [Submitting Changes](#submitting-changes)
6. [Reporting Issues](#reporting-issues)
7. [Pull Request Process](#pull-request-process)
8. [Contact](#contact)

---

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](./CODE_OF_CONDUCT.md). We aim to create an inclusive, welcoming environment, so please treat others with respect and professionalism.

## How to Contribute

You can contribute in several ways:

- Reporting bugs
- Suggesting enhancements
- Improving documentation
- Writing tests and improving code coverage
- Developing new features

## Development Setup

### Prerequisites

- **Python 3.x**: Ensure you have Python 3.7 or newer installed.
- **Dependencies**: Install the necessary dependencies with `pip`.

### Setup Instructions

1. **Fork the Repository**: Click the "Fork" button on the GitHub repository to create a copy under your GitHub account.
2. **Clone the Repository**: Clone your forked repository to your local machine.
   ```bash
   git clone https://github.com/DGT-Network/dgt_zk_protocol.git
   cd dgt_zk_protocol
```

3. **Create a Virtual Environment** (recommended):
    
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```
    
4. **Install Dependencies**:
    
    ```bash
    pip install -r requirements.txt
    ```
    

You are now ready to start developing!

## Coding Guidelines

Follow these guidelines to ensure a consistent codebase:

1. **Code Style**:
    
    * Follow [PEP 8](https://pep8.org/) for Python code.
    * Use 4 spaces per indentation level.
    * Avoid long lines; keep each line under 80 characters if possible.
2. **Docstrings and Comments**:
    
    * Use docstrings to describe the purpose and functionality of classes, functions, and methods.
    * Include type hints wherever possible.
    * Ensure all modules have header comments describing their purpose.
3. **Naming Conventions**:
    
    * Use `snake_case` for function and variable names.
    * Use `CamelCase` for class names.
    * Constants should be in `ALL_CAPS`.
4. **Testing**:
    
    * Ensure that new code is covered by unit tests.
    * Tests should be placed in the `tests` directory.
    * Use `pytest` for testing and aim for coverage above 80%.

## Submitting Changes

1. **Create a Branch**:
    
    * For new features or bug fixes, create a new branch with a descriptive name.
    * Branch names should follow the format: `feature/feature-name` or `fix/issue-name`.
    
    ```bash
    git checkout -b feature/add-new-encryption
    ```
    
2. **Make Commits**:
    
    * Commit small, logical changes with descriptive commit messages.
    * Follow the convention: `Type: Brief Description`, e.g., `fix: resolve range proof validation`.
3. **Keep Code Updated**:
    
    * Regularly sync with the main branch to minimize merge conflicts.
    * Rebase your branch to keep a clean commit history.
    
    ```bash
    git fetch origin
    git rebase origin/main
    ```
    

## Reporting Issues

When reporting an issue, please include:

* A descriptive title and summary of the issue.
* Steps to reproduce the issue if applicable.
* The expected and actual behavior.
* Any relevant error messages or screenshots.

If you’re suggesting an enhancement, explain why it would be useful and how it would improve the protocol.

## Pull Request Process

1. **Push Your Changes**: Push your branch to your GitHub fork.
    
    ```bash
    git push origin feature/add-new-encryption
    ```
    
2. **Create a Pull Request**:
    
    * Navigate to the original repository.
    * Click on the "Pull Requests" tab and select "New Pull Request."
    * Compare changes from your branch to the main branch.
3. **PR Review**:
    
    * Ensure the PR description includes a summary of changes and relevant issue references.
    * Once you submit a PR, it will be reviewed. Be prepared to discuss changes and make modifications as needed.
4. **Merge**: After the PR is approved and passes all checks, it will be merged by a maintainer.
    

## Contact

For any questions, reach out via the repository’s [Discussions](https://github.com/DGT-Network/dgt_zk_protocol/discussions) section or contact the maintainers.

* * *

Thank you for contributing to the DGT-ZK Protocol! We appreciate your efforts to improve the project and help create a secure, privacy-preserving protocol for distributed ledgers.