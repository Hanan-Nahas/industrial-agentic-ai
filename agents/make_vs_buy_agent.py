from __future__ import annotations

from typing import Dict

PART_PROFILES = {
    "SP-PX100-CPL-03": {
        "is_printable": False,
        "material": "NBR Elastomer",
        "default_action": "SOURCE",
        "notes": "Current local AM line is metal-focused; elastomer coupling insert should be sourced.",
    },
    "SP-PX100-IMP-01": {
        "is_printable": True,
        "material": "17-4PH",
        "default_action": "PRINT",
        "notes": "Printable after balancing + QA release.",
    },
    "SP-VL77-STEM-04": {
        "is_printable": True,
        "material": "410 SS",
        "default_action": "SCAN",
        "notes": "Scan/reverse engineering path is valid when OEM lead-time risk is high.",
    },
    "SP-CM220-VLV-11": {
        "is_printable": True,
        "material": "17-4PH",
        "default_action": "PRINT",
        "notes": "Metal AM feasible with QA qualification checks.",
    },
}


def run(part: str, constraints: list[str], retrieval_text: str) -> Dict:
    text = retrieval_text.lower()
    profile = PART_PROFILES.get(
        part,
        {
            "is_printable": True,
            "material": "Unknown",
            "default_action": "SOURCE",
            "notes": "Insufficient part profile confidence; defaulting to sourcing unless engineering approves local manufacture.",
        },
    )

    printable = bool(profile["is_printable"])
    recommendation = str(profile["default_action"])

    if not printable:
        recommendation = "SOURCE"
    elif "supplier_unavailable" in constraints:
        recommendation = "PRINT" if recommendation != "SCAN" else "SCAN"
    elif any(k in text for k in ["reverse engineer", "scan", "oem unavailable > 10"]):
        recommendation = "SCAN"
    elif any(k in text for k in ["lane disruption", "lead time > 10"]):
        recommendation = "PRINT"

    feasibility = {
        "is_printable": printable,
        "material": str(profile["material"]),
        "notes": str(profile["notes"]),
    }
    return {"recommended_action": recommendation, "manufacturing_feasibility": feasibility}
