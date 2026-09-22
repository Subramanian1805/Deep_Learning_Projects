# DermaCare — Skin Disease Detection Flask App

Unified AI skin condition screening portal combining three Teachable Machine models into one seamless prediction experience with treatment guidance, stage estimation, and reference imagery.

## Features

- **Unified prediction** — All three models run automatically; one cohesive diagnosis is returned
- **Psoriasis accuracy tuning** — Post-processing rules reduce confusion with eczema, atopic dermatitis, and actinic keratosis
- **Melanoma safety priority** — High-confidence melanoma detections are never suppressed
- **Hospital-themed UI** — Clean clinical design with upload and webcam capture
- **Rich results** — Disease description, estimated stage, treatment guidance, and stage reference photos
- **Well documented** — Modular code with docstrings and a separate disease metadata catalog

## Supported Conditions (10 classes)

| Model | Conditions |
|-------|-----------|
| model1 | Ring Worm, Cellulitis, Atopic Dermatitis |
| model2 | Scabies / Lyme, Seborrheic Dermatitis, Acne / Rosacea, Psoriasis |
| model3 | Melanoma, Eczema, Actinic Keratosis |

## Setup

```bash
pip install -r requirements.txt
python generate_stage_images.py   # creates reference SVG images (first run only)
python app.py
```

Open http://127.0.0.1:5000

## Project Structure

```
skin_disease_flask_app/
├── app.py                  # Flask app, unified prediction pipeline
├── disease_info.py         # Disease catalog, thresholds, label mapping
├── generate_stage_images.py
├── requirements.txt
├── models/
│   ├── model1/             # Ring worm, Cellulitis, Atopic dermatitis
│   ├── model2/             # Scabies-Lyme, Seborrheic, Acne-Rosacea, Psoriasis
│   └── model3/             # Melanoma, Eczema, Actinic keratosis
├── static/images/stages/   # Reference stage SVG images
└── templates/
    └── index.html          # Hospital-themed UI
```

## Tuning Prediction Accuracy

Edit thresholds in `disease_info.py`:

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `MIN_CONFIDENCE` | 55 | Below this → "Uncertain" result |
| `HIGH_CONFIDENCE` | 75 | High-confidence badge threshold |
| `PSORIASIS_ECZEMA_MARGIN` | 10 | Required gap for definitive Psoriasis |
| `MELANOMA_PRIORITY_THRESHOLD` | 60 | Melanoma wins outright above this |

## API

**POST /predict** — multipart form with `image` field

Response:
```json
{
  "disease": "Psoriasis",
  "confidence": 72.4,
  "stage": "Mild to Moderate",
  "description": "...",
  "prescription": "...",
  "stages": [{"name": "...", "image": "/static/...", "signs": "..."}],
  "alternatives": [{"disease": "Eczema", "confidence": 68.1}],
  "severity_badge": "medium",
  "melanoma_alert": false,
  "all_scores": [{"disease": "...", "confidence": 72.4}]
}
```

## Notes

- `TF_USE_LEGACY_KERAS=1` is set in `app.py` so modern TensorFlow can load Teachable Machine `.h5` files.
- Stage reference images are illustrative SVG placeholders — replace with licensed clinical photos for production use.
- Treatment information is for **awareness only** and is not medical advice.

## Disclaimer

This tool is for educational and portfolio purposes only. It is not a medical diagnostic device. Always consult a qualified dermatologist for diagnosis and treatment.
