import pandas as pd
import numpy as np
import pdb
from tqdm import tqdm
import nltk
import string
import pickle 
import yaml
import os

from helpers import text_preprocessing

from sentence_transformers import SentenceTransformer


CONFIG_FILE = 'config.yaml'


class Recommender():

    def __init__(self, primary_column:str = 'title', top_n:int = 10) -> None:

        # Open the configuration file to load parameters
        with open(CONFIG_FILE, "r") as file:
            try:
                self.params = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(exc)
        
        self.top_n = top_n
        self.primary_column = primary_column
        metadata_file = self.params['METADATA_FILE']
        self.metadata = pd.read_csv(metadata_file, index_col=0)
        self.preprocess_metadata()
        print("INFO: Initializing Model")
        self.model = SentenceTransformer('msmarco-distilbert-base-dot-prod-v3')
        print("INFO: Creating embeddings")
        self.embeddings = self.create_embeddings(column=primary_column)


    def preprocess_metadata(self) -> None:

        self.metadata['description'] = self.metadata['description'].apply(lambda x: text_preprocessing(eval(x)[0]))

    def create_embeddings(self, column) -> np.array:

        embeddings = self.model.encode(self.metadata[column].tolist(), device='cuda') 
        embeddings = np.asarray(embeddings.astype('float32'))
        self.save_embeddings(embeddings)
        return embeddings
    
    def save_embeddings(self, embeddings) -> None:

        print("INFO: Saving embeddings")
        if not os.path.exists(os.path.dirname(self.params['EMBEDDING_FILE'])):
            os.mkdir(os.path.dirname(self.params['EMBEDDING_FILE']))
        with open(self.params['EMBEDDING_FILE'],'wb') as file:
            pickle.dump(embeddings, file, protocol=pickle.HIGHEST_PROTOCOL)

    def return_most_similar(self, query):

        print("INFO: Retrieving items for query")
        query_vector = self.model.encode([query])
        similarity = np.dot(self.embeddings,query_vector.T)
        top_items = similarity.flatten().argsort()[-self.top_n:][::-1]
        print(self.metadata['title'].iloc[top_items])
        return top_items








if __name__ == '__main__':

    query = 'men socks'
    recommender = Recommender(primary_column='description')
    recommender.return_most_similar(query=query)
