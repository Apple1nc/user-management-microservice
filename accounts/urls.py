from django.urls import path
from .views import RegisterView, UserDetailView, LoginView,RootAPIView, send_shop_creation_message # my_data_view
# from accounts import views


app_name = 'accounts'

urlpatterns = [
    path('', RootAPIView.as_view(), name='root-api'),
    path('users/register/', RegisterView.as_view(), name='register'),
    path('users/login/', LoginView.as_view(), name='login'),
    path('users/<int:id>/', UserDetailView.as_view(), name='user-detail'),

    path('publish', send_shop_creation_message, name='publish'),
    # path('publish', my_data_view, name='publish'),
]
