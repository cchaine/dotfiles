############################
# aliases
############################

alias grep='grep --color=auto'

alias mutt='neomutt'

# Enable colors in ls on linux
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
  alias ls='ls --color'
fi
alias ll='ls -alhF'

############################
# environment variables 
############################

export CLICOLOR=1
# ls order by name
export LC_COLLATE=C
# silence macos default zsh
export BASH_SILENCE_DEPRECATION_WARNING=1

# load environment variables
source ~/.env

txtblk='\[\e[0;30m\]' # Black - Regular
txtred='\[\e[0;31m\]' # Red
txtgrn='\[\e[0;32m\]' # Green
txtylw='\[\e[0;33m\]' # Yellow
txtblu='\[\e[0;34m\]' # Blue
txtpur='\[\e[0;35m\]' # Purple
txtcyn='\[\e[0;36m\]' # Cyan
txtwht='\[\e[0;37m\]' # White
bldblk='\[\e[1;30m\]' # Black - Bold
bldred='\[\e[1;31m\]' # Red
bldgrn='\[\e[1;32m\]' # Green
bldylw='\[\e[1;33m\]' # Yellow
bldblu='\[\e[1;34m\]' # Blue
bldpur='\[\e[1;35m\]' # Purple
bldcyn='\[\e[1;36m\]' # Cyan
bldwht='\[\e[1;37m\]' # White
unkblk='\[\e[4;30m\]' # Black - Underline
undred='\[\e[4;31m\]' # Red
undgrn='\[\e[4;32m\]' # Green
undylw='\[\e[4;33m\]' # Yellow
undblu='\[\e[4;34m\]' # Blue
undpur='\[\e[4;35m\]' # Purple
undcyn='\[\e[4;36m\]' # Cyan
undwht='\[\e[4;37m\]' # White
bakblk='\[\e[40m\]'   # Black - Background
bakred='\[\e[41m\]'   # Red
badgrn='\[\e[42m\]'   # Green
bakylw='\[\e[43m\]'   # Yellow
bakblu='\[\e[44m\]'   # Blue
bakpur='\[\e[45m\]'   # Purple
bakcyn='\[\e[46m\]'   # Cyan
bakwht='\[\e[47m\]'   # White
txtrst='\[\e[0m\]'    # Text Reset

PROMPT_COMMAND=__prompt_command

nameColor="${bldpur}"
# Red name for root
if [ "${UID}" -eq "0" ]; then
  nameColor="${bldred}"
fi
pathColor="${bldblk}"

__prompt_command() {
  local exit="$?"
  PS1=""

  if [ $exit != 0 ]; then
    PS1+="${txtred}${exit} "
  fi


  PS1+="${nameColor}\u${pathColor}:\$PWD${txtrst}> "
}

############################
# git completion 
############################

if [ ! -f ~/.git-completion.bash ]; then
  curl https://raw.githubusercontent.com/git/git/master/contrib/completion/git-completion.bash -o ~/.git-completion.bash
  if [ $? -ne 0 ]; then
    echo "Error downloading .git-completion.bash"
  fi
fi

if [ -f ~/.git-completion.bash ]; then
  . ~/.git-completion.bash
fi
