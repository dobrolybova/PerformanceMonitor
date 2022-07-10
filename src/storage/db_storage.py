import uuid
from typing import List, Dict, Any

import psycopg2

from .storage import AbcStorage


class DbStorage(AbcStorage):
    def __init__(self):
        self.users_conn = psycopg2.connect(dbname='performancemonitor', user='postgres',
                                           password='example', host="db", port='5432')
        self.users_cursor = self.users_conn.cursor()
        self.sessions_conn = psycopg2.connect(dbname='performancemonitor', user='postgres',
                                              password='example', host="db", port='5432')
        self.sessions_cursor = self.sessions_conn.cursor()
        super().__init__()

    def get_hash(self, user_name: str) -> uuid.UUID:
        user_hash = uuid.uuid4()
        self.users_cursor.execute(f"SELECT user_id FROM users WHERE user_name='{user_name}'")
        rows = self.users_cursor.fetchall()
        row = rows[0]
        self.sessions_cursor.execute(f"INSERT INTO sessions(user_id, user_session) VALUES({row[0]}, '{user_hash}')")
        self.sessions_conn.commit()
        return user_hash

    def delete_all_users(self):
        self.users_cursor.execute(f'DELETE FROM users')
        self.users_conn.commit()

    def delete_all_sessions(self):
        self.sessions_cursor.execute(f'DELETE FROM sessions')
        self.sessions_conn.commit()

    def get_all_users(self):
        self.users_cursor.execute(f'SELECT * FROM users')
        return self.users_cursor.fetchall()

    def add_user(self, user: str, passwd: str) -> None:
        self.users_cursor.execute(
            f"INSERT INTO users(user_name, user_passwd) VALUES ('{user}', '{passwd}')")
        self.users_conn.commit()

    def is_user_exist(self, user_name: str) -> bool:
        self.users_cursor.execute(f"SELECT * FROM users WHERE user_name='{user_name}'")
        if not self.users_cursor.fetchall():
            return False
        return True

    def is_user_valid(self, user_name: str, passwd: str) -> bool:
        self.users_cursor.execute(f"SELECT * FROM users WHERE (user_name='{user_name}' AND user_passwd='{passwd}')")
        if not self.users_cursor.fetchall():
            return False
        return True

    def is_hash_valid(self, other: str) -> bool:
        self.sessions_cursor.execute(f"SELECT * FROM sessions WHERE user_session='{other}'")
        if not self.sessions_cursor.fetchall():
            return False
        return True

    def get_user_data(self, user_hash: str, time_range=None) -> List[Dict[str, float]]:
        self.sessions_cursor.execute(f"SELECT user_cpu, user_timestamp FROM sessions WHERE user_session='{user_hash}'")
        result_list = self.sessions_cursor.fetchall()
        return [{"timestamp": timestamp, "cpu": cpu} for cpu, timestamp in result_list if cpu and timestamp]

    def store_user_data(self, data: Dict[str, Any]) -> None:
        user_hash = data["hash"]
        cpu = data["cpu"]
        timestamp = data["time"]
        self.users_cursor.execute(f"SELECT user_id FROM sessions WHERE user_session='{user_hash}'")
        rows = self.users_cursor.fetchall()
        row = rows[0]
        self.sessions_cursor.execute(f"INSERT INTO sessions(user_id, user_session, user_cpu, user_timestamp) VALUES ('{row[0]}', '{user_hash}', '{cpu}', '{timestamp}')")
        self.sessions_conn.commit()

    def create_user_session(self, user_hash: str) -> None:
        pass



