from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt

api = Namespace('places', description='Place operations')

# --- Models ---
amenity_model = api.model('PlaceAmenity', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Name of the amenity')
})

user_model = api.model('PlaceUser', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name of the owner'),
    'last_name': fields.String(description='Last name of the owner'),
    'email': fields.String(description='Email of the owner')
})

review_model = api.model('PlaceReview', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Text of the review'),
    'rating': fields.Integer(description='Rating of the place (1-5)'),
    'user_id': fields.String(description='ID of the user')
})

place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'location': fields.String(required=True, description='Location/city of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place')
})

place_model = api.model('Place', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'location': fields.String(required=True, description='Location/city of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

# --- Serializer ---
def serialize_place(place, include_owner=True, include_amenities=True, include_reviews=False):
    data = {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "location": place.location,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner_id": str(place.owner_id) if place.owner_id else None
    }

    if include_owner and place.owner:
        data["owner"] = {
            "id": place.owner.id,
            "first_name": place.owner.first_name,
            "last_name": place.owner.last_name,
            "email": place.owner.email
        }

    if include_amenities:
        data["amenities"] = [
            {"id": a.id, "name": a.name}
            for a in place.amenities
        ]

    if include_reviews:
        data["reviews"] = [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user_id if r.user else r.user_id,
                "user_name": (
                    f"{r.user.first_name} {r.user.last_name}"
                    if r.user else "User"
                )
            }
            for r in place.reviews
        ]

    return data

# --- Endpoints ---
@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_input_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        current_user = get_jwt()
        user_id = current_user.get('sub')

        payload = api.payload.copy()
        payload["owner_id"] = user_id
        payload.setdefault("amenities", [])

        try:
            place = facade.create_place(payload)
            return serialize_place(place, include_owner=False, include_amenities=False, include_reviews=False), 201
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return [
            serialize_place(p, include_owner=False, include_amenities=False, include_reviews=False)
            for p in places
        ], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return serialize_place(place, include_owner=True, include_amenities=True, include_reviews=True), 200

    @jwt_required()
    @api.expect(place_input_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place (admin bypass allowed)"""
        current_user = get_jwt()
        user_id = str(current_user.get('sub'))
        is_admin = current_user.get('is_admin', False)

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        # Admins can bypass ownership
        if not is_admin and str(place.owner_id) != user_id:
            return {"error": "Unauthorized action"}, 403

        payload = api.payload.copy()
        payload.pop("owner_id", None)

        try:
            updated = facade.update_place(place_id, payload)
            return serialize_place(updated, include_owner=True, include_amenities=True, include_reviews=True), 200
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400

    @jwt_required()
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, place_id):
        """Delete a place (admin bypass allowed)"""
        current_user = get_jwt()
        user_id = str(current_user.get('sub'))
        is_admin = bool(current_user.get('is_admin', False))

        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        owner_id = str(place.owner_id)

        if not is_admin and owner_id != user_id:
            return {"error": "Unauthorized action"}, 403

        facade.delete_place(place_id)
        return {"message": "Place deleted successfully"}, 200

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user.id if r.user else r.user_id,
                "user_name": (
                    f"{r.user.first_name} {r.user.last_name}"
                    if r.user else "User"
                ),
                "place_id": place_id
            }
            for r in place.reviews
        ], 200

@api.route('/<place_id>/reviews/<review_id>')
class PlaceReviewResource(Resource):
    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, place_id, review_id):
        """Delete a review (admin bypass allowed)"""
        current_user = get_jwt()
        user_id = str(current_user.get('sub'))
        is_admin = current_user.get('is_admin', False)

        review = facade.get_review(review_id)
        if not review or str(review.place.id) != str(place_id):
            return {"error": "Review not found"}, 404

        if not is_admin and str(review.user_id) != user_id:
            return {"error": "Unauthorized action"}, 403

        facade.delete_review(review_id)
        return {"message": "Review deleted successfully"}, 200
