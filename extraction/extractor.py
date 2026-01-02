SympVocab={"headache", "tightness", "bloated", "soreness", "nausea", "heavy", "pain", "sinus", "cramps"}
FoodVocab={"coffee", "chai", "rice", "dal", "achar", "paneer", "oats", "biryani", "toast", "idli", "chips", "quinoa"}
EmoVocab={"anxious", "playful", "irritated", "calm", "stressed", "edgy", "nervous"}
MindVocab={"overthinking", "confused", "focused", "distracted", "worried", "thoughts"}

def intensity(text):
    if any(w in text for w in ["severe", "intense", "super", "extreme"]):
        return "high"
    if any(w in text for w in ["slight", "mild", "a bit"]):
        return "low"
    if any(w in text for w in ["heavy", "moderate"]):
        return "medium"
    return "unknown"

def time(text):
    if any(w in text for w in ["today", "this morning", "this evening"]):
        return "today"
    if any(w in text for w in ["last night", "yesterday"]):
        return "last_night"
    if any(w in text for w in ["past week", "this week", "few days"]):
        return "past_week"
    return "unknown"

def extract_obj(text):
    extracted=[]
    text=text.lower()
    intensity=intensity(text)
    time_bucket=time(text)
    def add_object(domain, evidence):
        extracted.append({"domain": domain,"evidence_span": evidence,"polarity": "present","intensity_bucket": intensity,"time_bucket": time_bucket})
    for word in SympVocab:
        if word in text:
            add_object("symptom", word)
    for word in FoodVocab:
        if word in text:
            add_object("food", word)
    for word in EmoVocab:
        if word in text:
            add_object("emotion", word)
    for word in MindVocab:
        if word in text:
            add_object("mind", word)
    return extracted
