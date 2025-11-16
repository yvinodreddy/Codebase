#!/bin/bash

# ===============================================
# Google Cloud AI Platform Setup Script
# For Healthcare AI Startup - $350K Credits
# ===============================================

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
PROJECT_ID="medigenius-ai-health"
REGION="us-central1"
CLUSTER_NAME="ai-healthcare-cluster"
DATASET_ID="healthcare_ai_data"

echo -e "${BLUE}========================================${NC}"
echo -e "${BLUE}  Google Cloud AI Platform Setup${NC}"
echo -e "${BLUE}  Healthcare AI Startup Qualification${NC}"
echo -e "${BLUE}========================================${NC}"

# Step 1: Check gcloud installation
echo -e "\n${YELLOW}Step 1: Checking gcloud CLI...${NC}"
if ! command -v gcloud &> /dev/null; then
    echo -e "${RED}gcloud CLI not found. Installing...${NC}"
    curl https://sdk.cloud.google.com | bash
    exec -l $SHELL
else
    echo -e "${GREEN}✓ gcloud CLI found${NC}"
fi

# Step 2: Authenticate
echo -e "\n${YELLOW}Step 2: Authenticating with Google Cloud...${NC}"
gcloud auth login --no-launch-browser

# Step 3: Create project
echo -e "\n${YELLOW}Step 3: Creating Google Cloud project...${NC}"
gcloud projects create $PROJECT_ID --name="MediGenius AI Healthcare" 2>/dev/null || echo "Project already exists"
gcloud config set project $PROJECT_ID

# Step 4: Enable billing (requires manual step)
echo -e "\n${YELLOW}Step 4: Enable billing for project${NC}"
echo -e "${RED}IMPORTANT: Please enable billing for project $PROJECT_ID${NC}"
echo -e "Visit: https://console.cloud.google.com/billing/linkedaccount?project=$PROJECT_ID"
read -p "Press enter when billing is enabled..."

# Step 5: Enable required AI APIs
echo -e "\n${YELLOW}Step 5: Enabling Google Cloud AI APIs...${NC}"

APIS=(
    "aiplatform.googleapis.com"
    "generativelanguage.googleapis.com"
    "automl.googleapis.com"
    "vision.googleapis.com"
    "healthcare.googleapis.com"
    "bigquery.googleapis.com"
    "bigquerymigration.googleapis.com"
    "bigquerystorage.googleapis.com"
    "cloudapis.googleapis.com"
    "cloudbuild.googleapis.com"
    "cloudfunctions.googleapis.com"
    "cloudresourcemanager.googleapis.com"
    "compute.googleapis.com"
    "container.googleapis.com"
    "containerregistry.googleapis.com"
    "dialogflow.googleapis.com"
    "documentai.googleapis.com"
    "iam.googleapis.com"
    "iamcredentials.googleapis.com"
    "lifesciences.googleapis.com"
    "logging.googleapis.com"
    "monitoring.googleapis.com"
    "notebooks.googleapis.com"
    "pubsub.googleapis.com"
    "run.googleapis.com"
    "servicemanagement.googleapis.com"
    "serviceusage.googleapis.com"
    "storage-api.googleapis.com"
    "storage-component.googleapis.com"
    "texttospeech.googleapis.com"
    "translate.googleapis.com"
)

for api in "${APIS[@]}"; do
    echo "Enabling $api..."
    gcloud services enable $api --project=$PROJECT_ID
done

echo -e "${GREEN}✓ All AI APIs enabled${NC}"

# Step 6: Create AI service account
echo -e "\n${YELLOW}Step 6: Creating AI service account...${NC}"
gcloud iam service-accounts create ai-healthcare-sa \
    --display-name="AI Healthcare Service Account" \
    --project=$PROJECT_ID 2>/dev/null || echo "Service account exists"

# Grant necessary roles
gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:ai-healthcare-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:ai-healthcare-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/bigquery.admin"

gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:ai-healthcare-sa@$PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/healthcare.fhirStoreAdmin"

echo -e "${GREEN}✓ Service account created${NC}"

