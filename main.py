import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import ISRIStemmer
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import wordnet
import PySimpleGUI as sg
import naftawayh.wordtag
import math
import os
import re
import nltk

pre = []
preprocessed_docs = []
num_keywords = 0
test = []


def normalize_words(words, lang):
    if lang == 'eng':
        lemmatizer = WordNetLemmatizer()
        normalized_words = []
        for word in words:
            tokens = word_tokenize(word)
            normalized_tokens = []
            for token in tokens:
                normalized_token = lemmatizer.lemmatize(token, get_wordnet_pos(token))
                normalized_tokens.append(normalized_token)
            normalized_words.append(' '.join(normalized_tokens))
    elif lang == 'arab':
        stemmer = ISRIStemmer()
        normalized_words = []
        for word in words:
            tokens = word_tokenize(word)
            normalized_tokens = []
            for token in tokens:
                base_word = stemmer.stem(token)
                normalized_tokens.append(base_word)
            normalized_words.append(' '.join(normalized_tokens))
    return normalized_words


def get_wordnet_pos(word):
    tag = nltk.pos_tag([word])[0][1][0].upper()
    tag_dict = {
        'J': wordnet.ADJ,
        'N': wordnet.NOUN,
        'V': wordnet.VERB,
        'R': wordnet.ADV
    }
    return tag_dict.get(tag, wordnet.NOUN)


# Remove special characters, punctuation, and numbers and make it lowercase(Normalization)
def remove_noise(text, lang):
    if lang == 'eng':
        clean_text = re.sub('[^a-zA-Z]', ' ', text)
        clean_text = clean_text.lower()
        clean_text = re.sub('\s+', ' ', clean_text)
    elif lang == 'arab':
        clean_text = re.sub(r"[^\u0600-\u06FF\s]", "", text)
        clean_text = re.sub('\s+', ' ', clean_text)
        clean_text = re.sub('،', ' ', clean_text)
        clean_text = re.sub('[^\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\s]', '', clean_text)
        clean_text = re.sub(r"[^\u0600-\u06FF\s]+", "",
                            clean_text)  # Remove special characters, punctuation, and numbers
        clean_text = re.sub(r"\s+", " ", clean_text)  # Replace multiple white spaces with a single space
        return clean_text
    return clean_text


# stop words and tokenization
def stop_words(doc, lang):
    filtered_tokens = []
    if lang == 'eng':
        with open("E:/university/year4_Sem8/NLP/Keyword_Extraction/stop_words_english.txt", "r", encoding="utf-8") as ar_stop_list:
            stop_words = ar_stop_list.read().split('\n')
        words = word_tokenize(doc)
        for w in words:
            if w not in (stop_words):
                filtered_tokens.append(w)

        # if not nltk.download('stopwords', quiet=True):
        #     stopwords.ensure_loaded()
        # if not nltk.download('punkt', quiet=True):
        #     nltk.download('punkt')
        # # nltk.download('stopwords')
        # tokens = word_tokenize(doc)
        # stop_words = set(stopwords.words('english'))
        # stop_words.add('us')
        # filtered_tokens = [word for word in tokens if word.casefold() not in stop_words]
    elif lang == 'arab':
        with open("E:/university/year4_Sem8/NLP/Keyword_Extraction/stop_words.txt", "r", encoding="utf-8") as ar_stop_list:
            stop_words = ar_stop_list.read().split('\n')
        words = word_tokenize(doc)
        for w in words:
            if w not in (stop_words):
                filtered_tokens.append(w)

    return filtered_tokens


