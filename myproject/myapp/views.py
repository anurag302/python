from .models import *
from rest_framework import viewsets 
from django.http import HttpResponse
from oauthlib.common import generate_token
from rest_framework.response import Response
from django.contrib.auth import authenticate
from django.utils.timezone import now, timedelta
from oauth2_provider.settings import oauth2_settings
from oauth2_provider.models import AccessToken, Application, RefreshToken
from django.core.mail import send_mail

class User_Registration_Viewset(viewsets.ViewSet):

    def create(self, request):
        email = request.data.get('email')
        username=request.data.get('username')
        password = request.data.get('password')
        date_of_birth = request.data.get('date_of_birth')
        blood_group=request.data.get('blood_group')
        mobile=request.data.get('mobile')
        user_type=request.data.get('user_type')
        address=request.data.get('address')
        user = User()
        user.email = email
        user.username=username
        user.mobile=mobile
        user.blood_group=blood_group
        user.set_password(password)
        user.date_of_birth = date_of_birth
        user.user_type=user_type
        user.address=address
        user.save()
        app = Application.objects.create(user=user)
        token = generate_token()
        refresh_token = generate_token()
        expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
        scope = "read write"
        access_token = AccessToken.objects.create(user=user,
                                            application=app,
                                            expires=expires,
                                            token=token,
                                            scope=scope,
                                            )
        print("access token ------->", access_token)
        RefreshToken.objects.create(user=user,
                                    application=app,
                                    token=refresh_token,
                                    access_token=access_token
                                    )
        response = {
            'access_token': access_token.token,
            'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
            'token_type': 'Bearer',
            'refresh_token': access_token.refresh_token.token,
            'client_id': app.client_id,
            'client_secret': app.client_secret
            }
       
        return Response({"response":response})

class User_login_viewset(viewsets.ViewSet):

    def create(self, request):
        username = request.data.get('mobile')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            app = Application.objects.get(user=user)
            token = generate_token()
            refresh_token = generate_token()
            expires = now() + timedelta(seconds=oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS)
            scope = "read write"
            access_token = AccessToken.objects.create(user=user,
                                                application=app,
                                                expires=expires,
                                                token=token,
                                                scope=scope,
                                                )
            print("access token ------->", access_token)
            RefreshToken.objects.create(user=user,
                                        application=app,
                                        token=refresh_token,
                                        access_token=access_token
                                        )
                                        
            response = {
                'access_token': access_token.token,
                'expires_in': oauth2_settings.ACCESS_TOKEN_EXPIRE_SECONDS,
                'token_type': 'Bearer',
                'refresh_token': access_token.refresh_token.token,
                'client_id': app.client_id,
                'client_secret': app.client_secret
                }
            
            return Response({"response":response})
        else:
           return Response({"message":"credentials not matched"})


class Doctor_viewset(viewsets.ViewSet):
    def list(self,request):
        doctors=User.objects.filter(user_type='D')
        
        doctor_list=[]
        for val in doctors:
            doctor_list.append({
                'doctor_name':val.username,
                'email':val.email,
                'mobile':val.mobile,
                'address':val.address,
                'action':'view',
                'id':val.id
            })
        return Response({'list_of_doctor':doctor_list})    

    def retrieve(self,request,pk=None):
        doctor=Education.objects.filter(doctor_associated__id=pk)
        # patients=User.objects.filter(user_type='P')
       
        doctor_details=[]
        for val in doctor:
            doctor_details.append({
               'full_name':val.doctor_associated.username,
               'mobile':val.doctor_associated.mobile,
               'email':val.doctor_associated.email,
               'date_of_birth':val.doctor_associated.date_of_birth,
               'blood_group':val.doctor_associated.blood_group,
               'id':val.doctor_associated.id
            })
        doctors=Education.objects.filter(doctor_associated__id=pk)
        container9=[]
        for value in doctors:
            container9.append({
                'doctor_degree':value.doctor_degree,
                'university':value.university,
                'year':value.year,
                'id':val.doctor_associated.id
            })
        appointments=Appointment.objects.filter(doctor__id=pk)
        container8=[]
        for value in appointments:
            container8.append({
                'patient_name':value.patient.username,
                'email':value.patient.email,
                'mobile':value.patient.mobile,
                'date':value.date,
                'time':value.time,
            }) 
        reports=Documents.objects.filter(doctor__id=pk)
        report=[]
        for val in reports:
            report.append({
                'document_name':val.document_name.url,
                'file_size':val.file_size,
                'upload_date':val.upload_date
            })    
        return Response({'User details':doctor_details,'education_details':container9,'appointment_details':container8,'reports':report})

