from django.urls import path, include
from djoser.views import UserViewSet
from knox import views as knox_views

from users.views import LoginView

urlpatterns = [
    # path('', include('djoser.urls')),
    path('me/', UserViewSet.as_view(actions={'get': 'me'}), name='user_me'),
    path('signup/', UserViewSet.as_view(actions={'post': 'create'}), name='signup'),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', knox_views.LogoutView.as_view(), name='knox_logout')
]
