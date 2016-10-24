
from unittest import TestCase
import tempfile

from syfh_params import Config

class TestConfig(TestCase):


    def setUp(self):
        self.config = Config()
        self.test_filename = tempfile.NamedTemporaryFile(mode='w')


    def test_load_params_empty_filename(self):
        self.assertEqual(self.config.load_params(), {})

    def test_save_params_empty_filename(self):
        self.config.save_params()

    def test_save_params_empty_config_overwrite_file(self):
        self.config.save_params(self.test_filename.name)

    def test_save_params_empty_config(self):
        self.test_filename.close()      # this also deletes it.
        self.config.save_params(self.test_filename.name)

    def test_save_params_test_config(self):
        testconfig= {
            'username': 'qwerqqq',
            'password': 'woeifjjoiasdf',
            'dont_save': ['password'],
            'website': 'http://asdflklkjasdf'}
        self.config.config = testconfig
        self.config.save_params(self.test_filename.name)
        loaded = self.config.load_params(self.test_filename.name)
        #print(loaded)
        self.assertEqual(loaded, testconfig)
