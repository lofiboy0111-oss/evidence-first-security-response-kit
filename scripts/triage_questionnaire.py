#!/usr/bin/env python3
"""Local, deterministic triage for security questionnaire CSVs.

Usage: python triage_questionnaire.py input.csv output.csv
Required input columns: question_id, question
No network access or external dependencies are used.
"""
import csv
import re
import sys
from pathlib import Path

RULES = [
    ("privacy", ["personal data", "pii", "gdpr", "privacy", "deletion", "retention", "subprocessor", "transfer"]),
    ("access_control", ["access control", "least privilege", "mfa", "multi-factor", "authentication", "authorization", "password"]),
    ("incident_response", ["incident", "breach", "security event", "notification", "response plan"]),
    ("business_continuity", ["business continuity", "disaster recovery", "backup", "recovery time", "recovery point", "availability"]),
    ("infrastructure", ["network", "firewall", "encryption", "hosting", "cloud", "data center", "architecture"]),
    ("secure_development", ["secure development", "sdlc", "code review", "vulnerability", "penetration", "dependency", "patch"]),
    ("compliance_audit", ["soc 2", "soc2", "iso 27001", "audit", "certification", "attestation", "compliance"]),
    ("vendor_management", ["vendor", "third party", "supplier", "risk assessment", "due diligence"]),
    ("personnel", ["background check", "employee", "personnel", "training", "termination", "onboarding"]),
]

HIGH_RISK = [
    "certify", "certification", "guarantee", "indemnify", "warranty", "breach notification",
    "legal", "regulatory", "contract", "signature", "right to audit", "financial penalty",
    "source code", "credentials", "penetration test report", "personal data", "health data",
]

EVIDENCE = {
    "privacy": "Privacy notice; data inventory; retention/deletion policy; subprocessor list; transfer documentation",
    "access_control": "Access-control policy; MFA standard; IAM configuration evidence; review records",
    "incident_response": "Incident-response plan; escalation matrix; exercise record; approved notification language",
    "business_continuity": "BC/DR plan; backup policy; recovery test; RTO/RPO evidence",
    "infrastructure": "Architecture diagram; encryption standard; network/security configuration; hosting scope",
    "secure_development": "SDLC policy; code-review standard; vulnerability management; test summary",
    "compliance_audit": "Current report, attestation, certification, or approved statement with scope and dates",
    "vendor_management": "Vendor-risk policy; assessment template; critical-vendor register; review record",
    "personnel": "Screening policy; training records; onboarding/offboarding controls",
    "other": "Question owner and authoritative policy or record",
}


def classify(text):
    normalized = re.sub(r"\s+", " ", text.lower()).strip()
    categories = []
    for category, terms in RULES:
        if any(term in normalized for term in terms):
            categories.append(category)
    category = ";".join(categories) if categories else "other"
    risk_terms = [term for term in HIGH_RISK if term in normalized]
    if risk_terms:
        priority = "high"
    elif category in {"compliance_audit", "privacy", "incident_response"} or ";" in category:
        priority = "medium"
    else:
        priority = "normal"
    flags = ";".join(risk_terms) if risk_terms else ""
    evidence = " | ".join(EVIDENCE.get(item, EVIDENCE["other"]) for item in category.split(";"))
    return category, priority, flags, evidence


def main():
    if len(sys.argv) != 3:
        print("Usage: python triage_questionnaire.py input.csv output.csv", file=sys.stderr)
        return 2
    source, destination = map(Path, sys.argv[1:])
    with source.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or "question_id" not in reader.fieldnames or "question" not in reader.fieldnames:
            raise SystemExit("Input CSV must contain question_id and question columns")
        rows = list(reader)
    fieldnames = list(reader.fieldnames)
    for field in ["category", "priority", "risk_flags", "suggested_evidence", "review_status"]:
        if field not in fieldnames:
            fieldnames.append(field)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            category, priority, flags, evidence = classify(row.get("question", ""))
            row.update({"category": category, "priority": priority, "risk_flags": flags, "suggested_evidence": evidence, "review_status": "human_review_required"})
            writer.writerow(row)
    print(f"Triaged {len(rows)} questions to {destination}")


if __name__ == "__main__":
    raise SystemExit(main())
