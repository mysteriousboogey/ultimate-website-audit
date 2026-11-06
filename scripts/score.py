#!/usr/bin/env python3
"""Calculate readiness scores from an evidence ledger; no network access."""
import json
import sys
from pathlib import Path
from urllib.parse import urlsplit

RUBRIC = json.loads((Path(__file__).resolve().parents[1] / 'references/rubric.json').read_text())

def calculate(data):
    if data.get('rubric_version') != RUBRIC['version']:
        raise ValueError('rubric_version must match ' + RUBRIC['version'])
    sites = data.get('sites')
    if not isinstance(sites, list) or not sites:
        raise ValueError('sites must be a nonempty list')
    result = []
    ids = {c['id'] for c in RUBRIC['criteria']}
    for site in sites:
        url = site.get('url', '')
        parsed = urlsplit(url)
        if parsed.scheme not in ('http', 'https') or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError('Each site requires an HTTP(S) URL without credentials')
        checks = site.get('checks', {})
        if not isinstance(checks, dict) or set(checks) - ids:
            raise ValueError('Unknown criterion IDs or invalid checks object')
        raw = {}
        raw_coverage = {}
        categories = {}
        for category in RUBRIC['overall_weights']:
            earned = verified = applicable = 0.0
            for criterion in RUBRIC['criteria']:
                if criterion['category'] != category:
                    continue
                units = checks.get(criterion['id'], [{'unit': 'unassessed', 'status': 'unknown', 'evidence': 'Criterion not assessed'}])
                if not isinstance(units, list) or not units:
                    raise ValueError(criterion['id'] + ': provide at least one unit')
                seen = set()
                counts = dict.fromkeys(('pass', 'fail', 'unknown', 'na'), 0)
                for unit in units:
                    if not isinstance(unit, dict):
                        raise ValueError('Each unit must be an object')
                    name, status, evidence = unit.get('unit'), unit.get('status'), unit.get('evidence')
                    if not isinstance(name, str) or not name.strip() or name in seen:
                        raise ValueError('Unit names must be nonempty and unique within a criterion')
                    if status not in counts or not isinstance(evidence, str) or not evidence.strip():
                        raise ValueError('Each unit needs a valid status and nonempty evidence/reason')
                    seen.add(name)
                    counts[status] += 1
                total = counts['pass'] + counts['fail'] + counts['unknown']
                if total:
                    weight = criterion['weight']
                    applicable += weight
                    earned += weight * counts['pass'] / total
                    verified += weight * (counts['pass'] + counts['fail']) / total
            score = 100 * earned / verified if verified else None
            coverage = 100 * verified / applicable if applicable else None
            raw[category] = score
            raw_coverage[category] = coverage
            categories[category] = {
                'score': round(score, 1) if score is not None else None,
                'coverage': round(coverage, 1) if coverage is not None else None,
                'rating': ('Good' if score >= 80 - 1e-9 else 'Needs improvement') if score is not None else 'Insufficient evidence',
                'provisional': coverage is None or coverage < 100 - 1e-9,
                'confidence': 'Insufficient coverage' if coverage is None or coverage < 80 - 1e-9 else 'Observed sample only',
            }
        weights = RUBRIC['overall_weights']
        overall = sum(weights[c] * raw[c] for c in weights) if all(v is not None for v in raw.values()) else None
        coverage = sum(weights[c] * (raw_coverage[c] or 0) for c in weights)
        result.append({'url': url, 'categories': categories, 'overall': {
            'score': round(overall, 1) if overall is not None else None,
            'coverage': round(coverage, 1),
            'rating': ('Good' if overall >= 80 - 1e-9 else 'Needs improvement') if overall is not None else 'Insufficient evidence',
            'provisional': any(v['provisional'] for v in categories.values()),
        }})
    return {'rubric_version': RUBRIC['version'], 'overall_weights': RUBRIC['overall_weights'], 'sites': result}

if __name__ == '__main__':
    try:
        if len(sys.argv) != 2:
            raise ValueError('Usage: python3 score.py audit.json')
        print(json.dumps(calculate(json.loads(Path(sys.argv[1]).read_text())), indent=2, allow_nan=False))
    except (ValueError, TypeError, KeyError, AttributeError, OSError) as exc:
        sys.exit('Invalid audit input: ' + str(exc))