# Step 7: Create GKE cluster for AI workloads
echo -e "\n${YELLOW}Step 7: Creating GKE cluster for AI workloads...${NC}"
gcloud container clusters create $CLUSTER_NAME \
    --region=$REGION \
    --num-nodes=3 \
    --machine-type=n1-standard-4 \
    --enable-autoscaling \
    --min-nodes=2 \
    --max-nodes=10 \
    --addons=HorizontalPodAutoscaling,HttpLoadBalancing \
    --enable-autorepair \
    --enable-autoupgrade \
    --scopes=cloud-platform \
    --project=$PROJECT_ID

# Add GPU node pool for AI inference
gcloud container node-pools create gpu-pool \
    --cluster=$CLUSTER_NAME \
    --region=$REGION \
    --accelerator=type=nvidia-tesla-t4,count=1 \
    --num-nodes=1 \
    --min-nodes=0 \
    --max-nodes=3 \
    --enable-autoscaling \
    --machine-type=n1-standard-4 \
    --project=$PROJECT_ID

echo -e "${GREEN}✓ GKE cluster created${NC}"

# Step 8: Create BigQuery dataset for ML
echo -e "\n${YELLOW}Step 8: Creating BigQuery dataset for ML...${NC}"
bq mk --dataset \
    --location=$REGION \
    --description="Healthcare AI Training Data" \
    $PROJECT_ID:$DATASET_ID

echo -e "${GREEN}✓ BigQuery dataset created${NC}"

# Step 9: Create Cloud Storage buckets
echo -e "\n${YELLOW}Step 9: Creating Cloud Storage buckets...${NC}"
gsutil mb -p $PROJECT_ID -c standard -l $REGION gs://${PROJECT_ID}-models/
gsutil mb -p $PROJECT_ID -c standard -l $REGION gs://${PROJECT_ID}-medical-images/
gsutil mb -p $PROJECT_ID -c standard -l $REGION gs://${PROJECT_ID}-training-data/

echo -e "${GREEN}✓ Storage buckets created${NC}"

# Step 10: Set up Vertex AI
echo -e "\n${YELLOW}Step 10: Initializing Vertex AI...${NC}"
gcloud ai platform locations list --project=$PROJECT_ID

# Create a Vertex AI dataset
gcloud ai datasets create \
    --display-name="medical-diagnosis-dataset" \
    --dataset-type=TEXT \
    --region=$REGION \
    --project=$PROJECT_ID

echo -e "${GREEN}✓ Vertex AI initialized${NC}"

# Step 11: Create initial AI models
echo -e "\n${YELLOW}Step 11: Setting up initial AI models...${NC}"

# Create AutoML training pipeline (placeholder)
cat > /tmp/automl-config.yaml << EOF
displayName: medical-diagnosis-automl
trainingTaskDefinition: gs://google-cloud-aiplatform/schema/trainingjob/definition/automl_text_classification_1.0.0.yaml
trainingTaskInputs:
  targetColumn: diagnosis
modelToUpload:
  displayName: medical-diagnosis-model
EOF

echo -e "${GREEN}✓ AI model configs created${NC}"

# Step 12: Deploy monitoring
echo -e "\n${YELLOW}Step 12: Setting up AI monitoring...${NC}"
gcloud alpha monitoring policies create \
    --notification-channels=projects/$PROJECT_ID/notificationChannels/basic \
    --display-name="AI Model Performance" \
    --condition-display-name="Low Accuracy Alert" \
    --condition-threshold-value=0.85 \
    --condition-threshold-duration=300s \
    --project=$PROJECT_ID 2>/dev/null || echo "Monitoring exists"

echo -e "${GREEN}✓ Monitoring configured${NC}"

# Step 13: Generate application credentials
echo -e "\n${YELLOW}Step 13: Generating application credentials...${NC}"
gcloud iam service-accounts keys create ./credentials.json \
    --iam-account=ai-healthcare-sa@$PROJECT_ID.iam.gserviceaccount.com \
    --project=$PROJECT_ID

echo -e "${GREEN}✓ Credentials saved to ./credentials.json${NC}"

# Step 14: Create .env file
echo -e "\n${YELLOW}Step 14: Creating environment configuration...${NC}"
cat > .env << EOF
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=$PROJECT_ID
GOOGLE_APPLICATION_CREDENTIALS=./credentials.json
GOOGLE_CLOUD_REGION=$REGION
GKE_CLUSTER=$CLUSTER_NAME

