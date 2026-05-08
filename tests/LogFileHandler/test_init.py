from LogFileHandler import LogFileHandler


class TestLogFileHandlerInitPos:

    def test_init_single_file_pass(self, tmp_path):
        (tmp_path / 'test.log').write_text('test', encoding='utf-8')

        handler = LogFileHandler(patterns=[], directory_path=str(tmp_path))

        assert handler.file_positions[str(tmp_path / 'test.log')] == 4

    def test_init_multiple_file_pass(self, tmp_path):
        (tmp_path / 'test.log').write_text('test', encoding='utf-8')
        (tmp_path / 'test2.log').write_text('test2', encoding='utf-8')
        (tmp_path / 'test3.log').write_text('testtest', encoding='utf-8')

        handler = LogFileHandler(patterns=[], directory_path=str(tmp_path))

        assert handler.file_positions[str(tmp_path / 'test.log')] == 4
        assert handler.file_positions[str(tmp_path / 'test2.log')] == 5
        assert handler.file_positions[str(tmp_path / 'test3.log')] == 8
