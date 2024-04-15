#!/bin/zsh

# This ZSH plugin reads the text from the current buffer
# and uses a Python script to complete the text.

# If zshgpt is not installed...
if (( $+commands[zshgpt] )) then
    echo "zshgpt already installed"
    # ...try to install with pipx...
elif (( $+commands[pipx] )) then
    pipx install zshgpt
else
    # ... or normal pip.
    python -m pip install zshgpt
fi

create_completion() {
    # Get the text typed until now.
    text=${BUFFER}
    completion=$(zshgpt $text )
    # Add completion to the current buffer.
    BUFFER="${text}"$'\n'"${completion}"
    # Put the cursor at the end of the line.
    CURSOR=${#BUFFER}
}

# Bind the create_completion function to a key.
zle -N create_completion

setopt interactivecomments
bindkey '^G' create_completion
