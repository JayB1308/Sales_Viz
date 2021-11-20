from django.urls import path
from . import views
urlpatterns=[
	path('',views.home,name='home'),
	path('about/',views.about,name='about'),
	path('file-upload/',views.upload_file,name='file-upload'),
	path('get-started/',views.get_started,name='get-started'),
	path('dashboard/',views.generate_dashboard,name='dashboard'),
	path('register/',views.create_user,name='register'),
	path('login/',views.login_user,name='login'),
	path('logout/',views.logout_user,name='logout'),

]