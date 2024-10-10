# hms-dfcu
## Deployment Guide

This guide provides instructions for deploying the Django project in a production environment.

### 1. Pre-requisites
Ensure the following are installed:

Python 3.6+
Virtualenv for Python virtual environments
### 2. Setup Steps
#### Step 1: Clone the Project
cd project
#### Step 2: Set Up Virtual Environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
#### Step 3: Install Dependencies
pip install -r requirements.txt
#### Step 4: Configure Environment Variables
Create a .env file or export variables directly:
DJANGO_SECRET_KEY=your_secret_key
#### Step 5: Run Database Migrations
python manage.py migrate
#### step 6: Run App
python manage.py runserver




