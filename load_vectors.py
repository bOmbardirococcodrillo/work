from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec


pc = Pinecone(api_key="pcsk_4UhxE8_w7LmkLRFRFG7LEP8C6JbgVSafDN36ECW71ugMqNSqMh6uLEgzwJLqr3zW4W5fR")  


if "fitness-vectors" not in pc.list_indexes().names():
    pc.create_index(
        name="fitness-vectors",
        dimension=384, 
        metric="euclidean",
        spec=ServerlessSpec(cloud="aws", region="us-west-2")
    )


index = pc.Index("fitness-vectors")


model = SentenceTransformer('all-MiniLM-L6-v2')

descriptions = ["20-minute cardio with treadmill", "High-protein chicken salad"]
embeddings = model.encode(descriptions).tolist()


ids = ["workout1", "meal1"]
index.upsert(vectors=zip(ids, embeddings))

print("Data added to Pinecone!")