class Family_viewset(viewsets.ViewSet):
    def list(self,request):
        return Response({'empty':'list'})

    def retrieve(self,request,pk=None):
        family=Family_Member.objects.filter(patient_id__id=pk)
        
        member=[]
        
        for val in family:    
            member.append({
                'id':val.patient_id.id,
            val.member_type:val.member_name
            })
         
        return Response({'family_member':member})

class Patient_viewset(viewsets.ViewSet):

    def list(self,request):

        patients=User.objects.filter(user_type='P')
        family_memb=Family_Member.objects.filter().count()
        patient_list=[]
        for val in patients:
            family_memb=Family_Member.objects.filter(patient_id__id=val.id).count()
            v=str(family_memb)
            patient_list.append({
                'id':val.id,
                'patient_name':val.username,
                'email':val.email,
                'date_of_birth':val.date_of_birth,
                'mobile':val.mobile,
                'family_member':v,
                'action':'view'
            })
        return Response({'list_of_patient':patient_list})
    
    def retrieve(self,request,pk=None):
        patient=User.objects.filter(id=pk)
        patient_details=[]
        for val in patient:
            patient_details.append({
               'full_name':val.username,
               'mobile':val.mobile,
               'email':val.email,
               'date_of_birth':val.date_of_birth,
               'blood_group':val.blood_group,
               'address':val.address
            }) 
        family=Family_Member.objects.filter(patient_id__id=pk)
        member=[]
        for val in family:
            member.append({
            val.member_type:val.member_name
            })
        
        appointment_list=Appointment.objects.filter(patient__id=pk)
        record=[]
        for val in appointment_list:
            record.append({
                'appointment_of_'+val.patient.username+'_with':val.doctor.username,
                'date':val.date,
                'appointment_id':val.id
            })
        
        reports=Documents.objects.filter(doctor__id=pk)
        report=[]
        for val in reports:
            report.append({
                'document_name':val.document_name.url,
                'file_size':val.file_size,
                'upload_date':val.upload_date
            })
        return Response({'patient_detail':patient_details,'family_member':member,'appointment_details':record,'reports':report})

