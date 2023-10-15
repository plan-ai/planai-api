import openai
from sklearn.metrics.pairwise import cosine_similarity
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")


def create_embeddings(api_key: str, text: str):
    openai.api_key = api_key
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response.data[0]["embedding"]


def calc_similarity(textA: str, textB: str):
    return cosine_similarity([create_embeddings(textA), create_embeddings(textB)])[0][1]
