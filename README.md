# ☁️ Google Cloud Platform - Vertex AI Voice Chat App

[![Badge: Google Cloud](https://img.shields.io/badge/Google%20Cloud-%234285F4.svg?logo=google-cloud&logoColor=white)](#readme)
[![Badge: macOS](https://img.shields.io/badge/macOS-000000.svg?logo=apple&logoColor=white)](#-quick-start)
[![Badge: GitHub](https://img.shields.io/github/license/cyclenerd/google-cloud-pricing-cost-calculator)](https://github.com/Cyclenerd/google-cloud-pricing-cost-calculator/blob/master/LICENSE)

This application facilitates interactive conversations between users and Vertex AI, Google's cloud-based AI platform. Users speak through their microphones, and AI responds with audio, providing an engaging and natural experience.

## 🔑 Key Features:

* Audio-based AI interaction: Users can speak questions or prompts, and Vertex AI responds with audio replies.
* Cloud-based deployment: Leverages Google Cloud Run containers for efficient scaling and management.
* Modular architecture: Separated frontend and backend components for improved development and maintenance.
* Vertex AI integration: Utilizes the power of Vertex AI for generating AI responses to user audio input.

## ✅ Prerequisites:

* Google Cloud Platform project with billing enabled
* gcloud command-line tool configured
* Basic understanding of Node.js, React, and cloud concepts

## 🚀 Deployment Guide

### Authenticate with Google Cloud

```bash
gcloud auth login
```

### Set default project for your deployment

```bash
gcloud config set project PROJECT_ID
```

### Enable APIs

```bash
gcloud services enable artifactregistry.googleapis.com
```

```bash
gcloud services enable cloudbuild.googleapis.com
```

```bash
gcloud services enable run.googleapis.com
```

```bash
gcloud services enable aiplatform.googleapis.com
```

```bash
gcloud services enable speech.googleapis.com
```

```bash
gcloud services enable texttospeech.googleapis.com
```


### Grant Vertex AI Service Agent role to the default compute engine service account

REPLACE ME: replace PROJECT_ID and PROJECT_NUMBER with your project's ID and nummber in the command below.

```bash
gcloud projects add-iam-policy-binding PROJECT_ID \
    --member=serviceAccount:PROJECT_NUMBER-compute@developer.gserviceaccount.com \
    --role=roles/aiplatform.serviceAgent
```

### Create Artifact Registry repository for Docker container images

```bash
gcloud artifacts repositories create vertexai-voice-chat-app \
  --repository-format="docker"\
  --description="Docker contrainer registry" \
  --location="europe-west1" \
  --quiet
```

### Initial Deploy Frontend

Note: You'll need to deploy the frontend twice. First, to obtain its URL. Later, when deploying the backend, remember to update the backend URL in the frontend code (explained in the next section: Configure Frontend Code), and then redeploy it.

1. Navigate to frontend folder

```bash
cd frontend/
```

2. Build a docker image with cloud build and push it to the Artifact Registry

REPLACE ME: replace PROJECT_ID with your project's ID in the command below.

```bash
gcloud builds submit \
    --tag="europe-west1-docker.pkg.dev/PROJECT_ID/vertexai-voice-chat-app/vertexai-voice-chat-frontend" \
    --timeout="1h" \
    --region="europe-west1" \
    --quiet 
```

3. Deploy frontend on Cloud Run

REPLACE ME: replace PROJECT_ID with your project's ID in the command below.

```bash
gcloud run deploy "vertexai-voice-chat-frontend" \
    --image="europe-west1-docker.pkg.dev/PROJECT_ID/vertexai-voice-chat-app/vertexai-voice-chat-frontend" \
    --region="europe-west1" \
    --allow-unauthenticated \
    --timeout="20m" \
    --quiet  \
    --port=8080
```

Write down the Service URL that is printed in the terminal (will be needed in next section to edit the backend code before it's deployment).
Looks something like this:
"Service URL: https://vertexai-voice-chat-frontend-gkbtxbspgq-ew.a.run.app"

### Configure Backend Code

1. Navigate to backend folder from the frontend folder

```bash
cd ../backend
```

2. Configure the backend code

Open main.py file, and replace the Frontend Service URL on the line 28 with the Service URL you noted in the previous step by deploying the Frontend.
This will allow the backend to recieve the requests from the backend.

### Deploy Backend


1. Build a docker image with cloud build and push it to the Artifact Registry

REPLACE ME: replace PROJECT_ID with your project's ID in the command below.

```bash
gcloud builds submit \
    --tag="europe-west1-docker.pkg.dev/PROJECT_ID/vertexai-voice-chat-app/vertexai-voice-chat-backend" \
    --timeout="1h" \
    --region="europe-west1" \
    --quiet 
```

2. Deploy backend on Cloud Run 

REPLACE ME: replace PROJECT_ID with your project's ID in the command below.

```bash
gcloud run deploy "vertexai-voice-chat-backend" \
    --image="europe-west1-docker.pkg.dev/PROJECT_ID/vertexai-voice-chat-app/vertexai-voice-chat-backend" \
    --region="europe-west1" \
    --allow-unauthenticated \
    --timeout="20m" \
    --quiet  \
    --port=8080
```

Write down the Service URL that is printed in the terminal (will be needed in next section to edit the frontend code before it's re-deployment).
Looks something like this:
"Service URL: https://vertexai-voice-chat-backend-gkbtxbspgq-ew.a.run.app"

### Configure Frontend Code

1. Navigate to frontend folder from the frontend folder

```bash
cd ../frontend/
```

2. Configure the frontend code

* In the src/components folder, open the Controller.tsx file. On the line 35, replace existing backend URL with yours. Of course, leave the /post-audio/ after the URL.
* In the src/components folder, open the Title.tsx file. On the line 19, replace existing backend URL with yours. Of course, leave the /reset/ after the URL.

Example:
* Line 35 was: .post("https://vertexai-voice-chat-backend-odxwj2pgcq-ew.a.run.app/post-audio/", formData, {
* After edit: .post("https://vertexai-voice-chat-backend-gkbtxbspgq-ew.a.run.app/post-audio/", formData, {

### Redeploy Frontend

1. Build a docker image with cloud build and push it to the Artifact Registry

REPLACE ME: replace PROJECT_ID with your project's ID in the command below.

```bash
gcloud builds submit \
    --tag="europe-west1-docker.pkg.dev/PROJECT_ID/vertexai-voice-chat-app/vertexai-voice-chat-frontend" \
    --timeout="1h" \
    --region="europe-west1" \
    --quiet 
```

2. Deploy frontend on 

REPLACE ME: replace PROJECT_ID with your project's ID in the command below.

```bash
gcloud run deploy "vertexai-voice-chat-frontend" \
    --image="europe-west1-docker.pkg.dev/PROJECT_ID/vertexai-voice-chat-app/vertexai-voice-chat-frontend" \
    --region="europe-west1" \
    --allow-unauthenticated \
    --timeout="20m" \
    --quiet  \
    --port=8080
```

### 🥳 Congratulations!

Congratulations on the successful deployment of the Vertex AI-based voice chat in your Google Cloud environment. Enjoy using the app now and talking with GenAI!

## 📜 License

All files in this repository are under the [Apache License, Version 2.0](LICENSE) unless noted otherwise.