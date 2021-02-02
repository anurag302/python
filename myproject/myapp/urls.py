from rest_framework import routers
from django.urls import path
from . import views

router=routers.DefaultRouter()
router.register(r'registration', views.User_Registration_Viewset, basename="RegisterUserViewset")
router.register(r'login', views.User_login_viewset, basename="User_login_viewset")
router.register(r'doctor_list',views.Doctor_viewset,basename='doctor_list')
router.register(r'patient_list',views.Patient_viewset,basename='patient_list')
router.register(r'family_members',views.Family_viewset,basename='family_list')
router.register(r'appointment',views.Appointment_viewset,basename='appointment')
router.register(r'live_consultancy',views.Liveconsultancy_viewset,basename='live_consultancy')
router.register(r'diagonastic',views.Diagonastic_viewset,basename='diagonastic')
router.register(r'pharmacy',views.Pharmacy_viewset,basename='pharmacy')
router.register(r'nurse',views.Nurse_viewset,basename='nurses')
router.register(r'nursing',views.nursing_Viewset,basename='nursing')
router.register(r'speciality',views.speciality_viewset,basename='speciality')
router.register(r'fees',views.fees_viewset,basename='fees_view')
router.register(r'dignost',views.Digonast_viewset,basename='dignost')
router.register(r'hospital',views.hospital_viewset,basename='hospital_views')
urlpatterns = router.urls


