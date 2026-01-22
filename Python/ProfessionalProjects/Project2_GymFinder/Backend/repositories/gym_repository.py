from typing import Optional, Dict, Any, List
from Backend.db import get_connection


class GymRepository:
    def list_gyms(self, city_filter: str = "") -> List[Dict[str, Any]]:
        city_filter = (city_filter or "").strip()

        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            if city_filter:
                like_pattern = f"%{city_filter}%"
                cur.execute(
                    """
                    SELECT
                        id, gym_name, gym_owner_name,
                        country, district, city, street, street_number,
                        size_m2, has_locker_room, has_boxing, has_sauna, has_pool
                    FROM gyms
                    WHERE LOWER(city) LIKE LOWER(%s)
                    """,
                    (like_pattern,),
                )
            else:
                cur.execute(
                    """
                    SELECT
                        id, gym_name, gym_owner_name,
                        country, district, city, street, street_number,
                        size_m2, has_locker_room, has_boxing, has_sauna, has_pool
                    FROM gyms
                    """
                )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    def create_gym(self, gym_data: Dict[str, Any]) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO gyms (
                    gym_name, gym_owner_name,
                    country, district, city, street, street_number,
                    google_maps_link, description, size_m2,
                    has_locker_room, has_boxing, has_sauna, has_pool,
                    owner_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    gym_data["gym_name"],
                    gym_data["gym_owner_name"],
                    gym_data["country"],
                    gym_data["district"],
                    gym_data["city"],
                    gym_data["street"],
                    gym_data["street_number"],
                    gym_data.get("google_maps_link"),
                    gym_data.get("description"),
                    gym_data.get("size_m2"),
                    gym_data.get("has_locker_room", 0),
                    gym_data.get("has_boxing", 0),
                    gym_data.get("has_sauna", 0),
                    gym_data.get("has_pool", 0),
                    gym_data["owner_id"],
                ),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            cur.close()
            conn.close()

    def get_gym_by_id(self, gym_id: int) -> Optional[Dict[str, Any]]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT
                    id, gym_name, gym_owner_name,
                    country, district, city, street, street_number,
                    google_maps_link, description, size_m2,
                    has_locker_room, has_boxing, has_sauna, has_pool,
                    owner_id
                FROM gyms
                WHERE id = %s
                """,
                (gym_id,),
            )
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()

    def get_owner_id(self, gym_id: int) -> Optional[int]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT owner_id FROM gyms WHERE id = %s", (gym_id,))
            row = cur.fetchone()
            return int(row["owner_id"]) if row and row["owner_id"] is not None else None
        finally:
            cur.close()
            conn.close()

    def delete_gym(self, gym_id: int) -> None:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM gyms WHERE id = %s", (gym_id,))
            conn.commit()
        finally:
            cur.close()
            conn.close()
