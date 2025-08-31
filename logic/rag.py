from pathlib import Path
from typing import List
import re
import numpy as np
import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from logic.similarity import preprocess_text


@st.cache_data(show_spinner=False)
def load_bio_text(base_dir: Path) -> str:
    try:
        return (base_dir / "assets" / "bio.txt").read_text(encoding="utf-8")
    except FileNotFoundError:
        return ""


def _split_paragraphs(text: str) -> List[str]:
    paras = [p.strip() for p in re.split(r"\n\s*\n", text or "")]
    return [p for p in paras if p]


@st.cache_resource(show_spinner=False)
def build_bio_index(bio_text: str):
    paragraphs = _split_paragraphs(bio_text)
    if not paragraphs:
        return None, None, []
    pre = [preprocess_text(p) for p in paragraphs]
    vec = TfidfVectorizer(min_df=1, analyzer="word", ngram_range=(1, 2))
    mat = vec.fit_transform(pre)
    return vec, mat, paragraphs


def retrieve_bio_context(query: str, bio_text: str, k: int = 3, min_chars: int = 400) -> str:
    vec, mat, paras = build_bio_index(bio_text)
    if not paras or vec is None:
        return ""
    q = preprocess_text(query)
    qv = vec.transform([q])
    sims = cosine_similarity(qv, mat).flatten()
    order = np.argsort(-sims)
    top_idx = order[: max(k, 1)]
    chunks = [paras[i] for i in top_idx]

    joined = "\n\n".join(chunks)
    if len(joined) < min_chars and len(paras) > k:
        extra = [i for i in order if i not in top_idx][: (k * 2)]
        chunks.extend([paras[i] for i in extra])
        joined = "\n\n".join(chunks)
    return joined