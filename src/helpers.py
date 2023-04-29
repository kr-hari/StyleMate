from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer

import pickle


# Run the below code if you are running for the first time run below code
# nltk.download()




def text_preprocessing(text: str):
    
    # Lowercase
    text = text.lower()
    # Remove Punctuation
    # text = "".join([char for char in text if char not in string.punctuation])
    words = word_tokenize(text)  
    # Remove Stopwords
    stop_words = stopwords.words('english')
    filtered_words = [word for word in words if word not in stop_words]
    ## Stemming
    # porter = PorterStemmer()
    # stemmed = [porter.stem(word) for word in filtered_words]
    # Lemmatization
    lemmatizer = WordNetLemmatizer()
    lemmatized = [lemmatizer.lemmatize(word) for word in filtered_words]
    
    return ' '.join(lemmatized)

def get_data_from_file(filename:str):

    with open(filenam, 'rb') as file:
        data = pickle.load(file)

    return data