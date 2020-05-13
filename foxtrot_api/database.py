import sqlite3
from cryptography.fernet import Fernet


class Database:
    def __init__(self, db_path, secret, name='user_agents'):
        self.name = name
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cipher = Fernet(repr(secret))

    def encrypt(self, data):
        return str(self.cipher.encrypt(bytes(data, 'utf-8')))[2:-1]

    def decrypt(self, data):
        return str(self.cipher.decrypt(bytes(data, 'utf-8')))[2:-1]

    def gen_key(self):
        return str(self.cipher.generate_key())[2:-1]

    def create_table(self):
        try:
            self.connection.cursor().execute(
                'CREATE TABLE ' + self.name
                + '(api_token TINYTEXT PRIMARY KEY NOT NULL, \
                    username TINYTEXT NOT NULL UNIQUE, \
                    request_count int NOT NULL DEFAULT(0), \
                    privilege int NOT NULL DEFAULT(0), \
                    check(privilege >= 0 AND privilege < 4));')
            return True
        except sqlite3.OperationalError:
            return False

    def get(self, field, token):
        try:
            return self.connection.cursor().execute('SELECT '
                                                    + str(field)
                                                    + ' FROM '
                                                    + self.name
                                                    + ' WHERE api_token="'
                                                    + str(token)
                                                    + '";').fetchone()[0]
        except sqlite3.OperationalError:
            return None

    def promote(self, requestor_token, username, new_privilege):
        current_privilege = self.get('privilege', requestor_token)
        if((current_privilege >= 2) and (new_privilege <= current_privilege)):
            try:
                self.connection.cursor().execute('UPDATE '
                                                 + self.name
                                                 + ' SET privilege='
                                                 + str(new_privilege)
                                                 + ' WHERE username="'
                                                 + str(username)
                                                 + '";')
                return True
            except sqlite3.OperationalError:
                return False
        else:
            return False

    def add_user_agent(self, username, token=None, privilege=0):
        if(token is None):
            token = self.gen_key()

        encrypted = self.encrypt(token)
        decrypted = self.decrypt(encrypted)

        print("\ttoken: " + str(token) + "\n\tencrpyted: " + str(encrypted) + "\n\tdecrypted: " + str(decrypted))

        if (decrypted != token): raise Exception('bad encrpytion')

        try:
            self.connection.cursor().execute(
                'INSERT INTO '
                + self.name
                + '(api_token, username, request_count, privilege) VALUES ("'
                + self.encrypt(token)
                + '", "'
                + str(username)
                + '", 0, '
                + str(privilege)
                + ');')
            self.commit()
            return token
        except sqlite3.OperationalError:
            return None

    def get_user_by_token(self, token):
        try:
            return self.connection.cursor().execute('SELECT * FROM '
                                                    + self.name
                                                    + ' WHERE api_token="'
                                                    + self.encrypt(token)
                                                    + '";').fetchone()
        except sqlite3.OperationalError:
            return None

    def get_user_by_name(self, username):
        try:
            return self.connection.cursor().execute('SELECT * FROM '
                                                    + self.name
                                                    + ' WHERE username="'
                                                    + str(username)
                                                    + '";').fetchone()
        except sqlite3.OperationalError:
            return None

    def get_all_user_agents(self):
        try:
            return self.connection.cursor().execute('SELECT * FROM '
                                                    + self.name
                                                    + ';').fetchall()
        except sqlite3.OperationalError:
            return []

    def increment_request_count(self, token):
        try:
            self.connection.cursor().execute(
                'UPDATE '
                + self.name
                + ' SET request_count='
                + str(self.get('request_count', token))
                + '+1 WHERE api_token="'
                + str(token)
                + '";').fetchall()
            self.commit()
            return True
        except sqlite3.OperationalError:
            return False

    def reset_request_count(self, token):
        try:
            self.connection.cursor().execute(
                'UPDATE '
                + self.name
                + ' SET request_count=0 WHERE api_token="'
                + str(token)
                + '";').fetchall()
            self.commit()
            return True
        except sqlite3.OperationalError:
            return False

    def commit(self):
        return self.connection.commit()

    def close(self):
        self.commit()
        self.connection.close()
