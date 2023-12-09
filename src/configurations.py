from threading import Lock, Thread
from pathlib import Path
from typing import Optional, Union
import os
import logging
from src.utils import dict_merge
import logging

LOGGER = logging.getLogger(__name__)


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    Straight from https://refactoring.guru/design-patterns/singleton/python/example#example-1
    """

    _instances = {}

    _lock: Lock = Lock()
    """
    We now have a lock object that will be used to synchronize threads during
    first access to the Singleton.
    """

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        # Now, imagine that the program has just been launched. Since there's no
        # Singleton instance yet, multiple threads can simultaneously pass the
        # previous conditional and reach this point almost at the same time. The
        # first of them will acquire lock and will proceed further, while the
        # rest will wait here.
        with cls._lock:
            # The first thread to acquire the lock, reaches this conditional,
            # goes inside and creates the Singleton instance. Once it leaves the
            # lock block, a thread that might have been waiting for the lock
            # release may then enter this section. But since the Singleton field
            # is already initialized, the thread won't create a new object.
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class Configs(metaclass=SingletonMeta):
    _dict = {}
    """
    We'll use this property to prove that our Singleton really works.
    """

    def __init__(self, arg_folder_path: Optional[Union[str, Path]] = None) -> None:
        self._dict.update(os.environ)
        logging.info(f"loading *.yaml in configs folder")

        folder_path: Union[str, Path, None] = self._dict.get("AUTOMATION_CONFIG_FOLDER_PATH")
        if not folder_path:
            logging.info("Did not find config folder path with env variable AUTOMATION_CONFIG_FOLDER_PATH")
            folder_path = arg_folder_path
        if not folder_path:
            logging.info("Did not find config folder path passed in as argument")

            logging.info("Defaulting to configs/ folder relative to configs.py")
            folder_path = Path(__file__).parent.parent / "configs"

        if folder_path:
            import yaml
            for yaml_file in Path(folder_path).glob("*.yaml"):
                with open(yaml_file, "r") as f:
                    self._dict.update(yaml.safe_load(f.read()))

    def __getitem__(self, key: str) -> str:
        """Allow usage of Configs object with square-bracket notation. 

        Example:

        ```python
        configs = Configs()
        redis_host = configs["redis_host"]
        ```

        Parameters
        ----------
        key : str 
            the config key name

        Returns
        -------
        str
            the config value
        """
        return self._dict[key]
    
    def __contains__(self, key: str) -> bool:
        """All

        Parameters
        ----------
        key : str
            the config key name

        Returns
        -------
        bool
            whether config exists in settings
        """
        return key in self._dict
    
    def __str__(self) -> str:
        return str(self._dict)
    
    def get(self, key: str, default: str = None) -> str:
        return self._dict.get(key, default)
    

    @staticmethod
    def get_postgres_url(
        username: str = None, 
        password: str = None, 
        host: str = None, 
        port: str | int = None, 
        db: str = None
    ) -> str:
        
        return f'postgresql+psycopg://{username}:{password}@{host}:{port}/{db}'
    
def make_postgres_url(
    username: str = None,
    password: str = None,
    host: str = None,
    port: str | int = None,
    dbname: str = None,
) -> str:
    app_configs = Configs()

    if not username:
        username = app_configs["postgres"]["username"]
    if not password:
        password = app_configs["postgres"]["password"]
    if not host:
        host = app_configs["postgres"]["host"]
    if not port:
        port = app_configs["postgres"]["port"]
    if not dbname:
        dbname = app_configs["postgres"]["dbname"]

    url = app_configs.get_postgres_url(
        username, password, host, port, dbname
    )

    LOGGER.debug(f"make_postgres_url made url: {url}")
    
    return url

def make_sqlite_url(name: str = "internetwithviet") -> str:
    return f"sqlite:///{name}.db"