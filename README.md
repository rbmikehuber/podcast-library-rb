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
2. Use `src/main.py` to transcribe the podcast into a JSON file (be sure to set the correct `language_code`!).
3. Put the podcast audio file into `backend/resources/audio-files/`.
4. Put the transcript JSON into `backend/resources/transcripts`.
5. Add the two files to the `podcasts` array in `backend/main.py`:
    - The podcast audio file with key `audio_file`.
    - The transcript JSON with key `transcript`.
    - Add a nice name with key `name`.

## Addding the full transcript text
1. After you have already uploaded the audio file to the GCP bucket (step 1 above)
2. Create a "new transcription" in the GCP console from the audio file you just added: https://console.cloud.google.com/speech/transcriptions/list?authuser=0&project=redbull-hack23szg-2116
3. Wait until the processing is complete, then click on your new transcript
4. Click the "DOWNLOAD" button at the top of the transcription and download the transcript as text
5. Move this file to `backend/resources/transcripts`
6. Add this file to the `podcasts` list at the top of `main.py` with the key `transcript_only`:
```python
podcasts = [
    {
        "name": "Airton Cozzolino interview",
        "audio_file": "resources/audio-files/audio-files_msw_airton.mp3",
        "transcript": "resources/transcripts/msw_airton.mp3.json",
        "transcript_only": "resources/transcripts/msw_airton.txt"
    }
]
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
