from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import torch
from sentence_transformers import SentenceTransformer
import psycopg2

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

model = SentenceTransformer(
    "jinaai/jina-embeddings-v5-text-nano",
    trust_remote_code=True,
    device=device,
    model_kwargs={"dtype": torch.bfloat16},
    #config_kwargs={"_attn_implementation": "flash_attention_2"},  # doenst work with my amd lmao
)


conn = psycopg2.connect(
    host="db",
    database="postgres",
    user="user",
    password="pass"
)

@app.get("/search")
def search(q: str):
    embedding = model.encode(
            sentences = [q],
            task = "retrieval",
            prompt_name="document",
            ).tolist()[0]
    cur = conn.cursor()
    cur.execute("""
        SELECT 
            app_id,
            1 - (embedding <=> %s::vector) AS similarity,
            name
        FROM games
        ORDER BY similarity DESC
        LIMIT 10
    """, (embedding,))
    rows = cur.fetchall()
    return [{"ID": r[0], "similarity": r[1], "title": r[2]} for r in rows]
