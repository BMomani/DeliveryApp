from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from api import views
from api.views import LoggedUserProfileView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'customers', views.CustomerViewSet)
router.register(r'agents', views.AgentViewSet)
router.register(r'agent-profiles', views.AgentProfileViewSet)
router.register(r'customer-profiles', views.CustomerProfileViewSet)
# router.register(r'api/loggedInUserProfile', views.LoggedUserProfileView)
# router.register(r'agents/:id/profile', views.AgentP)
# router.register(r'profiles', views.ProfileViewSet)
# router.register(r'profiles', views.ProfileViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/loggedInUserProfile', LoggedUserProfileView.as_view())

]
