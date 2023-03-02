import json
from pathlib import Path

import pytest
from ruamel.yaml import YAML

yaml = YAML()
BASE_DIR = Path(__file__).parent.resolve()


TEST_FILE_VARS = {
    "a": 10,
    "b": 20,
    "c": {
        "d" : 30,
        "e": {
            "f" : 40
        }
    },
    "g": [1, 2, 3, 4, 5],
    "h": "{{a}}",
    "i": "{{g}}",
    "j": ["{{a}}", "{{b}}", "{{e}}", ["{{h}}"]],
    "k": {"l": "{{j}}", "m": [{"ee": '{{e}}'}]}
}


@pytest.fixture()
def config_file():
    
    # setup (create json)
    config_file_path = BASE_DIR / "test.json"
    with config_file_path.open('w') as f:
        json.dump(TEST_FILE_VARS, f)
    yield config_file_path
    
    config_file_path.unlink() # "teardown (delete json)"

@pytest.fixture()
def json_config_file():
    
    # setup (create json)
    config_file_path = BASE_DIR / "config.json"
    with config_file_path.open('w') as f:
        json.dump(TEST_FILE_VARS, f)
    yield config_file_path
    
    config_file_path.unlink() # "teardown (delete json)"

@pytest.fixture()
def yaml_config_file():
    
    # setup (create json)
    config_file_path = BASE_DIR / "config.yaml"
    with config_file_path.open('w') as f:
        yaml.dump(TEST_FILE_VARS, f)
    yield config_file_path
    
    config_file_path.unlink() # "teardown (delete json)"

@pytest.fixture()
def yml_config_file():
    
    # setup (create json)
    config_file_path = BASE_DIR / "config.yml"
    with config_file_path.open('w') as f:
        yaml.dump(TEST_FILE_VARS, f)
    yield config_file_path
    
    config_file_path.unlink() # "teardown (delete json)"

@pytest.fixture()
def invalid_config_file():
    
    # setup (create json)
    config_file_path = BASE_DIR / "config.yml"
    with config_file_path.open('w') as f:
        yaml.dump(TEST_FILE_VARS, f)
        f.write("invalidate this")
    yield config_file_path
    
    config_file_path.unlink() # "teardown (delete json)"

@pytest.fixture()
def unknow_config_file():
    
    # setup (create json)
    config_file_path = BASE_DIR / "config.txt"
    with config_file_path.open('w') as f:
        f.write(json.dumps(TEST_FILE_VARS, indent=4, default=str))
    yield config_file_path
    
    config_file_path.unlink() # "teardown (delete json)"

@pytest.fixture()
def path_to_dir_with_config_file():
    
    # setup (create json)
    config_file_path = BASE_DIR / "config.yaml"
    with config_file_path.open('w') as f:
        f.write(json.dumps(TEST_FILE_VARS, indent=4, default=str))
    yield config_file_path.parent
    
    config_file_path.unlink() # "teardown (delete json)"
