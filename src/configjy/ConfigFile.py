import json
import logging
from pathlib import Path
from traceback import format_exc
from typing import Union

from ruamel.yaml import YAML

logger = logging.getLogger(__name__)
yaml = YAML()
yaml.indent(mapping=4, sequence=4, offset=2)  # https://stackoverflow.com/questions/44388701/how-get-the-sequences-properly-indented-with-ruamel-yaml

DEFAULT_CONFIG_FILE_NAME = "config"


class UnsupportedExtension(Exception):
    ...


class ConfigFile:

    def __dict_replace_value(self, d, old, new):
        new = str(new)
        x = {}
        for k, v in d.items():
            if isinstance(v, dict):
                v = self.__dict_replace_value(v, old, new)
            elif isinstance(v, list):
                v = self.__list_replace_value(v, old, new)
            elif isinstance(v, str):
                v = v.replace(old, new)
            x[k] = v
        return x

    def __list_replace_value(self, l, old, new):  # noqa: E741
        new = str(new)
        x = []
        for e in l:
            if isinstance(e, list):
                e = self.__list_replace_value(e, old, new)
            elif isinstance(e, dict):
                e = self.__dict_replace_value(e, old, new)
            elif isinstance(e, str):
                e = e.replace(old, new)
            x.append(e)
        return x

    def __replace(self, s, old, new):
        new = str(new)
        if isinstance(s, str):
            return s.replace(old, new)
        elif isinstance(s, list):
            return self.__list_replace_value(s, old, new)
        elif isinstance(s, dict):
            return self.__dict_replace_value(s, old, new)

    def __load(self, value, from_where: dict):
        value_before = value

        from_where = from_where.copy()
        for f_key, f_value in from_where.items():
            # if not isinstance(g_value, str): continue
            if isinstance(f_value, dict):
                value = self.__load(value, f_value)
            else:
                value = self.__replace(value, f"{{{{{f_key}}}}}", f_value)  # a var {{APP_PATH}} teria o valor da var APP_PATH

        # if the value after replacing is None, then fallback to old value
        if value is None:
            value = value_before

        return value

    def __find_config_file(self) -> Path:
        """Verifica se existe algum arquivo YAML, YML ou JSON no caminho do script/exec"""
        files = set()
        for ext in self.extensions:
            possible_config_file = self.path / f"{self.name}{ext}"
            files.add(possible_config_file)
            if possible_config_file.exists():
                # if the file exists, return it as a possible file to be loaded
                logger.debug(f"{possible_config_file = }")
                return possible_config_file

        msg = "Atenção!!\n\n{}\n\nNão existem! Crie algum desses arquivos na pasta:\n'{}'!".format('\n'.join(str(file) for file in files), str(self.path))
        logger.critical(msg)
        raise FileNotFoundError(msg)

    def __load_config_file(self, config_file: Path) -> dict:
        """Loads the config dict to the loaded_vars variable

        ---
        ### Entradas:
            * ``config_file`` (Path) : Path to a file to be read, the file should be an .json or .yaml format
        ---
        ### Saídas:
            * ``None``
        """

        logger.debug(f"Abrindo o arquivo de configuração: '{config_file}'.")

        extension = config_file.suffix
        if extension in [".yaml", ".yml"]:
            load_method = yaml.load
        elif extension in [".json"]:
            load_method = json.load
        else:
            raise UnsupportedExtension("Unknow extension: '{}'".format(extension))

        with open(config_file, encoding='utf-8') as file:
            try:
                config: dict = load_method(file) or dict()
            except Exception:
                msg = f"Erro carregando arquivo '{config_file}':\n{format_exc()}\n"
                logger.warning(msg)
                raise

        return config

    def __load_config_vars(self, config: dict) -> None:
        """Loads the config dict to the loaded_vars variable

        ---
        ### Entradas:
            * ``config`` (dict) : dict from file to be loaded into class variables
        ---
        ### Saídas:
            * ``None``
        """

        for key, value in config.items():
            value = self.__load(value, globals())
            value = self.__load(value, self.__dict__)

            self.loaded_vars[key] = value

            if self.print_when_create:
                logger.critical(f"\n{'-'*60}\nVariavel criada:\nNome: '{key}'\nValor: '{json.dumps(value, indent = 4, default = str)}'\nTipo: '{type(value)}'\n{'-'*60}\n")
        return

    def __init__(self, path: Union[str, Path], *, name="config", extensions=(".yaml", ".yml", ".json"), print_when_create=True):
        """Loads file content into a class
        If path to a file is given, uses the path, else searchs for name + extensions\n
        #### Usage:\n
        ---
        ```
        \n\n
        config_file = Path(__file__).parent.resolve()
        fvar = ConfigFile(config_file) # searchs for a config.(yaml, yml, json) in script dir
        key = fvar.get("key", "default value if not exists")
        multilevel = fvar.get("first_key.inside_first", "default value if not exists") # same as ["first_key"]["inside_first"]
        ```
        """
        if not isinstance(path, Path):
            path = Path(path).resolve()
        self.path = path
        self.name = name
        self.extensions = extensions

        self.print_when_create = print_when_create

        self.loaded_vars = dict()

        if self.path.is_file():
            self.config_file_path = self.path
        else:
            self.config_file_path = self.__find_config_file()
        
        self.reload()
        return

    def reload(self):
        """Reloads file, useful for long-running scripts if you want to change the file mid-run"""
        self.__config = self.__load_config_file(self.config_file_path)
        self.__load_config_vars(self.__config)
        return self

    def get(self, attr: str, default=None, *, print_when_not_exists=True, raise_when_not_exists=False):
        """ Returns the value of loaded key from config file.
        Possible to use multi-level, eg:
        ```
        get("var_a.var_b") == dict["var_a"]["var_b"]
        ```

        """

        value = self.loaded_vars.copy()
        for atr in attr.split('.'):
            try:
                value = value[atr]
            except KeyError:

                if raise_when_not_exists:
                    raise KeyError(f"Key '{attr}' does not exists!")
                if print_when_not_exists:
                    logger.warning(f"\n{'-'*80}\n\tKey '{attr}' does not exists! Returning default value: '{default}'\n{'-'*80}")
                return default
        return value

    def __str__(self):
        return f"Configurações carregadas do arquivo: '{self.config_file_path}'\n'{json.dumps(self.loaded_vars, indent=4, default=str)}'"
