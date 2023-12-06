
from rest_framework import serializers
from exam_sch.models import roles, user_table,Dept,Session,Programme_Level,gender,Subject,Program,StudentEnrollment,Specialization,Electives
from exam_sch.models import Semester,Slot


class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = roles
        fields = '__all__'

class UserTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_table
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    user_password = serializers.CharField(write_only=True) # 'write_only=True' ensures the password won't be displayed in responses

class DeptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dept
        fields = '__all__'

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'

class Program_LevelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Programme_Level
        fields = '__all__'


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = gender
        fields = '__all__'

class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = '__all__'

class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = '__all__'

class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = '__all__'

class SlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slot
        fields = '__all__'

class StudentEnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEnrollment
        fields = '__all__'
        
class EmailSerializer(serializers.Serializer):
    receiver_email = serializers.EmailField()

class BulkEmailSerializer(serializers.Serializer):
    receiver_emails = serializers.ListField(child=serializers.EmailField())
    subject = serializers.CharField()
    body = serializers.CharField()

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'
        
class ElectivesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Electives
        fields = '__all__'