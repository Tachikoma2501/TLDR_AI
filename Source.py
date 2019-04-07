# This was ceated with the help of the guide found at
# https://dev.to/davidisrawi/build-a-quick-summarizer-with-python-and-nltk

from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize, sent_tokenize

# The article is from https://www.livescience.com/63817-atlas-robot-parkour.html
text_str = '''
Remember Atlas, the robot that can run like a person? It can now do a lot more than that.

Yesterday, (Oct. 11) robotics company Boston Dynamics posted a new video on YouTube showcasing the robot's latest progress, carrying it past its prior agility goals in leaps and bounds — literally.

"Atlas does parkour," Boston Dynamics wrote in the video description. Footage shows Atlas nimbly leaping over a log and skipping between platforms of different heights "without breaking its pace," according to the description. [Robots on the Run! 5 Bots That Can Really Move]

As Atlas navigates the challenges of the obstacle course, a slow-motion sequence emphasizes the precision in its movements as it leaps between platforms, each one measuring about 16 inches (40 centimeters) high. Software and vision sensors control Atlas's navigation, according to the video description — nevertheless, the robot's coordination seem remarkably humanlike for a machine.

Described on the Boston Dynamics website as "the world's most dynamic humanoid," Atlas has a four-limbed, bipedal frame that would invite comparison to the human body regardless of how the robot moved. But in a series of videos released over the last few years, Atlas demonstrates mobility this is uncannily human: recovering after being shoved, performing backflips, jogging over a grassy field and practicing robot parkour.

The prospect of a humanoid robot that can leap, backflip and bound after you over rugged terrain is unsettling enough, but Atlas's creators at Boston Dynamics keep pushing the bot toward ever more ambitious gymnastic achievements.

What's next for the nimble Atlas? Only its designers know for sure.
'''


def _create_frequency_table(text_string) -> dict:
    """
    This creates the dictionary for the program
    :rtype: dict
    """
    stopWords = set(stopwords.words("english"))
    words = word_tokenize(text_string)
    ps = PorterStemmer()

    freqTable = dict()
    for word in words:
        word = ps.stem(word)
        if word in stopWords:
            continue
        if word in freqTable:
            freqTable[word] += 1
        else:
            freqTable[word] = 1

    return freqTable


def _score_sentences(sentences, freqTable) -> dict:

    sentenceValue = dict()

    for sentence in sentences:
        word_count_in_sentence = (len(word_tokenize(sentence)))
        word_count_in_sentence_except_stop_words = 0
        for wordValue in freqTable:
            if wordValue in sentence.lower():
                word_count_in_sentence_except_stop_words += 1
                if sentence[:10] in sentenceValue:
                    sentenceValue[sentence[:10]] += freqTable[wordValue]
                else:
                    sentenceValue[sentence[:10]] = freqTable[wordValue]

        sentenceValue[sentence[:10]] = sentenceValue[sentence[:10]] / word_count_in_sentence_except_stop_words


    return sentenceValue


def _find_average_score(sentenceValue) -> int:
    """
    This is used to find the average score from the sentence value dictionary
    """
    sumValues = 0
    for entry in sentenceValue:
        sumValues += sentenceValue[entry]

    # The average value of a sentence from original text is calculated by setting average to the
    # Sum divided by the len/value
    average = (sumValues / len(sentenceValue))

    return average


def _generate_summary(sentences, sentenceValue, threshold):
    sentence_count = 0
    summary = ''

    for sentence in sentences:
        if sentence[:10] in sentenceValue and sentenceValue[sentence[:10]] >= (threshold):
            summary += " " + sentence
            sentence_count += 1

    return summary

# Comments copied to show each step from the guide.
def run_summarization(text):
    # 1 Create the word frequency table
    freq_table = _create_frequency_table(text)

    # 2 Tokenize the sentences
    sentences = sent_tokenize(text)

    # 3 Important Algorithm: score the sentences
    sentence_scores = _score_sentences(sentences, freq_table)

    # 4 Find the threshold
    threshold = _find_average_score(sentence_scores)

    # 5 Important Algorithm: Generate the summary
    summary = _generate_summary(sentences, sentence_scores, 1.3 * threshold)

    return summary


if __name__ == '__main__':
    result = run_summarization(text_str)
print(result)