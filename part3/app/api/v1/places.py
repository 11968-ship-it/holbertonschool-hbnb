from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

# what user sends
place_input_model = api.model('PlaceInput', {
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place')
})

# what API returns
place_output_model = api.model('PlaceOutput', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(required=True, description='Title of the place'),
    'description': fields.String(description='Description of the place'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude of the place'),
    'longitude': fields.Float(required=True, description='Longitude of the place'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update')
})

# --- Endpoints ---
@api.route('/')
class PlaceList(Resource):
    @api.doc('create_place')
    @api.expect(place_input_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Create a new place"""
        place_data = api.payload
        
        try:
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'created_at': new_place.created_at.isoformat() if new_place.created_at else None,
                'updated_at': new_place.updated_at.isoformat() if new_place.updated_at else None
            }, 201
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

    @api.doc('list_places')
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Retrieve all places"""
        places = facade.get_all_places()
        return [{
            'id': p.id,
            'title': p.title,
            'description': p.description,
            'price': p.price,
            'latitude': p.latitude,
            'longitude': p.longitude,
            'created_at': p.created_at.isoformat() if p.created_at else None,
            'updated_at': p.updated_at.isoformat() if p.updated_at else None
        } for p in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.doc('get_place')
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'created_at': place.created_at.isoformat() if place.created_at else None,
            'updated_at': place.updated_at.isoformat() if place.updated_at else None
        }, 200

    @api.doc('update_place')
    @api.expect(place_input_model)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place"""
        place_data = api.payload

        try:
            updated = facade.update_place(place_id, place_data)
            if not updated:
                return {'error': 'Place not found'}, 404
            return {
                'id': updated.id,
                'title': updated.title,
                'description': updated.description,
                'price': updated.price,
                'latitude': updated.latitude,
                'longitude': updated.longitude,
                'updated_at': updated.updated_at.isoformat() if updated.updated_at else None
            }, 200
        except (ValueError, TypeError) as e:
            return {'error': str(e)}, 400

    @api.doc('delete_place')
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    def delete(self, place_id):
        """Delete a place"""
        result = facade.delete_place(place_id)
        if not result:
            return {'error': 'Place not found'}, 404
            
        return {'message': 'Place deleted successfully'}, 200
