from django.urls import include, path
from rest_framework.routers import DefaultRouter

from advertisements import views

router = DefaultRouter()
router.register('advertisements', views.AdvertisementViewSet, basename='advertisement')
router.register('comments', views.CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
]
