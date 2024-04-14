[![PyPI version](https://img.shields.io/pypi/v/vagrant-creator.svg?logo=pypi&logoColor=FFE873)](https://pypi.org/project/vagrant-creator/)
[![PyPI downloads](https://img.shields.io/pypi/dm/vagrant-creator.svg)](https://pypistats.org/packages/pypistats)
[![Licence](https://img.shields.io/github/license/hugovk/pypistats.svg)](LICENSE.txt)

# Vagrant Init Generator

## Overview

`vagrant-init-generator` is a command-line tool that simplifies the process of generating Vagrant `Vagrantfile` with custom configurations. It allows users to specify CPU, RAM, machine name, host name, IP address, forwarded ports, and provisioning commands easily through user-friendly prompts or default values.

## Features

- Generate `Vagrantfile` with custom configurations
- Interactive prompts for user input (CPU, RAM, machine name, host name, IP address, forwarded ports, provision commands)
- Support for specifying forwarded ports and provisioning commands
- Default values for skipped prompts
- Easy installation and usage

## Installation

To install `vagrant-creator`, you can use `pip`:

```bash
pip install vagrant-creator
```

## Usage

To generate a vagrant file, Run `vagrant-creator` to start the interactive setup and follow the steps as prompted to customize the file as required:

```bash
vagrant-creator
```

### Entering Information

- Pressing \`Enter\` will use the default value shown in parentheses.
- To add multiple forwarded ports or provisioning commands, follow the prompts.

#### Forwarded Ports

When prompted to add a forwarded port, enter `y` to add a port or `n` to skip.

- Guest Port: Enter the guest port number (default: 8080).
- Host Port: Enter the host port number (default: 8080).
- Auto Correct: Enable auto-correct (default: true). Enter `t` for true or `f` for false.

#### Provisioning Commands

When prompted to add a provisioning command, enter `y` to add a command or `n` to skip.

- Command: Enter the provisioning command (e.g., `sudo yum install ansible -y`).

### Example

Here's an example of the interactive setup:

```bash
$ vagrant-creator

===================================== Vagrant file generator =====================================
Enter vm box name (default: centos/7):
Enter CPU (default: 1):
Enter RAM in MB (default: 1024):
Enter Machine Name (default: default-machine):
Enter Host Name (default: localhost):
Enter IP Address (default: 192.168.33.10):
Do you want to add a forwarded port? [y (Yes) /n (No)]: y
Enter the guest port number (default: 8080):
Enter the host port number (default: 8080):
Enable auto correct? (default: true) [t (True) /f (False)]: t
Do you want to add a provisioning command? [y (Yes) /n (No)]: y
Enter the provisioning command (e.g., 'sudo yum install ansible -y'): sudo apt-get install ansible -y
Do you want to add a provisioning command? [y (Yes) /n (No)]: n
Vagrantfile generated successfully!
```

## License

This project is licensed under the MIT License. See `LICENSE` for more information.
