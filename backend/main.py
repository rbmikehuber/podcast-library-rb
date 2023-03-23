from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
from pydantic import BaseModel
import ffmpeg
from fastapi.responses import FileResponse
import tempfile
import openai
from fastapi.staticfiles import StaticFiles
import os

podcasts = [
    {
        "audio_file": "resources/audio-files/audio-files_msw_airton.mp3",
        "transcript": "resources/transcripts/msw_airton.mp3.json",
        "transcript_only": "resources/transcripts/msw_airton.txt"
    },
    {
        "audio_file": "resources/audio-files/audio-files_msw_airton.mp3",
        "transcript": "resources/transcripts/output.mp3.json",
        "transcript_only": "resources/transcripts/output.txt"
    }
]

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

@app.get("/podcasts/{id}/words")
def read_words(id: int):
    podcast = podcasts[id]
    with open(podcast["transcript"], 'r') as f:
        return json.loads(f.read())["words"]

@app.get("/podcasts/{id}/keywords")
def get_keywords(id: int):
    podcast = podcasts[id]
    with open(podcast["transcript_only"], 'r') as f:
        text = f.readlines()

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Extract keywords from this text:\n\n{text}",
        temperature=0.5,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.8,
        presence_penalty=0.0
    )
    keywords_text = str.strip(response["choices"][0]["text"])
    keywords_text = keywords_text.split("Keywords: ")[-1]
    keywords = keywords_text.split(", ")
    return json.dumps(keywords)


# !! This is actually quite a bit slower than expected.
# It took about 1.5 minutes for "msw_airton.txt"
@app.get("/podcasts/{id}/summary")
def get_summary(id: int):
    podcast = podcasts[id]
    with open(podcast["transcript_only"], 'r') as f:
        text = f.readlines()

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"{text}\n\nTl;dr",
        temperature=0.7,
        max_tokens=60,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=1
    )
    summary = str.strip(response["choices"][0]["text"])
    return summary


class Word(BaseModel):
    word: str
    start_time: str
    end_time: str

class ExcerptRequest(BaseModel):
    words: list[Word]

def time_str_to_num(timeStr: str):
    return float(timeStr)

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

if os.path.exists("dist"):
    app.mount("/", StaticFiles(directory="dist", html=True), name="dist")