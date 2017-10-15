"""
Loads configuration from the config file
"""
import yaml
import global_vars

def Config():
    """
    Configuration object
    """
    with open(global_vars.configfile, 'r') as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg
