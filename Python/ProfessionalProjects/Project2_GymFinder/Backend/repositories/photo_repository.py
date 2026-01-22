from typing import List, Dict, Any
from Backend.db import get_connection


class PhotoRepository:
    def list_gym_photos(self, gym_id: int) -> List[Dict[str, Any]]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT id, gym_id, photo_url
                FROM gym_photos
                WHERE gym_id = %s
                ORDER BY created_at DESC
                """,
                (gym_id,),
            )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    def add_gym_photo(self, gym_id: int, photo_url: str) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO gym_photos (gym_id, photo_url)
                VALUES (%s, %s)
                """,
                (gym_id, photo_url),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            cur.close()
            conn.close()
