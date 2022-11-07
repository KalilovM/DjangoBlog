from django.urls import path, include
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
  path("admin/", admin.site.urls),
  path("api/token/create/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
  path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
  path("api/users/", include("users.urls")),
  path("api/", include("posts.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL,
                                                                         document_root=settings.STATIC_ROOT)
