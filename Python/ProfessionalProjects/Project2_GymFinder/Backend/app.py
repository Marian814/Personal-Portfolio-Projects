from flask import Flask, jsonify, request, send_from_directory
from services.gymfinder_facade import GymFinderFacade


app = Flask(__name__, static_folder="../Frontend", static_url_path="")
facade = GymFinderFacade()

@app.route("/")
def index():
    return send_from_directory("../Frontend", "index.html")


@app.route("/api/register", methods=["POST"])
def register():
    try:
        data = request.get_json() or {}
        role = data.get("role", "member")
        facade.register_user(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            role=role,
        )
        return jsonify({"message": "Utilizator creat cu succes"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/login", methods=["POST"])
def login():
    try:
        data = request.get_json() or {}
        user = facade.login_user(username=data.get("username"), password=data.get("password"))
        return jsonify(
            {
                "message": "Autentificare reușită",
                "id": user["id"],
                "username": user["username"],
                "role": user["role"],
            }
        )
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except PermissionError as e:
        return jsonify({"error": str(e)}), 401


@app.route("/api/gyms", methods=["GET", "POST"])
def gyms_handler():
    if request.method == "POST":
        try:
            data = request.get_json() or {}
            facade.add_gym(data)
            return jsonify({"message": "Gym added successfully"}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    city = (request.args.get("city", "") or "").strip()
    gyms = facade.list_gyms(city=city)
    return jsonify({"gyms": gyms})


@app.route("/api/gyms/<int:gym_id>", methods=["GET", "DELETE"])
def gym_details(gym_id):
    if request.method == "GET":
        try:
            gym = facade.get_gym_details(gym_id)
            return jsonify(gym)
        except LookupError as e:
            return jsonify({"error": str(e)}), 404
    data = request.get_json() or {}
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    try:
        facade.delete_gym(gym_id=gym_id, user_id=int(user_id))
        return jsonify({"message": "Gym deleted"}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403


@app.route("/api/gyms/<int:gym_id>/photos", methods=["GET", "POST"])
def gym_photos(gym_id):
    if request.method == "GET":
        photos = facade.list_gym_photos(gym_id)
        return jsonify({"photos": photos})
    data = request.get_json() or {}
    photo_url = data.get("photo_url")
    user_id = data.get("user_id")
    try:
        new_id = facade.add_gym_photo(gym_id=gym_id, user_id=int(user_id), photo_url=photo_url)
        return jsonify({"message": "Photo added", "id": new_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403


@app.route("/api/gyms/<int:gym_id>/subscriptions", methods=["GET", "POST"])
def gym_subscriptions(gym_id):
    if request.method == "GET":
        subs = facade.list_gym_subscriptions(gym_id)
        return jsonify({"subscriptions": subs})
    data = request.get_json() or {}
    price = data.get("price")
    benefits = data.get("benefits")
    user_id = data.get("user_id")
    try:
        new_id = facade.add_gym_subscription(
            gym_id=gym_id, user_id=int(user_id), price=price, benefits=benefits
        )
        return jsonify({"message": "Subscription added", "id": new_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403


@app.route("/api/trainers", methods=["GET", "POST"])
def trainers_handler():
    if request.method == "POST":
        try:
            data = request.get_json() or {}
            new_id = facade.add_trainer(data)
            return jsonify({"message": "Trainer added successfully", "id": new_id}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    city = (request.args.get("city", "") or "").strip()
    trainers = facade.list_trainers(city=city)
    return jsonify({"trainers": trainers})


@app.route("/api/trainers/<int:trainer_id>", methods=["GET", "DELETE"])
def trainer_details(trainer_id):
    if request.method == "GET":
        try:
            trainer = facade.get_trainer_details(trainer_id)
            return jsonify(trainer)
        except LookupError as e:
            return jsonify({"error": str(e)}), 404
    data = request.get_json() or {}
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    try:
        facade.delete_trainer(trainer_db_id=trainer_id, user_id=int(user_id))
        return jsonify({"message": "Trainer deleted"}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403


@app.route("/api/trainers/<int:trainer_db_id>/subscriptions", methods=["GET", "POST"])
def trainer_subscriptions(trainer_db_id):
    if request.method == "GET":
        subs = facade.list_trainer_subscriptions(trainer_db_id)
        return jsonify({"subscriptions": subs})
    data = request.get_json() or {}
    price = data.get("price")
    benefits = data.get("benefits")
    user_id = data.get("user_id")
    try:
        new_id = facade.add_trainer_subscription(
            trainer_db_id=trainer_db_id, user_id=int(user_id), price=price, benefits=benefits
        )
        return jsonify({"message": "Subscription added", "id": new_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403


@app.route("/api/nutritionists", methods=["GET", "POST"])
def nutritionists_handler():
    if request.method == "POST":
        try:
            data = request.get_json() or {}
            new_id = facade.add_nutritionist(data)
            return jsonify({"message": "Nutritionist added successfully", "id": new_id}), 201
        except ValueError as e:
            return jsonify({"error": str(e)}), 400
    city = (request.args.get("city", "") or "").strip()
    nutritionists = facade.list_nutritionists(city=city)
    return jsonify({"nutritionists": nutritionists})


@app.route("/api/nutritionists/<int:nutr_id>", methods=["GET", "DELETE"])
def nutritionist_details(nutr_id):
    if request.method == "GET":
        try:
            nutr = facade.get_nutritionist_details(nutr_id)
            return jsonify(nutr)
        except LookupError as e:
            return jsonify({"error": str(e)}), 404
    data = request.get_json() or {}
    user_id = data.get("user_id")
    if not user_id:
        return jsonify({"error": "user_id required"}), 400
    try:
        facade.delete_nutritionist(nutr_db_id=nutr_id, user_id=int(user_id))
        return jsonify({"message": "Nutritionist deleted"}), 200
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403


@app.route("/api/nutritionists/<int:nutritionist_db_id>/subscriptions", methods=["GET", "POST"])
def nutritionist_subscriptions_handler(nutritionist_db_id):
    if request.method == "GET":
        subs = facade.list_nutritionist_subscriptions(nutritionist_db_id)
        return jsonify({"subscriptions": subs})
    data = request.get_json() or {}
    price = data.get("price")
    benefits = data.get("benefits")
    user_id = data.get("user_id")
    try:
        new_id = facade.add_nutritionist_subscription(
            nutr_db_id=nutritionist_db_id, user_id=int(user_id), price=price, benefits=benefits
        )
        return jsonify({"message": "Subscription added", "id": new_id}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except LookupError as e:
        return jsonify({"error": str(e)}), 404
    except PermissionError as e:
        return jsonify({"error": str(e)}), 403


if __name__ == "__main__":
    app.run(debug=True)