# AI Service Endpoints
VERTEX_AI_ENDPOINT=https://${REGION}-aiplatform.googleapis.com
GEMINI_API_ENDPOINT=https://generativelanguage.googleapis.com
HEALTHCARE_API_ENDPOINT=https://healthcare.googleapis.com

# BigQuery Configuration
BIGQUERY_DATASET=$DATASET_ID
BIGQUERY_PROJECT=$PROJECT_ID

# Storage Buckets
MODEL_BUCKET=gs://${PROJECT_ID}-models
IMAGE_BUCKET=gs://${PROJECT_ID}-medical-images
TRAINING_BUCKET=gs://${PROJECT_ID}-training-data

# Feature Flags
ENABLE_AI_DIAGNOSIS=true
ENABLE_AI_REPORTS=true
ENABLE_AI_PRESCRIPTIONS=true
ENABLE_AI_CHATBOT=true
ENABLE_IMAGE_ANALYSIS=true
ENABLE_HEALTH_PREDICTIONS=true

# AI Model Configuration
DIAGNOSIS_MODEL_NAME=medical-diagnosis-model
PREDICTION_MODEL_NAME=health-risk-predictor
IMAGE_MODEL_NAME=medical-image-analyzer

# Monitoring
ENABLE_AI_MONITORING=true
ALERT_EMAIL=admin@medigenius-ai.com
EOF

echo -e "${GREEN}✓ Environment configuration created${NC}"

# Step 15: Create sample AI request
echo -e "\n${YELLOW}Step 15: Creating sample AI request...${NC}"
cat > test-ai-diagnosis.json << EOF
{
  "patient": {
    "age": 45,
    "gender": "male",
    "medicalHistory": ["hypertension", "type2_diabetes"]
  },
  "symptoms": [
    "chest pain",
    "shortness of breath",
    "fatigue",
    "irregular heartbeat"
  ],
  "vitals": {
    "bloodPressure": "150/95",
    "heartRate": 110,
    "temperature": 98.6,
    "oxygenSaturation": 94
  },
  "labResults": {
    "cholesterol": 240,
    "bloodSugar": 180,
    "triglycerides": 200
  }
}
EOF

echo -e "${GREEN}✓ Sample request created${NC}"

# Final Summary
echo -e "\n${GREEN}========================================${NC}"
echo -e "${GREEN}  ✅ Google Cloud AI Setup Complete!${NC}"
echo -e "${GREEN}========================================${NC}"
echo -e "\n${BLUE}Project Details:${NC}"
echo -e "  Project ID: ${YELLOW}$PROJECT_ID${NC}"
echo -e "  Region: ${YELLOW}$REGION${NC}"
echo -e "  Cluster: ${YELLOW}$CLUSTER_NAME${NC}"
echo -e "  Dataset: ${YELLOW}$DATASET_ID${NC}"

echo -e "\n${BLUE}Next Steps:${NC}"
echo -e "  1. Run ${YELLOW}npm install${NC} to install dependencies"
echo -e "  2. Run ${YELLOW}npm run deploy:ai${NC} to deploy AI services"
echo -e "  3. Run ${YELLOW}npm run test:ai${NC} to test AI endpoints"
echo -e "  4. Visit ${YELLOW}https://console.cloud.google.com/ai-platform?project=$PROJECT_ID${NC}"

echo -e "\n${BLUE}Cost Estimate:${NC}"
echo -e "  Current setup: ~\$5/day"
echo -e "  With AI traffic: ~\$100-500/day"
echo -e "  ${GREEN}Covered by \$350K startup credits!${NC}"

echo -e "\n${YELLOW}⚠️  IMPORTANT:${NC}"
echo -e "  1. Keep credentials.json secure!"
echo -e "  2. Enable budget alerts in GCP Console"
echo -e "  3. Apply for Google Startup Program ASAP"
echo -e "  4. Review HIPAA compliance requirements"

echo -e "\n${GREEN}🚀 Ready to build AI Healthcare Platform!${NC}"