from google.cloud import speech_v1p1beta1 as speech
import json
import logging

GCP_PROJECT = "redbull-hack23szg-2116"
AUDIO_FILENAME = "bergwelten_2023_f02_februar_v1_230209.mp3"
AUDIO_FILE_URI = f"gs://podcasters/audio-files/{AUDIO_FILENAME}"


def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)-8s %(message)s",
        level=logging.DEBUG,
        datefmt="%Y-%m-%d %H:%M:%S",
    )

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
        language_code="de-DE",
        diarization_config=diarization_config,
    )

    logging.info("Waiting for operation to complete...")
    operation = client.long_running_recognize(config=config, audio=audio)

    response = operation.result(timeout=6000)

    # for result in response.results:
    #     print(result)
    #     for alternative in result.alternatives:
    #         print(alternative)
    # print("Transcript: {}".format(result.alternatives[0].transcript))
    # print("Confidence: {}".format(result.alternatives[0].confidence))

    # response_json = json.dumps(response)
    # with open('response.json', 'r') as outfile:
    #     outfile.write(response_json)

    # The transcript within each result is separate and sequential per result.
    # However, the words list within an alternative includes all the words
    # from all the results thus far. Thus, to get all the words with speaker
    # tags, you only have to take the words list from the last result:
    result = response.results[-1]
    # print(result)
    # print(json.dumps(result))

    words_info = result.alternatives[0].words
    logging.debug(words_info)
    # Printing out the output:
    json_out = {"words": []}
    for word_info in words_info:
        json_out["words"].append(
            {
                "word": word_info.word,
                "speaker_tag": word_info.speaker_tag,
                "start_time": word_info.start_time.total_seconds(),
                "end_time": word_info.end_time.total_seconds(),
            }
        )

    logging.debug(json_out)
    with open(f"{AUDIO_FILENAME}.json", "w") as fh:
        fh.write(json.dumps(json_out, indent=2))


if __name__ == "__main__":
    main()
