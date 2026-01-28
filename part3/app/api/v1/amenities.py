from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade
from flask import request
from flask_jwt_extended import jwt_required, get_jwt

api = Namespace('amenities', description='Amenity operations')

facade = HBnBFacade()

def admin_required():
    claims = get_jwt()
    if not claims.get("is_admin", False):
        return {"error": "Admin privileges required"}, 403
    return None

# Define the model for validation and Swagger docs
amenity_input_model = api.model('AmenityInput', {
    'name': fields.String(required=True, description='Name of the amenity')
})

amenity_output_model = api.model('AmenityOutput', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})

@api.route('/')
class AmenityList(Resource):
    @jwt_required()
    @api.expect(amenity_input_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def post(self):
        """Register a new amenity (Admin only)"""
        deny = admin_required()
        if deny:
            return deny
        
        data = api.payload
        try:
            amenity = facade.create_amenity(data)
            return {
                "id": amenity.id,
                "name": amenity.name,
                "created_at": amenity.created_at.isoformat(),
                "updated_at": amenity.updated_at.isoformat()
            }, 201
        except ValueError as e:
            return {"error": str(e)}, 400
        
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Retrieve a list of all amenities"""
        amenities = facade.get_all_amenities()
        # Manually convert each amenity to dict
        return [{
            "id": a.id,
            "name": a.name,
            "created_at": a.created_at.isoformat(),
            "updated_at": a.updated_at.isoformat()
        } for a in amenities], 200


@api.route('/<amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {"error": "Amenity not found"}, 404
        return {
            "id": amenity.id,
            "name": amenity.name,
            "created_at": amenity.created_at.isoformat(),
            "updated_at": amenity.updated_at.isoformat()
        }, 200

    @jwt_required()
    @api.expect(amenity_input_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    def put(self, amenity_id):
        """Update an amenity's information (Admin only)"""
        deny = admin_required()
        if deny:
            return deny
        
        data = api.payload
        
        try:
            amenity = facade.update_amenity(amenity_id, data)
            if not amenity:
                return {"error": "Amenity not found"}, 404
                
            return {"message": "Amenity updated successfully"}, 200
            
        except ValueError as e:
            return {"error": str(e)}, 400

    @jwt_required()
    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    @api.response(403, 'Admin privileges required')
    def delete(self, amenity_id):
        """Delete an amenity (Admin only)"""
        deny = admin_required()
        if deny:
            return deny
        
        result = facade.delete_amenity(amenity_id)
        if not result:
            return {"error": "Amenity not found"}, 404
        return {"message": "Amenity deleted successfully"}, 200
