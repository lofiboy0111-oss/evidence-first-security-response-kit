# Evidence-First Security Questionnaire Response Kit

A local, human-reviewed workflow for organizing B2B security questionnaires without pretending that AI can certify a company or replace security judgment.

## What this is

A lightweight starter kit for teams that receive customer security questionnaires and need a repeatable way to:

- inventory every question;
- identify likely evidence requirements;
- flag high-risk questions for expert review;
- maintain an evidence register;
- record citations and approvals; and
- produce an audit-friendly work trail.

The included script is deterministic and runs locally with Python’s standard library. It does not upload files, call an AI provider, submit questionnaires, or contact anyone.

## Quick start

1. Copy `demo/sample_questions.csv` and replace it with your questionnaire export.
2. Run:

```text
python scripts/triage_questionnaire.py demo/sample_questions.csv demo/triaged_questions.csv
```

3. Review every row. The script is triage support, not an answer generator.
4. Use `templates/evidence_register.csv` to track approved source documents.
5. Use `templates/qa_checklist.md` before releasing any customer-facing response.

## CSV input

Required columns:

- `question_id`
- `question`

Optional columns are preserved:

- `section`
- `customer_answer`
- `notes`

## Output fields

The script adds:

- `category`
- `priority`
- `risk_flags`
- `suggested_evidence`
- `review_status`

## Product boundary

This kit does not provide legal advice, audit opinions, security certifications, compliance determinations, or guaranteed response accuracy. A qualified human must review all customer-facing responses.

## Commercial packaging

Free entry product: local triage script plus blank templates.

Paid upgrade opportunity: $49–$149 expanded template library, vertical question mappings, evidence freshness tracker, answer-citation workbook, and update releases. A future team edition could add controlled collaboration, but the local version should remain useful on its own.

## License

MIT. Preserve this notice if you redistribute or modify the kit. The product is original to this workspace and is not a copy of ECC. ECC may be studied separately as an open-source reference for agent workflow patterns.
