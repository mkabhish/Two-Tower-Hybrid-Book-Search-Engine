# E-commerce Semantic Search Engine

A modern, industry-inspired product search engine for e-commerce, featuring hybrid retrieval (BM25 + dense vectors), cross-encoder reranking, and basic personalization. Built with FastAPI (backend), Streamlit (frontend), FAISS, Whoosh, and Transformers.

---

## Features
- **Hybrid Search:** Combines semantic (dense vector) and keyword (BM25) retrieval for robust, high-recall search.
- **Cross-Encoder Reranking:** Uses a transformer-based cross-encoder for high-precision ranking of top candidates.
- **Personalization:** Boosts products based on user interaction history.
- **Streamlit Frontend:** Simple, interactive web UI for search and feedback.
- **Evaluation Script:** Measure search quality with sample queries and metrics.

---

## Architecture
```
User (Streamlit UI)
    |
    v
FastAPI Backend
    |---> BM25 (Whoosh)
    |---> Dense Retrieval (FAISS + Sentence Transformers)
    |---> Cross-Encoder Reranker (Transformers)
    |---> Personalization Layer
    |
    v
Product Results
```

---

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/mkabhish/Two-Tower-Hybrid-Book-Search-Engine.git
cd Two-Tower-Hybrid-Book-Search-Engine
```

### 2. Set Up Python Environment
```sh
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
```

### 4. Prepare Data
- Place your product CSV (e.g., `products_sample.csv`) in the `backend/` directory.
- Ensure it has columns: `book_id`, `title`, `original_title` (or adjust code for your schema).

### 5. Run the Backend
```sh
uvicorn backend.main:app --reload
```
- Access API docs at [http://localhost:8000/docs](http://localhost:8000/docs)

### 6. Run the Frontend
```sh
streamlit run frontend/app.py
```
- Open [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage
- Enter a user ID and search query in the Streamlit UI.
- Click "I viewed this" on results to provide feedback and personalize future searches.
- Use `/user_history?user_id=YOUR_USER_ID` to view a user's history.
- Evaluate search quality with `python backend/evaluate.py`.

---

## Customization & Extensions
- **Scale up:** Swap Whoosh for Elasticsearch, or FAISS for a managed vector DB (Pinecone, Milvus).
- **Improve models:** Fine-tune or swap out transformer models for your domain.
- **Persistence:** Store user history in a database for production use.
- **Business logic:** Add filtering, boosting, or custom ranking rules.
- **Monitoring:** Add logging, metrics, and error handling for production.

---

## License
MIT License. See [LICENSE](LICENSE) for details. 