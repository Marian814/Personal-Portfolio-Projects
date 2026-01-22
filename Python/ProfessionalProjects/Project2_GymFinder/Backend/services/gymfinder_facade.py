from typing import Any, Dict, Optional, List
from werkzeug.security import generate_password_hash, check_password_hash

from Backend.repositories.user_repository import UserRepository
from Backend.repositories.gym_repository import GymRepository
from Backend.repositories.photo_repository import PhotoRepository
from Backend.repositories.gym_subscription_repository import GymSubscriptionRepository
from Backend.repositories.trainer_repository import TrainerRepository
from Backend.repositories.trainer_subscription_repository import TrainerSubscriptionRepository
from Backend.repositories.nutritionist_repository import NutritionistRepository
from Backend.repositories.nutritionist_subscription_repository import NutritionistSubscriptionRepository


class GymFinderFacade:
    def __init__(self) -> None:
        self.users = UserRepository()
        self.gyms = GymRepository()
        self.photos = PhotoRepository()
        self.gym_subs = GymSubscriptionRepository()
        self.trainers = TrainerRepository()
        self.trainer_subs = TrainerSubscriptionRepository()
        self.nutritionists = NutritionistRepository()
        self.nutritionist_subs = NutritionistSubscriptionRepository()

    def register_user(self, username: str, email: str, password: str, role: str) -> int:
        allowed = {"member", "gym_owner", "personal_trainer", "nutrition_coach"}
        if role not in allowed:
            raise ValueError("Rol invalid")
        if not username or not email or not password:
            raise ValueError("Toate câmpurile sunt obligatorii")
        if self.users.username_exists(username):
            raise ValueError("Username deja folosit")
        password_hash = generate_password_hash(password)
        return self.users.create_user(username, email, password_hash, role)

    def login_user(self, username: str, password: str) -> Dict[str, Any]:
        if not username or not password:
            raise ValueError("Username și parolă obligatorii")
        user = self.users.get_user_by_username(username)
        if not user or not check_password_hash(user["password"], password):
            raise PermissionError("Credențiale invalide")
        return {"id": user["id"], "username": user["username"], "role": user["role"]}

    def list_gyms(self, city: str = "") -> List[Dict[str, Any]]:
        return self.gyms.list_gyms(city_filter=city)

    def add_gym(self, data: Dict[str, Any]) -> int:
        required = ["gym_name", "gym_owner_name", "country", "district", "city", "street", "street_number", "owner_id"]
        if not all(data.get(k) for k in required):
            raise ValueError("Câmpuri obligatorii lipsă.")
        owner_id = int(data["owner_id"])
        role = self.users.get_user_role(owner_id)
        if role != "gym_owner":
            raise ValueError("Owner invalid")
        gym_data = {
            "gym_name": data["gym_name"],
            "gym_owner_name": data["gym_owner_name"],
            "country": data["country"],
            "district": data["district"],
            "city": data["city"],
            "street": data["street"],
            "street_number": data["street_number"],
            "google_maps_link": data.get("google_maps_link"),
            "description": data.get("description"),
            "size_m2": data.get("size_m2"),
            "has_locker_room": 1 if data.get("has_locker_room") else 0,
            "has_boxing": 1 if data.get("has_boxing") else 0,
            "has_sauna": 1 if data.get("has_sauna") else 0,
            "has_pool": 1 if data.get("has_pool") else 0,
            "owner_id": owner_id,
        }
        return self.gyms.create_gym(gym_data)

    def get_gym_details(self, gym_id: int) -> Dict[str, Any]:
        gym = self.gyms.get_gym_by_id(gym_id)
        if not gym:
            raise LookupError("Gym not found")
        return gym

    def delete_gym(self, gym_id: int, user_id: int) -> None:
        owner_id = self.gyms.get_owner_id(gym_id)
        if owner_id is None:
            raise LookupError("Gym not found")
        if int(owner_id) != int(user_id):
            raise PermissionError("Not allowed. You are not the owner of this gym.")
        self.gyms.delete_gym(gym_id)

    def list_gym_photos(self, gym_id: int) -> List[Dict[str, Any]]:
        return self.photos.list_gym_photos(gym_id)

    def add_gym_photo(self, gym_id: int, user_id: int, photo_url: str) -> int:
        if not photo_url or user_id is None:
            raise ValueError("photo_url and user_id are required")
        owner_id = self.gyms.get_owner_id(gym_id)
        if owner_id is None:
            raise LookupError("Gym not found")
        if int(owner_id) != int(user_id):
            raise PermissionError("Not allowed. You are not the owner of this gym.")
        return self.photos.add_gym_photo(gym_id, photo_url)

    def list_gym_subscriptions(self, gym_id: int) -> List[Dict[str, Any]]:
        return self.gym_subs.list_by_gym(gym_id)

    def add_gym_subscription(self, gym_id: int, user_id: int, price: Any, benefits: Optional[str]) -> int:
        if price is None or user_id is None:
            raise ValueError("price și user_id sunt obligatorii")
        owner_id = self.gyms.get_owner_id(gym_id)
        if owner_id is None:
            raise LookupError("Gym not found")
        if int(owner_id) != int(user_id):
            raise PermissionError("Not allowed. You are not the owner of this gym.")
        return self.gym_subs.add_to_gym(gym_id, price, benefits)

    def list_trainers(self, city: str = "") -> List[Dict[str, Any]]:
        return self.trainers.list_trainers(city_filter=city)

    def add_trainer(self, data: Dict[str, Any]) -> int:
        required = ["personal_trainer_name", "country", "district", "city", "experience_years", "trainer_id"]
        if not all(data.get(k) for k in required):
            raise ValueError("Câmpuri obligatorii lipsă.")
        trainer_user_id = int(data["trainer_id"])
        role = self.users.get_user_role(trainer_user_id)
        if role != "personal_trainer":
            raise ValueError("User invalid sau rol incorect pentru personal trainer.")
        repo_data = {
            "personal_trainer_name": data["personal_trainer_name"],
            "country": data["country"],
            "district": data["district"],
            "city": data["city"],
            "experience_years": data["experience_years"],
            "description": data.get("description"),
            "trainer_id": trainer_user_id,
        }
        return self.trainers.create_trainer(repo_data)

    def get_trainer_details(self, trainer_db_id: int) -> Dict[str, Any]:
        tr = self.trainers.get_trainer_by_db_id(trainer_db_id)
        if not tr:
            raise LookupError("Trainer not found")
        return tr

    def delete_trainer(self, trainer_db_id: int, user_id: int) -> None:
        owner_id = self.trainers.get_owner_user_id(trainer_db_id)
        if owner_id is None:
            raise LookupError("Trainer not found")
        if int(owner_id) != int(user_id):
            raise PermissionError("Not allowed. You are not the owner of this trainer profile.")
        self.trainers.delete_trainer(trainer_db_id)

    def list_trainer_subscriptions(self, trainer_db_id: int) -> List[Dict[str, Any]]:
        return self.trainer_subs.list_by_trainer(trainer_db_id)

    def add_trainer_subscription(self, trainer_db_id: int, user_id: int, price: Any, benefits: Optional[str]) -> int:
        if price is None or user_id is None:
            raise ValueError("price și user_id sunt obligatorii")
        owner_id = self.trainers.get_owner_user_id(trainer_db_id)
        if owner_id is None:
            raise LookupError("Trainer not found")
        if int(owner_id) != int(user_id):
            raise PermissionError("Not allowed. You are not the owner of this trainer profile.")
        return self.trainer_subs.add_to_trainer(trainer_db_id, price, benefits)

    def list_nutritionists(self, city: str = "") -> List[Dict[str, Any]]:
        return self.nutritionists.list_nutritionists(city_filter=city)

    def add_nutritionist(self, data: Dict[str, Any]) -> int:
        required = ["nutritionist_name", "country", "district", "city", "experience_years", "nutritionist_id"]
        if not all(data.get(k) for k in required):
            raise ValueError("Câmpuri obligatorii lipsă.")
        nutr_user_id = int(data["nutritionist_id"])
        role = self.users.get_user_role(nutr_user_id)
        if role != "nutrition_coach":
            raise ValueError("User invalid sau rol incorect pentru nutritionist.")
        repo_data = {
            "nutritionist_name": data["nutritionist_name"],
            "country": data["country"],
            "district": data["district"],
            "city": data["city"],
            "experience_years": data["experience_years"],
            "description": data.get("description"),
            "nutritionist_id": nutr_user_id,
        }
        return self.nutritionists.create_nutritionist(repo_data)

    def get_nutritionist_details(self, nutr_db_id: int) -> Dict[str, Any]:
        nutr = self.nutritionists.get_nutritionist_by_db_id(nutr_db_id)
        if not nutr:
            raise LookupError("Nutritionist not found")
        return nutr

    def delete_nutritionist(self, nutr_db_id: int, user_id: int) -> None:
        owner_id = self.nutritionists.get_owner_user_id(nutr_db_id)
        if owner_id is None:
            raise LookupError("Nutritionist not found")
        if int(owner_id) != int(user_id):
            raise PermissionError("Not allowed. You are not the owner of this nutritionist profile.")
        self.nutritionists.delete_nutritionist(nutr_db_id)

    def list_nutritionist_subscriptions(self, nutr_db_id: int) -> List[Dict[str, Any]]:
        return self.nutritionist_subs.list_by_nutritionist(nutr_db_id)

    def add_nutritionist_subscription(self, nutr_db_id: int, user_id: int, price: Any, benefits: Optional[str]) -> int:
        if price is None or user_id is None:
            raise ValueError("price și user_id sunt obligatorii")
        owner_id = self.nutritionists.get_owner_user_id(nutr_db_id)
        if owner_id is None:
            raise LookupError("Nutritionist not found")
        if int(owner_id) != int(user_id):
            raise PermissionError("Not allowed. You are not the owner of this nutritionist profile.")
        return self.nutritionist_subs.add_to_nutritionist(nutr_db_id, price, benefits)
