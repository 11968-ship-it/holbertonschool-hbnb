from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask import current_app

api = Namespace('auth', description='Authentication operations')

# Model for input validation

# Login model
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Signup model
signup_model = api.model('Signup', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name')
})

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================
@api.route('/signup')
class Signup(Resource):
    @api.expect(signup_model)
    def post(self):
        """Register a new user and return a JWT token"""
        user_data = api.payload
        
        # Validate required fields
        required_fields = ['email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if field not in user_data:
                return {'error': f'{field} is required'}, 400
        
        # Check if user already exists
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 409
        
        try:
            # Create new user
            new_user = facade.create_user(user_data)
            return {
                'id': new_user.id,
                'email': new_user.email,
                'first_name': new_user.first_name,
                'last_name': new_user.last_name
            }, 201
        except ValueError as e:
            return {'error': str(e)}, 400


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, 401

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(
        identity=str(user.id),   # only user ID goes here
        additional_claims={"is_admin": user.is_admin}  # extra info here
        )
        
        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, 200
 
@api.route('/protected')
class ProtectedResource(Resource):
    @jwt_required()
    def get(self):
         """A protected endpoint that requires a valid JWT token"""
         print("jwt------")
         print(get_jwt_identity())
         current_user = get_jwt_identity() # Retrieve the user's identity from the token
         #if you need to see if the user is an admin or not, you can access additional claims using get_jwt() :
         # addtional claims = get_jwt()
         #additional claims["is_admin"] -> True or False
         return {'message': f'Hello, user {current_user}'}, 200
        
@api.route('/register-admin')
class AdminRegistration(Resource):
    def post(self):
        """TEMPORARY: Create admin user - DISABLE IN PRODUCTION"""
        # Add environment check
        if not current_app.debug:
            return {'error': 'Endpoint disabled'}, 403
        
        admin_data = api.payload
        admin_data['is_admin'] = True
        
        # Create admin user
        admin = facade.create_user(admin_data)
        return {'message': 'Admin created', 'id': str(admin.id)}, 201
