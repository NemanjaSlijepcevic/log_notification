from pattern_functions import generate_defined_patterns


class TestGeneratePatternFunction:
    def test_generate_defined_patterns_pass(self):
        input_text = "Test1, Test2, Test3"
        output_pattern = ["Test1", "Test2", "Test3"]
        assert generate_defined_patterns(input_text) == output_pattern

    def test_generate_defined_patterns_empty_text(self):
        input_text = ""
        output_pattern = [""]
        assert generate_defined_patterns(input_text) == output_pattern

    def test_generate_defined_patterns_empty_pattern(self):
        input_text = "  ,   , "
        output_pattern = ["", "", ""]
        assert generate_defined_patterns(input_text) == output_pattern
