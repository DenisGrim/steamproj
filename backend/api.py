from fastapi import FastAPI
from sentence_transformers import SentenceTransformer
import psycopg2

app = FastAPI()

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
    database="mydb",
    user="postgres",
    password="password"
)

@app.get("/search")
def search(q: str):

    embedding = model.encode(q).tolist()

    cur = conn.cursor()

    cur.execute("""
        SELECT app_id
        FROM games
        ORDER BY embedding <=> %s
        LIMIT 10
    """, (embedding,))

    rows = cur.fetchall()

    return [{"ID": r[0]} for r in rows]
