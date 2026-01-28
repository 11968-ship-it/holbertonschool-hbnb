from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import jwt_required

api = Namespace('reviews', description='Review operations')

# Input validation model
# Input validation model (ONLY text + rating)
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place'),
    'rating': fields.Integer(required=True, description='Rating of the review (1-5)')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Text of the review'),
    'rating': fields.Integer(required=False, description='Rating of the place (1-5)'),
    'rating': fields.Integer(required=False, description='Rating of the review (1-5)')
})

# ------------------ /api/v1/reviews/ ------------------
class ReviewList(Resource):
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        """Create a new review (no place/user relationships yet)"""
        try:
            current_user = get_jwt_identity()
            payload = request.json or {}

            place_id = payload.get("place_id")
            if not place_id:
                return {"error": "Invalid input data"}, 400
            # Ensure only expected keys are passed
            data = {
                "text": payload.get("text"),
                "rating": payload.get("rating")
            }

            place = facade.get_place(place_id)
            if not place:
                return {"error": "Invalid input data."}, 400

            owner_value = None
            for attr in ("owner_id", "user_id", "host_id", "owner"):
                if hasattr(place, attr):
                    owner_value = getattr(place, attr)
                    break
                    
            if owner_value is not None and hasattr(owner_value, "id"):
                owner_value = owner_value.id
                
            if owner_value is not None and str(owner_value) == str(current_user):
                return {"error": "You cannot review your own place."}, 400

            existing = facade.get_review_by_user_and_place(current_user, place_id)
            if existing:
                return {"error": "You have already reviewed this place."}, 400
            
            payload["user_id"] = current_user
            
            review = facade.create_review(payload)
            review = facade.create_review(data)
            return review.to_dict(), 201
        

        except ValueError as e:
            return {"error": str(e)}, 400
        except Exception:
            return {"error": "Invalid input data"}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve all reviews"""
        reviews = facade.get_all_reviews()
        return [r.to_dict() for r in reviews], 200


# ------------------ /api/v1/reviews/<review_id> ------------------
@api.route('/<review_id>')
class ReviewResource(Resource):
@@ -84,64 +65,26 @@ def get(self, review_id):
    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review"""
        """Update a review (task scope: no ownership checks yet)"""
        try:
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
            
            if review_owner is None or str(review_owner) != str(current_user):
                return {"error": "Unauthorized action"}, 403

            payload = request.json or {}
            updated = facade.update_review(review_id, payload)
            if not updated:
                return {"error": "Review not found"}, 404

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

        if review_owner is None:
            return {"error": "Unauthorized action"}, 403
        
        if str(review_owner) != str(current_user):
            return {"error": "Unauthorized action"}, 403

        """Delete a review (task scope: no ownership checks yet)"""
        success = facade.delete_review(review_id)
        if not success:
            return {"error": "Review not found"}, 404
