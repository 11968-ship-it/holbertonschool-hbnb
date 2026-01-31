from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place'),
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Text of the review'),
    'rating': fields.Integer(required=False, description='Rating of the place (1-5)'),
})

# ------------------ /api/v1/reviews/ ------------------
@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review"""
        try:
            current_user = get_jwt_identity()
            payload = request.json or {}

            place_id = payload.get("place_id")
            text = payload.get("text")
            rating = payload.get("rating")

            if not place_id or text is None or rating is None:
                return {"error": "Invalid input data"}, 400

            place = facade.get_place(place_id)
            if not place:
                return {"error": "Invalid input data."}, 400

            # prevent reviewing own place (best-effort based on available attrs)
            owner_value = None
            for attr in ("owner_id", "user_id", "host_id", "owner"):
                if hasattr(place, attr):
                    owner_value = getattr(place, attr)
                    break
            if owner_value is not None and hasattr(owner_value, "id"):
                owner_value = owner_value.id
            if owner_value is not None and str(owner_value) == str(current_user):
                return {"error": "You cannot review your own place."}, 400

            if hasattr(facade, "get_review_by_user_and_place"):
                existing = facade.get_review_by_user_and_place(current_user, place_id)
                if existing:
                    return {"error": "You have already reviewed this place."}, 400

            data = {
                "text": text,
                "rating": rating,
                "place_id": place_id,
                "user_id": current_user,
            }

            review = facade.create_review(data)
            return review.to_dict(), 201

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


# ------------------ /api/v1/reviews/<review_id> ------------------
@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Retrieve a single review"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review"""
        try:
            claims = get_jwt()
            is_admin = claims.get("is_admin", False)
            current_user = get_jwt_identity()
            
            review = facade.get_review(review_id)
            if not review:
                return {"error": "Review not found"}, 404

            review_owner = None
            for attr in ("user_id", "author_id", "owner_id", "user", "author"):
                if hasattr(review, attr):
                    review_owner = getattr(review, attr)
                    break
            if review_owner is not None and hasattr(review_owner, "id"):
                review_owner = review_owner.id

            if not is_admin and (review_owner is None or str(review_owner) != str(current_user)):
                return {"error": "Unauthorized action"}, 403

            payload = request.json or {}
            updated = facade.update_review(review_id, payload)
            if not updated:
                return {"error": "Review not found"}, 404

            # return updated object if your facade returns it; otherwise message is ok
            return {"message": "Review updated successfully"}, 200

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception:
            return {"error": "Invalid input data"}, 400

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    def delete(self, review_id):
        """Delete a review"""
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)
        current_user = get_jwt_identity()
        
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404

        review_owner = None
        for attr in ("user_id", "author_id", "owner_id", "user", "author"):
            if hasattr(review, attr):
                review_owner = getattr(review, attr)
                break
        if review_owner is not None and hasattr(review_owner, "id"):
            review_owner = review_owner.id

        if not is_admin and (review_owner is None or str(review_owner) != str(current_user)):
            return {"error": "Unauthorized action"}, 403

        success = facade.delete_review(review_id)
        if not success:
            return {"error": "Review not found"}, 404

        return {"message": "Review deleted successfully"}, 200
