from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required

api = Namespace('reviews', description='Review operations')

# Input validation model (ONLY text + rating)
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the review (1-5)')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Text of the review'),
    'rating': fields.Integer(required=False, description='Rating of the review (1-5)')
})

# ------------------ /api/v1/reviews/ ------------------
@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new review (no place/user relationships yet)"""
        try:
            payload = request.json or {}

            # Ensure only expected keys are passed
            data = {
                "text": payload.get("text"),
                "rating": payload.get("rating")
            }

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
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            return {"error": "Review not found"}, 404
        return review.to_dict(), 200

    @jwt_required()
    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review (task scope: no ownership checks yet)"""
        try:
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
    def delete(self, review_id):
        """Delete a review (task scope: no ownership checks yet)"""
        success = facade.delete_review(review_id)
        if not success:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200
