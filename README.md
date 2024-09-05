<div align="center">

# Frost Go

</div>

## About
This is a search engine made using python.

# Contribution Guidelines

When contributing to `Frost GO`, whether on GitHub or in other community spaces:

- Be respectful, civil, and open-minded.
- Before opening a new pull request, try searching through the [issue tracker](https://github.com/IBK2024/frost-go/issues) for known issues or fixes.
- If you want to make code changes based on your personal opinion(s), make sure you open an issue first describing the changes you want to make, and open a pull request only when your suggestions get approved by maintainers.

## How to Contribute

### Prerequisites

In order to not waste your time implementing a change that has already been declined, or is generally not needed, start by [opening an issue](https://github.com/IBK2024/frost-go/issues/new/choose) describing the problem you would like to solve.
Also in order to modify the code you will need to install python to check:
```bash
  # macOS/linux
  python3 -V

  # Windows
  # You can also use `py -3 -V`
  python -V
```
It should return the python version if python is installed. The project uses version 3.10 and higher.

### Setup your environment locally
- First you will need to create a fork of the repository.
- Then clone the forked repository using the command but replacing`repository` with the url of the forked repository:
  ```bash
  git clone <repository>
  cd <repository>
  ```
- Then you will need to install poetry:
  ```bash
  # macOS/linux
  python3 -m pip install poetry

  # Windows
  # You can also use `py -3 -m pip install poetry`
  python -m pip install poetry
  ```
- Then you will need to make sure he virtual environment is created in the project folder:
  ```bash
  # macOS/linux
  python3 -m poetry config virtualenvs.in-project true

  # Windows
  # You can also use `py -3 -m poetry config virtualenvs.in-project true`
  python -m poetry config virtualenvs.in-project true 
  ```
- Then you will need to install dependencies:
  ```bash
  # macOS/linux
  python3 -m poetry install

  # Windows
  # You can also use `py -3 -m poetry install`
  python -m poetry install 
  ```
- Then you will need to create a `.env` file in the env directory with the content of `.env.example` file in the same directory
- Activate the virtual environment
  ```bash
  # macOS/linux
  python3 -m poetry shell

  # Windows
  # You can also use `py -3 -m poetry shell`
  python -m poetry shell
  ```
- If it does not automatically activate the virtual environment:
  ```bash
  # MacOS/linux
  source .venv/Scripts/activate

  # Windows
  .venv\Scripts\activate
  ```

### Implement your changes
Some commands to know. Make sure to activate the virtual environment first:
- To run the application:
  ```bash
  # macOS/linux
  poetry run python3 main.py

  # Windows
  # You can also use `poetry run py -3 main.py`
  poetry run python main.py
  ```
  > ⚠ Then, the development server will be started at http://127.0.0.1:5000/

  > ⚠ To view all the api routes go to http://127.0.0.1:5000/docs

- To run the bench mark of how fast the application is:
  ```bash
  # macOS/linux
  poetry run python3 performance_test.py

  # Windows
  # You can also use `poetry run py -3 performance_test.py`
  poetry run python performance_test.py
  ```
  If you want to see the performance visualy:
  ```bash
  poetry run python3 performance_test.py
  poetry run tuna assets/benchmark_result.prof
  ```
- To lint the application:
  ```bash
  poetry run mypy .
  poetry run pylint **/*.py
  ```
- To test the aplication:
  ```bash
  poetry run coverage run -m pytest @tests/tests.txt && poetry run coverage report -m
  ```

### When your done
Create a pull request