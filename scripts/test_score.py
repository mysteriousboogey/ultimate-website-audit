"""Run with python3 scripts/test_score.py."""
from copy import deepcopy
from score import RUBRIC, calculate

def unit(status, name='page'):
    return {'unit': name, 'status': status, 'evidence': 'fixture: observed response or explicit reason'}

def audit(status='pass'):
    return {'rubric_version': '1.0', 'sites': [{'url': 'https://example.com', 'checks': {c['id']: [unit(status)] for c in RUBRIC['criteria']}}]}

def output(data):
    return calculate(data)['sites'][0]

assert all(sum(c['weight'] for c in RUBRIC['criteria'] if c['category'] == cat) == 100 for cat in ('SEO', 'AEO', 'GEO'))
assert output(audit())['overall']['score'] == 100
assert output(audit('fail'))['overall']['score'] == 0
assert output(audit('unknown'))['overall']['score'] is None
assert output(audit('na'))['overall']['score'] is None
mixed = audit()
mixed['sites'][0]['checks']['S1'] = [unit('pass'), unit('unknown', 'unavailable')]
r = output(mixed)
assert r['categories']['SEO']['score'] == 100
assert r['categories']['SEO']['coverage'] == 92.5
assert r['overall']['provisional']
mixed['sites'][0]['checks']['S1'] = [unit('fail')]
assert output(mixed)['categories']['SEO']['score'] == 85
assert output(mixed)['overall']['score'] == 92.5
for criterion in RUBRIC['criteria']:
    if criterion['category'] == 'AEO':
        mixed['sites'][0]['checks'][criterion['id']] = [unit('unknown')]
assert output(mixed)['overall']['score'] is None
boundary = audit()
boundary['sites'][0]['checks']['G1'] = [unit('fail')]
assert output(boundary)['categories']['GEO']['score'] == 80
assert output(boundary)['categories']['GEO']['rating'] == 'Good'
minimal = audit()
minimal['sites'][0]['checks'] = {'S1': [unit('pass')]}
assert output(minimal)['categories']['SEO']['coverage'] == 15
assert output(minimal)['categories']['SEO']['confidence'] == 'Insufficient coverage'
multi = audit()
multi['sites'].append(deepcopy(audit('fail')['sites'][0]))
assert [s['overall']['score'] for s in calculate(multi)['sites']] == [100, 0]
for bad in ({'BAD': [unit('pass')]}, {'S1': []}, {'S1': [unit('pass'), unit('fail')]}, {'S1': [{'unit': 'x', 'status': 'pass', 'evidence': ''}]}):
    invalid = audit()
    invalid['sites'][0]['checks'] = bad
    try:
        calculate(invalid)
    except ValueError:
        pass
    else:
        raise AssertionError('Invalid input accepted')
print('Scoring checks passed: full/missing/NA/mixed evidence, weights, threshold, multiple sites and invalid input.')
