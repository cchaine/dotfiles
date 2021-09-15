# dotfiles

This repository contains every configuration files needed to setup my development environement.

## install

There are multiple targets that can be installed :
- `system` is the default, which contains configuration files for any *terminal based* program.
- `i3` is a target that can be installed when using the `i3 window manager`

Installing a target is done with :
```bash
make <target>
```

## local changes

Local changes can be made by updating the files as you would with any local configuration files. During the installation process, files for the target are copied to a *current* directory. Changes can be made there without impacting the original files.

## resetting the environment

When working on machine that isn't your own, you can reset the environment as it was before by using the command :
```bash
make reset
```
