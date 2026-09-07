# Event-Driven Data Pipeline Architecture

An end-to-end serverless data pipeline that ingests user activity, enriches it with profile data, and stores the consolidated result in MongoDB Atlas.

## Architecture Overview

```
+----------------+
| Event Stream   |
| (API Gateway)  |
+--------+-------+
         |
         v
+--------+-------+
| S3 Bucket      |
| (Raw Events)   |
+--------+-------+
         |
         v
+--------+-------+
| SQS Queue      |
| (Trigger)      |
+--------+-------+
         |
         v
+--------+-------+
| Lambda         |
| (Orchestrator) |
+--------+-------+
         |
         v
+--------+-------+--------+--------+
|   Parallel State       |
+--------+-------+--------+--------+
         |
         v
+--------+-------+   +--------+-------+
|  Profile Lambda |   | Activity Lambda|
+--------+-------+   +--------+-------+
         |
         v
+--------+-------+
|  Join State    |
+--------+-------+
         |
         v
+--------+-------+
| MongoDB Atlas  |
| (Consolidated) |
+--------+-------+
```

## Local Development Environment (Floci)

To run the pipeline locally and emulate AWS infrastructure, we use a Docker environment with **Floci** (a local cloud emulator) and a local MongoDB instance.

### Prerequisites

- Docker and Docker Compose installed
- Terraform installed

### Floci Setup & Deployment

1. **Start the local emulators:**
   ```bash
   docker-compose up -d
   ```
   *This starts the `eda-floci` container (mocking AWS DynamoDB, SQS, Lambda, Step Functions) and `eda-mongodb`.*

2. **Deploy infrastructure locally:**
   Since we transitioned to the real AWS cloud, the local Terraform configuration was backed up to the `floci/` folder.
   ```bash
   cd floci
   terraform init
   terraform apply
   ```

3. **Testing locally:**
   You can run the python seed scripts or tests pointing to `http://localhost:4566`.

### Cleanup

1. **Destroy local resources:**
   ```bash
   cd floci
   terraform destroy
   ```

2. **Stop the Docker environment:**
   ```bash
   docker-compose down
   ```

### Testing

1. **Generate test data:**

   ```bash
   python scripts/generate_test_data.py
   ```

2. **Run the Lambda function:**
   ```bash
   python tests/test_lambda.py
   ```

### Deployment

1. **Initialize Terraform:**

   ```bash
   cd terraform
   terraform init
   ```

2. **Review the plan:**

   ```bash
   terraform plan
   ```

3. **Apply the changes:**
   ```bash
   terraform apply
   ```

### Cleanup

1. **Destroy the resources:**

   ```bash
   cd terraform
   terraform destroy
   ```

2. **Stop the Docker environment:**
   ```bash
   docker-compose down
   ```

## Code Structure

- `floci/`: Local development environment code (temporary)
- `terraform/`: Terraform infrastructure definitions
- `src/`: Source code for Lambda functions
  - `lambda_function/`: Main orchestrator Lambda
  - `lambda_activity/`: User activity processing
  - `lambda_profile/`: User profile processing
- `scripts/`: Utility scripts for testing and automation
- `tests/`: Test scripts

## Security Best Practices

- Never hardcode credentials in code or Terraform files
- Use environment variables for secrets
- Use AWS SSM Parameter Store or Secrets Manager for production
- Always use the `portfolio-sandbox` AWS profile for local development
