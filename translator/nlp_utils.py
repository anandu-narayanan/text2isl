import spacy

try:
    from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

# ==========================================
# 1. Rule-Based SpaCy Setup (Fallback)
# ==========================================
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    import spacy.cli
    spacy.cli.download("en_core_web_sm")
    nlp = spacy.load("en_core_web_sm")

ISL_STOP_WORDS = {
    "a", "an", "the", "is", "am", "are", "was", "were", "be", "been", "being",
    "has", "have", "had", "do", "does", "did", "to", "of"
}

def process_text_to_isl_rules(text: str) -> list[str]:
    """Fallback rule-based SVO -> SOV translation"""
    doc = nlp(text)
    subjects, verbs, objects, times, others, questions = [], [], [], [], [], []
    for token in doc:
        lemma = token.lemma_.lower()
        if lemma in ISL_STOP_WORDS or token.pos_ == "PUNCT":
            continue
        if token.ent_type_ in ["TIME", "DATE"]:
            times.append(lemma)
            continue
        if token.tag_ in ["WDT", "WP", "WP$", "WRB"]:
            questions.append(lemma)
            continue
        if "subj" in token.dep_:
            subjects.append(lemma)
        elif token.pos_ == "VERB" or token.dep_ == "ROOT":
            verbs.append(lemma)
        elif "obj" in token.dep_ or token.dep_ in ["attr", "oprd", "acomp"]:
            objects.append(lemma)
        else:
            others.append(lemma)
            
    glosses = []
    for items in [times, subjects, others, objects, verbs, questions]:
        for item in items:
            if item not in glosses:
                glosses.append(item)
    return glosses

# ==========================================
# 2. AI Sequence-to-Sequence NLP Pipeline
# ==========================================
# We use a lightweight T5 model as a stand-in architecture. 
# Once you fine-tune your own ISL model, replace MODEL_NAME with your local path!
MODEL_NAME = "google/flan-t5-small"
ai_model = None
ai_tokenizer = None

def load_ai_model():
    global ai_model, ai_tokenizer
    if TRANSFORMERS_AVAILABLE and ai_model is None:
        try:
            print(f"Loading AI NLP Model ({MODEL_NAME})...")
            ai_tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
            ai_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
        except Exception as e:
            print(f"Warning: Failed to load HuggingFace AI model: {e}")

def process_text_to_isl_ai(text: str) -> list[str]:
    """Translates English to ISL gloss using a pre-trained Deep Learning model."""
    load_ai_model()
    
    if ai_model is None or ai_tokenizer is None:
        print("AI model unavailable, falling back to rule-based translation.")
        return process_text_to_isl_rules(text)
        
    prompt = f"Translate English to Indian Sign Language sequence: {text}"
    
    # Generate inference
    inputs = ai_tokenizer(prompt, return_tensors="pt")
    outputs = ai_model.generate(**inputs, max_new_tokens=50)
    generated_text = ai_tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]
    
    # Split the predicted gloss into an array of words
    glosses = [word.strip().lower() for word in generated_text.split() if word.strip()]
    return glosses

# ==========================================
# Main Router
# ==========================================
def process_text_to_isl(text: str, use_ai: bool = True) -> list[str]:
    if use_ai:
        return process_text_to_isl_ai(text)
    return process_text_to_isl_rules(text)
