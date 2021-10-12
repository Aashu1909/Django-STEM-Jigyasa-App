from django.db import models
from django.contrib.auth.models import AbstractUser
from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

# overriding Default django database user using our customUser
class CustomUser(AbstractUser):
    user_data_type=((1,'HOD'),(2,'Staff'),(3,'Student'))
    user_type=models.CharField(default=1 , choices=user_data_type ,max_length=10)

class AdminHOD(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    address=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Staff(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Course(models.Model):
    id=models.AutoField(primary_key=True)
    course_name=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Subject(models.Model):
    id=models.AutoField(primary_key=True)
    subject_name=models.CharField(max_length=200)
    course_id=models.ForeignKey(Course,on_delete=models.CASCADE)
    staff_id=models.ForeignKey(Staff,on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Student(models.Model):
    id=models.AutoField(primary_key=True)
    admin=models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    gender=models.CharField(max_length=10)
    profile_pic=models.FileField()
    address=models.TextField()
    course_id=models.ForeignKey(Course,on_delete=models.DO_NOTHING)
    session_start_year=models.DateTimeField()
    session_end_year=models.DateTimeField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class Attendence(models.Model):
    id=models.AutoField(primary_key=True)
    subject_id=models.ForeignKey(Subject,on_delete=models.DO_NOTHING)
    attendence_date=models.DateField(auto_now_add=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class AttendenceReport(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Student,on_delete=models.DO_NOTHING)
    attendence_id=models.ForeignKey(Attendence,on_delete=models.CASCADE)
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    objects=models.Manager()

class StduentLeave(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    leave_date=models.DateField(auto_now_add=True)
    message=models.TextField()
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    object=models.Manager()

class StaffLeave(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(Staff,on_delete=models.CASCADE)
    leave_date=models.DateField(auto_now_add=True)
    message=models.TextField()
    status=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    object=models.Manager()

class FeedbackStudent(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=200)
    feedback_reply=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    object=models.Manager()

class FeedbackStaff(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(Staff,on_delete=models.CASCADE)
    feedback=models.CharField(max_length=200)
    feedback_reply=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    object=models.Manager() 

class studentNotification(models.Model):
    id=models.AutoField(primary_key=True)
    student_id=models.ForeignKey(Student,on_delete=models.CASCADE)
    message=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    object=models.Manager() 

class staffNotification(models.Model):
    id=models.AutoField(primary_key=True)
    staff_id=models.ForeignKey(Staff,on_delete=models.CASCADE)
    message=models.CharField(max_length=200)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    object=models.Manager() 

class contact(models.Model):
    name = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    email = models.EmailField()
    message = models.CharField(max_length=5000)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)
    object=models.Manager()

# Now creating a signal in django.
# so when a new user is created i will add  a row In HOD,Staff
# student with its id in admin id column


# For creating of user profile
@receiver(post_save, sender=CustomUser)
def created_user_profile(sender,instance,created ,**kwargs):
    # if created==true ie data inserted
    if created:
        # instance is 2 than add data in the Stafftable (data is instance)
        if instance.user_type==1:
            AdminHOD.objects.create(admin=instance)    
        # instance is 2 than add data in the Stafftable (data is instance)
        if instance.user_type==2:
            Staff.objects.create(admin=instance)
        # instance is 3 than add data in the StudentTable (data is instance)
        if instance.user_type==3:
            Student.objects.create(admin=instance)

# for Saving the the created instace user profile
@receiver(post_save, sender=CustomUser)
def save_user_profile(sender,instance, **kwargs):
    if instance.user_type==1:
        instance.adminhod.save()
    
    if instance.user_type==2:
        instance.staff.save()
    
    if instance.user_type==3:
        instance.student.save()

# so all this works when we add new data in custom user after inserting 
# we will add the data into its respective place weather the instance is of HOD 
# staff studnet
