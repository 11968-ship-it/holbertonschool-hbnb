from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity

api = Namespace('users', description='User operations')

# POST
user_model = api.model('UserCreate', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password')
})

# PUT - User
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user')
})

# PUT - Admin
admin_user_update_model = api.model('AdminUserUpdate', {
    'first_name': fields.String(required=False, description='First name of the user'),
    'last_name': fields.String(required=False, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user'),
    'password': fields.String(required=False, description='User password'),
    'is_admin': fields.Boolean(required=False, description='Admin flag')
})

@api.route('/')
class UserList(Resource):
    #@jwt_required()
    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new user (Admin only)"""
        
        claims = get_jwt()
        if not claims.get("is_admin", False):
            return {'error': 'Admin privileges required'}, 403
        
        user_data = api.payload
        user_data.pop("is_admin", None)
        
        if facade.get_user_by_email(user_data['email']):
            return {'error': 'Email already registered'}, 400

        try:
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'message': 'User successfully created'
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400

    def get(self):
        """get User List"""
        users = facade.get_all_users()
        return [{'id': u.id, 'first_name': u.first_name, 'last_name': u.last_name, 'email': u.email} for u in users], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return {'id': user.id, 'first_name': user.first_name, 'last_name': user.last_name, 'email': user.email}, 200

    @api.expect(admin_user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @jwt_required() #Secure the user info with JWT Authentication
    def put(self, user_id):
        """Update user information (users can only modify their own data)"""
        claims = get_jwt()
        is_admin = claims.get("is_admin", False)

        # ADMIN PATH
        if is_admin:
            data = request.json or {}

            data.pop("is_admin", None)
            
            email = data.get("email")
            if email:
                existing = facade.get_user_by_email(email)
                if existing and str(existing.id) != str(user_id):
                    return {"error": "Email already in use"}, 400

            updated = facade.update_user(user_id, data)
            if not updated:
                return {"error": "User not found"}, 404
            return {"message": "User updated successfully"}, 200
        
        # USER PATH
        current_user_id = get_jwt_identity()
        if current_user_id != user_id: # Check if the authenticated user is trying to modify their own data
            return {'error': 'Unauthorized to modify this user'}, 403
        user_data = api.payload
        # ensure email and password are not in the payload
        if 'email' in user_data or 'password' in user_data:
            return {'error': 'Email and password cannot be modified'}, 400

        try:
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {'message': 'User updated successfully'}, 200
        except ValueError as e:
            return {'error': str(e)}, 400
