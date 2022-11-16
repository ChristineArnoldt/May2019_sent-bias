
import requests
URL = "https://int-emb-glove-de-wiki.s3.eu-central-1.amazonaws.com/vectors.txt"
response = requests.get(URL)
open("../sentbias/glove_vectors_de/vectors.txt", "wb").write(response.content)