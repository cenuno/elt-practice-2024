#!/bin/bash

# Path to the prepare-commit-msg hook script
HOOK_SCRIPT_PATH="dev/prepare-commit-msg"

# Check if the hook script exists
if [ ! -f "$HOOK_SCRIPT_PATH" ]; then
    echo "Error: prepare-commit-msg hook script not found at $HOOK_SCRIPT_PATH"
    exit 1
fi

# Determine the .git/hooks directory path
GIT_HOOKS_DIR=".git/hooks"

# Check if the .git/hooks directory exists
if [ ! -d "$GIT_HOOKS_DIR" ]; then
    echo "Error: .git/hooks directory not found. Are you in the root of your Git repository?"
    exit 1
fi

# Check if a prepare-commit-msg file already exists in .git/hooks
if [ -f "$GIT_HOOKS_DIR/prepare-commit-msg" ]; then
    # Prompt the user if they wish to overwrite the existing file
    read -p "A prepare-commit-msg file already exists in .git/hooks/. Do you want to overwrite it? (y/n): " overwrite_response
    if [ "$overwrite_response" != "y" ]; then
        echo "Aborting setup. No changes made."
        exit 0
    fi
fi

# Copy the hook script to the .git/hooks directory with preserving permissions
cp -p "$HOOK_SCRIPT_PATH" "$GIT_HOOKS_DIR/prepare-commit-msg"

# Verify that the hook script was copied successfully
if [ $? -eq 0 ]; then
    # Check if the script file is executable
    if [ ! -x "$GIT_HOOKS_DIR/prepare-commit-msg" ]; then
        # Make the script file executable
        chmod +x "$GIT_HOOKS_DIR/prepare-commit-msg"
        echo "File '$GIT_HOOKS_DIR/prepare-commit-msg' is now executable."
    else
        echo "File '$GIT_HOOKS_DIR/prepare-commit-msg' is already executable."
    fi
    echo "prepare-commit-msg hook has been set up successfully."
else
    echo "Error: Failed to set up prepare-commit-msg hook."
    exit 1
fi

exit 0