def process_dataset(lang):
    if lang == 'eng':
        for filenam in os.listdir("E:/university/year4_Sem8/NLP/Keyword_Extraction/dataset3"):
            file_path = os.path.join("E:/university/year4_Sem8/NLP/Keyword_Extraction/dataset3", filenam)

            # Process the file using the specified processing function
            with open(file_path, 'r') as file:
                file_content = file.read()
                processed_content = remove_noise(file_content, lang)
                processed_content = stop_words(processed_content, lang)
                pre.append(processed_content)
        for i in pre:
            preprocessed_docs.append(normalize_words(i, lang))
    elif lang == 'arab':
        for filenam in os.listdir("E:/university/year4_Sem8/NLP/Keyword_Extraction/dataset4"):
            file_path = os.path.join("E:/university/year4_Sem8/NLP/Keyword_Extraction/dataset4", filenam)

            # Process the file using the specified processing function
            with open(file_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                processed_content = remove_noise(file_content, lang)
                processed_content = stop_words(processed_content, lang)
                # processed_content = normalize_words(processed_content, lang)
                processed_content = remove_verbs(processed_content)

                # Add the processed content to the list
                pre.append(processed_content)

    return pre


def remove_verbs(text):
    tagger = naftawayh.wordtag.WordTagger()
    non_verbs = []

    # Iterate through each word in the word_list
    for word in text:
        if not tagger.is_verb(word) or word == "السويس":
            non_verbs.append(word)

    return non_verbs


def term_frequency(term, document):
    return document.count(term)


def inverse_document_frequency(term, documents):
    n = len(documents)
    df = sum(1 for doc in documents if term in doc)
    if df == 0:
        return 0
    else:
        return math.log10(n / df)


def calculate_tfidf_scores(document, documents):
    tfidf_score = {}
    for term in document:
        tf = term_frequency(term, document)
        idf = inverse_document_frequency(term, documents)
        tfidf_score[term] = tf * idf
    return tfidf_score


def write_tfidf_scores(tfidf_scores, top_n):
    sorted_terms = sorted(tfidf_scores.items(), key=lambda x: x[1], reverse=True)[:top_n]
    for term, score in sorted_terms:
        print(f"{term}: {score:.2f}")

# Define the GUI layout
layout = [
    [sg.Text('Select Language:')],
    [sg.Radio('English', 'radio_group', default=True, key='-OPTION1-'), sg.VSeparator(),
     sg.Radio('Arabic', 'radio_group', key='-OPTION2-')],
    [sg.Text("Select a text file:")],
    [sg.Input(key='-FILE-', enable_events=True), sg.FileBrowse()],
    [sg.Text("Number of Keywords: "), sg.Input(key='-NUM_KEYWORDS-', size=(5, 1))],
    [sg.Button("Find Keywords")],
    [sg.Output(size=(40, 10), key='-OUTPUT2-'), sg.VSeparator(), sg.Output(size=(40, 10), key='-OUTPUT-')]
]

# Create the window
window = sg.Window("Keyword Finder", layout)
lang = ""
# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED:
        break
    elif event == '-FILE-':
        filename = values['-FILE-']
    elif event == 'Find Keywords':

        with open(filename, 'r', encoding='utf-8') as file:
            file_content = file.read()
            window['-OUTPUT2-'].update(file_content)
        num_keywords = int(values['-NUM_KEYWORDS-'])
        if values['-OPTION1-']:
            lang = "eng"
            process_dataset(lang)
            # Open the file in read mode
            with open(filename, 'r') as file:
                # Read the content of the file
                content = file.read()
            content = remove_noise(content, lang)
            content = stop_words(content, lang)
            content = normalize_words(content, lang)
        elif values['-OPTION2-']:
            lang = "arab"
            process_dataset(lang)
            # Open the file in read mode
            with open(filename, 'r', encoding="utf-8") as file:
                # Read the content of the file
                content = file.read()
            content = remove_noise(content, lang)
            content = stop_words(content, lang)
            # content =normalize_words(content ,lang)
            content = remove_verbs(content)

        tfidf_scores = calculate_tfidf_scores(content, pre)
        window['-OUTPUT-'].update('')
        write_tfidf_scores(tfidf_scores, num_keywords)

# Close the window
window.close()
