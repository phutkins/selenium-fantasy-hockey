
from unittest import TestCase
import tempfile
import os

from syfh_params import Config

class TestConfig(TestCase):


    def setUp(self):
        self.param_file = tempfile.NamedTemporaryFile(mode='w', delete=False)
        self.config = Config(self.param_file.name)

    def tearDown(self):
        self.param_file.close()
        os.remove(self.param_file.name)

    def test_load_params_from_empty_file(self):
        ''' loading params from an empty file should return an empty dictionary '''
        self.assertEqual(self.config.load_params(), {})

    def test_save_params_empty_config_default_file(self):
        self.config.save_params()

    def test_save_params_empty_config_specified_file(self):
        self.config.save_params(self.param_file.name)

    def test_save_params_empty_config(self):
        self.param_file.close()
        os.remove(self.param_file.name)
        self.config.save_params(self.param_file.name)

    def test_save_params_test_config(self):
        test_params= {
            'testkey1': 'qwerqqq',
            'testkey2': 'woeifjjoiasdf',
            'dont_save': ['testkey2'],
            'website': 'http://asdflklkjasdf'}
        self.config.config = test_params
        self.config.save_params(self.param_file.name)
        loaded = self.config.load_params(self.param_file.name)
        self.assertEqual(loaded, test_params)

    def test_load_save_params_multiple_times(self):
        test_params = {
            'username': 'qwerqqq',
            'password': 'woeifjjoiasdf',
            'dont_save': ['password'],
            'website': 'http://asdflklkjasdf'}
        self.config.config = test_params
        self.config.save_params(self.param_file.name)
        loaded = self.config.load_params(self.param_file.name)
        self.assertEqual(loaded, test_params)
        loaded_again = self.config.load_params(self.param_file.name)
        self.assertEqual(loaded_again, test_params)
