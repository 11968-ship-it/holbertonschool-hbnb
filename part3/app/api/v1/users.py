from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity
from app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')
facade = HBnBFacade()

# ============================================================
# API MODELS
# ============================================================

# Model for creating users
user_model = api.model('UserCreate', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password')
})

# Model for regular user updates (only name fields)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user')
})

# Model for admin user updates (all fields)
admin_user_update_model = api.model('AdminUserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user'),
    'password': fields.String(required=False, description='User password')
})


# ============================================================
# PUBLIC ENDPOINTS (No authentication required)
# ============================================================

@api.route('/')
class UserList(Resource):
    @api.doc('list_users')
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Retrieve a list of all users (Public endpoint)"""
        users = facade.get_all_users()
        return [{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        } for user in users], 200


@api.route('/<user_id>')
class UserResource(Resource):
    @api.doc('get_user')
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID (Public endpoint)"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, 200
    
    @api.doc('update_user')
    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Unauthorized action')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """Update user information (Users can only modify their own profile)"""
        current_user_id = get_jwt_identity()
        
        # Check if user is trying to modify their own profile
        if str(current_user_id) != str(user_id):
            return {'error': 'Unauthorized action'}, 403
        
        data = api.payload
        
        # Regular users cannot modify email or password
        if 'email' in data or 'password' in data:
            return {'error': 'You cannot modify email or password'}, 400
        
        try:
            updated_user = facade.update_user(user_id, data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            
            return {
                'message': 'User updated successfully',
                'user': {
                    'id': updated_user.id,
                    'first_name': updated_user.first_name,
                    'last_name': updated_user.last_name,
                    'email': updated_user.email
                }
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400


# ============================================================
# ADMIN ENDPOINTS (Require admin privileges)
# ============================================================

@api.route('/admin/create')
class AdminUserCreate(Resource):
    @api.doc('admin_create_user')
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new user (Admin only)"""
        # Check if user is admin
        claims = get_jwt()
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        user_data = api.payload
        
        # Check if email already exists
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400
        
        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name,
                'email': new_user.email,
                'message': 'User successfully created'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/admin/<user_id>')
class AdminUserResource(Resource):
    @api.doc('admin_update_user')
    @api.expect(admin_user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required()
    def put(self, user_id):
        """Modify a user's details (Admin only - can modify any field including email and password)"""
        claims = get_jwt()
        
        # Check if user is admin
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        data = api.payload
        
        # If email is being changed, check for uniqueness
        if 'email' in data:
            existing_user = facade.get_user_by_email(data['email'])
            if existing_user and str(existing_user.id) != str(user_id):
                return {'error': 'Email already in use'}, 400
        
        try:
            updated_user = facade.update_user(user_id, data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            
            return {
                'message': 'User updated successfully',
                'user': {
                    'id': updated_user.id,
                    'first_name': updated_user.first_name,
                    'last_name': updated_user.last_name,
                    'email': updated_user.email
                }
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400
    
    @api.doc('admin_delete_user')
    @api.response(200, 'User deleted successfully')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @jwt_required()
    def delete(self, user_id):
        """Delete a user (Admin only)"""
        claims = get_jwt()
        
        # Check if user is admin
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, 403
        
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        
        try:
            facade.delete_user(user_id)
            return {'message': 'User deleted successfully'}, 200
        except Exception as e:
            return {'error': str(e)}, 400

