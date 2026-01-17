# Imgor

## Table of content
- [About the project](#about-the-project)
- [Installation](#installation)
  - [Creating a virtual environment](#creating-a-virtual-environment)
  - [Activating the virtual environment](#activating-the-virtual-environment)
  - [Installing requirements](#installing-requirements)
- [Uninstall](#uninstall)
  - [Remove installed dependencies](#remove-installed-dependencies)
  - [Delete directories and files](#delete-directories-and-files)
- [Formatting the code](#formatting-the-code)

## About the project
Imgor, is an image viewer and editor used mainly for digital image processing.
Currently, it is only a simple image viewer, meaning that we can only load and view images.

## Installation

Below, are the instructions for creating and activating a virtual environment
and installing the necessary dependencies from a requirements.txt file.

### Creating a virtual environment

```shell
python -m venv .venv
```

### Activating the virtual environment

```shell
.venv/Scripts/activate
```

### Installing requirements
```shell
pip install -r requirements.txt
```

## Uninstall

### Remove installed dependencies.

```shell
pip uninstall -r requirements.txt

```

### Delete directories and files

**Warning**: This will delete all the files and directories inside the current directory.
Use with caution.

```shell
rm -rf .
```

## Formatting the code

We can format our code for better readability and maintenance by running the
following command. We use the **black** formatter. More information about black,
can be found [here](https://black.readthedocs.io/en/stable/).

```shell
black **/*.py
```

## Checking for errors
We can and should check for warnings and errors in our code using **pylint** by running the following command.
More information about pylint can be found [here](https://pylint.readthedocs.io/en/stable/index.html#).
```shell
pylint **/*.py
```