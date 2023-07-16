# TF.IDFKeywordsExtraction
 This project aimed to identify important keywords from text documents using the TF-IDF algorithm, a widely used technique in natural language processing and information retrieval.

The project involved several key steps. Firstly, I leveraged the NLTK (Natural Language Toolkit) library in Python to perform text preprocessing tasks, including noise removal, tokenization, stop word removal, and normalization. For English text, I used WordNetLemmatizer for lemmatization, while for Arabic text, I utilized the ISRIStemmer for stemming. These preprocessing steps ensured that the resulting keywords were clean and representative of the document content.

Next, I implemented the TF-IDF algorithm, which calculates a weight for each term in a document based on its frequency within the document and its inverse frequency across the entire corpus of documents. This weight represents the term's importance or relevance within the document collection. By ranking the terms based on their TF-IDF scores, I identified the most significant keywords.

To evaluate the effectiveness of the TF-IDF keyword extraction, I utilized a dataset consisting of various documents, including both English and Arabic text. By fine-tuning the algorithm and optimizing the parameters, I achieved accurate and informative keyword extraction results.

The project also featured a user-friendly Graphical User Interface (GUI) built using the PySimpleGUI library. The GUI enabled users to select the language, input a text file for keyword extraction, and specify the desired number of keywords to extract. The output provided a list of the top keywords based on their TF-IDF scores.

This project enhanced my skills in natural language processing, text preprocessing, and information retrieval techniques. It showcased my ability to apply advanced algorithms, utilize relevant libraries, and develop practical solutions for extracting valuable insights from textual data.

# This is for English article example that is talking about the solar system and the plants 

![Screenshot 2023-07-17 002852](https://github.com/HagarSameh/TF.IDFKeywordsExtraction/assets/71992147/9f05dc37-2b3f-4d88-a624-8b0d0bb324fa)

# This is for Arabic article example that is talking about Egyptian pyramids and the Egyptian civilization

![Screenshot 2023-07-17 003020](https://github.com/HagarSameh/TF.IDFKeywordsExtraction/assets/71992147/6482f491-914e-450b-80e7-d5981ebaa5b2)

