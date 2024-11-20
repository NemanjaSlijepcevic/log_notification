import os
from LogFileHandler import LogFileHandler


class TestLogFileHandlerInitPos:

    def test_init_single_file_pass(self, mocker):
        with open('test.log', 'w') as file:
            file.write('test')

        handler = LogFileHandler(patterns=[], directory_path='.')

        assert handler.file_positions['./test.log'] == 4
        os.remove("test.log")

    def test_init_multiple_file_pass(self, mocker):
        with open('test.log', 'w') as file:
            file.write('test')

        with open('test2.log', 'w') as file:
            file.write('test2')

        with open('test3.log', 'w') as file:
            file.write('testtest')

        handler = LogFileHandler(patterns=[], directory_path='.')

        assert handler.file_positions['./test.log'] == 4
        assert handler.file_positions['./test2.log'] == 5
        assert handler.file_positions['./test3.log'] == 8
        os.remove("test.log")
        os.remove("test2.log")
        os.remove("test3.log")
