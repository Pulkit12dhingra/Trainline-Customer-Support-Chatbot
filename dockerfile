# Use Ubuntu as base image
FROM ubuntu:22.04

# Set environment variables to avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    curl \
    python3 \
    python3-pip \
    && rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -sSL https://install.ollama.com | bash

# Set working directory
WORKDIR /app

# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose necessary ports (11434 for Ollama, 8501 for Streamlit)
EXPOSE 11434 8501

# Start Ollama and Streamlit
CMD ollama serve & python3 -m streamlit run test.py --server.port 8501 --server.address 0.0.0.0
