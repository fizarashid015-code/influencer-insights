from textblob import TextBlob

def test_positive_sentiment():
    score = TextBlob("This is amazing!").sentiment.polarity
    assert score > 0

def test_negative_sentiment():
    score = TextBlob("This is terrible!").sentiment.polarity
    assert score < 0

def test_neutral_sentiment():
    score = TextBlob("this").sentiment.polarity
    assert score == 0

print("All tests passed!")