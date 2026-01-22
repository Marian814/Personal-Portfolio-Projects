from typing import List, Dict, Any, Optional
from Backend.db import get_connection


class NutritionistSubscriptionRepository:
    def list_by_nutritionist(self, nutr_db_id: int) -> List[Dict[str, Any]]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT id, nutritionist_id, price, benefits
                FROM nutritionist_subscriptions
                WHERE nutritionist_id = %s
                ORDER BY price ASC
                """,
                (nutr_db_id,),
            )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    def add_to_nutritionist(self, nutr_db_id: int, price: float, benefits: Optional[str]) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO nutritionist_subscriptions (nutritionist_id, price, benefits)
                VALUES (%s, %s, %s)
                """,
                (nutr_db_id, price, benefits),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            cur.close()
            conn.close()
