from typing import Optional, Dict, Any
from Backend.db import get_connection


class UserRepository:
    def username_exists(self, username: str) -> bool:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT id FROM users WHERE username = %s", (username,))
            return cur.fetchone() is not None
        finally:
            cur.close()
            conn.close()

    def create_user(self, username: str, email: str, password_hash: str, role: str) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO users (username, email, password, role)
                VALUES (%s, %s, %s, %s)
                """,
                (username, email, password_hash, role),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            cur.close()
            conn.close()

    def get_user_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                "SELECT id, username, email, password, role FROM users WHERE username = %s",
                (username,),
            )
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()

    def get_user_by_id(self, user_id: int) -> Optional[Dict[str, Any]]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT id, username, email, role FROM users WHERE id = %s", (user_id,))
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()

    def get_user_role(self, user_id: int) -> Optional[str]:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("SELECT role FROM users WHERE id = %s", (user_id,))
            row = cur.fetchone()
            return row[0] if row else None
        finally:
            cur.close()
            conn.close()
