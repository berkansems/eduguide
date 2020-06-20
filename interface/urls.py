from django.urls import path

from interface import views

urlpatterns = [
    path('',views.index,name="home"),
    path('login/',views.myLogin,name="my_login"),
    path('signup/',views.mySignup,name="sign_up"),
    path('my_logout/',views.myLogout,name="my_logout"),
    path('order/<str:pk>/',views.order,name="order"),
]