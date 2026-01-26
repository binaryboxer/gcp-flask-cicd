# Automated CI/CD Pipeline for a 2-Tier Flask Application on GCP

This project demonstrates a production-style workflow for deploying a containerized Flask application on Google Cloud Platform using Cloud Run and Artifact Registry.

The focus is on infrastructure, deployment, and operational clarity rather than application complexity.

---

## Architecture Overview

The application follows a simple 2-tier architecture:

- **Application Tier**: Flask-based REST API packaged as a Docker container
- **Platform Tier**: Google Cloud Run for serverless container execution

The container image is built locally, pushed to Artifact Registry, and deployed to Cloud Run.

---

## Tech Stack

- Python (Flask)
- Docker
- Google Cloud Run
- Artifact Registry
- GCP IAM
- Cloud Logging

---

## Application Endpoints

| Endpoint | Description |
|--------|------------|
| `/health` | Health check endpoint |
| `/hello` | Sample API endpoint |

---

## Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
python app/app.py
