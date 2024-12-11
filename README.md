# AccessVerifier

AccessVerifier is a Python microservice designed to enhance the security of the `ClientDataManager` service by validating incoming HTTP requests based on their originating IP addresses. It ensures only requests from allowed AWS IP ranges are processed.

---

## Features
- **IP Validation:** Verifies if incoming requests originate from allowed IP ranges.
- **Dynamic IP Updates:** Fetches and updates AWS IP ranges daily.
- **REST API:** Provides a `/verify` endpoint for HTTP request validation.
---

## Requirements
- Python 3.12+
- Flask
- Requests
- Pytest (for testing)
---

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/bartekbm/AccessVerifier.git
cd AccessVerifier
```

### 2. Create a Virtual Environment
For Linux/Mac:
```bash
python3.12 -m venv venv
source venv/bin/activate
```

For Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
Install production dependencies:
```bash
pip install -r requirements.txt
```

To install dependencies for testing:
```bash
pip install -r requirements-test.txt
```

### 4. Running the Application
Run Locally
```bash
python app.py
```
The service will be available at http://localhost:5000.

Run with Docker
```bash
docker build -t access-verifier .
docker run -d -p 5000:5000 --name access-verifier access-verifier
```

### 5. API Endpoints

### `/verify`
- **Method:** `POST`
- **Description:** Validates the origin of the incoming HTTP request.
- **Response:**
  - `200 OK` if the request is allowed.
  - `401 Unauthorized` if the request is denied.

Example:
```bash
curl -X POST http://localhost:5000/verify -H "Content-Type: text/plain"
```

### 6. Testing
Before running tests, make sure to install the required dependencies for testing:
```bash
pip install -r requirements-test.txt
```

Activate your virtual environment and run:
```bash
pytest tests/
```
### 7. Kubernetes Deployment
### Prerequisites
- A running Kubernetes cluster.
- `kubectl` configured to interact with the cluster.

#### 1. Apply Kubernetes Manifests
Navigate to the `k8s` directory and apply the manifests:
```bash
kubectl apply -f k8s/access-verifier-deployment.yaml
kubectl apply -f k8s/access-verifier-service.yaml
kubectl apply -f k8s/clientdata-ingress.yaml
kubectl apply -f k8s/cronjob-update-allowed-ips.yaml
```
#### 2. Verify the Deployment
Check if the pods, services, and ingress are running:
```bash
kubectl get pods
kubectl get services
kubectl get ingress
```

#### 3. Test the Ingress
Ensure that the ingress endpoint is accessible and integrated with AccessVerifier:
```bash
curl -X POST http://<your-ingress-hostname>/verify -H "Content-Type: text/plain"
```
#### 4. Logs and Debugging
If there are issues, check the logs of the AccessVerifier pod:
```bash
kubectl logs <pod-name>
```
