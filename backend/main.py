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
import random

podcasts = [
    {
        "name": "Airton Cozzolino interview",
        "audio_file": "resources/audio-files/audio-files_msw_airton.mp3",
        "transcript": "resources/transcripts/msw_airton.mp3.json",
        "transcript_only": "resources/transcripts/msw_airton.txt"
    },
    {
        "name": "Small test podcast",
        "audio_file": "resources/audio-files/output.mp3",
        "transcript": "resources/transcripts/output.mp3.json",
        "transcript_only": "resources/transcripts/output.txt"
    },
    {
        "name": "Long, Bergwelten Podcast",
        "audio_file": "resources/audio-files/bergwelten_2023_f02_februar_v1_230209.mp3",
        "transcript": "resources/transcripts/bergwelten_2023_f02_februar_v1_230209.mp3.json",
        "transcript_only": "resources/transcripts/bergwelten_2023_f02_februar_v1_230209.txt"
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

@app.get("/podcasts")
def get_podcasts():
    return [ { "id": i, "name": p["name"] } for i, p in enumerate(podcasts)]

@app.get("/podcasts/{id}/words")
def read_words(id: int):
    podcast = podcasts[id]
    with open(podcast["transcript"], 'r') as f:
        return json.loads(f.read())["words"]

@app.get("/podcasts/{id}/keywords")
def get_keywords(id: int):
    podcast = podcasts[id]

    keywords = []
    with open(podcast["transcript_only"], 'r') as f:
        for chunk in _read_chunked(f):
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=f"Extract the 5 most important keywords from this text and provide them as a comma-separated list:\n\n{chunk}",
                temperature=0.5,
                max_tokens=600,
                top_p=1.0,
                frequency_penalty=0.8,
                presence_penalty=0.0
            )
            keywords_text = str.strip(response["choices"][0]["text"])
            keywords_text = keywords_text.split("Keywords: ")[-1]
            keywords.extend(keywords_text.split(", "))
            print(keywords)

    keywords = [keyword for keyword in keywords if len(keyword.split()) == 1]
    return random.sample(keywords, 5)


@app.get("/podcasts/{id}/summary")
def get_summary(id: int):
    podcast = podcasts[id]

    text = ""
    with open(podcast["transcript_only"], 'r') as f:
        chunks = list(_read_chunked(f))
        if len(chunks) > 1:
            for chunk in chunks:
                text += f" {_get_openai_summary(chunk)}"
                return _get_openai_summary(text)
        else:
            return _get_openai_summary(chunks[0])

def _get_openai_summary(text):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages= [
            {"role": "user", "content": f"{text}\n\nTl;dr" }
        ]
    )
    print(response)
    summary = str.strip(response["choices"][0]["message"]["content"])

    return summary


# To get around the token size error:
# openai.error.InvalidRequestError: This model's maximum context length is 4097 tokens,
# however you requested 10736 tokens (10136 in your prompt; 600 for the completion).
# Please reduce your prompt; or completion length.
def _read_chunked(fh, chunk_size=8192):
    while True:
        data = fh.read(chunk_size)
        if not data:
            break
        yield data


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