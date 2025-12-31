Task 1: Extraction Schema Design

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

Task 2: Extraction Approach

  Pipeline Design:
  
  We use a deterministic, rule-based extraction pipeline to generate semantic
  objects from journal text. This approach avoids hallucination and ensures that
  the same input always produces the same output.
  
  Evidence Grounding:
  
  Evidence grounding is enforced by only extracting objects when a keyword match
  is found directly in the journal text. The extracted `evidence_span` is copied
  verbatim from the input text, ensuring all outputs are traceable to the source.
  
  Handling Uncertainty and Abstention:
  
  If the extractor cannot confidently determine an attribute such as intensity
  or time reference, it assigns the value `unknown`. If no valid evidence span
  exists for a potential concept, the system abstains from extraction rather than
  producing a hallucinated object.

Task 3: Evaluation Method

  Object Matching:
  Predicted objects are matched to gold objects based on domain agreement and
  evidence span overlap. A match is considered valid if the predicted evidence
  span overlaps with the gold evidence span as a substring.
  
  True / False Positives:
  - True Positive (TP): A predicted object that matches a gold object.
  - False Positive (FP): A predicted object with no matching gold object.
  - False Negative (FN): A gold object with no matching prediction.
  
  Attribute Scoring:
  Attribute accuracy is computed only for matched objects.
  - Polarity: Correct if predicted polarity equals gold polarity.
  - Intensity / Arousal Bucket: Correct if predicted bucket equals gold bucket.
  - Time Bucket: Correct if predicted time bucket equals gold time bucket.
  Predicted values of `unknown` are treated as incorrect but do not introduce
  false positives.
  
  Evidence Coverage:
  Evidence coverage rate is defined as the percentage of predicted objects whose
  evidence span is a valid verbatim substring of the journal text.
  
  Metrics:
  We report object-level precision, recall, and F1 score, along with polarity
  accuracy, bucket accuracy, and evidence coverage rate.
