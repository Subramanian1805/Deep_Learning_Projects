"""
Skin Disease Detection Flask Application
=========================================
Unified inference across three Teachable Machine models with post-processing
rules to reduce cross-model confusion (especially Psoriasis vs. similar conditions).

Endpoints:
  GET  /         — Hospital-themed upload / webcam UI
  POST /predict  — Unified diagnosis with treatment and stage information
"""

import os

os.environ['TF_USE_LEGACY_KERAS'] = '1'
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
from flask import Flask, request, jsonify, render_template
from PIL import Image
import tensorflow as tf
from tensorflow.keras.layers import DepthwiseConv2D

from disease_info import (
    CANONICAL_LABELS,
    DISEASE_CATALOG,
    UNCERTAIN_ENTRY,
    PSORIASIS_CONFUSERS,
    MIN_CONFIDENCE,
    HIGH_CONFIDENCE,
    PSORIASIS_ECZEMA_MARGIN,
    MELANOMA_PRIORITY_THRESHOLD,
)

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------------------
# Model loading
# ---------------------------------------------------------------------------

class CustomDepthwiseConv2D(DepthwiseConv2D):
    """Compatibility shim for Teachable Machine DepthwiseConv2D layers."""

    def __init__(self, **kwargs):
        kwargs.pop('groups', None)
        super().__init__(**kwargs)


CUSTOM_OBJECTS = {'DepthwiseConv2D': CustomDepthwiseConv2D}

MODEL_IDS = ['model1', 'model2', 'model3']
models = {}
labels = {}


def load_all_models():
    """Load all three .h5 models and their label files from disk."""
    for mid in MODEL_IDS:
        model_path = os.path.join(BASE_DIR, 'models', mid, 'keras_model.h5')
        labels_path = os.path.join(BASE_DIR, 'models', mid, 'labels.txt')
        models[mid] = tf.keras.models.load_model(
            model_path, custom_objects=CUSTOM_OBJECTS, compile=False
        )
        with open(labels_path, 'r', encoding='utf-8') as f:
            labels[mid] = [
                line.strip().split(' ', 1)[1] if ' ' in line.strip() else line.strip()
                for line in f.readlines() if line.strip()
            ]
        print(f'Loaded {mid}: {labels[mid]}')


def preprocess_image(image_file):
    """Resize and normalize an uploaded image for Teachable Machine models."""
    img = Image.open(image_file).convert('RGB')
    img = img.resize((224, 224), Image.LANCZOS)
    arr = np.asarray(img, dtype=np.float32).reshape(1, 224, 224, 3)
    arr = (arr / 127.5) - 1
    return arr


def predict_with_model(mid, arr):
    """Run inference for a single model and return all class scores."""
    prediction = models[mid].predict(arr, verbose=0)
    idx = int(np.argmax(prediction))
    return {
        'model_id': mid,
        'class_name': labels[mid][idx],
        'confidence': round(float(prediction[0][idx]) * 100, 2),
        'all_scores': [
            {
                'label': labels[mid][i],
                'confidence': round(float(prediction[0][i]) * 100, 2),
            }
            for i in range(len(labels[mid]))
        ],
    }


# ---------------------------------------------------------------------------
# Unified prediction with conflict resolution
# ---------------------------------------------------------------------------

def _canonical(name):
    """Map a raw model label to its canonical display name."""
    return CANONICAL_LABELS.get(name, name)


def _collect_global_scores(raw_results):
    """
    Merge per-model scores into one dict keyed by canonical disease name.
    When the same disease appears in multiple models, keep the highest score.
    """
    scores = {}
    for result in raw_results:
        for item in result['all_scores']:
            name = _canonical(item['label'])
            scores[name] = max(scores.get(name, 0), item['confidence'])
    return scores


