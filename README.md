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
