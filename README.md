# AccessVerifier

AccessVerifier is a Python microservice designed to enhance the security of the `ClientDataManager` service by validating incoming HTTP requests based on their originating IP addresses. It ensures only requests from allowed AWS IP ranges are processed.

---

## Features
- **IP Validation:** Verifies if incoming requests originate from allowed IP ranges.
- **Dynamic IP Updates:** The service fetches and updates AWS IP ranges daily using a built-in updater process.
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

### 1. Start the Service and Updater
Both the AccessVerifier service and the IP updater process run concurrently. Use the following command:
```bash
python app.py
```
The service will be available at `http://localhost:5000`.

---

## Testing Locally with curl

### 1. Test the `/verify` Endpoint
Once the service is running locally, you can test the `/verify` endpoint using `curl`. Replace `<IP_ADDRESS>` with the address you want to verify.

#### Example:
```bash
curl -X POST http://localhost:5000/verify -H "X-Forwarded-For: <IP_ADDRESS>"
```

#### Expected Responses:
- **200 OK**: The IP address is allowed.
- **401 Unauthorized**: The IP address is not allowed.

---

### 2. Test the IP Updater
The IP updater updates the list of allowed IPs daily by default. To test this manually:
1. Ensure the environment variable `AWS_REGION` is correctly set (default: `eu-west-1`).
2. Run the updater directly:
   ```bash
   python ip_updater.py
   ```
3. Check if the file `allowed_ips.json` has been updated with the new IP ranges.

---

## Docker Setup

### 1. Build Docker Image
The Dockerfile handles both the AccessVerifier service and the IP updater process. Build the Docker image as follows:
```bash
docker build -t access-verifier .
```

### 2. Run the Docker Container
Run the container using:
```bash
docker run -d -p 5000:5000 --name access-verifier access-verifier
```
The service will be accessible at `http://localhost:5000`.

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
   kubectl apply -f access-verifier-deployment.yaml
   kubectl apply -f access-verifier-service.yaml
   kubectl apply -f clientdata-ingress.yaml
   kubectl apply -f cronjob-update-allowed-ips.yaml
   ```

2. **Verify the Deployment:**
   Check if the pods, services, and ingress are running:
   ```bash
   kubectl get pods
   kubectl get services
   kubectl get ingress
   ```

3. **Test the Service:**
   - Test AccessVerifier:
     ```bash
     curl -X POST http://<external-ip>/verify -H "Content-Type: text/plain"
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
