
ENV_VARS=$(paste -sd, .api.env)
REGION="us-central1"

echo $ENV_VARS

gcloud run deploy $IMAGE_NAME \
  --image us-docker.pkg.dev/proyecto-cs-455920/gcr-compat/cloud-solutions-api:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --add-cloudsql-instances=proyecto-cs-455920:us-central1:postgres \
  --set-env-vars $ENV_VARS
