from sklearn.metrics.pairwise import cosine_similarity

_model = None

def load_model():
    global _model
    if _model is None:
        print("⏳ Loading BERT model...")
        from sentence_transformers import SentenceTransformer
        _model = SentenceTransformer('paraphrase-MiniLM-L3-v2')
        print("✅ Model loaded")
    return _model

def calculate_similarity(resume_text, job_desc):
    model = load_model()
    embeddings = model.encode([resume_text, job_desc])
    score = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return round(score * 100, 2)
