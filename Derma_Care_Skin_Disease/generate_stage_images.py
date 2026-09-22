"""Generate SVG placeholder reference images for disease stages."""

import os

BASE = os.path.join(os.path.dirname(__file__), 'static', 'images', 'stages')

# (filename, title, stage_name, base_color)
IMAGES = [
    ('ring_worm_early', 'Ring Worm', 'Early', '#ffcdd2'),
    ('ring_worm_mild', 'Ring Worm', 'Mild', '#ef9a9a'),
    ('ring_worm_severe', 'Ring Worm', 'Severe', '#e53935'),
    ('cellulitis_early', 'Cellulitis', 'Early', '#f8bbd0'),
    ('cellulitis_mild', 'Cellulitis', 'Mild', '#f48fb1'),
    ('cellulitis_severe', 'Cellulitis', 'Severe', '#c2185b'),
    ('atopic_early', 'Atopic Dermatitis', 'Early', '#ffe0b2'),
    ('atopic_mild', 'Atopic Dermatitis', 'Mild', '#ffcc80'),
    ('atopic_severe', 'Atopic Dermatitis', 'Severe', '#fb8c00'),
    ('scabies_early', 'Scabies / Lyme', 'Early', '#d1c4e9'),
    ('scabies_mild', 'Scabies / Lyme', 'Mild', '#b39ddb'),
    ('scabies_severe', 'Scabies / Lyme', 'Severe', '#7e57c2'),
    ('seborrheic_early', 'Seborrheic', 'Early', '#fff9c4'),
    ('seborrheic_mild', 'Seborrheic', 'Mild', '#fff176'),
    ('seborrheic_severe', 'Seborrheic', 'Severe', '#f9a825'),
    ('acne_early', 'Acne / Rosacea', 'Early', '#f0f4c3'),
    ('acne_mild', 'Acne / Rosacea', 'Mild', '#dce775'),
    ('acne_severe', 'Acne / Rosacea', 'Severe', '#afb42b'),
    ('psoriasis_mild', 'Psoriasis', 'Early / Mild', '#b2dfdb'),
    ('psoriasis_moderate', 'Psoriasis', 'Moderate', '#4db6ac'),
    ('psoriasis_severe', 'Psoriasis', 'Severe', '#00695c'),
    ('melanoma_early', 'Melanoma', 'Early', '#bcaaa4'),
    ('melanoma_mild', 'Melanoma', 'Mild', '#8d6e63'),
    ('melanoma_severe', 'Melanoma', 'Severe', '#4e342e'),
    ('eczema_early', 'Eczema', 'Early', '#ffccbc'),
    ('eczema_mild', 'Eczema', 'Mild', '#ffab91'),
    ('eczema_severe', 'Eczema', 'Severe', '#ff5722'),
    ('ak_early', 'Actinic Keratosis', 'Early', '#cfd8dc'),
    ('ak_mild', 'Actinic Keratosis', 'Mild', '#90a4ae'),
    ('ak_severe', 'Actinic Keratosis', 'Severe', '#546e7a'),
]

SVG_TEMPLATE = '''<svg xmlns="http://www.w3.org/2000/svg" width="320" height="180" viewBox="0 0 320 180">
  <rect width="320" height="180" fill="{bg}"/>
  <ellipse cx="160" cy="90" rx="70" ry="55" fill="{spot}" opacity="0.7"/>
  <ellipse cx="160" cy="90" rx="45" ry="35" fill="{spot2}" opacity="0.5"/>
  <text x="160" y="30" text-anchor="middle" font-family="Arial,sans-serif" font-size="13" fill="#333" font-weight="bold">{title}</text>
  <text x="160" y="165" text-anchor="middle" font-family="Arial,sans-serif" font-size="11" fill="#555">{stage} — Reference</text>
  <text x="160" y="100" text-anchor="middle" font-family="Arial,sans-serif" font-size="10" fill="#666" opacity="0.6">Illustrative only</text>
</svg>'''


def main():
    os.makedirs(BASE, exist_ok=True)
    for fname, title, stage, color in IMAGES:
        svg = SVG_TEMPLATE.format(
            bg='#f5f5f5', spot=color, spot2=color,
            title=title, stage=stage,
        )
        path = os.path.join(BASE, f'{fname}.svg')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(svg)
        print(f'Created {path}')
    print(f'Done — {len(IMAGES)} images generated.')


if __name__ == '__main__':
    main()