class Appointment_viewset(viewsets.ViewSet): 
    def list(self,request):
        appointee=Appointment.objects.filter(patient__user_type='P')
        lists=[]
        for val in appointee:
            lists.append({ 
                'patient_name':val.patient.username,
                'email':val.patient.email,
                'date_of_birth':val.patient.date_of_birth,
                'mobile':val.patient.mobile,
                'got_id':val.patient.id,
                'id':val.id,
                'action':'view'
            })
        return Response({'appointment_list':lists})

    def retrieve(self,request,pk=None):
        appointees=Appointment.objects.filter(patient__user_type='P',id=pk)
        container=[]
        for appointee in appointees:
            container.append({
                 'patient_name':appointee.patient.username,
                 'email':appointee.patient.email,
                 'mobile':appointee.patient.mobile,
                 'date_of_birth':appointee.patient.date_of_birth,
                 'got_id':appointee.patient.id
            }) 
        doctors=Appointment.objects.filter(patient__user_type='P',id=pk)
        container2=[]
        for val in doctors:
            container2.append({
              'doctor_name':val.doctor.username,
              'email':val.doctor.email,
              'mobile':val.doctor.mobile,
              'fees':val.charges
            })
        appointment=Appointment.objects.filter(patient__user_type='P',id=pk)
        
        container3=[]
        
        for val in appointment:
            container3.append({
            'speciality':val.plan_procedure,
            'date':val.date,
            'time':val.time,
            'status':val.status,
            'reason_for_consultation':val.add_notes
            })
        return Response({'patient_details':container,'doctor_details':container2,'appointment_details':container3})


    def create(self,request):
        date=request.data.get('date')
        time=request.data.get('time')
        doctor_name=request.data.get('doctor_name')
        planned_procedure=request.data.get('plan_procedure')
        add_notes=request.data.get('add_notes')
        charges=request.data.get('charges')
        status=request.data.get('status')
        patient=request.data.get('patient')
        appointee=Appointment()
        appointee.date=date
        appointee.time=time
        appointee.doctor_name=doctor_name
        appointee.plan_procedure=planned_procedure
        appointee.patient=patient
        appointee.status=status
        appointee.doctor_name=doctor_name
        appointee.charges=charges
        appointee.add_notes=add_notes
        appointee.save()
        return Response({'created':'successfully'})

    def update(self,request,pk=None):
        patient_name=request.data.get('patient')
        date=request.data.get('date')
        time=request.data.get('time')
        application=Appointment()
        application.patient=patient_name
        application.date=date
        application.time=time
        application.save()
        return Response({'updated':'successfully'})

    def destroy(self,response,pk=None):
        appointment=Appointment.objects.filter(id=pk)
        appointment.delete()
        return Response({'deleted':'successfully'})

#class Liveconsultancy_viewset(viewsets.ViewSet):
    #def list(self,request):
      #  consulting_person=LiveConsultancy.objects.all()
       # persons=[]
       # for val in consulting_person:
         #   persons.append({          
          #      'username':val.user.username,
            #    'speciality':val.speciality,
            #    'date':val.contact_date,
            #    'time':val.contact_time,
             #   'mobile':val.user.mobile,
             #   'call_type':val.call_type,
              #  'doctor_name':val.doctor.username,
              #  'patient_id':val.user.id,
              #  'status':val.status,
               # 'charges':val.charges,
              #  'my_id':val.id,
              #  'action':'view'
             #    })
        #return Response({'consultancies':persons})
    
   # def retrieve(self,request,pk=None):
     #   appointees=LiveConsultancy.objects.filter(id=pk) 
    #    container=[]
     #   container2=[]
      #  for appointee in appointees:
         #   container.append({
          #       'patient_name':appointee.user.username,
           #      'email':appointee.user.email,
            #     'mobile':appointee.user.mobile,
           #      'date_of_birth':appointee.user.date_of_birth,
            #     'gender':appointee.gender,
            #     'address':appointee.user.address,
             #    'got_id':appointee.user.id
            #})
           # if appointee.doctor is not None:
             #   physician=Diagonastic.objects.filter(id=pk)               
              #  for val in physician:
              #      container2.append({
               #      'doctor_name':val.doctor.username,
               #      'email':val.doctor.email,
                  #   'mobile':val.doctor.mobile,
                  #   'experience':'5.5',
                 #    'hospital_name':'fortis',
                  #   'fees':val.charges
                 #    }) 
       # details=LiveConsultancy.objects.filter(id=pk)
       # container3=[]
       # for val in details:
           # container3.append({
           #     'speciality':val.speciality,
           #     'date':val.contact_date,
           #     'time':val.contact_time,
            #    'mobile':val.user.mobile,
            #    'call_type':val.call_type,
            #    'doctor_name':val.doctor.username,
             #   'status':val.status,
             #  'charges':val.charges,
             #   'got_id':val.user.id,
          #  })
      #  return Response({'patient_details':container,'doctor_details':container2,'consultancy_details':container3})
     
   # def update(self,request,pk=None):
     #   req_obj=LiveConsultancy.objects.filter(id=pk)
     #   if req_obj.doctor is not None:
     #       doctor=request.data.get('doctor')
     #       live_obj=LiveConsultancy()
     #       live_obj.doctor=doctor
      #      live_obj.save()
      #  return Response({'updated':'successfully'})    



