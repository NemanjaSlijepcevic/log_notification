from pattern_functions import filter_patterns


class TestFilterPatternFunction:
    def test_filter_patterns_pass(self):
        input_text = ['\n', '\n', 'Text pattern1\n', 'Text pattern2\n']
        input_pattern = ["pattern1", "pattern2"]
        output = "Text pattern1\nText pattern2\n"
        assert filter_patterns(input_text, input_pattern) == output

    def test_filter_patterns_no_match(self):
        input_text = ['No match here\n']
        input_pattern = ["pattern1", "pattern2"]
        output = ""
        assert filter_patterns(input_text, input_pattern) == output

    def test_filter_patterns_empty_text(self):
        input_text = []
        input_pattern = ["pattern1", "pattern2"]
        output = ""
        assert filter_patterns(input_text, input_pattern) == output

    def test_filter_patterns_empty_patterns(self):
        input_text = ["Text pattern1\n", "Text pattern2"]
        input_pattern = []
        output = ""
        assert filter_patterns(input_text, input_pattern) == output
