rm -r artifact/
mkdir -p artifact
cp Dockerfile artifact

cd ../frontend
npm ci
npm run build
cp -r dist ../deployment/artifact
cd ../backend
cp -r * ../deployment/artifact

# build locally
# docker build -t podcast-library-rb .

# build & deploy on GCP

gcloud builds submit -t eu.gcr.io/redbull-hack23szg-2116/podcast-library-rb:latest .
gcloud run deploy podcast-insights --allow-unauthenticated --image eu.gcr.io/redbull-hack23szg-2116/podcast-library-rb:latest