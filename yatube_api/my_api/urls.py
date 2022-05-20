from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken import views

from my_api.views import UserViewSet, GroupViewSet, PostViewSet, CommentViewSet

app_name = 'my_api'

router = routers.DefaultRouter()
router.register(r'users', UserViewSet,
                basename='user')
router.register(r'groups', GroupViewSet,
                basename='group')
router.register(r'posts', PostViewSet,
                basename='post')
router.register(r'posts/(?P<post_id>[0-9]+)/comments',
                CommentViewSet, basename='comment')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', views.obtain_auth_token),
]
