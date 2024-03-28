# Use the base image from ECR
FROM 663524913446.dkr.ecr.us-east-2.amazonaws.com/palette-pal-base-image:latest

# Set work directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY ./app /app/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose port 8000 for the application
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "server.wsgi:application"]
