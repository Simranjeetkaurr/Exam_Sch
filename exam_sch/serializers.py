
from rest_framework import serializers
from exam_sch.models import roles, user_table,Dept,Session,Programme_Level,gender,Subject,Program,StudentEnrollment,Specialization,Electives
from exam_sch.models import Semester,Slot,SpecSlot,ElecSlot

class RolesSerializer(serializers.ModelSerializer):
    class Meta:
        model = roles
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
        
class SpecSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecSlot
        fields = '__all__'        

class ElecSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ElecSlot
        fields = '__all__'    
        
# class StudentEnrollmentSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = StudentEnrollment        
#         fields = '__all__'

class StudentEnrollmentReadSerializer(serializers.ModelSerializer):
    gender_name = serializers.CharField(source='gender.gender_name', read_only=True)
    program_name = serializers.CharField(source='program.program_name', read_only=True)
    semester_name = serializers.CharField(source='semester.semester_name', read_only=True)
    spec_names = serializers.SerializerMethodField()
    elec_names = serializers.SerializerMethodField()
    prog_level_name = serializers.CharField(source='program_level.prog_level_name', read_only=True)

    class Meta:
        model = StudentEnrollment
        exclude = ['gender', 'program', 'spec', 'elec', 'program_level','semester']

    def get_spec_names(self, obj):
        return [spec.spec_name for spec in obj.spec.all()]

    def get_elec_names(self, obj):
        return [elec.elec_name for elec in obj.elec.all()]
    
class StudentEnrollmentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentEnrollment
        fields = '__all__'

    
    

class UserTableReadSerializer(serializers.ModelSerializer):
    gender_name = serializers.CharField(source='user_gender.gender_name', read_only=True)
    department_name = serializers.CharField(source='department.dept_name', read_only=True)
    user_role_name = serializers.CharField(source='user_role.role_name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.role_name', read_only=True)
    class Meta:
        model = user_table
        exclude = ["user_role" ,"user_gender","department","created_by"]
        
        
class UserTableCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_table
        fields = '__all__'
        