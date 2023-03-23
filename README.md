# Initial Setup

Prepare python env:
```
conda create --name podcasters
conda activate podcasters
pip install -r requirements.txt
```

Setup GCP credentials:
```
gcloud auth login
gcloud auth application-default login
```

# Running

Start the backend:
```
cd backend/
uvicorn main:app --reload
```

Start the frontend:
```
cd frontend/
npm ci
npm run dev
```

# Notes

Find the sample rate of an MP3:

```
$ ffprobe msw_airton.mp3 
[...]
Input #0, mp3, from 'msw_airton.mp3':
  Duration: 00:16:36.36, start: 0.000000, bitrate: 127 kb/s
  Stream #0:0: Audio: mp3, 44100 Hz, stereo, fltp, 128 kb/s
```
