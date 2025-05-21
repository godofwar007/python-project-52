from django.contrib import admin
from django.urls import include, path

from task_manager.users.views import UserLoginView, UserLogoutView

from .views import home, index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('', home, name='home'),
    path('users/', include('task_manager.users.urls')),
    path('tasks/', include('task_manager.tasks.urls')),
    path('labels/', include('task_manager.labels.urls')),
    path('statuses/', include('task_manager.statuses.urls')),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
]
