# AccessVerifier

AccessVerifier is a Python microservice designed to enhance the security of the `ClientDataManager` service by validating incoming HTTP requests based on their originating IP addresses. It ensures only requests from allowed AWS IP ranges are processed.

---

## Features
- **IP Validation:** Verifies if incoming requests originate from allowed IP ranges.
- **Dynamic IP Updates:** Fetches and updates AWS IP ranges daily via a separate updater service.
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

#### For Linux/Mac:
```bash
python3.12 -m venv venv
source venv/bin/activate
```

#### For Windows:
```bash
python -m venv venv
venvScriptsactivate
```

### 3. Install Dependencies

#### Install production dependencies:
```bash
pip install -r requirements.txt
```

#### Install dependencies for testing:
```bash
pip install -r requirements-test.txt
```

---

## Running the Application Locally

### 1. Start the AccessVerifier Service
```bash
python app.py
```
The service will be available at `http://localhost:5000`.

### 2. Start the IP Updater
```bash
python ip_updater.py
```

---

## Docker Setup

### 1. Build Docker Images
There are two separate Dockerfiles for the AccessVerifier service and the IP updater.

#### Build AccessVerifier Image
```bash
docker build -f Dockerfile.app -t access-verifier .
```

#### Build IP Updater Image
```bash
docker build -f Dockerfile.updater -t ip-updater .
```

### 2. Run Docker Containers

#### Start AccessVerifier
```bash
docker run -d -p 5000:5000 --name access-verifier access-verifier
```

#### Start IP Updater
```bash
docker run -d --name ip-updater ip-updater
```

---

## Kubernetes Deployment

**This section has not been tested.**

### Prerequisites
- A running Kubernetes cluster.
- `kubectl` configured to interact with the cluster.

### Deployment Steps

1. **Apply Kubernetes Manifests:**
   Navigate to the `k8s` directory and apply the manifests:
   ```bash
   kubectl apply -f k8s/access-verifier-deployment.yaml
   kubectl apply -f k8s/access-verifier-service.yaml
   kubectl apply -f k8s/ip-updater-cronjob.yaml
   kubectl apply -f k8s/persistent-volume.yaml
   ```

2. **Verify the Deployment:**
   Check if the pods, services, and CronJobs are running:
   ```bash
   kubectl get pods
   kubectl get services
   kubectl get cronjobs
   ```

3. **Test the Service:**
   - Test AccessVerifier:
     ```bash
     curl -X POST http://<external-ip>:5000/verify -H "Content-Type: text/plain"
     ```
   - Verify the CronJob's success by checking logs:
     ```bash
     kubectl logs <job-pod-name>
     ```

4. **Logs and Debugging:**
   - Check AccessVerifier logs:
     ```bash
     kubectl logs <access-verifier-pod>
     ```
   - Check IP updater logs:
     ```bash
     kubectl logs <ip-updater-pod>
     ```

---

## Testing

Before running tests, make sure to install the required dependencies for testing:
```bash
pip install -r requirements-test.txt
```

Run tests:
```bash
pytest tests/
```

---

## Automatic IP List Reloading

The application includes a mechanism to automatically monitor the IP file (`allowed_ips.json`) if it is created or modified while the application is running.

- **Default File:** `allowed_ips.json`
- **Custom File:** You can specify a custom file by setting the `IP_FILE` environment variable:
  ```bash
  export IP_FILE="custom_ips.json"
  ```

---

## IP Verification Behavior

AccessVerifier validates incoming IP addresses against a predefined list of allowed IP ranges. By default, it supports network ranges in CIDR notation.

### Examples of Supported Ranges
- A specific IP: `192.168.1.1/32`
- A network range: `3.250.244.0/26` (covers IPs from `3.250.244.0` to `3.250.244.63`)

### Environment Variable: `ALLOW_NETWORK_RANGES`

By default, AccessVerifier allows IPs that match any network range in the list. This behavior is controlled by the `ALLOW_NETWORK_RANGES` environment variable:

- `ALLOW_NETWORK_RANGES=True` (default):
  - IPs within the range are allowed.
  - Example: For `3.250.244.0/26`, both `3.250.244.1` and `3.250.244.63` will be allowed.

- `ALLOW_NETWORK_RANGES=False`:
  - Only exact IP matches are allowed.
  - Example: For `3.250.244.0/26`, only the IP `3.250.244.0` will be allowed.

Set the variable as follows:
```bash
export ALLOW_NETWORK_RANGES=False
```
