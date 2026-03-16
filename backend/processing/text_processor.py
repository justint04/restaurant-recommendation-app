import os
import re
import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer

#remove stopwords using NLTK library
nltk.download('punkt')
nltk.download('punkt_tab')
nltk.download('stopwords')
nltk.download('wordnet')


def process_text(review_text):
    #lowercase
    review_text = review_text.lower()

    #remove numbers
    review_text = re.sub(r'\d+', '', review_text)
    
    #remove punctuation
    trans = str.maketrans('', '', string.punctuation)
    review_text = review_text.translate(trans)

    #remove extra whitespace
    review_text = " ".join(review_text.split())

    #remove stopwords using NLTK library
    tokens = word_tokenize(review_text)
    tokens = [w for w in tokens if w.lower() not in stopwords.words('english')]

    #lemmatization (getting root form of a word)
    le = WordNetLemmatizer()
    lemmas = [le.lemmatize(w) for w in tokens]

    return lemmas










    
