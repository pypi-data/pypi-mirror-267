# `archadeptcli` - ArchAdept Command Line Interface

[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/archadeptcli?logo=python&logoColor=white&style=for-the-badge)](https://pypi.org/project/archadept-cli)
[![PyPI](https://img.shields.io/pypi/v/archadeptcli?logo=pypi&color=green&logoColor=white&style=for-the-badge)](https://pypi.org/project/archadeptcli)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/ArchAdept/archadeptcli?logo=github&color=orange&logoColor=white&style=for-the-badge)](https://github.com/ArchAdept/archadeptcli/releases)
[![Operating Systems](https://img.shields.io/badge/os-linux%20%7C%20macOS%20%7C%20windows-yellow?style=for-the-badge)](https://github.com/ArchAdept/archadeptcli)
[![Architectures](https://img.shields.io/badge/arch-x86__64%20%7C%20arm64-purple?style=for-the-badge)](https://github.com/ArchAdept/archadeptcli)
[![PyPI - License](https://img.shields.io/pypi/l/archadeptcli?color=03cb98&style=for-the-badge)](https://github.com/ArchAdept/archadeptcli/blob/main/LICENSE.md)

Command line interface for building, running, debugging, and disassembling the
ArchAdept training course example projects.


## Introduction

Many of the lessons on our training courses involve practical coding exercises
for you to complete, or example code snippets for you to modify and run yourself
on simulated hardware.

One challenge often faced by newcomers to bare metal ARM architecture development
like this is getting all of the necessary tools installed and configured, especially
when accounting for all the differences between the Mac, Linux, and Windows
operating systems.

The ArchAdept CLI solves this issue by leveraging Docker containers "under-the-hood"
to provide a consistent environment that is preloaded and preconfigured with all
of the tools required to build, run, debug, and disassemble the ArchAdept training
course example projects, while abstracting away all of the complexities of managing
the actual Docker containers themselves.


## Installation

Tested as working on:

| Operating System  | Version                    | x86_64 | arm64 |
| ----------------- | -------------------------- | ------ | ----- |
| Mac               | macOS Sonoma 14.1          | TODO   | 🟢    |
| Windows 10        | Windows 10 Enterprise 22H2 | 🟢     | N/A   |
| Windows 11        | TODO                       | TODO   | TODO  |
| Linux             | Ubuntu 22.04 LTS           | 🟢     | TODO  |

Click to expand for your operating system:
<details>
<summary>macOS instructions</summary>

1. Install Docker Desktop by following the instructions at: https://www.docker.com/products/docker-desktop/

2. Install Homebrew by following the instructions at: https://brew.sh

3. Install Python 3.8 or newer via Homebrew:
```console
$ brew search python3
$ brew install python@3.12  # Chosen from results of `brew search python3`
```

4. Install `pipx` via Homebrew:
```console
$ brew install pipx
```

5. Let pipx correctly update your `$PATH`:
```console
$ pipx ensurepath
```

6. From a new terminal window, install the ArchAdept CLI via `pipx`:
```console
# From a new terminal window!
$ pipx install archadeptcli
```

7. Ensure the ArchAdept CLI is installed and accessible:
```console
$ archadept --help
```

8. To update the ArchAdept CLI in future:
```console
$ pipx upgrade archadeptcli
```

> [!TIP]
> Run `archadept pull` now to download the backend Docker image ahead of time; this may take a few minutes to complete.

Proceed to [usage](#usage).
</details>

<details>
<summary>Windows instructions</summary>

1. Install Docker Desktop by following the instructions at: https://www.docker.com/products/docker-desktop/

2. Install Python 3.8 or newer from https://www.python.org/downloads/windows/

> [!WARNING]
> We strongly recommend *not* using the Microsoft Store to install Python 3; please download and install from the official Python website.
>
> Furthermore, during installation, please ensure you tick the checkbox to add Python to your `$PATH`.

3. Install `pipx` via `pip`:
```console
PS> py -3 -m pip install --user pipx
```

4. Let `pipx` correctly update your `$PATH`:
```console
PS> py -3 -m pipx ensurepath
```

5. From a new terminal window, install the ArchAdept CLI via `pipx`:
```console
# From a new terminal window!
PS> py -3 -m pipx install archadeptcli
```

6. Ensure the ArchAdept CLI is installed and accessible:
```console
PS> archadept --help
```

7. To update the ArchAdept CLI in future:
```console
PS> py -3 -m pipx upgrade archadeptcli
```

> [!TIP]
> Run `archadept pull` now to download the backend Docker image ahead of time; this may take a few minutes to complete.

Proceed to [usage](#usage).
</details>

<details>
<summary>Linux instructions</summary>

1. Install Docker Desktop by following the instructions at: https://www.docker.com/products/docker-desktop/

2. Use your distribution's package manager to check the installed version of
   Python 3, for example on Ubuntu using `apt`:
```console
$ apt show python3 | grep Version
Version: 3.10.6-1~22.04
```

3. If necessary, use your distribution's package manager to upgrade to Python 3.8
   or newer, for example on Ubuntu using `apt`:
```console
$ sudo apt upgrade python3
```

4. Install `pipx` via `pip`:
```console
$ python3 -m pip install --user pipx
```

5. Let `pipx` correctly update your `$PATH`:
```console
$ python3 -m pipx ensurepath
```

6. From a new terminal window, install the ArchAdept CLI via `pipx`:
```console
# From a new terminal window!
$ python3 -m pipx install archadeptcli
```

7. Ensure the ArchAdept CLI is installed and accessible:
```console
$ archadept --help
```

8. To update the ArchAdept CLI in future:
```console
$ python3 -m pipx upgrade archadeptcli
```

> [!TIP]
> Run `archadept pull` now to download the backend Docker image ahead of time; this may take a few minutes to complete.

Proceed to [usage](#usage).
</details>

## Usage

The following commands are available:

| Command | Description                                                                |
| ------- | -------------------------------------------------------------------------- |
| `make`  | Invoke an ArchAdept project Makefile.                                      |
| `run`   | Run an ArchAdept project on a QEMU simulation of real hardware.            |
| `debug` | Attach debugger to an ArchAdept project running on a live QEMU simulation. |
| `pull`  | Pull the latest backend Docker image.                                      |
| `prune` | Cleanup any lingering Docker containers.                                   |


### `make`

```console
usage: archadept make [-h] [-v] [-p PROJECT] [-i IMAGE] [-t TAG] [TARGET]

Invokes an ArchAdept example project Makefile.

options:
  -h, --help  show this help message and exit
  -v          enable logging verbose debug messages

command-specific options:
  -p PROJECT    path to the ArchAdept project (default: current directory)
  -i IMAGE      override Docker image repository (default: archadept/archadeptcli-backend)
  -t TAG        override Docker image tag (default: latest)
  -S            interleave source with disassembly (only available for 'dis' target)
  -O {0,1,2,3}  override project's default optimization level

command-specific positional arguments:
  TARGET      Makefile target from {all,clean,rebuild,dis,syms} (default: all)
```

The following targets are defined by all ArchAdept training course example
project Makefiles:
 - `all` builds the project.
 - `clean` deletes all of a project's build artifacts.
 - `rebuild` performs a clean build, equivalent to `clean` followed by `all`.
 - `dis` rebuilds the project, then disassembles it.
 - `syms` rebuilds the project, then dumps its symbol table.
 - `sects` rebuilds the project, then dumps its section headers.

Note: The `dis` target accepts the following optional flags:
 - `-S` enables interleaving source code with the disassembly.


### `run`

```console
usage: archadept run [-h] [-v] [-p PROJECT] [-i IMAGE] [-t TAG] [-s]

Runs an ArchAdept example project on a simulated Raspberry Pi 3b using QEMU.

options:
  -h, --help  show this help message and exit
  -v          enable logging verbose debug messages

command-specific options:
  -p PROJECT  path to the ArchAdept project (default: current directory)
  -i IMAGE    override Docker image repository (default: archadept/archadeptcli-backend)
  -t TAG      override Docker image tag (default: latest)
  -s          spawn GDB debug server and pause simulation at kernel entrypoint
```

To quit the QEMU simulation, press `Ctrl-a` followed by `x`.


### `debug`

```console
usage: archadept debug [-h] [-v] CONTAINER

Attaches an LLDB debug session to a live QEMU simulation started by `archadept run -s`.

options:
  -h, --help  show this help message and exit
  -v          enable logging verbose debug messages

command-specific positional arguments:
  CONTAINER   container in which the QEMU simulation is running, as given by `archadept run`
```


### `pull`

```console
usage: archadept pull [-h] [--version] [-v] [-i IMAGE] [-t TAG]

Pulls the latest ArchAdept CLI backend Docker image from DockerHub.

options:
  -h, --help  show this help message and exit
  --version   display archadeptcli version info
  -v          enable logging verbose debug messages

command-specific options:
  -i IMAGE    override Docker image repository (default: archadept/archadeptcli-backend)
  -t TAG      override Docker image tag (default: latest)
```


### `prune`

```console
usage: archadept prune [-h] [-v]

Cleans up any lingering Docker containers from previous ArchAdept CLI invocations.

options:
  -h, --help  show this help message and exit
  -v          enable logging verbose debug messages
```

