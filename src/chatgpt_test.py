import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def tldr(text):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"{text}\n\nTl;dr",
    temperature=0.7,
    max_tokens=60,
    top_p=1.0,
    frequency_penalty=0.0,
    presence_penalty=1
  )
  print(response)

  # Output
  # {
  #   "choices": [
  #     {
  #       "finish_reason": "length",
  #       "index": 0,
  #       "logprobs": null,
  #       "text": ": Mario Gomez, a professional footballer, talks about the ups and downs of his career and how he maintained self-efficacy even in the face of failure. He shares his experience of playing at the highest level and advises
  # listeners to accept mistakes and maintain confidence in order to succeed. He suggests that believing"
  #     }
  #   ],
  #   "created": 1679592876,
  #   "id": "cmpl-6xJ7cYmXLvtEd6quinBYr2Bn2KGNU",
  #   "model": "text-davinci-003",
  #   "object": "text_completion",
  #   "usage": {
  #     "completion_tokens": 60,
  #     "prompt_tokens": 3342,
  #     "total_tokens": 3402
  #   }
  # }


def keywords(text):
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=f"Extract keywords from this text:\n\n{text}",
    temperature=0.5,
    max_tokens=60,
    top_p=1.0,
    frequency_penalty=0.8,
    presence_penalty=0.0
  )
  print(response)

  # Output
  # {
  #   "choices": [
  #     {
  #       "finish_reason": "stop",
  #       "index": 0,
  #       "logprobs": null,
  #       "text": "\n\nKeywords: professional play, score, pressure, doubts, self-efficacy, winning mentality, challenges, opportunities, confidence, mistakes part of success story, internalize failure"
  #     }
  #   ],
  #   "created": 1679592878,
  #   "id": "cmpl-6xJ7eeTkszGIzofSkmUMGsegy4Las",
  #   "model": "text-davinci-003",
  #   "object": "text_completion",
  #   "usage": {
  #     "completion_tokens": 37,
  #     "prompt_tokens": 3345,
  #     "total_tokens": 3382
  #   }
  # }


if __name__ == "__main__":
  TEST_TEXT = "Max Verstappen sits down with us to recap his extraordinary 2022 season where he won his second Formula 1 world title."

  with open("msw_mario.txt") as fh:
    long_transcript = fh.readlines()

  print("\nTL;DR")
  tldr(long_transcript)

  print("\nKeywords")
  keywords(long_transcript)
