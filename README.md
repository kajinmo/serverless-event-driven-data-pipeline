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

## Local Development Environment

To run the pipeline locally without AWS infrastructure, use the provided Docker environment:

### Prerequisites

- Docker and Docker Compose installed
- AWS CLI configured with a profile (e.g., `portfolio-sandbox`)
- Terraform installed

### Setup

1. **Create a `.env` file** in the project root (copy from `.env.example`):

   ```bash
   cp .env.example .env
   ```

2. **Update `.env`** with your MongoDB credentials:

   ```bash
   MONGO_USER=admin
   MONGO_PASSWORD=secret
   ```

3. **Start the environment:**
   ```bash
   docker-compose up -d
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
