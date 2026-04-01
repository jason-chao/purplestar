"""
Tests that generate 紫微斗數 natal charts for a set of fictional individuals
and save the output files to tests/output/.
"""
import json
import os
import re
import pytest

from purplestar.core.chart import generate_chart
from purplestar.output.json_schema import to_json_schema
from purplestar.output.plaintext import to_plaintext

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Fictional individuals for testing.
# (id, name, gender, solar_date, time_or_None, timezone, place)
# Some birth times are unknown (None).
INDIVIDUALS = [
    ('HK1', 'Chan Tai-man',    'male',   '1988-04-15', '06:30', 'Asia/Hong_Kong',       'Hong Kong'),
    ('TP1', 'Lin Mei-ling',    'female', '1993-07-22', None,    'Asia/Taipei',           'Taipei, Taiwan'),
    ('BJ1', 'Zhang Wei',       'male',   '1975-11-03', '14:15', 'Asia/Shanghai',         'Beijing, China'),
    ('SG1', 'Tan Hui-ling',    'female', '1990-02-14', '09:00', 'Asia/Singapore',        'Singapore'),
    ('LD1', 'Emily Hartley',   'female', '1982-08-30', None,    'Europe/London',         'London, England'),
    ('NY1', 'Michael Reeves',  'male',   '1967-05-20', '22:45', 'America/New_York',      'New York, United States'),
    ('SF1', 'David Chen',      'male',   '1979-12-01', None,    'America/Los_Angeles',   'San Francisco, United States'),
    ('KL1', 'Nurul Aina',      'female', '2001-09-11', '03:20', 'Asia/Kuala_Lumpur',     'Kuala Lumpur, Malaysia'),
    ('SY1', "James O'Brien",   'male',   '1958-03-18', '11:00', 'Australia/Sydney',      'Sydney, Australia'),
    ('TK1', 'Yuki Tanaka',     'female', '1995-06-07', None,    'Asia/Tokyo',            'Tokyo, Japan'),
    ('VN1', 'Lucas Bergmann',  'male',   '2004-01-29', '16:45', 'America/Vancouver',     'Vancouver, Canada'),
    ('PR1', 'Sophie Dubois',   'female', '1970-10-05', '08:30', 'Europe/Paris',          'Paris, France'),
]


def _abbrev_name(name: str) -> str:
    """Return initials of a name, splitting on spaces, hyphens, and apostrophes."""
    parts = re.split(r"[\s\-']+", name)
    return ''.join(p[0].upper() for p in parts if p)


def _stem(individual_id: str, name: str) -> str:
    """Return the base filename stem, e.g. 'HK1_CTM'."""
    return f'{individual_id}_{_abbrev_name(name)}'


def _generate_and_save(individual_id, name, gender, date, time, timezone, place):
    """Generate chart and save JSON and text files."""
    chart = generate_chart(
        gender=gender,
        solar_date=date,
        time=time,
        timezone=timezone,
        place=place,
        name=name,
    )

    stem = _stem(individual_id, name)
    json_path = os.path.join(OUTPUT_DIR, f'{stem}.json')
    txt_path = os.path.join(OUTPUT_DIR, f'{stem}.txt')

    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(to_json_schema(chart))

    with open(txt_path, 'w', encoding='utf-8') as f:
        f.write(to_plaintext(chart))

    return chart


@pytest.mark.parametrize('individual_id,name,gender,date,time,timezone,place', INDIVIDUALS)
def test_generate_chart(individual_id, name, gender, date, time, timezone, place):
    """Generate and save chart for each individual; validate basic structure."""
    chart = _generate_and_save(individual_id, name, gender, date, time, timezone, place)

    # Validate basic structure
    assert chart['chart_type'] == 'ziwei.natal'
    profile = chart['chart']['profile']
    assert profile['five_element_bureau']['number'] in (2, 3, 4, 5, 6)
    assert profile['ming_palace_position'] in range(1, 13)
    assert profile['body_palace_position'] in range(1, 13)

    # Exactly 12 palaces
    palaces = chart['chart']['palaces']
    assert len(palaces) == 12

    # Each palace has position, palace, stem, branch, stars
    for p in palaces:
        assert 1 <= p['position'] <= 12
        assert p['palace'] in (
            'life', 'parents', 'spirit', 'property', 'career', 'friends',
            'travel', 'health', 'wealth', 'children', 'spouse', 'siblings'
        )

    # Exactly 14 major stars placed across the chart
    major_stars = [s for p in palaces for s in p['stars'] if s['category'] == 'major']
    assert len(major_stars) == 14, f"Expected 14 major stars, got {len(major_stars)}"

    # Exactly 4 natal transformations
    transforms = {
        s['natal_transformation']
        for p in palaces
        for s in p['stars']
        if s.get('natal_transformation')
    }
    assert transforms == {'lu', 'quan', 'ke', 'ji'}, \
        f"Expected 4 transformations, got {transforms}"

    # Exactly one body palace
    body_palaces = [p for p in palaces if p['is_body_palace']]
    assert len(body_palaces) == 1

    # Unknown birth time: notes must mention it
    if time is None:
        text = to_plaintext(chart)
        assert '時間不詳' in text

    # Output files exist
    stem = _stem(individual_id, name)
    json_path = os.path.join(OUTPUT_DIR, f'{stem}.json')
    txt_path = os.path.join(OUTPUT_DIR, f'{stem}.txt')
    assert os.path.exists(json_path)
    assert os.path.exists(txt_path)

    # JSON is valid
    with open(json_path, encoding='utf-8') as f:
        data = json.load(f)
    assert data['schema_version'] == '2.0.0'
    assert data['chart_type'] == 'ziwei.natal'


def test_all_output_files():
    """Ensure all output files are generated (can be run standalone)."""
    for args in INDIVIDUALS:
        individual_id, name = args[0], args[1]
        stem = _stem(individual_id, name)
        json_path = os.path.join(OUTPUT_DIR, f'{stem}.json')
        txt_path = os.path.join(OUTPUT_DIR, f'{stem}.txt')
        if not os.path.exists(json_path) or not os.path.exists(txt_path):
            _generate_and_save(*args)
        assert os.path.exists(json_path), f"Missing {json_path}"
        assert os.path.exists(txt_path), f"Missing {txt_path}"
