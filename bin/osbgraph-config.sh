#!/bin/sh
# obsgraph-config.sh
# Purpose: Set up environment variables for ObsGraph Flask application

# Set the project root directory
export OBSGRAPH_PROJECT_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Create a Python virtual environment if it doesn't exist
if [ ! -d "$OBSGRAPH_PROJECT_ROOT/.venv-prod" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$OBSGRAPH_PROJECT_ROOT/.venv-prod"
    # Activate the virtual environment
    source "$OBSGRAPH_PROJECT_ROOT/.venv-prod/bin/activate"
    # Install required packages
    pip install -r "$OBSGRAPH_PROJECT_ROOT/requirements.txt"
else
    # Activate the existing virtual environment
    source "$OBSGRAPH_PROJECT_ROOT/.venv-prod/bin/activate"
fi

# Run the ObsGraph configurator script
python "$OBSGRAPH_PROJECT_ROOT/obsgraph_flask/tools/obsgraph_configurator.py"

deactivate
# #[EOF]#######################################################################