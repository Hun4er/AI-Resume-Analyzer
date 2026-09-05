from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-V2")

def semantic_similarity(text1, text2):
    encoding1 = model.encode(text1)
    encoding2 = model.encode(text2)

    similarity = cosine_similarity(
        [encoding1],
        [encoding2]
    )

    return similarity[0][0]