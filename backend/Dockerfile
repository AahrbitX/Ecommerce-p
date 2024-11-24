FROM python:3


# Set environment variable to avoid buffering
ENV PYTHONUNBUFFERED=1

# Set the working directory to the project root
WORKDIR /app

# Copy all project files into the container
COPY . .

# Upgrade pip to the latest version
RUN pip install --upgrade pip

# Install dependencies from the requirements file
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Expose port 8000 for the Django app
EXPOSE 8000

# Command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
