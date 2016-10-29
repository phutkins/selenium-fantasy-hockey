import yaml

PARAM_DESCRIPTIONS = (
    # Name,  Description,  Saved?
    ('chromedriver_path', 'Selenium Chrome Driver installation location'),
    ('team_website', 'Yahoo fantasy hockey team website'),
    ('days_to_start_active_payers', 'Days to start active players')
    # ('username', 'Yahoo username',),
    # ('password', 'Yahoo password', False),
)
DEFAULT_FILENAME = 'syfh_config.ini'


class Config():
    # members
    param_descs = PARAM_DESCRIPTIONS
    yaml_filename = DEFAULT_FILENAME
    config_default = {
        'dont_save': []
    }

    def __init__(self, yaml_filename=None):
        if yaml_filename is not None:
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

    def _get_param_desc(self, param):
        """ return the parameter description tuple for a parameter.
        Only returns first instance of tuple, or None"""
        return next((x for x in self.param_descs if x[0] is param), None)

    def validate_param(self, param):
        """ Raises an error if unknown parameter """
        param_desc = self._get_param_desc(param)
        if param_desc is None:
            raise ValueError("Unknown parameter : {}".format(param))

    def confirm_param(self,  var, prompt, saved=True):
        # double check it is a known parameter in the parameter description list
        self.validate_param(var)
        try:
            last_used_var = self.config[var]
        except KeyError:
            self.config[var] = input(
                "What is your {}? {} ".format(prompt, "(this will not be saved)" if saved is False else ""))
        else:
            self.config[var] = input("What is your {}?  (press <Enter> for: [{}])".format(prompt, last_used_var))
            if self.config[var] is '':
                self.config[var] = last_used_var
        if saved is False:
            try:
                self.config['dont_save'].append(var)
            except KeyError:
                self.config['dont_save'] = [var]

    def confirm_all_params(self):
        for param_desc in self.param_descs:
            self.confirm_param(*param_desc)
        return self.config
