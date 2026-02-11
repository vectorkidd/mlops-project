Vehicle Insurance MLOps Project

This repository demonstrates an end-to-end MLOps pipeline for a Vehicle Insurance project, including data ingestion, model training, evaluation, deployment, and CI/CD integration with AWS.

📁 Project Setup

Create Project Template
Run template.py to initialize the project structure.

Setup Local Packages

Edit setup.py and pyproject.toml to include your local packages.

Refer to crashcourse.txt for more details.

Create Virtual Environment and Install Requirements

conda create -n vehicle python=3.10 -y
conda activate vehicle
pip install -r requirements.txt


Verify Local Packages

pip list

🗄 MongoDB Setup

Sign up for MongoDB Atlas and create a new project.

Create a cluster (M0 free tier) and configure DB user credentials.

Add your IP to "Network Access" as 0.0.0.0/0.

Copy the connection string from “Get Connection String” → Python driver.

Create a notebook folder and a notebook mongoDB_demo.ipynb.

Add your dataset to the notebook folder.

Push data from your notebook to MongoDB.

Verify data in MongoDB Atlas under Browse Collections.

📝 Logging, Exception Handling & Notebooks

Implement and test logger.py in demo.py.

Implement and test exception.py in demo.py.

Add EDA and feature engineering notebooks.

🛠 Data Ingestion

Define variables in constants/__init__.py.

Add MongoDB connection code in configuration/mongo_db_connections.py.

Implement Proj1Data in data_access to fetch MongoDB data into pandas DataFrame.

Define DataIngestionConfig and DataIngestionArtifact in entity folder.

Implement components/data_ingestion.py and integrate with training pipeline.

Set MongoDB URL environment variable:

Bash:

export MONGODB_URL="mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
echo $MONGODB_URL


PowerShell:

$env:MONGODB_URL="mongodb+srv://<username>:<password>@cluster0.mongodb.net/?retryWrites=true&w=majority"
echo $env:MONGODB_URL

🔄 Data Validation, Transformation & Model Training

Complete utils/main_utils.py and config/schema.yaml for data validation.

Implement Data Validation similar to data ingestion workflow.

Implement Data Transformation (add estimator.py in entity folder).

Implement Model Trainer (add classes in estimator.py).

☁ AWS Setup for Model Evaluation & Deployment

Login to AWS, set region us-east-1.

Create IAM user with AdministratorAccess and download access keys.

Set environment variables:

Bash:

export AWS_ACCESS_KEY_ID="YOUR_KEY"
export AWS_SECRET_ACCESS_KEY="YOUR_SECRET"


PowerShell:

$env:AWS_ACCESS_KEY_ID="YOUR_KEY"
$env:AWS_SECRET_ACCESS_KEY="YOUR_SECRET"


Update constants/__init__.py with:

MODEL_EVALUATION_CHANGED_THRESHOLD_SCORE = 0.02
MODEL_BUCKET_NAME = "my-model-mlopsproj"
MODEL_PUSHER_S3_KEY = "model-registry"


Create S3 bucket my-model-mlopsproj in us-east-1.

Implement aws_storage configurations and s3_estimator.py for S3 interactions.

🚀 Model Evaluation, Model Pusher & Prediction Pipeline

Implement Model Evaluation and Model Pusher components.

Create Prediction Pipeline structure and app.py.

Add static and template directories for the web app.

🐳 CI/CD with Docker & GitHub Actions

Create Dockerfile and .dockerignore.

Setup GitHub Actions workflow under .github/workflows/aws.yaml.

Create AWS IAM user for deployment (usvisa-user) and configure access keys.

Create ECR repository vehicleproj for Docker images.

Launch EC2 instance vehicledata-machine (Ubuntu 24.04, t2.medium, 30GB storage).

Install Docker on EC2:

sudo apt-get update -y
sudo apt-get upgrade -y
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker ubuntu
newgrp docker


Setup GitHub self-hosted runner on EC2 to connect Actions to your server.

Add GitHub secrets: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION, ECR_REPO.

CI/CD pipeline triggers on next commit and push.

🌐 Launch App

Activate port 5080 in EC2 Security Groups.

Access app at: http://<EC2_PUBLIC_IP>:5080.

Model training can be triggered at /training route.

📌 Notes

Always push notebooks using [skip ci] if you don’t want the deployment workflow to run.

Environment variables must be set before running any scripts.

Ensure artifact directory is added to .gitignore.
