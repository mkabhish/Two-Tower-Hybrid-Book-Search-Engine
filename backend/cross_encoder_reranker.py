from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

class CrossEncoderReranker:
    def __init__(self, model_name='cross-encoder/ms-marco-MiniLM-L-6-v2', device=None, text_func=None):
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForSequenceClassification.from_pretrained(model_name)
        self.device = device or ('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)
        self.model.eval()
        # By default, use title + description
        self.text_func = text_func or (lambda c: f"{c.get('title', '')} {c.get('description', '')}")

    def rerank(self, query, candidates, top_k=5):
        pairs = [(query, self.text_func(c)) for c in candidates]
        encodings = self.tokenizer.batch_encode_plus(pairs, padding=True, truncation=True, return_tensors='pt', max_length=128)
        encodings = {k: v.to(self.device) for k, v in encodings.items()}
        with torch.no_grad():
            outputs = self.model(**encodings)
            scores = outputs.logits.squeeze(-1).cpu().numpy()
        # Attach scores and sort
        for c, s in zip(candidates, scores):
            c['rerank_score'] = float(s)
        reranked = sorted(candidates, key=lambda x: x['rerank_score'], reverse=True)
        return reranked[:top_k] 