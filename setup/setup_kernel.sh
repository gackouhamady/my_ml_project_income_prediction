#!/usr/bin/env bash
# ==============================================
#  Codespaces Kernel Setup - Hamady GACKOU
# ==============================================

PROJECT_NAME="my_ml_project_income_prediction"
VENV_DIR=".venv"
KERNEL_NAME="my_ml_project_env"
DISPLAY_NAME="Python (.venv ${PROJECT_NAME})"

echo "Setting up Python virtual environment and Jupyter kernel for ${PROJECT_NAME}..."

# 1. Create and activate virtual environment
if [ ! -d "${VENV_DIR}" ]; then
  echo "Creating virtual environment..."
  python3 -m venv ${VENV_DIR}
else
  echo "Virtual environment already exists."
fi

# Activate venv
source ${VENV_DIR}/bin/activate

# 2. Upgrade pip and install dependencies
echo "Upgrading pip and installing essentials..."
pip install --upgrade pip
pip install ipykernel jupyter notebook pandas matplotlib

# 3. Register the IPython kernel
echo "Registering Jupyter kernel..."
python -m ipykernel install --user --name=${KERNEL_NAME} --display-name="${DISPLAY_NAME}"

# 4. Show kernel info
echo "Kernel list:"
jupyter kernelspec list

echo "Kernel JSON content:"
cat ~/.local/share/jupyter/kernels/${KERNEL_NAME}/kernel.json

# 5. Check current Python path
echo "Checking active Python interpreter..."
python -c "import sys; print('Python executable:', sys.executable)"

# 6. Optional: Launch console for test
echo "Launching Jupyter console (press Ctrl+C to exit)..."
jupyter console --kernel=${KERNEL_NAME}
