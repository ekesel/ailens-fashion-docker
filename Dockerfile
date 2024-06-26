# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /ailensfashion

# Install dependencies
COPY requirements.txt /ailensfashion/
COPY wait-for-db.sh /wait-for-db.sh
RUN pip install --no-cache-dir -r requirements.txt && \ 
    adduser \                                           
        --disabled-password \
        --no-create-home \
        django-user

# Copy the project code into the container
COPY . /ailensfashion/

RUN chown -R django-user:django-user /ailensfashion

# Apply migrations and collect static files as root
RUN python manage.py collectstatic --noinput

# Change the ownership and permissions of the static files directory
RUN chown -R django-user:django-user /ailensfashion/static && \
    chmod -R u+rwx /ailensfashion/static

USER django-user

CMD ["/wait-for-db.sh", "db:3307"]