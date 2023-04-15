from rest_framework import generics, permissions
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from rest_framework.generics import RetrieveAPIView

from api.models import Customer, Agent, AgentProfile, User, CustomerProfile
from api.permissions import (
    IsOwnerOrReadOnly, IsSameUserAllowEditionOrReadOnly
)
from api.serializers import CustomerSerializer, AgentSerializer, AgentProfileSerializer, UserSerializer, \
    RegisterAgentSerializer, MyTokenObtainPairSerializer, CustomerProfileSerializer
from api.utils import get_tokens_for_user


class UserViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = (permissions.IsAuthenticated,)
    # def create(self, request):
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CustomerViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Customer.customer.all()
    serializer_class = CustomerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsSameUserAllowEditionOrReadOnly,)


class AgentViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = Agent.agent.all()
    serializer_class = AgentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsSameUserAllowEditionOrReadOnly,)


class AgentProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = AgentProfile.objects.all()
    serializer_class = AgentProfileSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)


class CustomerProfileViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.

    """
    queryset = CustomerProfile.objects.all()
    serializer_class = CustomerProfileSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,
    #                       IsOwnerOrReadOnly,)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# Register API
class ProfileViewSet(generics.GenericAPIView):
    serializer_class = RegisterAgentSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
            "token": get_tokens_for_user(user).access
        })


class LoggedUserProfileView(generics.GenericAPIView):

    def get(self, request):
        user_profile = None
        availability = True
        try:
            if request.user.role == User.Role.AGENT:
                user_profile = AgentProfile.objects.get_or_create(agent=request.user)
                availability = user_profile.availability
            else:
                user_profile = CustomerProfile.objects.get_or_create(customer=request.user)[0]
            status_code = status.HTTP_200_OK
            response = {
                'first_name': request.user.first_name,
                'last_name': request.user.last_name,
                'email': request.user.email,
                'role': request.user.role,
                "id": user_profile.id,
                'phone_number': user_profile.phone_number,
                'location': user_profile.location,
                'availability': availability
            }
        except Exception as e:
            status_code = status.HTTP_400_BAD_REQUEST
            response = {
                'success': 'false',
                'status code': status.HTTP_400_BAD_REQUEST,
                'message': 'User does not exists',
                'error': str(e)
            }
        return Response(response, status=status_code)
