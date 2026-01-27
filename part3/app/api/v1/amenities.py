from flask_restx import Namespace, Resource, fields
from app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')

facade = HBnBFacade()

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
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new amenity (Admin only)"""
        
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
        
    @api.marshal_list_with(amenity_output_model)
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
    @api.marshal_with(amenity_output_model)
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

    @api.expect(amenity_input_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    def put(self, amenity_id):
        """Update an amenity's information (Admin only)"""
        data = api.payload
        
        try:
            amenity = facade.update_amenity(amenity_id, data)
            if not amenity:
                return {"error": "Amenity not found"}, 404
                
            return {
                "id": amenity.id,
                "name": amenity.name,
                "created_at": amenity.created_at.isoformat(),
                "updated_at": amenity.updated_at.isoformat()
            }, 200
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    def delete(self, amenity_id):
        """Delete an amenity (Admin only)"""

        result = facade.delete_amenity(amenity_id)
        if not result:
            return {"error": "Amenity not found"}, 404

        return {"message": "Amenity deleted"}, 200
