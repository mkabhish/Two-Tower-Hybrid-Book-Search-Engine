import streamlit as st
import requests

st.title("E-commerce Product Search")

# user_id = st.text_input("Enter your user ID (for personalization):")
user_id = 1
query = st.text_input("Enter your search query:")

if st.button("Search"):
    if query:
        with st.spinner("Searching..."):
            try:
                response = requests.get(
                    "http://localhost:8000/search",
                    params={"query": query, "top_k": 5, "user_id": user_id},
                    timeout=10
                )
                data = response.json()
                results = data.get("results", [])
                if results:
                    st.subheader("Results:")
                    for r in results:
                        st.markdown(f"**{r['title']}** (Score: {r.get('score', 'N/A')})")
                        st.write(r['description'])
                        if st.button(f"I viewed this", key=f"view_{r['id']}"):
                            if user_id:
                                feedback = requests.post(
                                    "http://localhost:8000/feedback",
                                    params={"user_id": user_id, "product_id": r['id']},
                                    timeout=5
                                )
                                if feedback.status_code == 200:
                                    st.success(f"Feedback recorded for product {r['id']}")
                                else:
                                    st.error("Failed to record feedback.")
                            else:
                                st.warning("Please enter a user ID to record feedback.")
                        st.write("---")
                else:
                    st.info("No results found.")
            except Exception as e:
                st.error(f"Error: {e}")
    else:
        st.warning("Please enter a search query.") 