from google.cloud import speech
from google.cloud import speech_v1p1beta1 as speech
import json

GCP_PROJECT="redbull-hack23szg-2116"
AUDIO_FILE_URI="gs://podcasters/audio-files/msw_airton.mp3"

# Recognize speakers 
# Adapted from https://cloud.google.com/speech-to-text/docs/multiple-voices?authuser=1

client = speech.SpeechClient()

audio = speech.RecognitionAudio(uri=AUDIO_FILE_URI)

diarization_config = speech.SpeakerDiarizationConfig(
    enable_speaker_diarization=True,
    min_speaker_count=2,
    max_speaker_count=10,
)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.MP3,
    sample_rate_hertz=44100,
    language_code="en-US",
    diarization_config=diarization_config,
)

print("Waiting for operation to complete...")
operation = client.long_running_recognize(config=config, audio=audio)

response = operation.result(timeout=600)

response_json = json.dumps(response)
with open('response.json', 'r') as outfile:
    outfile.write(response_json)

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:
result = response.results[-1]

words_info = result.alternatives[0].words

# Printing out the output:
for word_info in words_info:
    print(
        "word: '{}', speaker_tag: {}".format(word_info.word, word_info.speaker_tag)
    )


