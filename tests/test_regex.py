import yaml
import os
import unittest
from pathlib import Path

from models import signature_basic

SIGNATURES_PATH = (Path(__file__).parents[1] / 'signatures').resolve()


def load_signatures_basic() -> list:
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
                    loaded_def = signature_basic.load_from_yaml(sig_path)
                    for sig in loaded_def:
                        if sig.status == 'enabled':
                            loaded_signatures.append(sig)
        return loaded_signatures
    except Exception as e:
        raise e


def check_yaml(sig):
    try:
        yaml_sig = yaml.safe_load(sig)
    except:
        return False
    return True


class TestSigs(unittest.TestCase):
    def test_signatures_format(self):
        """Check signatures are properly formed YAML and match the basic Watchman structure"""

        for root, dirs, files in os.walk(SIGNATURES_PATH):
            for sig_file in files:
                sig_path = (Path(root) / sig_file).resolve()
                if sig_path.name.endswith('.yaml'):
                    with open(sig_path) as yaml_file:
                        self.assertTrue(check_yaml(yaml_file.read()), msg=f'Malformed YAML: {yaml_file.name}')

    def test_signature_matching_cases(self):
        """Test that the match case strings match the regex. Skip if the match case is 'blank'"""

        sig_list = load_signatures_basic()
        for signature in sig_list:
            for pattern in signature.patterns:
                for test_case in signature.test_cases.match_cases:
                    if not test_case == 'blank':
                        self.assertRegex(
                            test_case,
                            pattern,
                            msg='Regex does not detect given match case'
                        )

    def test_signature_failing_cases(self):
        """Test that the fail case strings don't match the regex. Skip if the fail case is 'blank'"""

        sig_list = load_signatures_basic()
        for signature in sig_list:
            for pattern in signature.patterns:
                if signature.test_cases.fail_cases:
                    for test_case in signature.test_cases.fail_cases:
                        if not test_case == 'blank':
                            self.assertNotRegex(
                                test_case,
                                pattern,
                                msg='Regex does detect given failure case, it should not'
                            )


if __name__ == '__main__':
    unittest.main()
