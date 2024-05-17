from django.urls import path
from .views import *

urlpatterns = [
   path('signup/',Sgnupuser.as_view()),
   path('login/',Userlogin.as_view()),
   path('leave/<int:id>',Leavemanagent.as_view()),
   path('alldata/',Alllist.as_view()),
   path('superuser/',SuperuserLoginView.as_view()),
   path('alluser/',Alluser.as_view()),
   path('updatestatus/',UpdateStatus.as_view()),



]