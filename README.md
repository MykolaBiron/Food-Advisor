# FoodAdvisor

FoodAdvisor is an AI-powered nutrition tracker that identifies meals from photos and estimates calories and macronutrients.

## Repository Structure

- [django-backend](django-backend): Django app, ML integration, API logic, static/template UI
- [react-frontend](react-frontend): React frontend workspace

## Main Documentation

Detailed setup and project documentation are in:

- [django-backend/README.md](django-backend/README.md)

## Quick Start (Backend)

```bash
cd django-backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Deployment

This project is deployed on Railway.

If deploying from this monorepo, set the service root to [django-backend](django-backend) so build scripts and dependencies are resolved correctly.
