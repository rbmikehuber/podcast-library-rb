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
        "audio_file": "resources/audio-files/audio-files_msw_airton.mp3",
        "transcript": "resources/transcripts/msw_airton.mp3.json"
    },
    {
        "audio_file": "resources/audio-files/audio-files_msw_airton.mp3",
        "transcript": "resources/transcripts/output.mp3.json"
    }
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"]
)

@app.get("/podcasts/{id}/words")
def read_words(id: int):
    podcast = podcasts[id]
    with open(podcast["transcript"], 'r') as f:
        return json.loads(f.read())["words"]

class Word(BaseModel):
    word: str
    start_time: str
    end_time: str

class ExcerptRequest(BaseModel):
    words: list[Word]

def time_str_to_num(timeStr: str):
    return float(timeStr)

def word_length(w: Word):
    length=time_str_to_num(w.end_time) - time_str_to_num(w.start_time)
    print(f"{w.word}: {length}s")
    return length

def get_temp_file_name():
    tmp_dir = tempfile._get_default_tempdir()
    return tmp_dir + "/" + next(tempfile._get_candidate_names())

@app.post("/podcasts/{id}/excerpt")
def get_excerpt(id: int, req: ExcerptRequest):
    start_time = time_str_to_num(req.words[0].start_time)
    end_time = time_str_to_num(req.words[-1].end_time)

    print(f"Generating excerpt from {start_time}s to {end_time}s")

    tmp_file = f"{get_temp_file_name()}.mp3"

    podcast = podcasts[id]
    (
        ffmpeg
        .input(podcast["audio_file"], ss=start_time, to=end_time)
        .output(tmp_file)
        .run()
    )

    return FileResponse(tmp_file, media_type="audio/mpeg")
