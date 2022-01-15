# GUHS

GRUB UEFI HTTP Selector, configure your boot order externaly via web server.

You can install GUHS in your system using [GUHS CLI](https://github.com/jamofer/guhs-cli) once you deployed
the GUHS Server somewhere the host machine could reach it using HTTP.

## Why GUHS could be useful?
* Integrate it in your home automation system: "OK Google, start living room PC with Ubuntu".
* Configure it manually which target to boot before you start the computer.
* Schedule when you prefer to boot your targets depending on calendar.

## Requirements
* To have GRUB with UEFI.
* Network card available.
* A reachable server for the PC network. (IE: Raspberry PI)

## What does include
* GUHS CLI for target machine with GRUB.
* GUHS HTTP web server with exposed API and simple frontend.
