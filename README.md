# GUHS
⚠️ WIP project ⚠️

GRUB UEFI HTTP Selector, configure your boot order externaly via web server.

## Why GUHS could be useful?
* Integrate it in your home automation system: "OK Google, start living room PC with Ubuntu".
* Configure it manually which target to boot before you start the computer.
* Schedule when you prefer to boot your targets depending on calendar.

## Requirements
* To have GRUB with UEFI.
* Ethernet connection available.
* Deploy the web server somewhere where it will be available and reachable for the PC network. (IE: Raspberry PI)
* Docker for the web server OS

## What does include
* GUHS CLI for target machine with GRUB.
* GUHS HTTP web server with exposed API and simple frontend.
