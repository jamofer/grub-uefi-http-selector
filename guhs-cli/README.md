# GUHS CLI
⚠️ WIP project ⚠️

GRUB UEFI HTTP Selector CLI. Configure your GRUB environment pointing to your deployed GUHS server. 

## Requirements
* python3.
* Linux OS with UEFI GRUB as bootloader.

## Installation
```shell
pip3 install guhs-cli
```

## Usage
### Interactive shell configuration
```shell
$ guhs-cli configure
GUHS HTTP server hostname/ip? <<user input>>
Available boot targets:
  1. Ubuntu
  2. Ubuntu2
  3. Windows XP
Default target? [1] <<user input>>
```

### Show current configuration
```shell
$ guhs-cli show
GUHS status: ENABLED
GUHS HTTP server: 192.168.1.1:8080
Default target: 1. Ubuntu
Boot selection timeout: 10
```

### Show boot targets
```shell
$ guhs-cli ls
1. Ubuntu
2. Ubuntu2
3. Windows XP
```

### Set/Get configuration
```shell
## Set GUHS HTTP server
$ guhs-cli set server=192.168.1.1:80

## Get GUHS HTTP server
$ guhs-cli get server
192.168.1.1:80

## Set boot order
$ guhs-cli set default-target=1
$ guhs-cli set default-target=Ubuntu
$ guhs-cli set default-target=Windows XP

## Get boot order
$ guhs-cli get default-target
1
```

### Remove GUHS from GRUB
```shell
$ guhs-cli uninstall
$ guhs-cli show
GUHS was not found in the system. Did you configure it with "guhs-cli configure"?
```