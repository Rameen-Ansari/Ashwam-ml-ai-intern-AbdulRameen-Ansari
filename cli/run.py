import json
import os
from extraction.extractor import extract_obj

DATA_PATH = "data/journals.jsonl"
OUT_DIR = "out"

def load_journals(path):
    journals=[]
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            journals.append(json.loads(line))
    return journals

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    journals=load_journals(DATA_PATH)
    per_journal_scores=[]
    total_predicted=0
    total_valid_evidence=0
    for journal in journals:
        journal_id=journal.get("journal_id")
        text=journal.get("text", "")
        predictions=extract_obj(text)
        total_predicted+=len(predictions)
        for obj in predictions:
            if obj["evidence_span"].lower() in text.lower():
                total_valid_evidence+=1
        per_journal_scores.append({"journal_id": journal_id,"num_predicted_objects": len(predictions),"predicted_objects": predictions})
    evidence_coverage=(
        total_valid_evidence / total_predicted
        if total_predicted>0 else 0.0
    )
    score_summary={"total_journals":len(journals),"total_predicted_objects":total_predicted,"evidence_coverage_rate":round(evidence_coverage, 3)}
    with open(os.path.join(OUT_DIR, "score_summary.json"), "w") as f:
        json.dump(score_summary, f, indent=2)
    with open(os.path.join(OUT_DIR, "per_journal_scores.jsonl"), "w") as f:
        for item in per_journal_scores:
            f.write(json.dumps(item) + "\n")
    print("Pipeline complete.")
    print("Outputs written to /out directory.")

if __name__ == "__main__":
    main()
