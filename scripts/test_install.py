"""Offline installation smoke test, including scoring from the installed copy."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path
from install import install

with tempfile.TemporaryDirectory() as folder:
    target = Path(folder) / 'host skills' / 'ultimate-website-audit'
    assert install(target) == target
    assert (target / 'SKILL.md').is_file()
    assert (target / 'references/runtime.md').is_file()
    assert not list(target.rglob('*.pyc'))
    output = subprocess.run([sys.executable, str(target / 'scripts/score.py'), str(target / 'examples/audit-input.json')], check=True, capture_output=True, text=True)
    assert json.loads(output.stdout)['sites'][0]['overall']['score'] is None
    before = (target / 'SKILL.md').read_bytes()
    try:
        install(target)
    except ValueError:
        pass
    else:
        raise AssertionError('Existing destination was not rejected')
    assert (target / 'SKILL.md').read_bytes() == before
print('Portable installation and installed scoring checks passed; existing files preserved.')
