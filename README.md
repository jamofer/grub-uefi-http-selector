# GUHS

GRUB UEFI HTTP Selector, configure your boot order externaly via web server.

You can install GUHS in your system using [GUHS CLI](https://github.com/jamofer/guhs-cli) once you deployed
the [GUHS Server](https://github.com/jamofer/guhs-server) in other machine.

## Why GUHS could be useful?
* Integrate it in your home automation system: "OK Google, start living room PC with Ubuntu".
* Configure it manually which target to boot before you start the computer.
* Schedule when you prefer to boot your targets depending on calendar.

## Requirements
* Python3.7 or above for both CLI and Server APPs.
* Root permissions for the CLI.
* To have GRUB with UEFI.
* Network card available.
* A second machine to deploy GUHS Server. (IE: Raspberry PI)

## How to install
### Install and deploy GUHS server
```shell
# Install the web server
pip3 install guhs-server

# Run it in background
nohup guhs-server &
```

### Install GUHS in GRUB
```shell
# Install it in your desirable GRUB system
sudo pip3 install guhs-cli

# Install GUHS in your GRUB bootloader
$ guhs-cli install
GUHS Server hostname/ip? <<user input>>
Available boot targets:
  1. Ubuntu
  2. Ubuntu2
  3. Windows XP
Default target? <<user input>>
Boot selection timeout? <<user_input>>
```
