from django.urls import path
from panel import views

urlpatterns = [
    path('',views.panel,name='panel'),

    path('branch_add/',views.branchAdd,name='branch_add'),
    path('branch_list/',views.branchList,name='branch_list'),
    path('branch_delete/<str:pk>/',views.branchDelete,name='branch_delete'),
    path('branch_update/<str:pk>/',views.branchUpdate,name='branch_update'),

    path('course_add/',views.courseAdd,name='course_add'),
    path('course_list/',views.courseList,name='course_list'),
    path('course_delete/<str:pk>/',views.courseDelete,name='course_delete'),
    path('course_update/<str:pk>/',views.courseUpdate,name='course_update'),
    path('course_status_update/<str:pk>/',views.courseStatusUpdate,name='course_status_update'),


    path('slider_add/', views.sliderAdd, name='slider_add'),
    path('slider_list/',views.sliderList,name='slider_list'),
    path('slider_delete/<str:pk>/',views.sliderDelete,name='slider_delete'),
    path('slider_update/<str:pk>/',views.sliderUpdate,name='slider_update'),

    path('teacher_add/',views.teacherAdd,name='teacher_add'),
    path('teacher_list/',views.teacherList,name='teacher_list'),
    path('teacher_update/<str:pk>/',views.teacherUpdate,name='teacher_update'),
    path('teacher_delete/<str:pk>/',views.teacherDelete,name='teacher_delete'),

    path('applies/', views.applies, name='applies'),
    path('student_status_accept/<str:pk>/', views.studentStatusAccept, name='student_status_accept'),
    path('student_status_reject/<str:pk>/', views.studentStatusReject, name='student_status_reject'),
    path('student_status_pending/<str:pk>/', views.studentStatusPending, name='student_status_pending'),


]