from django.urls import path
from .views import index, MileageCreateView, login_view, logout, register_view, my_view, other


urlpatterns = [
    path('signup/', register_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout, name='logout'),
    path('', index, name='index'),
    path('create', MileageCreateView.as_view(), name='create'),
    path('my', my_view, name='my_view'),
    path('other', other, name='other')
    
]