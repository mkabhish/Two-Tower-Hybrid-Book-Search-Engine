from sentence_transformers import SentenceTransformer
from typing import List, Dict
import torch
import numpy as np
import faiss
import os
from backend.product_loader import load_products

class TwoTowerRetrievalModel:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2', index_path='backend/faiss.index', emb_path='backend/product_embeddings.npy'):
        self.model = SentenceTransformer(model_name)
        self.products = []  # List of product dicts
        self.index = None   # FAISS index
        self.id_map = []    # Maps FAISS index to product index
        self.index_path = index_path
        self.emb_path = emb_path

    def index_products(self, products: List[Dict], text_key: str = 'title'):
        self.products = products
        dim = None
        # Try to load FAISS index and embeddings from disk
        if os.path.exists(self.index_path) and os.path.exists(self.emb_path):
            self.index = faiss.read_index(self.index_path)
            embeddings = np.load(self.emb_path)
            dim = embeddings.shape[1]
            self.id_map = list(range(len(products)))
        else:
            texts = [p[text_key] for p in products]
            embeddings = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
            faiss.normalize_L2(embeddings)
            dim = embeddings.shape[1]
            self.index = faiss.IndexFlatIP(dim)
            self.index.add(embeddings)
            self.id_map = list(range(len(products)))
            # Save index and embeddings
            faiss.write_index(self.index, self.index_path)
            np.save(self.emb_path, embeddings)

    def search(self, query: str, top_k: int = 5, text_key: str = 'title') -> List[Dict]:
        query_emb = self.model.encode([query], convert_to_numpy=True)
        faiss.normalize_L2(query_emb)
        D, I = self.index.search(query_emb, top_k)
        results = []
        for score, idx in zip(D[0], I[0]):
            if idx < 0 or idx >= len(self.products):
                continue
            product = self.products[self.id_map[idx]]
            book_id = product.get('book_id')
            try:
                book_id = int(book_id)
            except (TypeError, ValueError):
                continue  # skip if book_id is missing or invalid
            results.append({
                'id': book_id,
                'title': product.get('title'),
                'description': product.get('original_title'),
                'score': float(score)
            })
        return results 