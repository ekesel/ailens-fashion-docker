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
RUN pip install -r requirements.txt

# Copy the project code into the container
COPY . /ailensfashion/

CMD ["/wait-for-db.sh", "db:3306"]