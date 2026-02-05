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

## Troubleshooting & Key Learnings

During the deployment process, I encountered an authentication issue while pushing Docker images to Google Artifact Registry. Despite correct IAM permissions and billing being enabled, Docker push requests consistently failed with an `Unauthenticated request` error.

### Root Cause
The issue was caused by running Docker commands using `sudo`. While `sudo` allowed access to the Docker daemon, it changed the user context to `root`. As a result, Docker attempted to use credentials from `/root/.docker/config.json`, bypassing the GCP credential helper configured for the normal user.

Since Artifact Registry authentication relies on the Docker credential helper configured by `gcloud`, this user context mismatch caused all push attempts to fail.

### Resolution
- Added the user to the `docker` group to allow Docker commands to run without `sudo`
- Applied the group membership change via logout/login
- Re-ran Docker tag and push commands as the normal user

After correcting the Linux permissions and user context, Docker was able to authenticate successfully with Artifact Registry and the image push completed as expected.

### Key Takeaways
- Docker authentication issues can stem from Linux permission and user context problems, not just IAM configuration
- Running Docker with `sudo` can break credential helpers and should be avoided in CI/CD workflows
- Proper user and group management is essential for secure and predictable container operations
