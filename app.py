import pickle
import streamlit as st
from sentence_transformers import SentenceTransformer

st.title("Hardly")
st.write("Predicts whether an exam question is easy or hard, based on how real students answered.")

@st.cache_resource
def load_everything():
    encoder = SentenceTransformer("all-MiniLM-L6-v2")
    with open("data/model.pkl", "rb") as f:
        saved = pickle.load(f)
    return encoder, saved["clf"]

encoder, clf = load_everything()

question = st.text_area("Paste a question:", height=100)

if st.button("Predict"):
    if len(question.strip()) < 10:
        st.warning("Question is too short.")
    else:
        vector = encoder.encode([question])
        prediction = clf.predict(vector)[0]
        confidence = clf.predict_proba(vector)[0]

        if prediction == 1:
            st.error("HARD")
        else:
            st.success("EASY")

        st.write("Confidence:", round(float(max(confidence)), 3))

st.caption("Trained on 50 questions rated by 13 students. Cross-validated accuracy: 0.70 (baseline 0.64).")