from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets,status
from .models import user_table,roles,Dept,Session,Programme_Level,gender,Program,Subject,Semester,Slot,StudentEnrollment
from .serializers import UserTableSerializer, LoginSerializer,DeptSerializer,SessionSerializer,Program_LevelSerializer
from .serializers import RolesSerializer,GenderSerializer,ProgramSerializer,SubjectSerializer,SemesterSerializer,SlotSerializer,StudentEnrollmentSerializer
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken



@api_view(['GET', 'POST'])
def roles_create(request):
    if request.method == 'GET':
        role = roles.objects.all()
        serializer = RolesSerializer(role, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
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

    
@api_view(['GET', 'POST'])
def user_table_create(request):
    if request.method == 'GET':
        user_tables = user_table.objects.all()
        serializer = UserTableSerializer(user_tables, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = UserTableSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
                    'user_id': user.id,
                    'user_role_id': user.user_role.role_id,
                    'user_name': user.user_name}
                return Response(response_data, status=status.HTTP_200_OK)
    
            else:
                # Password is incorrect
                return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# Department 

@api_view(['GET', 'POST'])
def dept_list(request):
    if request.method == 'GET':
        depts = Dept.objects.all()
        serializer = DeptSerializer(depts, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = DeptSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a single Dept
@api_view(['GET', 'PUT', 'DELETE'])
def dept_detail(request, pk):
    try:
        dept = Dept.objects.get(pk=pk)
    except Dept.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DeptSerializer(dept)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = DeptSerializer(dept, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        dept.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

# Session

@api_view(['GET', 'POST'])
def session_list(request):
    if request.method == 'GET':
        sessions = Session.objects.all()
        serializer = SessionSerializer(sessions, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = SessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Retrieve, update, or delete a single Session
@api_view(['GET', 'PUT', 'DELETE'])
def session_detail(request, pk):
    try:
        session = Session.objects.get(pk=pk)
    except Session.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SessionSerializer(session)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = SessionSerializer(session, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        session.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # permission_classes = [permissions.IsAuthenticated]


@api_view(['GET', 'POST'])
def create_gender(request):
    if request.method == 'GET':
        genders = gender.objects.all()
        serializer = GenderSerializer(genders, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
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



# Program

@api_view(['GET', 'POST'])
def program_list(request):
    if request.method == 'GET':
        program_types = Program.objects.all()
        serializer = ProgramSerializer(program_types, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving, updating, and deleting a specific program type
@api_view(['GET', 'PUT', 'DELETE'])
def program_detail(request, pk):
    try:
        program_type = Program.objects.get(pk=pk)
    except Program_type.DoesNotExist:
        return Response({'message': 'Program type not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ProgramSerializer(program_type)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ProgramSerializer(program_type, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        program_type.delete()
        return Response({'message': 'Program deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def program_search_api(request):
    if request.method == 'GET':
        prog_level_id = request.GET.get('prog_level_id')
        if prog_level_id is not None:
            programs = Program.objects.filter(prog_level_id=prog_level_id)
            serializer = ProgramSerializer(programs, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'prog_level_id parameter is required.'}, status=400)

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

@api_view(['GET'])
def subject_search_api(request):
    if request.method == 'GET':
        program_id = request.GET.get('program_id')
        semester_id = request.GET.get('semester_id')
        if program_id is not None and semester_id is not None:
            subjects = Subject.objects.filter(program_id=program_id, semester_id=semester_id)
            subject_data = [{"subject_id":subject.subject_id ,"subject_name": subject.subject_name, "subject_code": subject.subject_code} for subject in subjects]
            return Response({"subjects": subject_data})
        else:
            return Response({'error': 'Both program_id and semester_id parameters are required.'}, status=400)

# Semester

@api_view(['GET', 'POST'])
def semester_list(request):
    if request.method == 'GET':
        semesters = Semester.objects.all()
        serializer = SemesterSerializer(semesters, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SemesterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving, updating, and deleting a specific semester
@api_view(['GET', 'PUT', 'DELETE'])
def semester_detail(request, pk):
    try:
        semester = Semester.objects.get(pk=pk)
    except semester.DoesNotExist:
        return Response({'message': 'semester not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SemesterSerializer(semester)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SemesterSerializer(semester, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        semester.delete()
        return Response({'message': 'semester deleted'}, status=status.HTTP_204_NO_CONTENT)


#Slot

@api_view(['GET', 'POST'])
def slot_list(request):
    if request.method == 'GET':
        slots = Slot.objects.all()
        serializer = SlotSerializer(slots, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving, updating, and deleting a specific slot
@api_view(['GET', 'PUT', 'DELETE'])
def slot_detail(request, pk):
    try:
        slot = Slot.objects.get(pk=pk)
    except Slot.DoesNotExist:
        return Response({'message': 'Slot not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SlotSerializer(slot)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SlotSerializer(slot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        slot.delete()
        return Response({'message': 'Slot deleted'}, status=status.HTTP_204_NO_CONTENT)


#StudentEnrollments

@api_view(['GET', 'POST'])
def studentenrollment_list(request):
    if request.method == 'GET':
        StudentEnrollments = StudentEnrollment.objects.all()
        serializer = StudentEnrollmentSerializer(StudentEnrollments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentEnrollmentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving, updating, and deleting a student enrolled record
@api_view(['GET', 'PUT', 'DELETE'])
def studentenrollment_detail(request, pk):
    try:
        StudentEnrollments = StudentEnrollment.objects.get(pk=pk)
    except StudentEnrollments.DoesNotExist:
        return Response({'message': 'enrolled student record not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = StudentEnrollmentSerializer(slot)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SlotSerializer(StudentEnrollments, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        StudentEnrollment.delete()
        return Response({'message': 'enrolledstudent deleted'}, status=status.HTTP_204_NO_CONTENT)


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

