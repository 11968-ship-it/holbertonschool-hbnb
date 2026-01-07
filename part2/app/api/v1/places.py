from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade

api = Namespace('places', description='Place operations')

# -------------------------
# Response models (nested)
# -------------------------
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

# -------------------------
# Input models (POST/PUT)
# -------------------------
place_create_model = api.model('PlaceCreate', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),
    # Accept amenity IDs for input (recommended for create/update)
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

# For PUT we should allow partial updates: no required=True here
place_update_model = api.model('PlaceUpdate', {
    'title': fields.String(description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude of the place'),
    'longitude': fields.Float(description='Longitude of the place'),
    'owner_id': fields.String(description='ID of the owner'),
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

# Response model for documentation (what GET returns)
place_model = api.model('Place', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'owner_id': fields.String(required=True, description='ID of the owner'),

    'owner': fields.Nested(user_model, description='Owner of the place'),
    'amenities': fields.List(fields.Nested(amenity_model), description='List of amenities'),
    'reviews': fields.List(fields.Nested(review_model), description='List of reviews')
})


def serialize_place(place, include_owner=True, include_amenities=True, include_reviews=False):
    # Make owner_id robust even if "owner" relationship object is not attached
    owner_id = getattr(place, "owner_id", None) or (place.owner.id if getattr(place, "owner", None) else None)

    data = {
        "id": place.id,
        "title": place.title,
        "description": getattr(place, "description", None),
        "price": place.price,
        "latitude": place.latitude,
        "longitude": place.longitude,
        "owner_id": owner_id,
    }

    if include_owner and getattr(place, "owner", None):
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


@api.route('/')
class PlaceList(Resource):
    @api.expect(place_create_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new place"""
        try:
            payload = api.payload or {}
            place = facade.create_place(payload)
            return serialize_place(place, include_owner=False, include_amenities=False, include_reviews=False), 201
        except (ValueError, TypeError) as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve a list of all places"""
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

    @api.expect(place_update_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place's information"""
        try:
            payload = api.payload or {}
            updated = facade.update_place(place_id, payload)
            if not updated:
                return {"error": "Place not found"}, 404
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
