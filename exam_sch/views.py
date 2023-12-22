from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets,status
from .serializers import ElectivesSerializer
from .models import user_table,roles,Dept,Session,Programme_Level,gender,Program,Subject,Semester,Slot,StudentEnrollment,Specialization,Electives,SpecSlot,ElecSlot
from .serializers import UserTableCreateSerializer,UserTableReadSerializer, LoginSerializer,DeptSerializer,SessionSerializer,Program_LevelSerializer,SemesterSerializer,SpecializationSerializer,BulkEmailSerializer
from .serializers import RolesSerializer,GenderSerializer,ProgramSerializer,SubjectSerializer,SemesterSerializer,SlotSerializer,StudentEnrollmentCreateSerializer,StudentEnrollmentReadSerializer ,EmailSerializer
from .serializers import SpecSlotSerializer,ElecSlotSerializer
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_q.tasks import async_task
from django.http import JsonResponse
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import secrets
import string
from exam_sch.utlis import generate_jwt_token,CustomRefreshToken
from rest_framework.exceptions import AuthenticationFailed
 # Import the settings module
from exam_sch.permissions import CheckRolePermission
    
class UserPagination(PageNumberPagination):
    page_size = 200  # Set the number of items per page
    page_size_query_param = 'page_size'
    max_page_size = 200


def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + "!#$,-+*@"
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

