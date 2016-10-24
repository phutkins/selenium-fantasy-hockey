import yaml

PARAM_NAMES = (
    # Name,  Description,  Saved?
    ('website', 'Yahoo fantasy hockey team website'),
    ('username', 'Yahoo username',),
    ('password', 'Yahoo password', False),
)


class Config():
    DEFAULT_FILENAME = ''

    # members
    yaml_filename = DEFAULT_FILENAME
    config = {}

    def __init__(self, yaml_filename=None):
        if yaml_filename is None:
            yaml_filename = self.DEFAULT_FILENAME
        self.yaml_filename = yaml_filename

    def load_params(self, yaml_filename=None):
        if yaml_filename is None:
            yaml_filename = self.yaml_filename
        try:
            self.config = yaml.load(open(yaml_filename, 'r'))
        except yaml.YAMLError as exc:
            print("Error in configuration file:", exc)
        except:
            # any problems.. just don't load the yaml
            pass
        return self.config

    def save_params(self, yaml_filename=None):
        if yaml_filename is None:
            yaml_filename = self.yaml_filename
        try:
            yaml.dump(self.config, open(yaml_filename, 'w'))
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


