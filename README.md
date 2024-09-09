# elt-practice-2024
Practice repo for learning about ELT in 2024

## Appendix

Below is context about the repo to help you in your understanding of the repo.

### Dependencies

This project assumes you have the following:

* Docker Desktop
    + You can view the exact version this repo used at time of creation here:
      | Resource | Version |
      | :---: | :---: |
      | Docker Desktop | 4.33.0 |
      | Engine | 27.1.1 |
      | Compose | 2.29.1-desktop.1 |
      | Credential Helper | 0.8.2 |
      | Kubernetes | 1.30.2 |
* A Unix-like operating system
* Ability to run commands from the command line, specifically entering a docker container from the command line.
* You've copied all of the `*_env_copy` files and created new files without the `_copy` suffix. Example command of `cp .pgadmin_env_copy .pgadmin`
* Within each of your personal `*_env` files, you've modified the credentials to be that of your own.


### Use of Poetry for Python Packaging & Depdency Management

This project uses [Poetry](https://python-poetry.org/) to build, package and track the dependencies used. You can learn more by reading through this [tutorial](https://realpython.com/dependency-management-python-poetry/).

#### Sanity check that `poetry` was installed in container correctly

You should be able to spin up the `python` container by running `sh run.sh`. Afterwards, try running `docker exec -it python poetry env info` to verify that you're seeing what I'm seeing:

```text
Virtualenv
Python:         3.12.5
Implementation: CPython
Path:           /opt/venv
Executable:     /opt/venv/bin/python
Valid:          True

Base
Platform:   linux
OS:         posix
Python:     3.12.5
Path:       /usr/local
Executable: /usr/local/bin/python3.12
```

### Setting up prepare-commit-msg

This repo adopts a practice of prepending the branch name to our commits to easily sift through changes by including a `prepare-commit-msg` hook in this repository.

Follow these steps to set up the `prepare-commit-msg` hook on your local machine:

1. Ensure you are in the root of this project repo

2. Run the provided script to automatically install the `prepare-commit-msg hook`:

```sh
sh dev/setup_prepare_commit_msg_hook.sh
```

### Pull requests will lint & test feature branches via GitHub Actions

There exists a `.github/workflows/lint.yaml` file that ensures all changes from feature branches that wish to make it to `main` branch, along with `staging` branch or `release/**` branches, pass a series of linters and tests.

See `.github/workflows/README.md` for more information about GitHub Actions.

### Setting up pre-commit hooks

> Git hook scripts are useful for identifying simple issues before submission to code review. We run our hooks on every commit to automatically point out issues in code such as missing semicolons, trailing whitespace, and debug statements. By pointing these issues out before code review, this allows a code reviewer to focus on the architecture of a change while not wasting time with trivial style nitpicks. - [Source: pre-commit.com](https://pre-commit.com/)

Please follow the quick start [guide](https://pre-commit.com/#quick-start) to ensure that you can use the pre-commit hooks found in this repo.

#### Run `pre-commit` within Docker container

The `python` Docker container comes with all Poetry packages installed for you, including the hooks used in `pre-commit`. Therefore, please consider running `pre-commit run --all-files` to ensure that your code passes lints and tests before submitting a PR.
