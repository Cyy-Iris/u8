# Automodelling
## Introduction

Automodelling of CC contracts is a long-awaited feature allowing to accelerate the tedious and error-prone process of creating CC projects manually.
Aiming to provide a copilot approach to the CC modelling, the automodelling feature is based on the following principles:
- The user provides a PDF of the insurance contract to be modelled
- The PDF is parsed and the information is extracted
- The extracted information is subject to user review and correction
- The corrected information is used to create a draft CC project
- The user reviews the draft CC project and makes the necessary corrections

Current target is to provide an acceleration of the CC modelling process. The automodelling feature is not intended to provide a complete CC project, but rather to provide a draft CC project that can be used as a starting point for the CC modelling.

Data will be collected over time and used to improve the automodelling feature until full automation can be achieved.

## Local development

### Prerequisites

1. python 3.11.x

We recommend using pyenv as the `.python-version` file in the repo will allow pyenv to automatically download and install the exact same version of python for everyone.

```bash
# prefered approach is to use pyenv
brew install pyenv
# [pyenv shell setup](https://github.com/pyenv/pyenv#set-up-your-shell-environment-for-pyenv)
# for zsh:
echo 'export PYENV_ROOT="$HOME/.pyenv"' >> ~/.zshrc
echo 'command -v pyenv >/dev/null || export PATH="$PYENV_ROOT/bin:$PATH"' >> ~/.zshrc
echo 'eval "$(pyenv init -)"' >> ~/.zshrc
```

If for some reason you can't or don't want to use pyenv then simply install python 3.11 using your preferred mean. As an example you could use brew:

```bash
# alternatively you can just install python 3.11 with brew
brew install python@3.11
```

2. poetry

```bash
brew install poetry
```

3. poppler (dependency for pdftotext)

```bash
brew install poppler
```

### Setup

1. Clone the repository

```bash
git clone git@github.com:AXATechLab/unit8-experimental.git
```

2. Install the virtual environment with poetry

```bash
cd unit8-experimental
poetry install

# enter a shell within the .venv created:
poetry shell

# run a command within the shell:
poetry run ...

```

3. Set extensions in VS Code to work with the provided .vscode/settings.json

* go in the extensions tab in vscode
* search for @recommended
* install all the workspace recommendations

### Adding new dependencies

New package depedencies can be added using poetry commands.

```bash
# adding a regular package used in all env:
poetry add <package-name>

# adding a package only used in dev:
poetry add -G dev <package-name>
```

### Run

Overall process is file-based, and local development should rely on local filesystem.

#### Run Airflow Standalone

Airflow come with a standalone version running on sqlite which makes it easy to test your pipeline and wrapped task locally directly within the poetry env.

1. `cd unit8-experimental`
2. `poetry install --with standalone`
3. `make airflow_standalone`

Airflow will create a folder .airflow in your folder that will be used to store everything related to airflow (logs, sqlite db, ...).
It will also start the webserver that you can visit at `http://localhost:8080`.
The username will be admin and password defined in `.airflow/standalone_admin_password.txt`.


#### Run with Docker Compose

The docker compose version is much closer to prod as it builds an image with the required dependencies for running the tasks.

1. `make airflow_docker`
2. You can now use airflow on [localhost](http://localhost:8080).
3. Credentials are `airflow:airflow`
4. DAGs are hot-reloaded from `dags/`

## Architecture

### Overview

The automodelling feature is based on the following components:
- Airflow for the orchestration of the automodelling process
- Python packages for the implementation of the automodelling steps
- Local filesystem for the storage of the automodelling data

### Airflow

Airflow is used to orchestrate the automodelling process. The automodelling process is implemented as a DAG (Directed Acyclic Graph) in Airflow. The DAG is composed of the following steps:

1. PDF parsing
2. Data extraction
3. Data correction
4. CC project creation
