#!/usr/bin/env bash

dotfilesDir=$(pwd)

function linkDotFile {
  dest="${HOME}/${1}"
  dateStr=$(date +%Y-%m-%d-%H%M)
  backup="dotfileBackup${dateStr}/"
  
  if [ -h ~/${1} ]; then
    # Existing symlink
    echo "Removing existing symlink: ${dest}"
    rm ${dest}

  elif [ -f "${dest}" ]; then
    # Existing file
    echo "Backing up existing file: ${dest}"
    mv ${dest}{,.${dateStr}}

  elif [ -d "${dest}" ]; then
    # Existing dir
    echo "Backing up existing dir: ${dest}"
    mv ${dest}{,.${dateStr}}
  fi

  echo "Creating new symlink: ${dest}"
  ln -s ${dotfilesDir}/${1} ${dest}
}

linkDotFile .vim
linkDotFile .vimrc

linkDotFile .bash_profile
source ~/.bash_profile

linkDotFile .hushlogin
