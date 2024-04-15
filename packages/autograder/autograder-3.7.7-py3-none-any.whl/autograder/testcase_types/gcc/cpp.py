from autograder.testcase_types.gcc.c import TestCase as CTestCase
from autograder.testcase_utils.shell import get_shell_command


class TestCase(CTestCase):
    source_suffix = ".cpp"
    compiler = get_shell_command("g++")

    @classmethod
    def get_template_dir(cls):
        return cls.type_source_file.parent / "c++_templates"
