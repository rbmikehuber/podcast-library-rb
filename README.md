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

# Adding a podcast to the app

1. Upload the podcast audio file to a GCP storage bucket.
2. Use `src/main.py` to transcribe the podcast into a JSON file.
3. Put the podcast audio file into `backend/resources/audio-files/`.
4. Put the transcript JSON into `backend/resources/transcripts`.
5. Add the two files to the `podcasts` array in `backend/main.py`.

# Notes

Find the sample rate of an MP3:

```
$ ffprobe msw_airton.mp3 
[...]
Input #0, mp3, from 'msw_airton.mp3':
  Duration: 00:16:36.36, start: 0.000000, bitrate: 127 kb/s
  Stream #0:0: Audio: mp3, 44100 Hz, stereo, fltp, 128 kb/s
```
