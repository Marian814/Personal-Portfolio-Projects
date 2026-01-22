from typing import List, Dict, Any, Optional
from Backend.db import get_connection


class TrainerRepository:
    def list_trainers(self, city_filter: str = "") -> List[Dict[str, Any]]:
        city_filter = (city_filter or "").strip()

        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            if city_filter:
                like_pattern = f"%{city_filter}%"
                cur.execute(
                    """
                    SELECT
                        id, personal_trainer_name,
                        country, district, city,
                        experience_years, description, trainer_id
                    FROM trainers
                    WHERE LOWER(city) LIKE LOWER(%s)
                    """,
                    (like_pattern,),
                )
            else:
                cur.execute(
                    """
                    SELECT
                        id, personal_trainer_name,
                        country, district, city,
                        experience_years, description, trainer_id
                    FROM trainers
                    """
                )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    def create_trainer(self, data: Dict[str, Any]) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO trainers (
                    personal_trainer_name,
                    country, district, city,
                    experience_years, description,
                    trainer_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    data["personal_trainer_name"],
                    data["country"],
                    data["district"],
                    data["city"],
                    data["experience_years"],
                    data.get("description"),
                    data["trainer_id"],
                ),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            cur.close()
            conn.close()

    def get_trainer_by_db_id(self, trainer_db_id: int) -> Optional[Dict[str, Any]]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT id,
                       personal_trainer_name,
                       country, district, city,
                       experience_years,
                       description,
                       trainer_id
                FROM trainers
                WHERE id = %s
                """,
                (trainer_db_id,),
            )
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()

    def get_owner_user_id(self, trainer_db_id: int) -> Optional[int]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT trainer_id FROM trainers WHERE id = %s", (trainer_db_id,))
            row = cur.fetchone()
            return int(row["trainer_id"]) if row else None
        finally:
            cur.close()
            conn.close()

    def delete_trainer(self, trainer_db_id: int) -> None:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM trainers WHERE id = %s", (trainer_db_id,))
            conn.commit()
        finally:
            cur.close()
            conn.close()
