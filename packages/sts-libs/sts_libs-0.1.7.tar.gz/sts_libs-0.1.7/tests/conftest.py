#  Copyright: Contributors to the sts project
#  GNU General Public License v3.0+ (see LICENSE or https://www.gnu.org/licenses/gpl-3.0.txt)

import json
import logging
import time
from os import getenv
from pathlib import Path
from typing import cast

from sts.utils.tmt import CustomResults, TmtResult, remove_nones

pytest_plugins = [
    'sts.fixtures.iscsi_fixtures',
    'sts.fixtures.rdma_fixtures',
]

test_data_dir = getenv('TMT_TEST_DATA')
if not test_data_dir:
    from uuid import uuid4

    dir_name = f'/var/tmp/{uuid4().hex[-9:]}'

    logging.warning(f'TMT_TEST_DATA env var not detected. Using {dir_name}')
    test_data_dir = dir_name
    Path(test_data_dir).mkdir(parents=True, exist_ok=True)

test_data_path = Path(test_data_dir)


def map_outcome(outcome: str) -> TmtResult:
    """Map pytest outcomes to TMT results."""
    if outcome in {'passed', 'xfailed'}:
        result = 'pass'
    elif outcome == 'failed':
        result = 'fail'
    elif outcome == 'xpassed':
        result = 'warn'
    elif outcome == 'skipped':
        result = 'info'
    else:
        result = 'error'

    return cast(TmtResult, result)


def pytest_terminal_summary(terminalreporter) -> None:  # noqa: ANN001
    """Generate TMT-compatible custom results.json."""
    results = []
    for report in (
        terminalreporter.stats.get('passed', [])
        + terminalreporter.stats.get('failed', [])
        + terminalreporter.stats.get('xfailed', [])
        + terminalreporter.stats.get('xpassed', [])
        + terminalreporter.stats.get('skipped', [])
    ):
        name = report.location[-1]
        status = map_outcome(report.outcome)
        duration = time.strftime('%H:%M:%S', time.gmtime(report.duration))

        result = CustomResults(
            name=f'/{name}',
            result=status,
            duration=duration,
            ids=None,
            serialnumber=None,
            guest=None,
            note=None,
            log=None,
        )

        # Always include pytest's stdout
        out_file_name = f'stdout-{name}'
        out_file = test_data_path / out_file_name
        with out_file.open('w') as f:
            f.write(report.capstdout)

        result.update({'log': [out_file_name]})

        # Handle optional user_properties
        if report.user_properties:
            props = dict(report.user_properties)
            for key in result:
                if key in props:
                    # Appends to logs instead of overwriting
                    if key == 'log':
                        log_list: list[str] = result['log']
                        log_list.append(props[key])
                        result.update({key: log_list})
                        print(result)
                    else:
                        result.update({key: props[key]})

        results.append(remove_nones(result))

    file = test_data_path / 'results.json'
    with file.open('w') as f:
        json.dump(results, f)