@api_view(['GET', 'POST'])
@permission_classes([CheckRolePermission])
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
    paginator = UserPagination()
    if request.method == 'GET':
        user_tables = user_table.objects.all()
        result_page = paginator.paginate_queryset(user_tables, request)
        serializer = UserTableReadSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    elif request.method == 'POST':
        serializer = UserTableCreateSerializer(data=request.data)
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
        serializer = UserTableReadSerializer(user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserTableReadSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        user.delete()
        return Response({'message': 'User deleted'}, status=status.HTTP_204_NO_CONTENT)



##### Password RESET #######
    
@api_view(['PUT'])
def password_reset(request, email):
    email = email[1:-1]
    print("hello",email)
    try:
        user = user_table.objects.get(user_email=email)
    except user_table.DoesNotExist:
        return Response({'message': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        # Generate a new random password
        new_password = generate_random_password()

        # Update the user's password
        user.user_password = new_password
        user.save()
                
        sender_email = 'parth.e15279@cumail.in'
        receiver_email = email
        password = 'iuvw krkn voud rvnu' 
        #You may also want to send the new password to the user via email here
        subject = "Password Reset Instruction"
        body = f"Dear {user.user_name},\n\nYour password has been reset. Below is your new password:\n\n{new_password}\n\nPlease copy and paste the new password when logging in. We recommend changing your password after logging in.\n\nBest regards,\nCO-ED Team"

        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        # Set up the SMTP server
        smtp_server = "smtp.gmail.com"
        port = 465  # Use 587 for TLS, or 465 for SSL
        context = ssl.create_default_context()

        # Connect to the server and send the email
        with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())

        return Response({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)
        serializer = UserTableSerializer(user)
        return Response(serializer.data)

    return Response({'message': 'Invalid request method'}, status=status.HTTP_400_BAD_REQUEST)




# @api_view(['POST'])
# def user_login(request):
#     if request.method == 'POST':
#         serializer = LoginSerializer(data=request.data)
#         if serializer.is_valid():
#             user_email_registered = serializer.validated_data['user_email']
#             provided_password = serializer.validated_data['user_password']
#             try:
#                 user = user_table.objects.get(user_email=user_email_registered)
#             except user_table.DoesNotExist:
#                 return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

#             if user.status == 'active':
#                 # Check if the provided password matches the stored password
#                 if provided_password == user.user_password:
#                     # Password is correct; log in the user
#                     refresh = RefreshToken.for_user(user)
#                     response_data = {
#                         'refresh': str(refresh),
#                         'access': str(refresh.access_token),
#                         'message': 'Login successful',
#                         'user_id': user.id,
#                         'user_role_id': user.user_role.role_id,
#                         'user_name': user.user_name}
#                     user_ip = request.META.get('REMOTE_ADDR', None)
#                     user.update_last_login()
#                     user.update_last_login_ip(user_ip)
#                     return Response(response_data, status=status.HTTP_200_OK)
#                 else:
#                     # Password is incorrect
#                     return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)
#             else:
#                 # User is inactive
#                 return Response({'message': 'User is inactive'}, status=status.HTTP_403_FORBIDDEN)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user_email_registered = serializer.validated_data['user_email']
            provided_password = serializer.validated_data['user_password']
            try:
                user = user_table.objects.get(user_email=user_email_registered)
            except user_table.DoesNotExist:
                return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)

            if user.status == 'active':
                # Check if the provided password matches the stored password
                if provided_password == user.user_password:
                    # Password is correct; log in the user
                    print(f"User ID: {user.id}")
                    print(f"User Role ID: {user.user_role.role_id}")
                    #refresh = RefreshToken.for_user(user)
                    refresh = CustomRefreshToken.for_user(user)
                    access_token = str(refresh.access_token)
                    #access_token = generate_jwt_token(user)  # Generate the JWT token
                    response_data = {
                        'refresh': str(refresh),
                        'access': access_token,
                        'message': 'Login successful',
                        'user_id': user.id,
                        'user_role_id': user.user_role.role_id,
                        'user_name': user.user_name
                    }
                    user_ip = request.META.get('REMOTE_ADDR', None)
                    user.update_last_login()
                    user.update_last_login_ip(user_ip)
                    return Response(response_data, status=status.HTTP_200_OK)
                else:
                    # Password is incorrect
                    return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                # User is inactive
                return Response({'message': 'User is inactive'}, status=status.HTTP_403_FORBIDDEN)

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


# SPec Slot

@api_view(['GET', 'POST'])
def spec_slot_list(request):
    if request.method == 'GET':
        slots = SpecSlot.objects.all()
        serializer = SpecSlotSerializer(slots, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SpecSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving, updating, and deleting a specific slot
@api_view(['GET', 'PUT', 'DELETE'])
def spec_slot_detail(request, pk):
    try:
        slot = SpecSlot.objects.get(pk=pk)
    except Slot.DoesNotExist:
        return Response({'message': 'Slot not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SpecSlotSerializer(slot)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SpecSlotSerializer(slot, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        slot.delete()
        return Response({'message': 'Slot deleted'}, status=status.HTTP_204_NO_CONTENT)

# Elec Slot


@api_view(['GET', 'POST'])
def elec_slot_list(request):
    if request.method == 'GET':
        slots = ElecSlot.objects.all()
        serializer = ElecSlotSerializer(slots, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ElecSlotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving, updating, and deleting a specific slot
@api_view(['GET', 'PUT', 'DELETE'])
def elec_slot_detail(request, pk):
    try:
        slot = ElecSlot.objects.get(pk=pk)
    except Slot.DoesNotExist:
        return Response({'message': 'Slot not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ElecSlotSerializer(slot)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = ElecSlotSerializer(slot, data=request.data)
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
    paginator = UserPagination()
    if request.method == 'GET':
        StudentEnrollments = StudentEnrollment.objects.all()
        result_page = paginator.paginate_queryset(StudentEnrollments, request)
        serializer = StudentEnrollmentReadSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == 'POST':
        serializer = StudentEnrollmentCreateSerializer(data=request.data)
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
        serializer = StudentEnrollmentReadSerializer(slot)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = StudentEnrollmentReadSerializer(StudentEnrollments, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        StudentEnrollment.delete()
        return Response({'message': 'enrolledstudent deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def studentenrollment_seacrh(request):
    if request.method == 'GET':
        student_email = request.GET.get('student_email')
        if student_email is not None:
            enrolled = StudentEnrollment.objects.filter(student_email=student_email)
            serializer = StudentEnrollmentReadSerializer(enrolled, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'student_email parameter is required.'}, status=400)

@api_view(['GET'])
def studentenrollment_session_seacrh(request):
    if request.method == 'GET':
        student_email = request.GET.get('student_email')
        session_code = request.GET.get('session_id')
        if student_email is not None and session_code is not None:
            enrolled = StudentEnrollment.objects.filter(student_email=student_email, session_id = session_code)
            serializer = StudentEnrollmentReadSerializer(enrolled, many=True)
            return Response(serializer.data)
        else:
            return Response({'error': 'student_email parameter and session_code is required'}, status=400)
# myapp/views.py

@api_view(['POST'])
def send_email(request):
    serializer = BulkEmailSerializer(data=request.data)
    if serializer.is_valid():
        data = serializer.validated_data
        sender_email = 'parth.e15279@cumail.in'
        password = 'iuvw krkn voud rvnu'  # Replace with your app password

        subject = data.get("subject")
        body = data.get("body")

        receiver_emails = data.get("receiver_emails", [])

        smtp_server = "smtp.gmail.com"
        port = 465
        context = ssl.create_default_context()

        # List to store emails that failed to send
        failed_emails = []
    

        for receiver_email in receiver_emails:
            message = MIMEMultipart()
            message["From"] = sender_email
            message["To"] = receiver_email
            message["Subject"] = subject
            message.attach(MIMEText(body, "plain"))

            try:
                with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
                    server.login(sender_email, password)
                    server.sendmail(sender_email, receiver_email, message.as_string())
            except Exception as e:
                # Log the exception or add the email to the list of failed emails
                failed_emails.append({"email": receiver_email, "error": str(e)})

        if failed_emails:
            return Response({'message': 'Emails sent with some failures', 'failed_emails': failed_emails}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'message': 'Emails sent successfully'}, status=status.HTTP_200_OK)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def specialization_list(request):
    if request.method == 'GET':
        specs = Specialization.objects.all()
        serializer = SpecializationSerializer(specs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = SubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# View for retrieving, updating, and deleting a specific subject
@api_view(['GET', 'PUT', 'DELETE'])
def specialization_detail(request, spec_id):
    try:
        specs = Specialization.objects.get(spec_id=spec_id)
    except Specialization.DoesNotExist:
        return Response({'message': 'specialization not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = SpecializationSerializer(specs)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SpecializationSerializer(specs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        specs.delete()
        return Response({'message': 'Specialization deleted'}, status=status.HTTP_204_NO_CONTENT)

@api_view(['GET'])
def specialization_search_api(request):
    if request.method == 'GET':
        program_id = request.GET.get('program_id')
        semester_id = request.GET.get('semester_id')
        
        if program_id is not None and semester_id is not None:
            specials = Specialization.objects.filter(program_id=program_id, semester_id=semester_id)
            
            specialization_data = {}
            for special in specials:
                category = special.spec_category
                spec_id = special.spec_id
                if category not in specialization_data:
                    specialization_data[category] = {
                        "category": category,
                        "specializationList": []
                    }
                specialization_data[category]["specializationList"].append({
                    "specialization_name": special.spec_name,
                    "specialization_code": special.spec_code,
                    "spec_id":spec_id,
                })
            
            return Response({"specialization": list(specialization_data.values())})
        else:
            return Response({'error': 'Both program_id and semester_id parameters are required.'}, status=400)


###### Electives #################

@api_view(['GET', 'POST'])
def Electives_list(request):
    if request.method == 'GET':
        elecs = Electives.objects.all()
        serializer = ElectivesSerializer(elecs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ElectivesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for retrieving, updating, and deleting a specific subject
@api_view(['GET', 'PUT', 'DELETE'])
def Electives_detail(request, elec_id):
    try:
        elecs = Electives.objects.get(elec_id=elec_id)
    except Electives.DoesNotExist:
        return Response({'message': 'electives not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ElectivesSerializer(elecs)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = SpecializationSerializer(elecs, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        elecs.delete()
        return Response({'message': 'electives deleted'}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def electives_search_api(request):
    if request.method == 'GET':
        program_id = request.GET.get('program_id')
        semester_id = request.GET.get('semester_id')

        if program_id is not None and semester_id is not None:
            electives = Electives.objects.filter(program_id=program_id, semester_id=semester_id)

            # Organize electives based on elective_category
            elective_data = {}
            for elective in electives:
                if elective.elec_category not in elective_data:
                    elective_data[elective.elec_category] = []

                elective_data[elective.elec_category].append({
                    "elective_id": elective.elec_id,
                    "elective_name": elective.elec_name,
                    "elective_code": elective.elec_code
                })

            # Convert the dictionary to a list
            elective_list = [{"category": category, "electiveList": electives} for category, electives in elective_data.items()]

            return Response({"electives": elective_list})
        else:
            return Response({'error': 'Both program_id and semester_id parameters are required.'}, status=400)

# myapp/views.py


#####BULK EMAIL ##########
# @csrf_exempt
# @api_view(['POST'])
# def send_email(request):
#     serializer = EmailSerializer(data=request.data)
#     if serializer.is_valid():
#         data = serializer.validated_data
#         sender_email = 'parth.e15279@cumail.in'  # Use get() to avoid KeyError
#         receiver_emails = data.get('receiver_email')
#         password = 'lktx ovbx qvoh yxsp'  # Replace with your app password
#         subject = "Password Reset Instruction"
#         body = """
# Subject: Password Reset Request for [Your Application Name]

# Dear [User],

# We recently received a request to reset your password for [Your Application Name]. If you did not make this request, you can ignore this email.

# To reset your password, please follow the link below:
# [Password Reset Link]

# Please note that this link is valid for a limited time. If you have any issues or did not request a password reset, please contact our support team at [Your Support Email].

# Thank you for using [Your Application Name].

# Best regards,
# [Your Application Team]
# """

#         # # Check if the receiver's email is registered
#         # # if not StudentEnrollment.objects.filter(student_email=receiver_email).exists():
#         # #     return JsonResponse({'error': 'Receiver email not registered'}, status=status.HTTP_400_BAD_REQUEST)

#         # # Create the email message
#         # message = MIMEMultipart()
#         # message["From"] = sender_email
#         # message["To"] = receiver_email
#         # message["Subject"] = subject
#         # message.attach(MIMEText(body, "plain"))

#         # # Set up the SMTP server
#         # smtp_server = "smtp.gmail.com"
#         # port = 465  # Use 587 for TLS, or 465 for SSL
#         # context = ssl.create_default_context()
        
#         for receiver_email in receiver_emails:
#             # Create the email message for each recipient
#             message = MIMEMultipart()
#             message["From"] = sender_email
#             message["To"] = ", ".join(receiver_emails)
#             message["Subject"] = subject
#             message.attach(MIMEText(body, "plain"))

#             # Set up the SMTP server
#             smtp_server = "smtp.gmail.com"
#             port = 465  # Use 587 for TLS, or 465 for SSL
#             context = ssl.create_default_context()

#         # Connect to the server and send the email
#         with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
#             server.login(sender_email, password)
#             server.sendmail(sender_email, receiver_email, message.as_string())

#         return JsonResponse({'message': 'Email sent successfully'}, status=status.HTTP_200_OK)

#     return JsonResponse({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


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

