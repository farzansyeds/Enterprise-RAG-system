FROM python:3.10

# Create a non-root user that Hugging Face Spaces requires for disk writes
RUN useradd -m -u 1000 user
USER user

# Set environment variables for the user
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Set the working directory
WORKDIR $HOME/app

# Copy requirements and install
COPY --chown=user requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your project (including the compiled frontend/dist)
COPY --chown=user . .

# Hugging Face Spaces expects apps to run on port 7860
EXPOSE 7860

# Start the unified FastAPI server
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]