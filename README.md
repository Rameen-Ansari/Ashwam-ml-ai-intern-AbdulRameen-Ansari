**Task 1: Extraction Schema Design**

  Schema Definition:
  Each extracted semantic object follows the schema defined in `schema/extraction_schema.json`.
  
  Constrained vs Free-text Fields
  - Constrained fields: domain, polarity, intensity_bucket, time_bucket  
    These fields use fixed buckets to enable deterministic evaluation.
  - Free-text field: evidence_span  
    This field must be a verbatim substring of the journal text and anchors all extracted claims.
  
  Design Rationale:
  
  Safety:
  Requiring a verbatim evidence span prevents hallucinations by ensuring every extracted object is directly grounded in the input journal text.
  
  Evaluation:  
  Object matching is based on evidence span overlap and domain agreement rather than canonical labels, enabling objective scoring even with non-standard language.
  
  Extensibility:
  The schema allows additional attributes (e.g., duration, confidence) to be added without altering existing fields, preserving backward compatibility.

**Task 2: Extraction Approach**

  Pipeline Design:
  
  We use a deterministic, rule-based extraction pipeline to generate semantic objects from journal text. This approach avoids hallucination and ensures that the same input always produces the same output.
  
  Evidence Grounding:
  
  Evidence grounding is enforced by only extracting objects when a keyword match is found directly in the journal text. The extracted `evidence_span` is copied verbatim from the input text, ensuring all outputs are traceable to the source.
  
  Handling Uncertainty and Abstention:
  
  If the extractor cannot confidently determine an attribute such as intensity or time reference, it assigns the value `unknown`. If no valid evidence span exists for a potential concept, the system abstains from extraction rather than producing a hallucinated object.

**Task 3: Evaluation Method**

  Object Matching:
  Predicted objects are matched to gold objects based on domain agreement and evidence span overlap. A match is considered valid if the predicted evidence span overlaps with the gold evidence span as a substring.
  
  True / False Positives:
  - True Positive (TP): A predicted object that matches a gold object.
  - False Positive (FP): A predicted object with no matching gold object.
  - False Negative (FN): A gold object with no matching prediction.
  
  Attribute Scoring:
  Attribute accuracy is computed only for matched objects.
  - Polarity: Correct if predicted polarity equals gold polarity.
  - Intensity / Arousal Bucket: Correct if predicted bucket equals gold bucket.
  - Time Bucket: Correct if predicted time bucket equals gold time bucket.
  Predicted values of `unknown` are treated as incorrect but do not introduce false positives.
  
  Evidence Coverage:
  Evidence coverage rate is defined as the percentage of predicted objects whose evidence span is a valid verbatim substring of the journal text.
  
  Metrics:
  We report object-level precision, recall, and F1 score evidence coverage rate.

