from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

# Input validation model
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'place_id': fields.String(required=True, description='ID of the place')
})

review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Text of the review'),
    'rating': fields.Integer(required=False, description='Rating of the place (1-5)')
})

# ------------------ /api/v1/reviews/ ------------------
@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        try:
            current_user = get_jwt_identity()
            payload = request.json or {}

            place_id = payload.get("place_id")
            if not place_id:
                return {"error": "Invalid input data"}, 400

            place = facade.get_place(place_id)
            if not place:
                return {"error": "Invalid input data."}, 400

            if str(place.owner_id) == str(current_user):
                return {"error": "You cannot review your own place."}, 400

            existing = facade.get_review_by_user_and_place(current_user, place_id)
            if existing:
                return {"error": "You have already reviewed this place."}, 400
            
            payload["user_id"] = current_user
            
            review = facade.create_review(payload)
            return review.to_dict(), 201
        
        except ValueError as e:
            return {"error": str(e)}, 400

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
    @api.response(403, 'Unauthorized action')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review"""
        try:
            current_user = get_jwt_identity()
            review = facade.get_review(review_id)
            if not review:
                return {"error": "Review not found"}, 404

            if str(review.user_id) != str(current_user):
                return {"error": "Unauthorized action"}, 403

            payload = request.json or {}
            updated = facade.update_review(review_id, payload)
            if not updated:
                return {"error": "Review not found"}, 404

            return {"message": "Review updated successfully"}, 200
        
        except ValueError as e:
            return {"error": str(e)}, 400

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

        if str(review.user_id) != str(current_user):
            return {"error": "Unauthorized action"}, 403

        success = facade.delete_review(review_id)
        if not success:
            return {"error": "Review not found"}, 404
        return {"message": "Review deleted successfully"}, 200
