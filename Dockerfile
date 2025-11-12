# Minimal Dockerfile for robert-health-coach
# Builds a container that can run the skills and agent (example)

FROM python:3.10-slim

# Set working dir
WORKDIR /app

# Copy project files
COPY pyproject.toml README.md /app/
COPY skills/ /app/skills/
COPY tests/ /app/tests/
COPY integrations/ /app/integrations/

# Install runtime deps (adjust as needed)
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir pytest black flake8
# If project has package deps, install them here (or use editable install):
# RUN pip install -e .

# Default command: run a shell (override with docker run)
CMD ["/bin/bash"]
