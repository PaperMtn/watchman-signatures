import os
import unittest
from pathlib import Path

from models import signature_slack_eg

SIGNATURES_PATH = (Path(__file__).parents[1] / 'signatures').resolve()


def assert_empty(obj):
    if obj[0] is None:
        return True
    else:
        return False


def assert_not_empty(obj):
    if obj[0] is None:
        return False
    else:
        return True


def load_signatures_slack() -> list:
    """Load signatures from YAML files

    Returns:
        List containing loaded definitions as Signatures objects
    """

    loaded_signatures = []
    try:
        for root, dirs, files in os.walk(SIGNATURES_PATH):
            for sig_file in files:
                sig_path = (Path(root) / sig_file).resolve()
                if sig_path.name.endswith('.yaml'):
                    loaded_def = signature_slack_eg.load_from_yaml(sig_path)
                    for sig in loaded_def:
                        if sig.status == 'enabled' and 'slack_std' in sig.watchman_apps:
                            loaded_signatures.append(sig)
        return loaded_signatures
    except Exception as e:
        raise e


class TestSigs(unittest.TestCase):
    def test_signatures_format_slack(self):
        """Check signatures are properly formed YAML ready to be ingested for Slack Watchman"""

        try:
            load_signatures_slack()
        except AttributeError:
            self.assertTrue(False)

    def test_search_strings_format(self):
        print('Testing search string format')
        signatures = load_signatures_slack()

        for sig in signatures:
            if 'slack' in sig.watchman_apps:
                assert isinstance(sig.search_strings, list), f'Signature {sig.name} has' \
                                                             f' incorrectly formatted Slack search strings'

    def test_search_strings_content(self):
        print('Testing search strings content')
        signatures = load_signatures_slack()

        for sig in signatures:
            if 'slack' in sig.watchman_apps:
                self.assertTrue(assert_not_empty(sig.search_strings), f'Signature {sig.name} has no search strings.'
                                                                      f' There must be at least one to be used with Slack Watchman')

    def test_scope_format(self):
        print('Testing scope options')
        signatures = load_signatures_slack()

        for sig in signatures:
            if 'slack' in sig.watchman_apps:
                assert isinstance(sig.scope, list), f'Signature {sig.name} has' \
                                                    f' incorrectly formatted Slack Watchman scopes'

    def test_scope_content(self):
        print('Testing scope content')
        signatures = load_signatures_slack()

        for sig in signatures:
            if 'slack' in sig.watchman_apps:
                self.assertTrue(assert_not_empty(sig.scope), f'Signature {sig.name} has no scopes.'
                                                             f' There must be at least one to be used with Slack '
                                                             f'Watchman')


if __name__ == '__main__':
    unittest.main()
