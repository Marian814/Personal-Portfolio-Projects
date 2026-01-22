from typing import List, Dict, Any, Optional
from Backend.db import get_connection


class GymSubscriptionRepository:
    def list_by_gym(self, gym_id: int) -> List[Dict[str, Any]]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT id, gym_id, price, benefits
                FROM gym_subscriptions
                WHERE gym_id = %s
                ORDER BY price ASC
                """,
                (gym_id,),
            )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    def add_to_gym(self, gym_id: int, price: float, benefits: Optional[str]) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO gym_subscriptions (gym_id, price, benefits)
                VALUES (%s, %s, %s)
                """,
                (gym_id, price, benefits),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            cur.close()
            conn.close()
