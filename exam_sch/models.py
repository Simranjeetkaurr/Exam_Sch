from xml.dom import ValidationErr
from django.db import models
import secrets
import string

def generate_random_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
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
    
    
    # for permission
    # class Meta:
    #     permissions = [
    #         ("can_add_roles", "Can add roles"),
    #         ("can_change_roles", "Can change roles"),
    #         ("can_delete_roles", "Can delete roles"),
    #     ]


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
    session_code = models.CharField(max_length=6, unique=True, editable=False)

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
    prog_id = models.AutoField(primary_key=True)
    prog_name = models.CharField(unique=True,max_length=10, choices=Prog_Level_CHOICES)
    prog_status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    

    def __str__(self):
        return self.prog_name


# Program_type (BBA)
class Program_type(models.Model):
    program_type_id = models.AutoField(primary_key=True)
    program_type_name = models.CharField(max_length=255)
    program_type_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.program_type_name
    
class Subject(models.Model):
    subject_id = models.AutoField(primary_key=True)
    subject_name = models.CharField(max_length=255, unique=True)
    subject_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.subject_name
    
# Semester
class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True)
    semester_name = models.CharField(max_length=255, unique=True)
    # semester_code = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.semester_name    
    

# Slots

class Slot(models.Model):
    slot_id = models.AutoField(primary_key=True)
    start_time = models.TimeField()
    end_time = models.TimeField()
    date = models.DateField()
    slot_created = models.CharField(max_length=11, editable=False, unique=True)

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
