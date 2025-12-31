SympVocab={"headache","tightness","bloated","soreness","heartburn","nausea","heavy","pain","sinus","cramps"}
FoodVocab={"coffee","tea","dinner","lunch","chai","rice","dal","achar","breakfast","paneer","oats","biryani","toast","idli","chips","quinoa"}
EmoVocab={"anxious","playful","irritated","calm","stressed","edgy","nervous"}
MindVocab={"overthinking","confused","focused","distracted","worried","thoughts"}

def domain(evidence):
    span=evidence.lower()
    for word in SympVocab:
        if word in span:
            return "symptom"
    for word in FoodVocab:
        if word in span:
            return "food"
    for word in EmoVocab:
        if word in span:
            return "emotion"
    for word in MindVocab:
        if word in span:
            return "mind"
    return "unknown"

text="I felt this dull headache behind my eyes."
evidence="headache"
res={}
res["exists_verbatim"]=evidence in text
res["domain"]=domain(evidence)
print(res)
