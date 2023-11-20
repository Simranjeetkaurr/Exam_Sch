from xml.dom import ValidationErr
from django.db import models
import secrets
import string
def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation[0:6]
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password
  
class roles(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(unique=True,max_length=12, choices=[
        ('Admin','Admin'), ('Co-Ordinator','Co-ordinator'),   
        ('Student','Student'),
    ])
     
    status = models.CharField(max_length=12, choices=[
        ('active', 'Active'),   
        ('inactive', 'Inactive'),
    ], default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class gender(models.Model):
    gender_id = models.AutoField(primary_key=True)
    gender_name = models.CharField(max_length=12, choices=[('Male', 'male'), ('Female', 'female'), ('Other', 'other')])
    gender_status = models.CharField(max_length=12, choices=[('active', 'Active'), ('inactive', 'Inactive')])

class Dept(models.Model):
    DEPT_CHOICES = [('online', 'Online'),('odl', 'Online-Distance Learning'),('regular', 'Regular'),]
    STATUS_CHOICES = [('active', 'Active'),('inactive', 'Inactive'),]
    dept_id = models.AutoField(primary_key=True)
    dept_name = models.CharField(unique=True,max_length=10, choices=DEPT_CHOICES)
    dept_status = models.CharField(max_length=10, choices=STATUS_CHOICES)

    def __str__(self):
        return self.dept_name


class user_table(models.Model):
    user_role = models.ForeignKey(roles, on_delete=models.CASCADE, default=3)
    user_id = models.AutoField(primary_key=True)
    user_name = models.CharField(max_length=255)
    user_email = models.EmailField(unique=True)
    user_password= models.TextField(default=generate_random_password)  
    user_gender = models.ForeignKey(gender,on_delete=models.CASCADE)
    department = models.ForeignKey(Dept,on_delete=models.CASCADE,default=1)
    created_at = models.DateTimeField(auto_now_add=True,null=True)
    created_by = models.ForeignKey(roles, on_delete=models.SET_NULL, null=True, related_name='users_created')
    #created_by = models.ForeignKey(roles, on_delete=models.CASCADE, related_name='users_with_rolename',null=True)
    status = models.CharField(max_length=12, choices=[('active', 'Active'), ('inactive', 'Inactive')])

    def save(self, *args, **kwargs):
        if not self.created_by:
            self.created_by = self.user_role
        super().save(*args, **kwargs)


    
# SESSION 

class Session(models.Model):
    START_MONTH = [('01', 'January'),('07', 'July'),]
    END_MONTH = [('05', 'May'),('12', 'December'),]
    
    start_year = models.PositiveIntegerField()
    end_year = models.PositiveIntegerField()
    start_month = models.CharField(max_length=3, choices=START_MONTH)
    end_month = models.CharField(max_length=3, choices=END_MONTH)
    session_code = models.CharField(primary_key = True,max_length=6, unique=True, editable=False)

    def save(self, *args, **kwargs):
        # Generate the session_code as a combination of start_year and start_month
        self.session_code = f'{self.start_year}{self.start_month}'
        super(Session, self).save(*args, **kwargs)

    def __str__(self):
        return f'{self.start_month} {self.start_year} - {self.end_month} {self.end_year}'
 
#   Programme_Level

class Programme_Level(models.Model):
    Prog_Level_CHOICES = [('UG', 'UG'),('PG', 'PG')]
    STATUS_CHOICES = [('active', 'Active'),('inactive', 'Inactive'),]
    prog_level_id = models.AutoField(primary_key=True)
    prog_level_name = models.CharField(unique=True,max_length=10, choices=Prog_Level_CHOICES)
    prog_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    

    def __str__(self):
        return self.prog_name

# Semester
class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True)
    semester_name = models.CharField(max_length=255, unique=True)
    # semester_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.semester_name    

# Programs (BBA)
class Program(models.Model):
    program_id = models.AutoField(primary_key=True)
    program_name = models.CharField(max_length=255)
    program_code = models.CharField(max_length=10, unique=True)
    prog_level = models.ForeignKey(Programme_Level, on_delete=models.CASCADE,null=True,default=None)

    def __str__(self):
        return self.program_name
    
class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255, unique=True)
    subject_code = models.CharField(max_length=10, unique=True)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)


    def __str__(self):
        return self.subject_name
        

# Slots

class Slot(models.Model):
    slot_id = models.AutoField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    slot_created = models.CharField(max_length=11, editable=False, unique=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE,null=True,default=None)

    def clean(self):
        # Calculate the duration in minutes between start_time and end_time
        duration = (self.end_time - self.start_time).seconds // 60

        # Check if the duration is more than 180 minutes (3 hours)
        if duration > 180:
            raise ValidationErr(('The slot duration cannot be more than 3 hours.'))

    def save(self, *args, **kwargs):
        # Generate the slot_created as a combination of start_time and end_time
        self.slot_created = f'{self.start_time.strftime("%H:%M")}-{self.end_time.strftime("%H:%M")}'
        super(Slot, self).save(*args, **kwargs)


class StudentEnrollment(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE,null=True,default=None)
    student_id= models.AutoField(primary_key=True)
    program_level = models.ForeignKey(Programme_Level, on_delete=models.CASCADE,null=True,default=None)
    student_uid = models.CharField(max_length=11, editable=False, unique=True)
    student_email = models.EmailField(unique=True)
    gender = models.ForeignKey(gender, on_delete=models.CASCADE,null=True,default=None)
    program = models.ForeignKey(Program, on_delete=models.CASCADE)
    subjects = models.ManyToManyField(Subject)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE,null=True,default=None)


    def __str__(self):
        return f"{self.student.user_name} - {self.course.program_name}"


# class SlotBooking(models.Model):
#     slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
#     student = models.ForeignKey(user_table, on_delete=models.CASCADE)  # Assuming user_table is your student table
#     subject = models.ForeignKey(Subject, on_delete=models.CASCADE)  # Adding reference to the Subject model
#     booking_date = models.DateField(auto_now_add=True)
#     is_approved = models.BooleanField(default=1)

#     def __str__(self):
#         return f"{self.slot} - {self.student} - {self.subject}"
