SympVocab={"headache", "tightness", "bloated", "soreness", "heartburn", "nausea", "heavy", "pain", "sinus", "cramps"}
FoodVocab={"coffee", "tea", "dinner", "lunch", "chai", "rice", "dal", "achar", "breakfast", "paneer", "oats", "biryani", "toast", "idli", "chips", "quinoa"}
EmoVocab={"anxious", "playful", "irritated", "calm", "stressed", "edgy", "nervous"}
MindVocab={"overthinking", "confused", "focused", "distracted", "worried", "thoughts"}

def extract_obj(text):
    """Extracts evidence-grounded semantic objects from a journal entry. Returns a list of objects following the extraction schema."""
    extracted=[]
    text=text.lower()
    
    def add_object(domain,evidence):
        extracted.append({"domain": domain,"evidence_span": evidence,"polarity": "present","intensity_bucket": "unknown","time_bucket": "unknown"})
        
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
