import sys
import os.path
import os
import subprocess

# Set config files for each program
bash_files = ["bash/.bashrc", "bash/.env"]
vim_files = ["vim/.vimrc", "vim/.vim"]
i3_files = ["i3", "i3status"]

# Set individual targets with their path's prefix
system_target = ("", bash_files + vim_files)
i3_target = (".config", i3_files)

# Target dictionary
available_targets = {"system": system_target, "i3": i3_target}


if len(sys.argv) < 5:
    print("Usage: command dst_dir backup_dir selected_targets ...")
    exit(-1)

# Check if the command is known
command = sys.argv[1]
if command not in ["apply", "reset"]:
    print("The specified command doesn't belong to [\"apply\", \"reset\"]")
    exit(-1)
# Check if the dst_dir exists
dst_dir = sys.argv[2]
if not os.path.isdir(dst_dir):
    print("The specified destination directory doesn't exist")
    exit(-1)
# Check if the backup_dir exists
backup_dir = sys.argv[3]
if not os.path.isdir(backup_dir):
    print("The specified backup directory doesn't exist")
    exit(-1)
# Check if the selected targets are known
selected_targets = sys.argv[4:]
if not all(target in available_targets for target in selected_targets):
    print("The specified targets doesn't belong to", str([key for key in available_targets]))
    exit(-1)  

def run(command):
    process = subprocess.Popen(command.split(), stderr=subprocess.DEVNULL)
    process.communicate()
    return process.returncode

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# 
# Resets the environment from the backup files
#
def reset_target(name):
    prefix, files = available_targets[target]
    home = os.path.expanduser("~")
    for f in files:
        # Check if a link to the file exists
        filename = f.split("/")[-1]
        prefix_home = os.path.join(home, prefix)
        file_home = os.path.join(prefix_home, filename)
        if os.path.islink(file_home):
            # Remove it
            print("Remove", file_home)
            ret = run("rm -rf " + file_home)
            if ret != 0:
                print(bcolors.FAIL + "Failed to remove", file_home, bcolors.ENDC)
                continue
        # Check if there is a backup
        prefix_backup = os.path.join(backup_dir, prefix)
        file_backup = os.path.join(prefix_backup, filename)
        if os.path.isfile(file_backup) or os.path.isdir(file_backup):
            # Move it back in place
            print("Restore", file_backup)
            ret = run("mv " + file_backup + " " + file_home)
            if ret != 0:
                print(bcolors.FAIL + "Failed to restore the backup for", f, bcolors.ENDC)

#
# Apply a target to the environment
#
def apply_target(name):
    prefix, files = available_targets[target]
    # Create the destination prefix if it doesn't exist
    target_dst = os.path.join(dst_dir, prefix)
    if not os.path.isdir(target_dst):
        os.mkdir(target_dst)

    print(bcolors.BOLD + bcolors.OKBLUE + "Applying target", name, bcolors.ENDC)

    # Copy the files to the destination prefix
    for f in files:
        filename = f.split("/")[-1]
        file_dst = os.path.join(target_dst, f.split("/")[-1])

        # Check if the file already exists in the dst folder
        if os.path.isfile(file_dst) or os.path.isdir(file_dst):
            # Remove it
            print("\tRemoving previous file", file_dst)
            err = run("rm -rf " + file_dst)
            if err != 0:
                print(bcolors.FAIL + "\t Failed to remove previous file", file_dst)
                print(bcolors.FAIL + "Failed to apply target", name, bcolors.ENDC)
                return

        print("\tCopying file", filename, "->", target_dst)

        ret = run("cp -rf " + f + " " + file_dst)
        if ret != 0:
            print(bcolors.FAIL + "\tError copying file " + f + " to " + file_dst, bcolors.ENDC)
            print(bcolors.FAIL + "Failed to apply target", name, bcolors.ENDC)
            return

    print(bcolors.BOLD + bcolors.OKBLUE + "Linking target", name, bcolors.ENDC)

    home = os.path.expanduser("~")
    # Link the files to the home directory
    for f in files:
        filename = f.split("/")[-1]
        # Check if the prefix exists
        prefix_home = os.path.join(home, prefix)
        if not os.path.isdir(prefix_home):
            print("\tCreating folder", prefix_home)
            os.mkdir(prefix_home)
        
        file_home = os.path.join(prefix_home, filename)
        # Check if the file already exists and it is not a previous symlink
        if (os.path.isfile(file_home) or os.path.isdir(file_home)) and not os.path.islink(file_home):
            # Check if the prefix exists in the backup folder
            prefix_backup = os.path.join(backup_dir, prefix)
            if not os.path.isdir(prefix_backup):
                print("\tCreating folder", prefix, "in backup folder")
                os.mkdir(prefix_backup)

            file_backup = os.path.join(prefix_backup, filename)
            # Check if the file exists in the backup folder
            if os.path.isdir(file_backup) or os.path.isfile(file_backup):
                # Remove the previous backup
                print("\tRemoving previous backup for", file_home)
                ret = run("rm -rf " + file_backup)
                if ret != 0:
                    print(bcolors.FAIL + "\tFailed to remove previous backup", file_home, bcolors.ENDC)
                    print(bcolors.WARNING + "\tFile", f, "was not linked to the home directory", bcolors.ENDC)    
                    continue
            
            # Copy to the backup folder
            print("\tBackup", file_home)
            ret = run("mv " + file_home + " " + prefix_backup)
            if ret != 0:
                print(bcolors.FAIL + "\tFailed to backup", file_home, bcolors.ENDC)
                print(bcolors.WARNING + "\tFile", f, "was not linked to the home directory", bcolors.ENDC)    
                continue
        # Check if there is already a symlink
        if os.path.islink(file_home):
            # Remove the symlink 
            print("\tRemoving symlink", file_home)
            ret = run("rm -rf " + file_home)
            if ret != 0:
                print(bcolors.FAIL + "\tFailed to remove", file_home, bcolors.ENDC)
                print(bcolors.WARNING + "\tFile", f, "was not linked to the home directory", bcolors.ENDC)    
                continue

        # Link the file to home
        # We need an absolute path to do the linking
        absolute_target_dst = os.path.join(os.getcwd(), target_dst)
        absolute_file_dst = os.path.join(absolute_target_dst, filename)
        print("\tLinking", absolute_file_dst, "->", file_home)
        ret = run("ln -s " + absolute_file_dst + " " + file_home)
        if ret != 0:
            print(bcolors.FAIL + "\tFailed to create symlink from", file_dst, "->", file_home, bcolors.ENDC)
            continue

    print(bcolors.BOLD + bcolors.OKGREEN + "Successfully applied target", name, bcolors.ENDC)

for target in selected_targets:
    if command == "apply":
        apply_target(target)
    elif command == "reset":
        reset_target(target)
