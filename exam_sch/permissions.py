from rest_framework import permissions
import jwt
from django.conf import settings

# class HasRolePermission(permissions.BasePermission):
#     def has_permission(self, request, view):
#         print("is this avialble")
#         # Check if the user is authenticated
#         if request.user.is_authenticated:
#             try:
#                 token_value = request.auth.token
#                 decoded_token = jwt.decode(token_value, settings.SECRET_KEY, algorithms=['HS256'])
#                 #decoded_token = jwt.decode(request.auth, settings.SECRET_KEY, algorithms=['HS256'])
#                 user_role_id = decoded_token.get('role_id')
#                 print(f"User Role ID: {user_role_id}")
#             except jwt.ExpiredSignatureError:
#                 raise AuthenticationFailed("Token has expired")
#             except jwt.InvalidTokenError:
#                 raise AuthenticationFailed("Invalid token")

#             allowed_role_ids = [1]  # Add the role IDs that have permission

#             if user_role_id in allowed_role_ids:
#                 return True
#             else:
#                 print("User does not have the required role.")
#         else:
#             print("User is not authenticated.")

#         return False

class CheckRolePermission(permissions.BasePermission):
    def check_permission(self, request, view):
        # Check if the user is authenticated using JWT
        if request.auth and request.auth.token:
            try:
                token_value = request.auth.token
                decoded_token = jwt.decode(token_value, settings.SECRET_KEY, algorithms=['HS256'])
                user_role_id = decoded_token.get('role_id')
                print(f"User Role ID: {user_role_id}")

                allowed_role_ids = [1]  # Add the role IDs that have permission

                if user_role_id in allowed_role_ids:
                    return True
                else:
                    print("User does not have the required role.")
            except jwt.ExpiredSignatureError:
                raise AuthenticationFailed("Token has expired")
            except jwt.InvalidTokenError:
                raise AuthenticationFailed("Invalid token")
        else:
            print("User is not authenticated using JWT.")
        return False
# class CheckRolePermission(permissions.BasePermission):
#     def check_permission(self, request, view):
#         print("can you hear m e")
#         try:
#             print("Checking permission for user:", request.user.id)
#             # Your existing code...
#         except Exception as e:
#             print("Exception in has_permission:", e)
#             return False

