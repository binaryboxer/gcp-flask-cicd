# Automated CI/CD Pipeline for a 2-Tier Flask Application on GCP

## Overview
This project demonstrates an end-to-end CI/CD workflow for deploying a containerized Flask application on **Google Cloud Platform** using **Cloud Run**, **Artifact Registry**, and **GitHub Actions** with **Workload Identity Federation (OIDC)**.

The primary focus of this project is **cloud deployment, secure CI/CD automation, and real-world troubleshooting**, rather than application complexity.

---

## Architecture

**High-level architecture:**

- **Application Layer**
  - Flask-based REST API
  - Containerized using Docker

- **Platform Layer**
  - Google Cloud Run (fully managed, serverless container runtime)
  - Artifact Registry for container image storage

- **CI/CD Layer**
  - GitHub Actions
  - OIDC-based authentication to GCP (no long-lived credentials)

---

## Technology Stack

- Python (Flask)
- Docker
- Google Cloud Run
- Google Artifact Registry
- GitHub Actions
- GCP IAM & Workload Identity Federation
- Cloud Logging

---

## Application Endpoints

| Endpoint | Description |
|--------|------------|
| `/` | Root endpoint |
| `/health` | Health check endpoint |

---

## Local Development

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r app/requirements.txt
python app/app.py


##Containerization

The application is packaged as a Docker image using a production-ready configuration.

docker build -t flask-ci-cd -f docker/Dockerfile .
docker run -p 8080:8080 flask-ci-cd

## CI/CD Pipeline

The CI/CD pipeline is implemented using **GitHub Actions** and is triggered on every push to the `master` branch.

### Pipeline Steps
1. Checkout source code  
2. Authenticate to Google Cloud using **OIDC (Workload Identity Federation)**  
3. Build Docker image  
4. Push image to Artifact Registry  
5. Deploy the application to Cloud Run  

This approach avoids storing service account keys and follows cloud security best practices.

---

## Deployment

The application is deployed to **Google Cloud Run** with:

- Automatic scaling
- HTTPS endpoint
- Revision-based deployments
- Easy rollback to previous revisions

---

## Troubleshooting & Key Learnings

During development and deployment, several real-world issues were encountered and resolved:

### Docker Authentication
- Docker push failures were caused by running Docker commands with `sudo`, which changed the user context and bypassed the configured GCP credential helper.
- Resolved by adding the user to the `docker` group and running Docker without `sudo`.

### Linux Permissions
- Docker daemon communication relies on a Unix domain socket (`/var/run/docker.sock`).
- Correct user and group permissions were required for stable Docker operation.

### OIDC Authentication
- OIDC authentication failures were caused by mismatched Workload Identity provider configuration and incorrect audience values.
- Resolved by aligning GitHub Actions configuration with the exact provider resource name in GCP.

### Cloud Run Runtime
- Initial deployment returned errors on the root URL due to a missing `/` route in the Flask application.
- Adding an explicit root endpoint resolved the issue.

---

## Key Takeaways

- Docker authentication issues often stem from Linux permission and user-context problems.
- Running Docker with `sudo` can break CI/CD credential helpers.
- OIDC-based CI/CD requires precise alignment between GitHub, IAM bindings, and provider configuration.
- Cloud Run expects applications to explicitly handle the root (`/`) route.

---

## Future Improvements

- Provision infrastructure using Terraform
- Introduce environment separation (dev/stage/prod)
- Integrate Secret Manager for sensitive configuration
- Add monitoring and alerting

---

## Author Notes

This project was built to gain hands-on experience with **cloud-native deployments, CI/CD automation, and real-world debugging** scenarios commonly encountered in DevOps and Cloud Engineering roles.


## Architecture Diagram

```text
┌──────────────┐
│   Developer  │
│  (Git Push)  │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│   GitHub Repository  │
│  (master branch)     │
└──────┬───────────────┘
       │  Push Trigger
       ▼
┌──────────────────────┐
│   GitHub Actions     │
│   CI/CD Pipeline     │
│                      │
│  - OIDC Auth to GCP  │
│  - Docker Build      │
│  - Docker Push       │
└──────┬───────────────┘
       │
       ▼
┌──────────────────────────────┐
│   Artifact Registry (GCP)    │
│   Container Image Storage    │
└──────┬───────────────────────┘
       │
       ▼
┌──────────────────────────────┐
│       Cloud Run Service      │
│  - Serverless Container App  │
│  - Auto Scaling              │
│  - HTTPS Endpoint            │
└──────────────────────────────┘
