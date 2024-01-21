#!/bin/bash

# Step 1: Create Python virtual environment
python -m venv env &&

# Step 2: Activate the virtual environment
source env/Scripts/activate &&

# Check if virtual environment is activated
if [ -n "$VIRTUAL_ENV" ]; then
    echo "Virtual environment is activated: $VIRTUAL_ENV"
    # Step 3: Upgrade pip within the virtual environment
    python -m pip install --upgrade pip &&

    # Step 4: Sleep for 5 seconds
    sleep 5 &&

    # Step 5: Install Python packages from requirements.txt within the virtual environment
    pip install -r requirements.txt &&

    # Optional: Display a message indicating successful setup
    echo "Python environment created, activated, pip upgraded, slept for 5 seconds, and packages installed successfully."

else
    echo "No virtual environment is currently activated."
fi

