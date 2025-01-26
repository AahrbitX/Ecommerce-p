FROM python:3

ENV PYTHONUNBUFFERED=1

# Set the working directory to /app (project root for backend)
WORKDIR /app

# Copy the backend directory contents to the container's /app
COPY . /app

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose the Django port
EXPOSE 8000

# Run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
