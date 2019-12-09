import configparser


def trimmed(string: str) -> str:
    return string[1:-1]


class Config:

    def __init__(self):
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read("./config.ini")

    def get_database_host(self):
        return self.get('Database', 'host')

    def get_database_user(self):
        return self.get('Database', 'user')

    def get_database_password(self):
        return self.get('Database', 'password')

    def get_database_name(self):
        return self.get('Database', 'database')

    def get_server_host(self):
        return self.get('Server', 'host')

    def get_server_debug(self):
        return self.config_parser.getboolean('Server', 'debug')

    def get(self, section: str, index: str):
        return self.config_parser[section][index]


config = Config()
