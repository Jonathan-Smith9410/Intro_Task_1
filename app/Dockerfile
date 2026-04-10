# Stage 1: Builder
FROM python:3.9-slim as builder

WORKDIR /install

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends gcc python3-dev

COPY requirements.txt .

# Install dependencies to a specific folder, --user installs them to /root/.local
RUN pip install --user --no-cache-dir -r requirements.txt


# Stage 2: Final Runtime
FROM python:3.9-slim

WORKDIR /app

# Copy only the installed python packages from the builder stage
COPY --from=builder /root/.local /root/.local
COPY --from=builder /install/requirements.txt .

# Copy the application code
COPY app.py .
COPY templates/ ./templates/

# Ensure the scripts in .local/bin are in the PATH
ENV PATH=/root/.local/bin:$PATH

# Execute the application
CMD ["python", "app.py"]