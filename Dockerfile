FROM python:3.11-slim

# Set working dir inside the container
WORKDIR /app

# Copy only requirements first (cache layer)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the app
COPY . .

# Set environment variable to avoid Python buffering
ENV PYTHONUNBUFFERED=1

HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD pgrep -f "main.py" || exit 1

# Run the bot
CMD ["python", "main.py"]
