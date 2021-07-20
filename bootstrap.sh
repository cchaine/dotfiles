#!/usr/bin/env bash

dotfilesDir=$(pwd)
backup="${dotfilesDir}/backup"

function linkDotFile {
  if [ -z "${2}" ]; then
    dest="${HOME}/${1}"
  else
    dest="${HOME}/${2}"
  fi
  
  mkdir -p ${backup}    
  
  if [ -h ~/${1} ]; then
    # Existing symlink
    echo "Removing existing symlink: ${dest}"
    rm ${dest}

  elif [ -f "${dest}" ]; then
    # Exiting file
    echo "Backing up existing file: ${dest}"
    mv ${dest} ${backup}/${1}

  elif [ -d "${dest}" ]; then
    # Existing dir
    echo "Backing up existing dir: ${dest}"
    mv ${dest} ${backup}/${1}
  fi

  echo "Creating new symlink: ${dest}"
  ln -s ${dotfilesDir}/${1} ${dest}
}

function unlinkDotFile {
  if [ -h ${HOME}/${1} ]; then
    rm ${HOME}/${1}
    echo "Removing ${HOME}/${1}"
  fi

  if [ -f "${backup}/${1}" ];then 
    mv ${backup}/${1} ${HOME}/${1}
    echo "Restoring ${1}"
  elif [ -d "${backup}/${1}" ]; then
    mv ${backup}/${1} ${HOME}/${1}
    echo "Restoring ${1}"
  fi
}

function printUsage {
  echo "Usage: $0 [set|reset]"
}

if [ $# -ne 2 ]; then
  if [ "$1" == "set" ]; then
    linkDotFile .vim
    linkDotFile .vimrc

    if [ "$OSTYPE" == "darwin" ]; then
      linkDotFile .bash_profile
      source ~/.bash_profile
    else
      linkDotFile .bash_profile .bashrc
      source ~/.bashrc
    fi 

    linkDotFile .tmux.conf

    linkDotFile .env

    linkDotFile .config
  elif [ "$1" == "reset" ]; then
    unlinkDotFile .vim
    unlinkDotFile .vimrc

    if [ "$OSTYPE" == "darwin" ]; then 
      unlinkDotFile .bash_profile
    else
      unlinkDotFile .bashrc
    fi

    unlinkDotFile .tmux.conf

    printf "\n\n"
    echo "Run the following command to reset the terminal :"
    if [ -f ${HOME}/.bashrc ]; then
      printf "\n\tsource ${HOME}/.bashrc\n\n"
    else
      printf "\n\tsource /etc/skel/.bashrc\n\n"
    fi

    unlinkDotFile .env

    unlinkDotFile .config
  else
    printUsage
  fi
else
  printUsage
fi

