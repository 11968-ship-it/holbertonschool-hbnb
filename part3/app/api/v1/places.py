from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('places', description='Place operations')

# Models
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

# Input model for creating/updating a place
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place')
})

# Response model for full place details
place_model = api.model('Place', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})

# Serializer
def serialize_place(place, include_owner=True, include_amenities=True, include_reviews=False):
    data = {
        "id": place.id,
        "title": place.title,
        "description": place.description,
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner_id": place.owner.id if place.owner else None,
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
            for a in getattr(place, "amenities", [])
        ]

    if include_reviews:
        reviews = facade.get_reviews_by_place(place.id)
        data["reviews"] = [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user.id if getattr(r, "user", None) else getattr(r, "user_id", None),
            }
            for r in (reviews or [])
        ]

    return data

# Endpoints
@api.route('/')
class PlaceList(Resource):
    @jwt_required()
    @api.expect(place_input_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        current_user = get_jwt_identity()
        payload = request.get_json(silent=True) or {}
        payload["owner_id"] = current_user  # enforce ownership

        if "amenities" not in payload:
            payload["amenities"] = []

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
        """Update a place"""
        current_user = get_jwt_identity()
        place = facade.get_place(place_id)

        if not place:
            return {"error": "Place not found"}, 404
        
        if place.owner or str(place.owner.id) != str(current_user):
            return {"error": "Unauthorized action"}, 403

        payload = request.get_json(silent=True) or {}

        payload.pop("owner_id", None)
        try:
            updated = facade.update_place(place_id, payload)
            return serialize_place(updated, include_owner=True, include_amenities=True, include_reviews=True), 200
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400

@api.route('/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                "id": r.id,
                "text": r.text,
                "rating": r.rating,
                "user_id": r.user.id if getattr(r, "user", None) else getattr(r, "user_id", None),
                "place_id": place_id
            }
            for r in (reviews or [])
        ], 200