class Diagonastic_viewset(viewsets.ViewSet):
    def list(self,request):
        diagonast=Diagonastic.objects.all().order_by('-id')
        details=[]
        for detail in diagonast:
            details.append({
             'id':detail.patient.id,
             'test':detail.test,
             'date':detail.date,
             'time':detail.time,
             'address':detail.patient.address,
             'username':detail.patient.username,
             'mobile':detail.patient.mobile,
             'charges':detail.charges
            })
        return Response({'detail':details})    

    def retrieve(self,request,pk=None):
        appointees=Diagonastic.objects.filter(patient__user_type='P',id=pk) 
        container=[]
        container2=[]
        for appointee in appointees:
            container.append({
                 'patient_name':appointee.patient.username,
                 'email':appointee.patient.email,
                 'mobile':appointee.patient.mobile,
                 'date_of_birth':appointee.patient.date_of_birth,
                 'address':appointee.patient.address,
                 'got_id':appointee.patient.id
            }) 
            if appointee.doctor is not None:
                physician=Diagonastic.objects.filter(id=pk)               
                for val in physician:
                    container2.append({
                     'doctor_name':val.doctor.username,
                     'email':val.doctor.email,
                     'mobile':val.doctor.mobile,
                     'experience':'5.5',
                     'hospital_name':'fortis',
                     'fees':val.charges
                     }) 
        physician=Diagonastic.objects.filter(patient__id=pk) 
        container3=[]
        grand_total=0
        for val in physician:
            grand_total=grand_total+val.charges
            container3.append({
            'test_name':val.test,
            'date':val.date,
            'time':val.time,
            'charges':val.charges
            })
        response={'grand_total':grand_total}    
        return Response({'patient_details':container,'doctor_details':container2,'test_details':container3,'grand_total':response})


class Pharmacy_viewset(viewsets.ViewSet):
    def list(self,request):
        user_lists=Pharmacy.objects.all()
        user_list=[]
        for val in user_lists:
            user_list.append({
              'id':val.patient2.id,  
              'medicine_name':val.medicine_name,
              'username':val.patient2.username,
              'email':val.patient2.email,
              'mobile':val.patient2.mobile,
              'charges':val.charges
            })
        return Response({'pharmacy_details':user_list})
    



# related name concept
class Nurse_viewset(viewsets.ViewSet):
    def list(self,request):
        containerx=[]
        nar=Nurse.objects.all()
        for val in nar:
            for val2 in val.nurse.all():
                containerx.append({
                  'care_type':val2.care_type
                })
        return Response({"care_type":containerx})


    def create(self,request):
        name=request.data.get('name')
        email=request.data.get('email')
        phone_no=request.data.get('phone')
        experience=request.data.get('experience')
        hospital=request.data.get('hospital')
        charges=request.data.get('charges')
        nurse=Nurse()
        nurse.name=name
        nurse.email=email
        nurse.phone=phone_no
        nurse.experience=experience
        nurse.hospital=hospital
        nurse.charges=charges
        nurse.save()
        return Response({"created":"successfully"})


class nursing_Viewset(viewsets.ViewSet):
    def list(self,request):
        nurse=Nursing.objects.all()
        nurses=[]
        for val in nurse:
            nurses.append({   
                'patient_id':val.patient.id,       
                'username':val.patient.username,
                'address':val.patient.address,
                'nurse_name':val.nurse.name,
                'care_type':val.care_type,
                'mobile':val.patient.mobile,
                'timing':val.timing,
                'days':val.days,
                'start_date':val.start_date,
                'end_date':val.end_date,
                'charges':val.charges
                 })
        return Response({"nurse_list":nurses})
       
    def retrieve(self,request,pk=None):
        nurse=Nursing.objects.filter(id=pk)
        nurses=[]
        container2=[]
        for val in nurse:
            nurses.append({   
                'patient_id':val.patient.id,       
                'username':val.patient.username,
                'address':val.patient.address,

                'nurse_name':val.nurse.name,
                'care_type':val.care_type,
                'mobile':val.patient.mobile,
                'timing':val.timing,
                'charges':val.charges
                 })
            if  val.patient.id is not None:
                nurse_details=Nursing.objects.filter(id=pk)               
                for val in nurse_details:
                    container2.append({
                     'nurse_name':val.nurse.name,
                     'email':val.nurse.email,
                     'mobile':val.nurse.phone,
                     'experience':val.nurse.experience,
                     'hospital_name':val.nurse.hospital_name,
                     'fees':val.nurse.charges
                     }) 
        
        nursing_details=Nursing.objects.filter(id=pk)
        container3=[]
        for val in nursing_details:
            container3.append({
              'care_type':val.care_type,
              'nature_of care':val.nature_of_care,
              'timing':val.timing,
              'days':val.days,
              'start_date':val.start_date,
              'end_date':val.end_date,
              'nursing_charge':val.charges
            })
        return Response({"user_details":nurses,"nurse_details":container2,'Nursing_details':container3})

