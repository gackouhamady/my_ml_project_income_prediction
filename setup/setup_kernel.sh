#!/usr/bin/env bash
# ==============================================
#  Codespaces Kernel Setup - Hamady GACKOU
#  Fixed & hardened version
# ==============================================

set -Eeuo pipefail

PROJECT_NAME="my_ml_project_income_prediction"
VENV_DIR=".venv"
KERNEL_NAME="my_ml_project_env"
DISPLAY_NAME="Python (.venv ${PROJECT_NAME})"

echo "▶ Setting up Python virtual environment and Jupyter kernel for ${PROJECT_NAME}..."

# 0) Find a working python executable
if command -v python3 >/dev/null 2>&1; then
  SYS_PYTHON="python3"
elif command -v python >/dev/null 2>&1; then
  SYS_PYTHON="python"
else
  echo "❌ No python interpreter found on PATH." >&2
  exit 1
fi
echo "✔ Using system Python: ${SYS_PYTHON}"

# 1) Create venv if missing
if [ ! -d "${VENV_DIR}" ]; then
  echo "▶ Creating virtual environment at ${VENV_DIR}..."
  "${SYS_PYTHON}" -m venv "${VENV_DIR}"
else
  echo "ℹ Virtual environment already exists at ${VENV_DIR}."
fi

VENV_PY="${VENV_DIR}/bin/python"
VENV_PIP="${VENV_DIR}/bin/pip"

# 2) Upgrade pip/setuptools/wheel and install essentials
echo "▶ Upgrading pip/setuptools/wheel..."
"${VENV_PY}" -m pip install --upgrade pip setuptools wheel

echo "▶ Installing Jupyter essentials (ipykernel, jupyter, notebook, pandas, matplotlib)..."
"${VENV_PIP}" install ipykernel jupyter notebook pandas matplotlib

# 3) Install project requirements if present
if [ -f "requirements.txt" ]; then
  echo "▶ requirements.txt found — installing dependencies..."
  "${VENV_PIP}" install -r requirements.txt
else
  echo "ℹ No requirements.txt found — skipping project deps."
fi

# 4) Register the IPython kernel (idempotent)
echo "▶ Registering Jupyter kernel '${KERNEL_NAME}'..."
"${VENV_PY}" -m ipykernel install --user --name="${KERNEL_NAME}" --display-name="${DISPLAY_NAME}"

# 5) Show kernel list
echo "▶ Kernel list:"
jupyter kernelspec list

# 6) Show kernel.json path & content (resolved dynamically)
echo "▶ Resolving kernelspec path for '${KERNEL_NAME}'..."
KERNEL_PATH="$(jupyter kernelspec list | awk -v k="${KERNEL_NAME}" '$1==k {print $2}')"
if [ -n "${KERNEL_PATH:-}" ] && [ -f "${KERNEL_PATH}/kernel.json" ]; then
  echo "✔ kernel.json at: ${KERNEL_PATH}/kernel.json"
  cat "${KERNEL_PATH}/kernel.json"
else
  echo "⚠ Could not automatically resolve kernel.json path. It may still be installed."
fi

# 7) Check active interpreter
echo "▶ Checking venv Python interpreter..."
"${VENV_PY}" - <<'PY'
import sys, pkgutil
print("Python executable:", sys.executable)
print("Version:", sys.version.replace("\n"," "))
print("ipykernel installed:", bool(pkgutil.find_loader("ipykernel")))
PY

echo "✅ Done. You can now select kernel: ${DISPLAY_NAME} in Jupyter/VS Code."
# Optional quick test (non-interactive) — uncomment to run a smoke test:
# jupyter console --kernel="${KERNEL_NAME}" -y -f <(echo 'import sys; print("Hello from", sys.executable); exit()')
