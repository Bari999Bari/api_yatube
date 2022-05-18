from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken import views

from my_api.views import UserViewSet, GroupViewSet,\
    PostViewSet, CommentsDetailAPIView, CommentsListAPIView

router = routers.DefaultRouter()
router.register(r'api/v1/users', UserViewSet)
router.register(r'api/v1/groups', GroupViewSet)
router.register(r'api/v1/posts', PostViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api/v1/api-token-auth/', views.obtain_auth_token),
    path('api/v1/posts/<int:post_id>/comments/',
         CommentsListAPIView.as_view()),
    path('api/v1/posts/<int:post_id>/comments/<int:comment_id>/',
         CommentsDetailAPIView.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    urlpatterns += static(
        settings.STATIC_URL, document_root=settings.STATIC_ROOT
    )
