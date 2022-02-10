#!/usr/bin/env python3

# This file should be called from the Makefile

import sys
from os import listdir, walk, getcwd
from os.path import isfile, join, isdir, expanduser, islink
import subprocess

def usage():
    print("Usage: {} [install|restore]".format(sys.argv[0]))

def run(command):
    process = subprocess.Popen(command.split(), stderr=subprocess.DEVNULL)
    process.communicate()
    return process.returncode

def home(f):
    return expanduser("~") + "/" + f

def ask(text, default):
    default_char = "Y" if default else "N"
    ret = input(text)
    if len(ret) != 0 and ret.upper() == default_char:
        answer = default
    else:
        answer = not default
    return ret

if len(sys.argv) != 2:
    usage()
    exit(1)

command = sys.argv[1]

if command == "install":
    #
    # Copy files to a .current directory
    #
    sources = [f for f in listdir("src") if f != ".config"]
    config = [".config/"+f for f in listdir("src/.config")]
    for f in sources + config:
        # Check if the file is already in the current folder and is different from this one
        if isfile(".current/"+f) or isdir(".current/"+f):
            if run("diff src/"+f+" .current/"+f) != 0:
                # Ask the user if he wants to discard the changes
                print(f+" has been modified.")
                discard = ask("Would you like to discard your changes ? [y/N] ", False)
                if discard:
                    # Remove the file in the .current directory
                    err = run("rm .current/"+f)
                    if err != 0:
                        print("Error: failed to override "+f)
                        exit(1)
                    # Copy the new file to the .current directory
                    err = run("cp -r src/"+f+" .current/"+f)
                    if err != 0:
                        print("Error: failed to copy src/"+f+" to .current")
                        exit(1)
        else:
            # Copy the file to the .current directory
            err = run("cp -r src/"+f+" .current/"+f)
            if err != 0:
                print("Error: failed to copy src/"+f+" to .current")
                exit(1)

    #
    # Link files to the home directory
    #
    if isdir(home(".config")):
        sources = [f for f in listdir(".current") if f != ".config"]
        sources += [".config/" + f for f in listdir(".current/.config")]
    else:
        sources = [f for f in listdir(".current")]

    for f in sources:
        # Check if a file already exist in the home directory
        if islink(home(f)):
            # Remove previous symlink
            err = run("rm -rf "+home(f))
            if err != 0:
                print("Error: failed to remove previous symlink for "+f)
                exit(1)
        elif isfile(home(f)) or isdir(home(f)):
            # Backup the file to the .backup folder
            print("backup of " + f)
            err = run("mv " +home(f) + " .backup/"+f)
            if err != 0:
                print("Error: failed to backup "+f)
                exit(1)

        # Link the file to the home directory
        print("linking " + join(getcwd(), ".current/"+f) + " -> " + home(f))
        err = run("ln -s " + join(getcwd(), ".current/"+f) + " " + home(f))
        if err != 0:
            print("Error: failed to link "+f)
            exit(1)

    print("You can link X11 configuration with the following command :")
    print("\tln -s " + home("/.config/xorg/20-xorg-user.conf") + " /etc/share/X11/xorg.conf.d/20-xorg-user.conf")
elif command == "restore":
    sources = [f for f in listdir(".backup")]
    for f in sources:
        if islink(home(f)):
            # Remove symlink
            err = run("rm -rf "+home(f))
            if err != 0:
                print("Error: failed to remove symlink "+home(f))
                exit(1)

        # Move the backup back
        print("restoring "+f)
        err = run("mv .backup/"+f+" "+home(f))
        if err != 0:
            print("Error: failed to restore "+f)
else:
    print("Error: Unknown '{}' command".format(command))
    usage()
    exit(1)

