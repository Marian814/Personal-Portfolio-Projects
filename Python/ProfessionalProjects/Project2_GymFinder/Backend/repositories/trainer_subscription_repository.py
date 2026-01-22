from typing import List, Dict, Any, Optional
from Backend.db import get_connection


class TrainerSubscriptionRepository:
    def list_by_trainer(self, trainer_db_id: int) -> List[Dict[str, Any]]:
        conn = get_connection()
        try:
            cur = conn.cursor(dictionary=True)
            cur.execute(
                """
                SELECT id, trainer_id, price, benefits
                FROM trainer_subscriptions
                WHERE trainer_id = %s
                ORDER BY price ASC
                """,
                (trainer_db_id,),
            )
            return cur.fetchall()
        finally:
            cur.close()
            conn.close()

    def add_to_trainer(self, trainer_db_id: int, price: float, benefits: Optional[str]) -> int:
        conn = get_connection()
        try:
            cur = conn.cursor()
            cur.execute(
                """
                INSERT INTO trainer_subscriptions (trainer_id, price, benefits)
                VALUES (%s, %s, %s)
                """,
                (trainer_db_id, price, benefits),
            )
            conn.commit()
            return cur.lastrowid
        finally:
            cur.close()
            conn.close()
