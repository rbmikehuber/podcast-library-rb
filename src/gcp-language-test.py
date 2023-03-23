# Imports the Google Cloud client library
from google.cloud import language_v1

def get_sentiment(text):
    # Instantiates a client
    client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    print("Text: {}".format(text))
    print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

    # Output
    # Text: Max Verstappen sits down with us to recap his extraordinary 2022 season where he won his second Formula 1 world title.
    # Sentiment: 0.5, 0.5


def classify(text, verbose=True):
    """Classify the input text into categories."""

    language_client = language_v1.LanguageServiceClient()

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT
    )
    response = language_client.classify_text(request={"document": document})
    categories = response.categories

    result = {}

    for category in categories:
        # Turn the categories into a dictionary of the form:
        # {category.name: category.confidence}, so that they can
        # be treated as a sparse vector.
        result[category.name] = category.confidence

    if verbose:
        print(text)
        for category in categories:
            print("=" * 20)
            print("{:<16}: {}".format("category", category.name))
            print("{:<16}: {}".format("confidence", category.confidence))

    # Output
    # Max Verstappen sits down with us to recap his extraordinary 2022 season where he won his second Formula 1 world title.
    # ====================
    # category        : /Sports/Motor Sports
    # confidence      : 0.9700000286102295

    return result


def sample_classify_text(text_content):
    """
    Classifying Content in a String

    Args:
      text_content The text content to analyze.
    """

    client = language_v1.LanguageServiceClient()

    # text_content = "That actor on TV makes movies in Hollywood and also stars in a variety of popular new TV shows."

    # Available types: PLAIN_TEXT, HTML
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # Optional. If not specified, the language is automatically detected.
    # For list of supported languages:
    # https://cloud.google.com/natural-language/docs/languages
    language = "en"
    document = {"content": text_content, "type_": type_, "language": language}

    content_categories_version = (
        language_v1.ClassificationModelOptions.V2Model.ContentCategoriesVersion.V2
    )
    response = client.classify_text(
        request={
            "document": document,
            "classification_model_options": {
                "v2_model": {"content_categories_version": content_categories_version}
            },
        }
    )
    # Loop through classified categories returned from the API
    for category in response.categories:
        # Get the name of the category representing the document.
        # See the predefined taxonomy of categories:
        # https://cloud.google.com/natural-language/docs/categories
        print("Category name: {}".format(category.name))
        # Get the confidence. Number representing how certain the classifier
        # is that this category represents the provided text.
        print("Confidence: {}".format(category.confidence))

    # Output
    # Category name: /Sports/Motor Sports/Auto Racing
    # Confidence: 0.9255370497703552
    # Category name: /News/Sports News
    # Confidence: 0.799889862537384
    # Category name: /Sports/International Sports Competitions/Other
    # Confidence: 0.2289700210094452



TEST_TEXT = "Max Verstappen sits down with us to recap his extraordinary 2022 season where he won his second Formula 1 world title."

print("\nget_sentiment")
get_sentiment(TEST_TEXT)

print("\nclassify")
classify(TEST_TEXT)

print("\nsample_classify")
sample_classify_text(TEST_TEXT)
