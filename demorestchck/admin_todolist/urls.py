from django.conf.urls import url
import views

urlpatterns = [

    url(r'^gettodolist$', views.GetTodoList.as_view(), name="gettodolist"),
    url(r'^gettodolist/(?P<todo_list_guid>.*)$', views.GetTodoList.as_view(), name="gettodolist"),
    url(r'^todolistupdate$', views.UpdateTodoList.as_view(), name="todolistupdate"),
    url(r'^todolistupdate/(?P<todo_list_guid>.*)$', views.UpdateTodoList.as_view(), name="todolistupdate"),
]