class speciality_viewset(viewsets.ViewSet):
    def list(self,request):
        object1=Speciality.objects.filter()
        containery=[]
        for val in object1:
            containery.append({
                'speciality':val.speciality
            })
        return Response({'specialities':containery})    
    
    def create(self,request):
        speciality=request.data.get('speciality')
        special=Speciality()
        special.speciality=speciality
        return Response({'created':'successfully'}) 

    def destroy(self,response,pk=None):
        object1=Speciality.objects.filter(id=pk)
        object1.delete()
        return Response({'destroyed':'successfully'})

class subset_viewset(viewsets.ViewSet):
   def create(self,request):
       test=request.data.get('test')
       subtestx=request.data.get('subtest')
       tes=subtest()
       tes.test=test
       tes.subtest=subtest
       return Response({'created':'successfully'})



class fees_viewset(viewsets.ViewSet):
    def list(self,request):
        object1=Fees.objects.all()
        containerz=[]
        for val in object1:
            containerz.append({
            'fess':val.fees,
            'charges':val.charges
            })
        return Response({'list':containerz})

    def create(self,request):
        fees=request.data.get('fees')
        charges=request.data.get('charges')
        fee=Fees()
        fee.charges=charges
        fee.fees=fees
        fee.save()
        return Response({'created':'successfully'}) 

    def destroy(self,response,pk=None):
        object1=Speciality.objects.filter(id=pk)
        object1.delete()
        return Response({'destroyed':'successfully'})

class Digonast_viewset(viewsets.ViewSet):
    def list(self,request):
        dignastic=Digonast.objects.filter()
        containerp=[]
        for itera in dignastic:
            containerp.append({
            'id':itera.id,
            'test':itera.test,
            'test_amount':itera.test_amount
            })
        return Response({'Diagonast':containerp})
    
    def retrieve(self,request,pk=None):
        dia_object=Digonast.objects.filter(id=pk)
        print(dia_object[0].test_name)
        dia_box=[]
        sub_obj=subtest.objects.filter(test__test_name=dia_object[0].test_name)
        for itr in sub_obj:
            dia_box.append({
                'subtest':itr.subtest,
                'charges':itr.charges
            })          
        return Response({dia_object[0].test_name:dia_box})

    def create(self,request):
        test=request.data.get('test')
        amount=request.data.get('test_amount')
        t1=Digonast()
        t1.test=test
        t1.test_amount=amount
        t1.save()
        return Response({'created':'successfully'})
    
    def destroy(self,response,pk=None):
        object1=Digonast.objects.filter(id=pk)
        object1.delete()
        return Response({'destroyed':'successfully'})

class hospital_viewset(viewsets.ViewSet):
    def list(self,request):
        hospital_list=Hospital.objects.all()
        hospitals1=[]
        for hospital in hospital_list:
            hospitals1.append({
                'id':hospital.id,
                'hospital_name':hospital.hospital_name,
                'enter_specialisation':hospital.enter_specialisation,
                'clinical_phone_no':hospital.clinic_phone_no
                })     
            hospitals1.append({
                  'address_line1':hospital.address_line1,
                  'country':hospital.select_country,
                  'state':hospital.select_state,
                  'city':hospital.s