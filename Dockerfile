# Use Python 3.10 base image
FROM python:3.10-slim

# Create app directory
WORKDIR /app

# Copy all files to the app folder
COPY . /app

# Install requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "bot.py"]
