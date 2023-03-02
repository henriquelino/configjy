from pathlib import Path

import pytest
from ruamel.yaml import scanner
from src.configjy import ConfigFile, UnsupportedExtension
from .fixtures import *



class TestVars:
    
    def test_reload(self, config_file: Path):
        fvar = ConfigFile(config_file).reload()
        assert isinstance(fvar, ConfigFile)
        
    def test_print(self, config_file: Path):
        fvar = ConfigFile(config_file).reload()
        assert "Configurações carregadas do arquivo" in str(fvar)
        
    def test_var(self, config_file: Path):
        fvar = ConfigFile(config_file)
        assert fvar.get("a") == 10
    
    def test_var_not_exists_default(self, config_file: Path):
        fvar = ConfigFile(config_file)
        assert fvar.get("this_does_not_exists", 10) == 10
        
    def test_var_not_exists_none(self, config_file: Path):
        fvar = ConfigFile(config_file)
        assert fvar.get("this_does_not_exists") is None
        
    def test_var_not_exists_none_no_print(self, config_file: Path):
        fvar = ConfigFile(config_file)
        assert fvar.get("this_does_not_exists", print_when_not_exists=False) is None
        
    def test_var_not_exists_raise(self, config_file: Path):
        fvar = ConfigFile(config_file)
        with pytest.raises(KeyError):
            fvar.get("this_does_not_exists", raise_when_not_exists=True)
        
    def test_print_when_creating(self, config_file: Path):
        fvar = ConfigFile(config_file, print_when_create=False)
        assert fvar.get("b") == 20
    
    def test_multi_level(self, config_file:Path):
        fvar = ConfigFile(config_file)
        assert fvar.get("c.d") == 30
        
    def test_self_int_reference(self, config_file:Path):
        fvar = ConfigFile(config_file)
        assert fvar.get("h") == str(fvar.get("a"))
        
    def test_self_list_reference(self, config_file:Path):
        fvar = ConfigFile(config_file)
        assert [int(val) for val in fvar.get("i").replace('[', '').replace(']', '').split(',')] == fvar.get("g")
        
class TestPaths:
        
    def test_invalid_path(self):
        with pytest.raises(FileNotFoundError):
            ConfigFile("")
            
    def test_invalid_config(self, invalid_config_file: Path):
        with pytest.raises(scanner.ScannerError):
            ConfigFile(invalid_config_file)
            
    def test_unknow_extension(self, unknow_config_file: Path):
        with pytest.raises(UnsupportedExtension):
            ConfigFile(unknow_config_file)
            
    def test_path_to_config_dir(self, path_to_dir_with_config_file: Path):
        fvar = ConfigFile(path_to_dir_with_config_file)
        assert fvar.get("a") == 10
        
    def test_json(self, json_config_file: Path):
        fvar = ConfigFile(json_config_file)
        assert fvar.get("a") == 10
    
    def test_yaml(self, yaml_config_file: Path):
        fvar = ConfigFile(yaml_config_file)
        assert fvar.get("b") == 20
    
    def test_yml(self, yml_config_file:Path):
        fvar = ConfigFile(yml_config_file)
        assert fvar.get("c.d") == 30
