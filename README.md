# AeroEase Backend

This project uses `pyenv` to manage the depenedencies.
You can install the same with `python3 -m pip install --user pipenv`

## Using pipenv

- Install a dependency `XYZ` with `pipenv install XYZ`
- To activate this project's virtualenv, run `pipenv shell`
- Run a command inside the virtualenv of this project with `pipenv run`

## Running the project

```bash
pipenv install
pipenv run python main.py
```

The server would be deployed on the port `5000` on the localhost network.
