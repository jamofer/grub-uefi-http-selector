# GUHS

GRUB UEFI HTTP Selector, configure your boot order externaly via web server.

## How it works?

![image](https://user-images.githubusercontent.com/9080627/151705197-012a94e1-802b-48ed-8c5c-fbd421deb953.png)

You need to install [GUHS Server](https://github.com/jamofer/guhs-server) in a external machine and then
install [GUHS CLI](https://github.com/jamofer/guhs-cli) in your system pointing to the deployed server.

## Why GUHS could be useful?
GUHS exposes via REST API it's configuration, so you can automate which target do you want to boot the next time you power on your computer. Even you can create a frontend/mobile APP or a home-assistant integration in order to control the boot configuration and combine it with Wake On Lan.

## Requirements
* Python3.7 or above for both CLI and Server APPs.
* Root permissions for the CLI.
* To have GRUB with UEFI and network stack enabled.
* If you use secureboot you need to have HTTP module signed.
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
## Known issues
### Secure boot
By default GRUB doesn't have HTTP module signed, you can setup in your UEFI configuration secureboot to "Other OS" in order to solve this.

### Network stack on GRUB
I just tried on my own computer and VirtualBox
* Asus ROG STRIX X570-I GAMING: It sometimes doesn't initialize network stack, disabling fastboot works better but sometimes network stack does not initialize.
* VirtualBox UEFI: Works perfect.
