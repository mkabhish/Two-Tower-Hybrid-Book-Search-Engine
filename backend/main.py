from fastapi import FastAPI, Query
from typing import List
from backend.product_loader import load_products
from backend.two_tower_model import TwoTowerRetrievalModel
from backend.bm25_search import BM25Search
from backend.cross_encoder_reranker import CrossEncoderReranker

app = FastAPI()

# Load and index products at startup
products = load_products('backend/products_sample.csv')
retriever = TwoTowerRetrievalModel()
retriever.index_products(products, text_key='title')
bm25 = BM25Search()
bm25.build_index(products, id_key='book_id', text_key='title')
reranker = CrossEncoderReranker()

# In-memory user history: user_id -> set of product_ids
user_history = {}

@app.get("/search")
def search(query: str = Query(..., description="Search query"), top_k: int = 5, user_id: str = Query(None, description="User ID for personalization")):
    # Get FAISS results
    faiss_results = retriever.search(query, top_k=20, text_key='title')
    faiss_ids = {r['id'] for r in faiss_results}
    # Get BM25 results (as product IDs)
    bm25_ids = bm25.search(query, top_k=20)
    # Merge: add BM25 hits not already in FAISS results
    merged_results = faiss_results.copy()
    for pid in bm25_ids:
        if pid not in faiss_ids:
            product = next((p for p in products if int(p['book_id']) == pid), None)
            if product:
                try:
                    book_id = int(product.get('book_id'))
                except (TypeError, ValueError):
                    continue
                merged_results.append({
                    'id': book_id,
                    'title': product.get('title'),
                    'description': product.get('original_title'),
                    'score': None  # No FAISS score
                })
    # Personalization: boost products in user's history
    if user_id and user_id in user_history:
        history = user_history[user_id]
        for r in merged_results:
            if r['id'] in history:
                r['personalization_boost'] = 1
            else:
                r['personalization_boost'] = 0
    else:
        for r in merged_results:
            r['personalization_boost'] = 0
    # Rerank with cross-encoder (using both title and description), then boost personalized
    reranked = reranker.rerank(query, merged_results, top_k=len(merged_results))
    reranked = sorted(reranked, key=lambda x: (x['personalization_boost'], x.get('rerank_score', 0)), reverse=True)
    # Remove rerank_score and personalization_boost from output
    for r in reranked:
        r.pop('rerank_score', None)
        r.pop('personalization_boost', None)
    return {"results": reranked[:top_k]}

@app.post("/feedback")
def feedback(user_id: str = Query(...), product_id: int = Query(...)):
    # Record that a user viewed/clicked a product
    if user_id not in user_history:
        user_history[user_id] = set()
    user_history[user_id].add(product_id)
    return {"status": "ok"}

@app.get("/user_history")
def get_user_history(user_id: str = Query(...)):
    history = list(user_history.get(user_id, set()))
    return {"user_id": user_id, "history": history} 