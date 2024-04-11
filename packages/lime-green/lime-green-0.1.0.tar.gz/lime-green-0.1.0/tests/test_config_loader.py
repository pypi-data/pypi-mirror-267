import os, sys, json, time
from unittest import mock
import pytest

from lime.common.models.config import ConfigLoader

config_usr_fn = './tests/data/stubs/config-toy-1.yaml'
config_workspace_fn = './tests/data/stubs/config-toy-2.yaml'

# @pytest.mark.dev
def test_toy_example_1():
    '''
        a toy config to demonstrate expected behavior:
            - exisiting attributes are overwritten by one config
              file (the usr) being loaded to ConfigLoader.
            - the class names correspond to the top-level keys in config
    '''

    # Demonstrate inheritance
    class Alpha(ConfigLoader):
        item_x = 0
    class Beta(ConfigLoader):
        x = 0
    
    # Dmonstrate only attrs available before
    # ConfigLoader._load() and Child._initialize() 
    # are called, are defined in the class definition
    assert Alpha.item_x == 0
    assert Beta.x == 0
    try:
        Alpha.item_a
        raise Exception("Alpha.item_a should not exist yet")
    except: 
        pass
    
    # load only one config for now
    ConfigLoader._load(config_usr_fn)
    Alpha._initialize()
    Beta._initialize()

    # assert proper things have been added, updated, overwritten, (or not added)
    assert Alpha.item_x == 0    # remained present
    assert Beta.x == 2           # overwrote value
    assert Alpha.item_a['fn'] == 2    # added
    
    try:
        Alpha.item_b
        raise Exception("Alpha.item_b should not exist yet")
    except:
        pass
    
    return
            
def test_toy_example_2():
    '''
        a toy config to demonstrate expected behavior:
            two conflicting config files are loaded
            and the last one loaded overwrites the first
    '''

    # Demonstrate inheritance
    class Alpha(ConfigLoader):
        item_x = 0
    class Beta(ConfigLoader):
        x = 0
    
    # Demonstrate there's not contamination between previous tests
    try:
        Alpha.item_a
        raise Exception("Alpha.item_a should not exist yet")
    except: 
        pass
    
    # load both configs: first: usr, second: workspace
    ConfigLoader._load(config_usr_fn)
    ConfigLoader._load(config_workspace_fn)

    Alpha._initialize()
    Beta._initialize()

    # check if outcome is what we expect
    assert Beta.x == 2                  # overwrote value in usr
    assert Alpha.item_x == 0            # remained present
    assert Alpha.item_a['fn'] == 99     # added by usr, overwritten by workspace
    assert Alpha.item_c['fn'] == 2      # added by usr
    assert Alpha.item_z['fn'] == 99     # added by worksapce
    
    try:
        Alpha.item_b
        raise Exception("Alpha.item_b should not exist yet")
    except:
        pass
    

def test_toy_example_3():
    '''
        a toy config to demonstrate expected behavior:
            two config files are loaded
            _urn is defined to:
                - in Alpha: get the `fn` key
                - in CustomClass: define the data key
    '''

    # Demonstrate inheritance
    class Alpha(ConfigLoader):
        _urn = {
            'value': lambda data, key: data.get(key).get('fn'),
        }
        item_x = 0

    class MyConfigClass(ConfigLoader):
        _urn = {
            'data': lambda config: config.get('Delta'),
        }
        x = 0
    
    # Demonstrate there's not contamination between previous tests
    try:
        Alpha.item_a
        raise Exception("Alpha.item_a should not exist yet")
    except: 
        pass
    
    # load both configs: first: usr, second: workspace
    ConfigLoader._load(config_usr_fn)
    ConfigLoader._load(config_workspace_fn)

    Alpha._initialize()
    MyConfigClass._initialize()

    assert Alpha.item_x == 0            # already existing attr
    assert Alpha.item_a == 99           # check its a value, not a dict
    assert Alpha.item_c == 2            # check if not interfered with
    assert MyConfigClass.x == 0         # already existing attr
    assert MyConfigClass.z == 99        # loaded from config.Delta using _urn for data
    
    try:
        Alpha.item_b
        raise Exception("Alpha.item_b should not exist yet")
    except:
        pass
    
def test_toy_example_4():
    '''
        bug check: when loading an empty section
        that information is not overwritten
    '''
    ConfigLoader._load(config_usr_fn)
    ConfigLoader._load(config_workspace_fn)

    # Demonstrate not overwriting previous loaded values
    class Epsilon(ConfigLoader):
        predefined = 0

    Epsilon._initialize()

    # this is loaded in usr as Epsilon.epsilon
    # but in workspace the key is absent, just
    # the Epsilon tag is present with no sub_attr
    # therefore the value should not be overwritten
    assert Epsilon.epsilon == 2

    # Demonstrate overwriting previous loaded values with null
    class Gamma(ConfigLoader):
        predefined = 0

    # these are already called
    # ConfigLoader._load(config_usr_fn)
    # ConfigLoader._load(config_workspace_fn)

    Gamma._initialize()

    # this is loaded in usr as Gamma.gamma =2
    # but in workspace the Gamma.gamma = null
    # therefore the value should be overwritten
    assert Gamma.gamma == None


def test_toy_example_5():
    '''
        if class is defined but not in any of the
        loaded config files, then it should not be 
        remain only with its defined attributes
    '''

    # these classes dont exist in the config files
    # let's make sure we handle that case as well
    class NewNameOne(ConfigLoader):
        item_x = 0

    class NewNameTwo(ConfigLoader):
        pass

    ConfigLoader._load(config_usr_fn)
    ConfigLoader._load(config_workspace_fn)

    NewNameOne._initialize()
    NewNameTwo._initialize()

    assert NewNameOne.item_x == 0

    assert NewNameTwo._get_attrs() == {}
    






