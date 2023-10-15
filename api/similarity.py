import openai
from sklearn.metrics.pairwise import cosine_similarity
import configparser

config = configparser.ConfigParser()
config.read("../config.ini")
openai.api_key = config["openAI"]["apiKey"]


def create_embeddings(text: str):
    response = openai.Embedding.create(input=text, model="text-embedding-ada-002")
    return response.data[0]["embedding"]


def calc_similarity(textA: str, textB: str):
    return cosine_similarity([create_embeddings(textA), create_embeddings(textB)])[0][1]
