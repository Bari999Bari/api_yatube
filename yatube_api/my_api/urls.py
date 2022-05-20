from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from my_api.views import UserViewSet, GroupViewSet, PostViewSet, CommentViewSet

app_name = 'my_api'

router = routers.DefaultRouter()
router.register(r'api/v1/users', UserViewSet)
router.register(r'api/v1/groups', GroupViewSet)
router.register(r'api/v1/posts', PostViewSet)
router.register(r'api/v1/posts/(?P<post_id>[0-9]+)/comments',
                CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(router.urls)),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
]
