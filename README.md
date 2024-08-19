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