def apply_conflict_rules(scores):
    """
    Apply post-processing rules to reduce known misclassification patterns.

    Psoriasis is penalised when visually similar conditions (eczema, atopic
    dermatitis, actinic keratosis) also score highly. Melanoma is never
    suppressed — if it exceeds the priority threshold it wins outright.
    """
    if not scores:
        return {
            'disease': 'Uncertain — consult a dermatologist',
            'confidence': 0,
            'alternatives': [],
            'uncertain': True,
        }

    melanoma_score = scores.get('Melanoma', 0)
    if melanoma_score >= MELANOMA_PRIORITY_THRESHOLD:
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        alts = [{'disease': d, 'confidence': c} for d, c in ranked[1:3]]
        return {
            'disease': 'Melanoma',
            'confidence': round(melanoma_score, 2),
            'alternatives': alts,
            'uncertain': False,
            'melanoma_alert': True,
        }

    adjusted = scores.copy()
    psoriasis = scores.get('Psoriasis', 0)

    if psoriasis > 0:
        for confuser, factor in PSORIASIS_CONFUSERS.items():
            confuser_score = scores.get(confuser, 0)
            if confuser == 'Melanoma':
                continue
            if confuser_score > 40:
                penalty = (confuser_score / 100) * (1 - factor)
                adjusted['Psoriasis'] = adjusted.get('Psoriasis', 0) * (1 - penalty)

    ranked = sorted(adjusted.items(), key=lambda x: x[1], reverse=True)
    top_disease, top_conf = ranked[0]
    alternatives = [{'disease': d, 'confidence': round(c, 2)} for d, c in ranked[1:4]]

    if top_conf < MIN_CONFIDENCE:
        return {
            'disease': 'Uncertain — consult a dermatologist',
            'confidence': round(top_conf, 2),
            'alternatives': alternatives,
            'uncertain': True,
        }

    # Psoriasis must lead eczema/atopic by a minimum margin when both are strong.
    if top_disease == 'Psoriasis':
        eczema_score = max(scores.get('Eczema', 0), scores.get('Atopic Dermatitis', 0))
        if eczema_score > 40 and (top_conf - eczema_score) < PSORIASIS_ECZEMA_MARGIN:
            return {
                'disease': 'Psoriasis (possible)',
                'confidence': round(top_conf, 2),
                'alternatives': [
                    {'disease': 'Eczema / Atopic Dermatitis', 'confidence': round(eczema_score, 2)},
                    *alternatives[:2],
                ],
                'uncertain': False,
            }

    return {
        'disease': top_disease,
        'confidence': round(top_conf, 2),
        'alternatives': alternatives,
        'uncertain': False,
    }


def estimate_stage(confidence, uncertain=False):
    """
    Estimate disease stage from prediction confidence.

    Note: this is a heuristic proxy — actual clinical staging requires
    in-person examination by a dermatologist.
    """
    if uncertain:
        return 'Inconclusive — professional evaluation recommended'
    if confidence >= 85:
        return 'Moderate to Severe'
    if confidence >= HIGH_CONFIDENCE:
        return 'Mild to Moderate'
    if confidence >= MIN_CONFIDENCE:
        return 'Early / Mild'
    return 'Inconclusive — professional evaluation recommended'


def _prescription_for_stage(catalog_entry, stage_label):
    """Return the treatment text matching the estimated severity stage."""
    rx = catalog_entry.get('prescription', {})
    stage_lower = stage_label.lower()
    if 'severe' in stage_lower:
        return rx.get('severe', '')
    if 'moderate' in stage_lower:
        return rx.get('moderate', '')
    return rx.get('mild', '')


def predict_unified(arr):
    """
    Run all models, merge scores, apply conflict rules, and enrich with
    disease metadata (description, prescription, stage photos).
    """
    raw_results = [predict_with_model(mid, arr) for mid in MODEL_IDS]
    scores = _collect_global_scores(raw_results)
    final = apply_conflict_rules(scores)

    disease_key = final['disease'].replace(' (possible)', '')
    if final.get('uncertain') or disease_key.startswith('Uncertain'):
        catalog = UNCERTAIN_ENTRY
    else:
        catalog = DISEASE_CATALOG.get(disease_key, UNCERTAIN_ENTRY)

    stage = estimate_stage(final['confidence'], final.get('uncertain', False))
    prescription = _prescription_for_stage(catalog, stage)

    severity_badge = 'low'
    if final.get('melanoma_alert'):
        severity_badge = 'critical'
    elif final['confidence'] >= HIGH_CONFIDENCE:
        severity_badge = 'high'
    elif final['confidence'] >= MIN_CONFIDENCE:
        severity_badge = 'medium'

    return {
        'disease': final['disease'],
        'confidence': final['confidence'],
        'stage': stage,
        'description': catalog.get('description', ''),
        'prescription': prescription,
        'prescriptions_all': catalog.get('prescription', {}),
        'stages': catalog.get('stages', []),
        'alternatives': final.get('alternatives', []),
        'severity_badge': severity_badge,
        'melanoma_alert': final.get('melanoma_alert', False),
        'uncertain': final.get('uncertain', False),
        'all_scores': sorted(
            [{'disease': d, 'confidence': round(c, 2)} for d, c in scores.items()],
            key=lambda x: x['confidence'],
            reverse=True,
        ),
    }


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400

    image_file = request.files['image']
    try:
        arr = preprocess_image(image_file)
    except Exception as exc:
        return jsonify({'error': f'Invalid image: {exc}'}), 400

    result = predict_unified(arr)
    return jsonify(result)


if __name__ == '__main__':
    load_all_models()
    app.run(debug=False, use_reloader=False, host='0.0.0.0', port=5000)
