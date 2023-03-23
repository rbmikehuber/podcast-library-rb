from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel
import ffmpeg
from fastapi.responses import FileResponse
import tempfile

# TODO: don't use these but rather a format like in ../src/output.mp3.json

podcasts = [
    {
        "audio_file": "resources/audio-files/audio-files_msw_mario.mp3",
        "transcript": "resources/transcripts/transcripts_msw_mario.mp3-20230323024230.json"
    },
    {
        "audio_file": "resources/audio-files/short_podcast.mp3",
        "transcript": "resources/transcripts/transcripts_short_podcast.mp3-20230323030932.json"
    }
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)


@app.get("/podcasts/{id}/transcript")
def read_transcript(id: int):
    podcast = podcasts[id]
    with open(podcast["transcript"], 'r') as f:
        return json.loads(f.read())["results"][0]["alternatives"][0]["transcript"]


@app.get("/podcasts/{id}/words")
def read_words(id: int):
    podcast = podcasts[id]
    with open(podcast["transcript"], 'r') as f:
        return json.loads(f.read())["results"][0]["alternatives"][0]["words"]

class Word(BaseModel):
    word: str
    startTime: str
    endTime: str

class ExcerptRequest(BaseModel):
    words: list[Word]

def time_str_to_num(timeStr: str):
    return float(timeStr[:-1])

def word_length(w: Word):
    return time_str_to_num(w.endTime) - time_str_to_num(w.startTime)

def get_temp_file_name():
    tmp_dir = tempfile._get_default_tempdir()
    return tmp_dir + "/" + next(tempfile._get_candidate_names())

@app.post("/podcasts/{id}/excerpt")
def get_excerpt(id: int, req: ExcerptRequest):
    start_time = time_str_to_num(req.words[0].startTime)
    length_seconds = sum([word_length(w) for w in req.words[1:]])

    print(f"Generating excerpt starting at {start_time}s, duration {length_seconds}s")

    tmp_file = f"{get_temp_file_name()}.mp3"

    print(tmp_file)
    podcast = podcasts[id]
    (
        ffmpeg
        .input(podcast["audio_file"], ss=start_time, to=start_time+length_seconds)
        .output(tmp_file)
        .run()
    )

    return FileResponse(tmp_file, media_type="audio/mpeg")
