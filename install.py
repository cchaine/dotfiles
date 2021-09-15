import sys
import os.path
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



if len(sys.argv) < 4:
	print("Usage: command dst_dir selected_targets ...")
	exit(-1)

# Check if the command is known
command = sys.argv[1]
if command not in ["apply", "reset"]:
	print("The specified command doesn't belong to [\"apply\", \"reset\"]")
	exit(-1)
# Check if the dst_dir exists
dst_dir = sys.argv[2]
if not os.path.isdir(dst_dir):
	print("The specified directory doesn't exist")
	exit(-1)
# Check if the selected targets are known
selected_targets = sys.argv[3:]
if not all(target in available_targets for target in selected_targets):
	print("The specified targets doesn't belong to", str([key for key in available_targets]))
	exit(-1)  

def reset_target(name):
	print("Reseting target", name)

def apply_target(name):
	prefix, files = available_targets[target]
	# Create the destination prefix if it doesn't exist
	target_dst = os.path.join(dst_dir, prefix)
	if not os.path.isdir(target_dst):
		os.mkdir(target_dst)

	print("Applying target", name)

	# Copy the files to the destination prefix
	for f in files:
		filename = f.split("/")[-1]
		file_dst = os.path.join(target_dst, f.split("/")[-1])

		print("\tCopying file", filename, "to", target_dst)

		command = "cp -rf " + f + " " + file_dst
		process = subprocess.Popen(command.split())
		# If the command didn't work, reset
		process.communicate()
		if process.returncode != 0:
			print("\tError copying file " + f + " to " + file_dst)
			reset_target(name)
			exit(-1)

	print("Linking target", name)

	home = os.path.expanduser("~")
	# Link the files to the home directory
	for f in files:
		# Check if the prefix exists
		prefix_dst = os.path.join(home, prefix)
		if not os.path.isdir(prefix_dst):
			print("\tCreating folder", prefix_dst)
			os.mkdir(prefix_dst)
		
		link_dst = os.path.join(prefix_dst, f.split("/")[-1])
		# Check if the file already exists
		if os.path.isfile(link_dst):
			print(link_dst)
	

for target in selected_targets:
	if command == "apply":
		apply_target(target)
	elif command == "reset":
		reset_target(target)
