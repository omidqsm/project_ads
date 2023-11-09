from django.urls import path
from djoser.views import UserViewSet

from users.views import LoginView, LogoutView

urlpatterns = [
    # path('', include('djoser.urls')),
    path('me/', UserViewSet.as_view(actions={'get': 'me'}), name='user_me'),
    path('signup/', UserViewSet.as_view(actions={'post': 'create'}), name='signup'),
    path('login/', LoginView.as_view(), name='knox_login'),
    path('logout/', LogoutView.as_view(), name='knox_logout')
]
