#!/usr/bin/env python3

import sys
from os import listdir, walk, getcwd
from os.path import isfile, join, isdir, expanduser, islink
import subprocess

def run(command):
    process = subprocess.Popen(command.split(), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    process.communicate()
    return process.returncode

def run_with_output(command):
    process = subprocess.Popen(command.split(), stderr=subprocess.DEVNULL)
    process.communicate()
    return process.returncode

def home(f):
    return expanduser("~") + "/" + f

def ask(text, options, default):
    default_char = options[default].upper()
    ret = input(text)
    if len(ret) == 0:
        answer = default
    else:
        for i in range(len(options)):
            if options[i].upper() == ret.upper():
                answer = i
    return answer

sources = [f for f in listdir(".current") if f != ".config"]
config = [".config/"+f for f in listdir(".current/.config")]
for f in sources + config:
    if isfile("src/"+f) or isdir("src/"+f):
        if run("diff .current/"+f+" src/"+f) != 0:
            print(f+" has been modified.")
            again = True
            while again:
                update = ask("Do you want to update "+f+" ? [d/y/N] ", ['d','y','N'], 2)
                if update == 0:
                    run_with_output("diff .current/"+f+" src/"+f)
                    continue
                elif update == 1:
                    err = run("rm -rf src/"+f)
                    if err != 0:
                        print("Failed to remove src/"+f)
                        exit(1)
                    err = run("cp -r .current/"+f+" src/"+f);
                    if err != 0:
                        print("Failed to update "+f)
                        exit(1)
                    print("Updated "+f)
                again = False
