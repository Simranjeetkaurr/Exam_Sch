from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets,status
from .models import user_table,roles,Dept,Session,Programme_Level,gender,Program_type
from .serializers import UserTableSerializer, LoginSerializer,DeptSerializer,SessionSerializer,Program_LevelSerializer
from .serializers import RolesSerializer,GenderSerializer,Program_typeSerializer
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

@api_view(['POST'])
def roles_create(request):
    if request.method == 'POST':
        serializer = RolesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def roles_detail(request, pk):
    try:
        role_obj = roles.objects.get(pk=pk)
    except roles.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RolesSerializer(role_obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RolesSerializer(role_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        role_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
def user_table_create(request):
    if request.method == 'POST':
        serializer = UserTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def user_table_detail(request, pk):
    try:
        user_obj = user_table.objects.get(pk=pk)
    except user_table.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserTableSerializer(user_obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = UserTableSerializer(user_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        user_obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




@api_view(['POST'])
def user_login(request):
    if request.method== 'POST':
        serializer = LoginSerializer(data= request.data)
        if serializer.is_valid():
            user_email_registered = serializer.validated_data['user_email']
            provided_password = serializer.validated_data['user_password']
            try:
                user = user_table.objects.get(user_email=user_email_registered)
            except user_table.DoesNotExist:
                return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

            if provided_password == user.user_password:
                # Password is correct; log in the user
                # You can customize the response data here
                #print("sdfsdfd",user.user_role)
                refresh = RefreshToken.for_user(user)
                response_data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'message': 'Login successful',
                    'user_id': user.user_id,
                    'user_role_id': user.user_role.role_id,
                    'user_name': user.user_name}
                return Response(response_data, status=status.HTTP_200_OK)
    
            else:
                # Password is incorrect
                return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Department 

class DeptViewSet(viewsets.ModelViewSet):
    queryset = Dept.objects.all()
    serializer_class = DeptSerializer

class SessionViewSet(viewsets.ModelViewSet):
    queryset = Session.objects.all()
    serializer_class = SessionSerializer
    # permission_classes = [permissions.IsAuthenticated]

class Programme_LevelViewSet(viewsets.ModelViewSet):
    queryset = Programme_Level.objects.all()
    serializer_class = Program_LevelSerializer
    # permission_classes = [permissions.IsAuthenticated]

class GenderViewSet(viewsets.ModelViewSet):
    queryset = gender.objects.all()
    serializer_class = GenderSerializer

@api_view(['POST'])
def create_gender(request):
    if request.method == 'POST':
        serializer = GenderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def gender_detail(request, pk):
    try:
        gender_obj = gender.objects.get(pk=pk)
    except gender.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = GenderSerializer(gender_obj)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = GenderSerializer(gender_obj, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        gender_obj.delete()
        return Response({'message': 'record deleted'},status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def user_table_detail(request, pk):
    try:
        user = user_table.objects.get(pk=pk)
    except user_table.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = UserTableSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserTableSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def program_level_list(request):
    if request.method == 'GET':
        programs = Programme_Level.objects.all()
        serializer = Program_LevelSerializer(programs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Program_LevelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def program_level_detail(request, pk):
    try:
        program = Programme_Level.objects.get(pk=pk)
    except Program.DoesNotExist:
        return Response({'message': 'Program not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Program_LevelSerializer(program)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Program_LevelSerializer(program, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        program.delete()
        return Response({'message': 'Program deleted'}, status=status.HTTP_204_NO_CONTENT)



# Program_type

@api_view(['GET', 'POST'])
def program_type_list(request):
    if request.method == 'GET':
        program_types = Program_type.objects.all()
        serializer = Program_typeSerializer(program_types, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = Program_typeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving, updating, and deleting a specific program type
@api_view(['GET', 'PUT', 'DELETE'])
def program_type_detail(request, program_type_id):
    try:
        program_type = Program_type.objects.get(program_type_id=program_type_id)
    except Program_type.DoesNotExist:
        return Response({'message': 'Program type not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = Program_typeSerializer(program_type)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = Program_typeSerializer(program_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        program_type.delete()
        return Response({'message': 'Program type deleted'}, status=status.HTTP_204_NO_CONTENT)

# Subject

@api_view(['GET', 'POST'])
def subject_list(request):
    if request.method == 'GET':
        subjects = Subject.objects.all()
        serializer = SubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving, updating, and deleting a specific subject
@api_view(['GET', 'PUT', 'DELETE'])
def subject_detail(request, subject_id):
    try:
        subject = Subject.objects.get(subject_id=subject_id)
    except Subject.DoesNotExist:
        return Response({'message': 'Subject not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SubjectSerializer(subject)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        subject.delete()
        return Response({'message': 'Subject deleted'}, status=status.HTTP_204_NO_CONTENT)


# from rest_framework import permissions

# class IsAdminUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'admin'  # Assuming 'admin' is a role name.

# class IsTeacherUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'teacher'  # Assuming 'teacher' is a role name.

# class IsStudentUser(permissions.BasePermission):
#     def has_permission(self, request, view):
#         return request.user.role == 'student'  # Assuming 'student' is a role name.


# @api_view(['POST'])
# @permission_classes([IsAdminUser])
# def roles_create(request):
#     # Only admin users can access this view.

# @api_view(['POST'])
# @permission_classes([IsAdminUser, IsTeacherUser])
# def user_table_create(request):
#     # Both admin and teacher users can access this view.

# @api_view(['GET'])
# @permission_classes([IsTeacherUser])
# def list_students(request):
#     # Only teacher users can access this view to list students.

# @api_view(['GET'])
# @permission_classes([IsStudentUser])
# def view_student_profile(request, student_id):
#     # Only student users can access this view to view their own profile.

