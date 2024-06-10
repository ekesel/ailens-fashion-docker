# Project Title

Local Setup Guide for Django Project with MySQL

## Introduction

This guide provides step-by-step instructions to set up and run the Django project locally using MySQL as the database.

## Table of Contents

- [Installation](#installation)
- [Database Setup](#database-setup)
- [Environment Configuration](#environment-configuration)
- [Running the Project](#running-the-project)
- [Troubleshooting](#troubleshooting)

## Installation

### Step 1: Install MySQL

First, update your package index and install the MySQL server.

```bash
sudo apt update
sudo apt install mysql-server
```

### Step 2: Verify MySQL Installation

Run the following command to check if MySQL is installed and running.

```bash
sudo mysql
```

## Database Setup

### Step 3: Create Database

Log into MySQL and create the required database.

```sql
CREATE DATABASE ailens;
```

Verify the creation of the database.

```sql
SHOW DATABASES;
```

### Step 4: Create MySQL User

Create a new MySQL user and grant the necessary permissions.

```sql
CREATE USER 'djangouser'@'localhost' IDENTIFIED WITH mysql_native_password BY 'password';
GRANT ALL ON ailens.* TO 'djangouser'@'localhost';
FLUSH PRIVILEGES;
exit
```

Restart MySQL to apply changes.

```bash
sudo systemctl restart mysql
```

## Environment Configuration

### Step 5: Create .env File

In the root directory of your project, create a `.env` file and add the following configurations.

```env
# Django settings
SECRET_KEY=django-insecure-tp18b!fqi_q=uto!*56c6h=d+dg9yjkv*)xr49^ao#7c5#+3e1
DEBUG=True

# MySQL settings
MYSQL_ROOT_PASSWORD=
MYSQL_DATABASE=ailens
MYSQL_USER=
MYSQL_PASSWORD=
```

Ensure you replace the placeholders with the actual MySQL credentials.

## Running the Project

### Step 6: Build and Run the Project

Use Docker to build and run the project.

```bash
docker compose build
docker compose up
```

## Troubleshooting

If you encounter any issues during the setup, consider the following tips:

- Ensure MySQL service is running using `sudo systemctl status mysql`.
- Check the `.env` file for correct configurations.
- Verify Docker installation and configuration.
- Consult the project's documentation for specific error messages and solutions.

For further assistance, please refer to the project documentation or contact the project maintainers.
