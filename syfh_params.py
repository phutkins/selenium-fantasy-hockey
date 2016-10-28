import yaml

PARAM_NAMES = (
    # Name,  Description,  Saved?
    ('chromedriver_path', 'Selenium Chrome Driver installation location'),
    ('team_website', 'Yahoo fantasy hockey team website'),
    ('days_to_start_active_payers', 'Days to start active players')
    # ('username', 'Yahoo username',),
    # ('password', 'Yahoo password', False),
)

class Config():
    DEFAULT_FILENAME = 'syfh_config.ini'

    # members
    yaml_filename = DEFAULT_FILENAME
    config_default = {
        'dont_save': []
    }

    def __init__(self, yaml_filename=None):
        if yaml_filename is None:
            yaml_filename = self.DEFAULT_FILENAME
        self.yaml_filename = yaml_filename
        self.config = self.config_default
        self.load_params(self.yaml_filename)

    def load_params(self, yaml_filename=None):
        '''
        Loads parameters from yaml_filename into the configuration.
        Can be called more than once.
        Any parameter conflicts will prefer the new parameter over the pre-existing.
        '''
        yaml_dict = {}
        if yaml_filename is None:
            yaml_filename = self.yaml_filename
        try:
            yaml_dict = yaml.load(open(yaml_filename, 'r'))
            if yaml_dict is None:
                yaml_dict = {}
        except yaml.YAMLError as exc:
            print("Error in configuration file:", exc)
        except:
            # any problems.. just don't load the yaml
            pass
        self.config.update(yaml_dict)
        return yaml_dict

    def save_params(self, yaml_filename=None):
        if yaml_filename is None:
            yaml_filename = self.yaml_filename
        trimmed = self.config
        try:
            dont_save_these = self.config['dont_save']
            del trimmed['dont_save']
        except KeyError:
            dont_save_these = []
        for trim_this in dont_save_these:
            try:
                del trimmed[trim_this]
            except:
                pass
        try:
            yaml.dump(trimmed, open(yaml_filename, 'w'), default_flow_style=False)
        except yaml.YAMLError as exc:
            print("Error in configuration file:", exc)
        except FileNotFoundError as exc:
            print('Unable to save configuration file:', exc)

        return yaml.dump(self.config)

    def confirm_params(self):
        self.load_params(self.yaml_filename)

        def confirm_last_used(var, prompt, saved=True):
            try:
                last_used_var = self.config[var]
            except KeyError:
                self.config[var] = input(
                    "What is your {}? {} ".format(prompt, "(this will be saved)" if saved is True else ""))
            else:
                self.config[var] = input("What is your {}?  (press <Enter> for: [{}])".format(prompt, last_used_var))
                if self.config[var] is '':
                    self.config[var] = last_used_var
            if saved is False:
                try:
                    self.config['dont_save'].append(var)
                except KeyError:
                    self.config['dont_save'] = [var]

        for args in PARAM_NAMES:
            confirm_last_used(*args)
        return self.config