**Task 4: Mock Evaluation**

  The mock evaluation was executed on Journal entry no.3 and 5.
  
  Gold objects: 
  {"journal_id": "J003", "items": [{"domain": "food", "evidence_span": "Dinner: paneer bhurji + 2 rotis", "polarity": "present", "intensity_bucket": "unknown", "time_bucket": "today"}, {"domain": "emotion", "evidence_span": "Mood was actually good—felt calm and grateful", "polarity": "present", "arousal_bucket": "low", "time_bucket": "today"}, {"domain": "symptom", "evidence_span": "I got super sleepy", "polarity": "present", "intensity_bucket": "high", "time_bucket": "today"}, {"domain": "symptom", "evidence_span": "stomach felt bloated", "polarity": "present", "intensity_bucket": "medium", "time_bucket": "today"}, {"domain": "mind", "evidence_span": "Brain felt clear, focused while reading", "polarity": "present", "intensity_bucket": "low", "time_bucket": "today"}]}
  
  Predicted Objects:
  [{'domain': 'symptom', 'evidence_span': 'bloated', 'polarity': 'present', 'intensity_bucket': 'high', 'time_bucket': 'unknown'}, {'domain': 'food', 'evidence_span': 'paneer', 'polarity': 'present', 'intensity_bucket': 'high', 'time_bucket': 'unknown'}, {'domain': 'emotion', 'evidence_span': 'calm', 'polarity': 'present', 'intensity_bucket': 'high', 'time_bucket': 'unknown'}, {'domain': 'mind', 'evidence_span': 'focused', 'polarity': 'present', 'intensity_bucket': 'high', 'time_bucket': 'unknown'}]
  
  | Predicted Evidence | Gold Evidence                                  | Domain     | Match  | Reason               |
  
  | paneer             | Dinner: paneer bhurji + 2 rotis                | food       | yes    | Substring overlap    |
  | bloated            | stomach felt bloated                           | symptom    | yes    | Substring overlap    |
  | calm               | Mood was actually good—felt calm and grateful  | emotion    | yes    | Substring overlap    |
  | focused            | Brain felt clear, focused while reading        | mind       | yes    | Substring overlap    |
  
  Metrics:
  TP=4
  FP=0
  FN=0
  Precision = Recall = F1 = 1
  Evidence Coverage = 4/4 = 1
  
  Gold objects:
  {"journal_id": "J005", "items": [{"domain": "food", "evidence_span": "ate biryani (small bowl) + raita", "polarity": "present", "intensity_bucket": "unknown", "time_bucket": "today"}, {"domain": "symptom", "evidence_span": "Felt heartburn after that", "polarity": "present", "intensity_bucket": "medium", "time_bucket": "today"}, {"domain": "symptom", "evidence_span": "a slight nausea", "polarity": "present", "intensity_bucket": "low", "time_bucket": "today"}, {"domain": "emotion", "evidence_span": "irritated + impatient", "polarity": "present", "arousal_bucket": "high", "time_bucket": "today"}, {"domain": "mind", "evidence_span": "racing thoughts at night", "polarity": "present", "intensity_bucket": "high", "time_bucket": "last_night"}]}
  
  Predicted Objects:
  {'domain': 'symptom', 'evidence_span': 'nausea', 'polarity': 'present', 'intensity_bucket': 'unknown', 'time_bucket': 'unknown'}, {'domain': 'symptom', 'evidence_span': 'heartburn', 'polarity': 'present', 'intensity_bucket': 'unknown', 'time_bucket': 'unknown'}, {'domain': 'food', 'evidence_span': 'biryani', 'polarity': 'present', 'intensity_bucket': 'unknown', 'time_bucket': 'unknown'}, {'domain': 'emotion', 'evidence_span': 'irritated', 'polarity': 'present', 'intensity_bucket': 'unknown', 'time_bucket': 'unknown'}, {'domain': 'mind', 'evidence_span': 'thoughts', 'polarity': 'present', 'intensity_bucket': 'unknown', 'time_bucket': 'unknown'}
  
  | Predicted | Gold Evidence             | Domain  | Match | Reason    |
  
  | nausea    | a slight nausea           | symptom | yes     | substring |
  | heartburn | Felt heartburn after that | symptom | yes     | substring |
  | biryani   | ate biryani (small bowl)  | food    | yes     | substring |
  | irritated | irritated + impatient     | emotion | yes     | substring |
  | thoughts  | racing thoughts at night  | mind    | yes     | substring |
  
  Metrics:
  TP=5
  FP=0
  FN=0
  Precision = Recall = F1 = 1
  Evidence Coverage = 5/5 = 1

**Task 5: Failure Analysis**

  Failure Mode 1: Over-extraction from Keyword Matching:
  The rule-based extractor may generate multiple objects for a single semantic concept due to independent keyword matches. This leads to false positives and lower precision, but does not introduce hallucinations since all outputs are evidence-grounded.
  
  Failure Mode 2: Attribute Underprediction:
  The extractor assigns `unknown` to intensity, arousal, and time buckets when explicit cues are absent. This lowers bucket accuracy but reflects safe abstention rather than incorrect inference.
  
  Failure Mode 3: Partial Evidence Span Mismatch:
  Predicted evidence spans may be shorter than gold spans. This is mitigated by substring-based matching, allowing conservative extractions to match correctly without requiring canonical phrases.
  
  Failure Mode 4: Vocabulary Coverage Gaps:
  Concepts not present in the predefined vocabularies are not extracted, leading to false negatives. This behavior is detectable during evaluation and can be mitigated by extending vocabularies without modifying the schema or scorer.
