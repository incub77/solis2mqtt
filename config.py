import yaml


class DefaultDict(dict):
    def __init__(self, arg_dict, defaults_dict):
        super().__init__(arg_dict)
        self.defaults_dict = defaults_dict

        for key, value in self.items():
            if type(value) is dict:
                self[key] = DefaultDict(value, self.defaults_dict[key])

    def get(self, key):
        return super().get(key) if super().get(key) is not None else self.defaults_dict.get(key)

    def __getitem__(self, key):
        return super().__getitem__(key) if key in self \
                                           and super().__getitem__(key) is not None else self.defaults_dict[key]


class Config(DefaultDict):
    def __init__(self, cfg_file, defaults_cfg_file='defaults_config.yaml'):
        with open(cfg_file) as yaml_cfg_file:
            with open(defaults_cfg_file) as yaml_defaults_cfg_file:
                super().__init__(yaml.load(yaml_cfg_file, yaml.Loader), yaml.load(yaml_defaults_cfg_file, yaml.Loader))
