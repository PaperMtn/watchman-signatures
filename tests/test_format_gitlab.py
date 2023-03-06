import os
import unittest
from pathlib import Path

from models import signature_gitlab

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


def load_signatures_gitlab() -> list:
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
                    loaded_def = signature_gitlab.load_from_yaml(sig_path)
                    for sig in loaded_def:
                        if sig.status == 'enabled' and 'gitlab' in sig.watchman_apps:
                            loaded_signatures.append(sig)
        return loaded_signatures
    except Exception as e:
        raise e


class TestSigs(unittest.TestCase):
    def test_signatures_format_gitlab(self):
        """Check signatures are properly formed YAML ready to be ingested for GitLab Watchman"""

        try:
            load_signatures_gitlab()
        except AttributeError:
            self.assertTrue(False)

    def test_search_strings_format(self):
        print('Testing search string format')
        signatures = load_signatures_gitlab()

        for sig in signatures:
            if 'gitlab' in sig.watchman_apps:
                assert isinstance(sig.search_strings, list), f'Signature {sig.name} has' \
                                                             f' incorrectly formatted GitLab search strings'

    def test_search_strings_content(self):
        print('Testing search strings content')
        signatures = load_signatures_gitlab()

        for sig in signatures:
            if 'gitlab' in sig.watchman_apps:
                self.assertTrue(assert_not_empty(sig.search_strings), f'Signature {sig.name} has no search strings.'
                                                                      f' There must be at least one to be used with GitLab Watchman')

    def test_scope_format(self):
        print('Testing scope options')
        signatures = load_signatures_gitlab()

        for sig in signatures:
            if 'gitlab' in sig.watchman_apps:
                assert isinstance(sig.scope, list), f'Signature {sig.name} has' \
                                                    f' incorrectly formatted GitLab scopes'

    def test_scope_content(self):
        print('Testing scope content')
        signatures = load_signatures_gitlab()

        for sig in signatures:
            if 'gitlab' in sig.watchman_apps:
                self.assertTrue(assert_not_empty(sig.scope), f'Signature {sig.name} has no scopes.'
                                                             f' There must be at least one to be used with GitLab Watchman')

if __name__ == '__main__':
    print('Running GitLab signature tests')
    print('-----')
    unittest.main()
    print('-----')
