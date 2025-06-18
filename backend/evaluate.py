import requests

test_set = [
    {"query": "harry potter", "relevant_ids": [2]},
    {"query": "hunger games", "relevant_ids": [1]},
    {"query": "twilight", "relevant_ids": [3]},
    {"query": "to kill a mockingbird", "relevant_ids": [4]},
]

BACKEND_URL = "http://localhost:8000/search"
TOP_K = 5

def precision_at_k(results, relevant_ids, k):
    top_k = results[:k]
    hits = sum(1 for r in top_k if int(r['id']) in relevant_ids)
    return hits / k

def main():
    for test in test_set:
        response = requests.get(BACKEND_URL, params={"query": test["query"], "top_k": TOP_K})
        results = response.json().get("results", [])
        p_at_5 = precision_at_k(results, test["relevant_ids"], TOP_K)
        print(f"Query: '{test['query']}' | Precision@{TOP_K}: {p_at_5:.2f}")
        print(f"  Relevant IDs: {test['relevant_ids']}")
        print(f"  Top {TOP_K} returned IDs: {[r['id'] for r in results]}")
        print()

if __name__ == "__main__":
    main() 