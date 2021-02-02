from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser)
import datetime

class MyUserManager(BaseUserManager):
    def create_user(self,email,username,mobile,blood_group,date_of_birth,address,user_type,is_admin,password=None):
        """
        Creates and saves a User with the given email, date of birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            username=username,           
            mobile=mobile,
            blood_group=blood_group,
            date_of_birth=date_of_birth,
            address=address,
            user_type=user_type,
            is_admin=is_admin   
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,username, mobile,blood_group,email, date_of_birth,address,user_type,is_admin, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            username=username,           
            mobile =mobile,
            blood_group=blood_group,
            date_of_birth=date_of_birth,
            address=address,
            user_type=user_type,
            is_admin=is_admin,
            password=password
        )
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username=models.CharField(max_length=20)
    mobile=models.CharField(max_length=10,unique=True)
    date_of_birth = models.DateField(null=True)
    blood_group=models.CharField(max_length=3)
    differentiate=(
        ('D','Doctor'),('P','Patient'))
    user_type=models.CharField(choices=differentiate,max_length=20,blank=False,default=False)
    address=models.TextField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    
    USERNAME_FIELD = 'mobile'
    REQUIRED_FIELDS = ['date_of_birth','username','email','blood_group','address','user_type','is_admin']

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    
    def has_permission(self, request, view):
        return request.user.is_admin
    
    @property
    def is_staff(self):
        return self.is_admin



class Education(models.Model):
    doctor_associated=models.ForeignKey(User,on_delete=models.CASCADE,limit_choices_to={'user_type': 'D'},unique=False)
    doctor_degree=models.CharField(max_length=20)
    university=models.CharField(max_length=20)
    year = models.DateField()

   # def __str__(self):
       # return str(self.doctor_associated.username)

    # def get_birth_year(self):
    #     return datetime.now().year - self.date_of_birth.year 
    
    # def __str__(self):
    #     return str(self.doctor_associated.username)

class Documents(models.Model):
    doctor=models.ForeignKey(User,on_delete=models.CASCADE,related_name='hello')
    # file_name=models.CharField(max_length=20)
    document_name=models.FileField(upload_to='media/document')
    upload_date=models.DateField(auto_now=True)
    file_size=models.IntegerField(default=0)
    
    #def __str__(self):
     #   return str(self.document_name)
   

class Family_Member(models.Model):
    patient_id=models.ForeignKey(User,on_delete=models.CASCADE,related_name='patient_id',limit_choices_to={'user_type':'P'})
    member_type=(('Father','Father'),('Mother','Mother'),('Brother','Brother'),('Sister','Sister'),('Wife','Wife'))
    member_type=models.CharField(choices=member_type,max_length=25)
    member_name=models.CharField(max_length=30,blank=False)
   # def __str__(self):
   #     return str(self.member_name)



class Appointment(models.Model):
    patient=models.ForeignKey(User,on_delete=models.CASCADE,related_name='patients',limit_choices_to={'user_type':'P'})
    status_choices=(
        ('pend','pending'),
        ('prog','in_progress'),
        ('comp','complete')
    )
    status=models.CharField(max_length=20,choices=status_choices)
    date=models.DateField(auto_now_add=True,null=True)
    time=models.TimeField(auto_now_add=True,null=True)
    charges=models.IntegerField()
    plan_procedure=models.CharField(max_length=20)
    add_notes=models.TextField()
    doctor=models.ForeignKey(User,on_delete=models.CASCADE,related_name='doctor_name',limit_choices_to={'user_type':'D'},)
    
   # def __str__(self):
     #   return str(self.patient)



#class LiveConsultancy(models.Model):
   # user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='user1',limit_choices_to={'user_type':'P'})
   # doctor=models.ForeignKey(User,on_delete=models.CASCADE,related_name='doctor1',limit_choices_to={'user_type':'D'},null=True,blank=True)
    #call_choices=(('video','video'),('audio','audio'))
    #call_type=models.CharField(choices=call_choices,max_length=20,null=False,default='audio')
   # status_choices=(
        ('pend','pending'),
        ('prog','in_progress'),
        ('comp','complete')
    )
   # gender_choices=(('M','male'),('F','female'))
    #gender=models.CharField(choices=gender_choices,max_length=10)
    #status=models.CharField(max_length=20,choices=status_choices)
    #harges=models.IntegerField()
   # speciality=models.CharField(max_length=20,default='dermotologist')
   # contact_date = models.DateField(blank=True)
   # contact_time = models.TimeField( blank=True)
    #reports=models.FileField(upload_to='media/')
    
   # def __str__(self):
      #  return (self.doctor.username)

class Diagonastic(models.Model):
    test=models.CharField(max_length=20,null=False,blank=False)
    patient=models.ForeignKey(User,on_delete=models.CASCADE,related_name='paint',limit_choices_to={'user_type':'P'})
    date = models.DateField(auto_now=True,blank=True)
    time = models.TimeField(auto_now=True,blank=True)
    charges=models.IntegerField()
    reports=models.FileField(upload_to='media/')
    doctor=models.ForeignKey(User,on_delete=models.CASCADE,related_name='jack',limit_choices_to={'user_type':'D'},null=True,blank=True)
    
   # def __str__(self):
     #   return str(self.patient.email)

class Pharmacy(models.Model):
    medicine_name=models.TextField()
    charges=models.IntegerField(default=500)
    patient2=models.ForeignKey(User,on_delete=models.CASCADE,related_name='patient9',limit_choices_to={'user_type':'P'})
    
   # def __str__(self):
    #    return str(self.patient2.username)


class Doctor_at_home(models.Model):
    patient=models.ForeignKey(User,on_delete=models.CASCADE,related_name='patient3',limit_choices_to={'user_type':'P'})        
    doctor=models.ForeignKey(User,on_delete=models.CASCADE,related_name='doctor',limit_choices_to={'user_type':'D'})
    emergencycase=models.BooleanField(default=False,null=False,blank=False)
    charges=models.IntegerField()
    
    #def __str__(self):
     #   return str(self.patient3.username)
class Nurse(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    phone = models.BigIntegerField()
    experience=models.DecimalField(max_digits=2,decimal_places=1)
    hospital_name=models.TextField()
    charges=models.IntegerField()
    
    #def __str__(self):
    #    return str(self.name)

class Nursing(models.Model):
    patient=models.ForeignKey(User,on_delete=models.CASCADE,related_name='pati',limit_choices_to={'user_type':'P'}) 
    nurse=models.ForeignKey(Nurse,on_delete=models.CASCADE,related_name='nurse')
    care_type=models.CharField(max_length=25,null=False)
    timing=models.CharField(max_length=20)
    days=models.TextField()
    start_date=models.DateField()
    end_date=models.DateField()
    nature_of_care=models.TextField()
    charges=models.IntegerField()
    
    #def __str__(self):
     #   return str(self.nurse.name)


class Digonast(models.Model):
    test=models.CharField(max_length=30,unique=True)
    test_name=models.CharField(max_length=20,unique=True)
    test_amount=models.IntegerField(default=400)
    #def __str__(self):
    #    return str(self.test)

class Speciality(models.Model):
    speciality=models.CharField(max_length=30)
    #def __str__(self):
    #    return str(self.speciality)

class subtest(models.Model):
    test=models.ForeignKey(Digonast,on_delete=models.CASCADE,related_name='dignast')
    subtest=models.CharField(max_length=30)
    charges=models.IntegerField(default=600)
   # def __str__(self):
     #   return (self.subtest)

class Fees(models.Model):
    fees=models.CharField(max_length=20)
    charges=models.IntegerField(default=500)
   # def __str__(self):
    #    return str(self.fees)


class Hospital(models.Model):
    hospital_name=models.CharField(max_length=30)
    enter_specialisation=models.CharField(max_length=30)
    clinic_phone_no=models.BigIntegerField()
    address_line1=models.CharField(max_length=20)
    select_country=models.CharField(max_length=20)
    select_state=models.CharField(max_length=20)
    select_city=models.CharField(max_length=20)
    documents=models.FileField(upload_to='media/hospital_documents')
    doctor_hospital=models.ForeignKey(User,on_delete=models.CASCADE,related_name='doctor_appoint')
    doctor_appointment_hospital=models.ForeignKey(Appointment,on_delete=models.CASCADE,related_name='doctor_appointment_hospital') 
    
    #def __str__(self):
    #    return str(self.hospital_name)