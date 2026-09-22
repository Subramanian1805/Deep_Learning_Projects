"""
Disease metadata catalog for the Skin Disease Detection app.

Each entry provides clinical descriptions, treatment guidance (informational
only — not a substitute for professional care), severity stages, and reference
image paths for user awareness.
"""

# Maps raw Teachable Machine label strings to canonical display names.
CANONICAL_LABELS = {
    "Ring worm": "Ring Worm",
    "Cellulitis": "Cellulitis",
    "Atopic dermititis": "Atopic Dermatitis",
    "Scabis_Lyme": "Scabies / Lyme",
    "Sebirrheic": "Seborrheic Dermatitis",
    "Acne_Rosacea": "Acne / Rosacea",
    "Psoriasis": "Psoriasis",
    "Melanoma": "Melanoma",
    "Eczema": "Eczema",
    "Actinic keratosis": "Actinic Keratosis",
}

# Conditions that visually overlap with Psoriasis and may cause misclassification.
PSORIASIS_CONFUSERS = {
    "Atopic Dermatitis": 0.85,
    "Eczema": 0.90,
    "Actinic Keratosis": 0.88,
    "Melanoma": 1.10,  # Safety priority — never suppress melanoma signals.
}

# Prediction tuning parameters (adjustable without retraining models).
MIN_CONFIDENCE = 55.0
HIGH_CONFIDENCE = 75.0
PSORIASIS_ECZEMA_MARGIN = 10.0
MELANOMA_PRIORITY_THRESHOLD = 60.0

