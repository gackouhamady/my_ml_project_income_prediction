# ---- Base image ----
FROM python:3.11-slim

# Avoid interactive tz prompts & speed up pip
ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# System deps often needed for scientific stacks
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      curl \
      git \
      ca-certificates \
   && rm -rf /var/lib/apt/lists/*

# Create a non-root user that will own the mounted workspace
ARG NB_USER=appuser
ARG NB_UID=1000
ARG NB_GID=1000
RUN groupadd -g ${NB_GID} ${NB_USER} && \
    useradd -m -s /bin/bash -u ${NB_UID} -g ${NB_GID} ${NB_USER}

# Working directory inside the container (will be bind-mounted)
WORKDIR /workspace

# Copy only requirements (not your notebooks/code)
# If you don't have requirements.txt, comment this block.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt || true

# Jupyter & common goodies (kept separate so it’s cached even if requirements change)
RUN pip install jupyterlab ipykernel && \
    python -m ipykernel install --name=project-kernel --user

# Expose Jupyter port
EXPOSE 8888

# Drop privileges
USER ${NB_USER}

# Default command: Jupyter Lab listening on all interfaces, no token
CMD ["jupyter", "lab", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--NotebookApp.token=", "--NotebookApp.password="]
