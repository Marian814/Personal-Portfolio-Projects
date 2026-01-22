from typing import List, Dict, Any, Optional
from Backend.db import get_connection


class NutritionistRepository:
    def list_nutritionists(self, city_filter: str = "") -> List[Dict[str, Any]]:
        city_filter = (city_filter or "").strip()

        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            if city_filter:
                like_pattern = f"%{city_filter}%"
                cur.execute(
                    """
                    SELECT
                        id, nutritionist_name,
                        country, district, city,
                        experience_years, description, nutritionist_id
                    FROM nutritionists
                    WHERE LOWER(city) LIKE LOWER(%s)
                    """,
                    (like_pattern,),
                )
            else:
                cur.execute(
                    """
                    SELECT
                        id, nutritionist_name,
                        country, district, city,
                        experience_years, description, nutritionist_id
                    FROM nutritionists
                    """
                )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    def create_nutritionist(self, data: Dict[str, Any]) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO nutritionists (
                    nutritionist_name,
                    country, district, city,
                    experience_years, description,
                    nutritionist_id
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    data["nutritionist_name"],
                    data["country"],
                    data["district"],
                    data["city"],
                    data["experience_years"],
                    data.get("description"),
                    data["nutritionist_id"],
                ),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            cur.close()
            conn.close()

    def get_nutritionist_by_db_id(self, nutr_db_id: int) -> Optional[Dict[str, Any]]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT id,
                       nutritionist_name,
                       country, district, city,
                       experience_years,
                       description,
                       nutritionist_id
                FROM nutritionists
                WHERE id = %s
                """,
                (nutr_db_id,),
            )
            return cur.fetchone()
        finally:
            cur.close()
            conn.close()

    def get_owner_user_id(self, nutr_db_id: int) -> Optional[int]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute("SELECT nutritionist_id FROM nutritionists WHERE id = %s", (nutr_db_id,))
            row = cur.fetchone()
            return int(row["nutritionist_id"]) if row else None
        finally:
            cur.close()
            conn.close()

    def delete_nutritionist(self, nutr_db_id: int) -> None:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute("DELETE FROM nutritionists WHERE id = %s", (nutr_db_id,))
            conn.commit()
        finally:
            cur.close()
            conn.close()
