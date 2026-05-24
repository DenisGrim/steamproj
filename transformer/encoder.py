from sentence_transformers import SentenceTransformer
import torch
# from sklearn.metrics.pairwise import cosine_similartiy  # this will compare two embeddings

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {device}")

model = SentenceTransformer(
    "jinaai/jina-embeddings-v5-text-nano",
    trust_remote_code=True,
    device=device,
    model_kwargs={"dtype": torch.bfloat16},
    #config_kwargs={"_attn_implementation": "flash_attention_2"},  # doenst work with my amd lmao
)


# TODO: maybe this gets a lot faster with batching. multiple reviews/games at once
# TODO might need to split reviews into seperate ones and have it embed those. There was something
# for this, I'm pretty sure
def embed_text(text):
    embedding = model.encode(
            sentences = [text],
            task = "retrieval",
            prompt_name="document",
            )
    return embedding[0]


def embed_batch(app_texts):
    app_ids = list(app_texts.keys())
    texts = list(app_texts.values())

    embeddings = model.encode(
        sentences=texts,
        task="retrieval",
        prompt_name="document",
    )

    return dict(zip(app_ids, embeddings))