DISEASE_CATALOG = {
    "Ring Worm": {
        "description": "A fungal infection (tinea) causing circular, scaly, itchy patches on the skin.",
        "prescription": {
            "mild": "Topical antifungal creams (clotrimazole, terbinafine) applied twice daily for 2–4 weeks.",
            "moderate": "Oral antifungals if topical treatment fails; keep affected area clean and dry.",
            "severe": "Extended oral antifungal course under dermatologist supervision.",
        },
        "stages": [
            {"name": "Early", "image": "/static/images/stages/ring_worm_early.svg",
             "signs": "Small red, slightly raised patch with mild itching."},
            {"name": "Mild", "image": "/static/images/stages/ring_worm_mild.svg",
             "signs": "Distinct ring-shaped lesion with clearer center and scaly border."},
            {"name": "Severe", "image": "/static/images/stages/ring_worm_severe.svg",
             "signs": "Multiple spreading rings, intense itching, possible secondary infection."},
        ],
    },
    "Cellulitis": {
        "description": "A bacterial skin infection causing redness, swelling, warmth, and pain.",
        "prescription": {
            "mild": "Oral antibiotics (e.g., cephalexin) as prescribed; elevate affected limb.",
            "moderate": "Broad-spectrum antibiotics; monitor for fever and spreading redness.",
            "severe": "Hospitalization and IV antibiotics — seek emergency care if spreading rapidly.",
        },
        "stages": [
            {"name": "Early", "image": "/static/images/stages/cellulitis_early.svg",
             "signs": "Localized redness and mild warmth."},
            {"name": "Mild", "image": "/static/images/stages/cellulitis_mild.svg",
             "signs": "Swelling, tenderness, and expanding red area."},
            {"name": "Severe", "image": "/static/images/stages/cellulitis_severe.svg",
             "signs": "Fever, chills, rapid spread — medical emergency."},
        ],
    },
    "Atopic Dermatitis": {
        "description": "Chronic inflammatory skin condition (eczema) causing dry, itchy, inflamed skin.",
        "prescription": {
            "mild": "Fragrance-free moisturizers, mild topical corticosteroids for flare-ups.",
            "moderate": "Prescription-strength topical steroids or calcineurin inhibitors.",
            "severe": "Systemic immunosuppressants or biologics (dupilumab) under specialist care.",
        },
        "stages": [
            {"name": "Early", "image": "/static/images/stages/atopic_early.svg",
             "signs": "Dry patches, mild itching, slight redness."},
            {"name": "Mild", "image": "/static/images/stages/atopic_mild.svg",
             "signs": "Visible rash, moderate itching, skin thickening from scratching."},
            {"name": "Severe", "image": "/static/images/stages/atopic_severe.svg",
             "signs": "Widespread inflammation, cracking, bleeding, sleep disruption."},
        ],
    },
    "Scabies / Lyme": {
        "description": "Scabies: mite infestation causing intense itching and burrow tracks. Lyme: tick-borne rash (erythema migrans).",
        "prescription": {
            "mild": "Scabies: permethrin 5% cream. Lyme: doxycycline if early localized infection confirmed.",
            "moderate": "Scabies: repeat treatment after 7 days; treat all close contacts.",
            "severe": "Lyme with systemic symptoms: extended antibiotic course; specialist referral.",
        },
        "stages": [
            {"name": "Early", "image": "/static/images/stages/scabies_early.svg",
             "signs": "Small bumps, burrows between fingers; or bull's-eye Lyme rash."},
            {"name": "Mild", "image": "/static/images/stages/scabies_mild.svg",
             "signs": "Intense night itching; expanding Lyme rash ring."},
            {"name": "Severe", "image": "/static/images/stages/scabies_severe.svg",
             "signs": "Crusted (Norwegian) scabies; Lyme joint/neurological symptoms."},
        ],
    },
    "Seborrheic Dermatitis": {
        "description": "Common inflammatory condition affecting oily areas — scalp, face, chest — with flaking and redness.",
        "prescription": {
            "mild": "Antifungal shampoos (ketoconazole 2%), mild topical steroids.",
            "moderate": "Prescription antifungal creams; calcineurin inhibitors for face.",
            "severe": "Oral antifungals or stronger topical regimens under dermatologist guidance.",
        },
        "stages": [
            {"name": "Early", "image": "/static/images/stages/seborrheic_early.svg",
             "signs": "Mild dandruff, slight scalp or facial redness."},
            {"name": "Mild", "image": "/static/images/stages/seborrheic_mild.svg",
             "signs": "Greasy yellowish scales, persistent flaking."},
            {"name": "Severe", "image": "/static/images/stages/seborrheic_severe.svg",
             "signs": "Thick crusting, significant inflammation across multiple areas."},
        ],
    },
    "Acne / Rosacea": {
        "description": "Acne: clogged pores with pimples and inflammation. Rosacea: facial redness, visible vessels, bumps.",
        "prescription": {
            "mild": "Benzoyl peroxide or salicylic acid (acne); gentle skincare and SPF (rosacea).",
            "moderate": "Topical retinoids, antibiotics; metronidazole or azelaic acid for rosacea.",
            "severe": "Isotretinoin (acne) or oral antibiotics / laser therapy (rosacea) — specialist required.",
        },
        "stages": [
            {"name": "Early", "image": "/static/images/stages/acne_early.svg",
             "signs": "Occasional pimples or mild facial flushing."},
            {"name": "Mild", "image": "/static/images/stages/acne_mild.svg",
             "signs": "Regular breakouts or persistent facial redness."},
            {"name": "Severe", "image": "/static/images/stages/acne_severe.svg",
             "signs": "Cystic acne or rhinophyma / ocular rosacea complications."},
        ],
    },
    "Psoriasis": {
        "description": "Autoimmune condition causing rapid skin cell buildup — red plaques with silvery scales.",
        "prescription": {
            "mild": "Topical corticosteroids, vitamin D analogues, coal tar, daily moisturizers.",
            "moderate": "Phototherapy (UVB), topical calcineurin inhibitors, combination therapy.",
            "severe": "Systemic biologics (TNF, IL-17, IL-23 inhibitors) — dermatologist required.",
        },
        "stages": [
            {"name": "Early / Mild", "image": "/static/images/stages/psoriasis_mild.svg",
             "signs": "Small red patches with fine silvery scaling."},
            {"name": "Moderate", "image": "/static/images/stages/psoriasis_moderate.svg",
             "signs": "Thicker plaques, more body surface area affected."},
            {"name": "Severe", "image": "/static/images/stages/psoriasis_severe.svg",
             "signs": "Large plaques, pustular or erythrodermic forms — urgent care needed."},
        ],
    },
    "Melanoma": {
        "description": "The most serious form of skin cancer; may appear as new or changing pigmented lesions.",
        "prescription": {
            "mild": "Surgical excision with clear margins — immediate dermatologist evaluation required.",
            "moderate": "Wide local excision; sentinel lymph node biopsy if indicated.",
            "severe": "Immunotherapy, targeted therapy, or chemotherapy — oncology referral.",
        },
        "stages": [
            {"name": "Early", "image": "/static/images/stages/melanoma_early.svg",
             "signs": "New mole or spot — asymmetric, irregular border, color variation."},
            {"name": "Mild", "image": "/static/images/stages/melanoma_mild.svg",
             "signs": "Growing lesion >6 mm, evolving in size, shape, or color."},
            {"name": "Severe", "image": "/static/images/stages/melanoma_severe.svg",
             "signs": "Ulceration, bleeding, satellite lesions — urgent specialist care."},
        ],
    },
    "Eczema": {
        "description": "Inflammatory skin condition with dry, itchy, red patches — often overlapping with atopic dermatitis.",
        "prescription": {
            "mild": "Emollients applied liberally; avoid triggers (soaps, allergens).",
            "moderate": "Low-to-mid potency topical corticosteroids during flares.",
            "severe": "Wet-wrap therapy, systemic agents, or biologics under specialist care.",
        },
        "stages": [
            {"name": "Early", "image": "/static/images/stages/eczema_early.svg",
             "signs": "Dry skin, mild itch, faint redness."},
            {"name": "Mild", "image": "/static/images/stages/eczema_mild.svg",
             "signs": "Red inflamed patches, moderate itching, occasional weeping."},
            {"name": "Severe", "image": "/static/images/stages/eczema_severe.svg",
             "signs": "Widespread rash, lichenification, infection risk from scratching."},
        ],
    },
    "Actinic Keratosis": {
        "description": "Rough, scaly patches from sun damage; considered precancerous and requires monitoring.",
        "prescription": {
            "mild": "Topical 5-fluorouracil, imiquimod, or cryotherapy (liquid nitrogen).",
            "moderate": "Field treatment (photodynamic therapy) for multiple lesions.",
            "severe": "Surgical removal if thick or suspected progression to squamous cell carcinoma.",
        },
        "stages": [
            {"name": "Early", "image": "/static/images/stages/ak_early.svg",
             "signs": "Small rough sandpaper-like spot on sun-exposed skin."},
            {"name": "Mild", "image": "/static/images/stages/ak_mild.svg",
             "signs": "Red or brown scaly patch, 3–10 mm, slightly raised."},
            {"name": "Severe", "image": "/static/images/stages/ak_severe.svg",
             "signs": "Thick horn-like lesion (cutaneous horn) — biopsy recommended."},
        ],
    },
}

UNCERTAIN_ENTRY = {
    "description": "The image could not be classified with sufficient confidence.",
    "prescription": {
        "mild": "Consult a dermatologist for an in-person examination.",
        "moderate": "Consult a dermatologist for an in-person examination.",
        "severe": "Consult a dermatologist for an in-person examination.",
    },
    "stages": [],
}
