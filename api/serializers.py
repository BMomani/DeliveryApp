from abc import ABC

from rest_framework import serializers
from api.models import Customer, Agent, CustomerProfile, AgentProfile, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        depth = 1
        fields = ('url', 'id', 'username', 'password', 'first_name', 'last_name', 'email',
                  'is_superuser', 'is_staff', 'role')

    def create(self, validated_data):
        if validated_data['role'] is None:
            validated_data['role'] = User.Role.CUSTOMER

        user = User.objects.create_user(username=validated_data['username'],
                                        email=validated_data['email'],
                                       password= validated_data['password'])
        user.role = validated_data['role']
        user.save()
        return user





class CustomerProfileSerializer(serializers.HyperlinkedModelSerializer):
    # user_url = serializers.HyperlinkedIdentityField(view_name='user-detail')
    # # user = serializers.ReadOnlyField(source='user.id')
    # id = serializers.IntegerField(source='pk', read_only=True)
    # username = serializers.CharField(source='user.username', read_only=True)
    # email = serializers.CharField(source='user.email')
    # first_name = serializers.CharField(source='user.first_name')
    # last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = CustomerProfile
        depth = 1
        fields = '__all__'

    def get_full_name(self, obj):
        request = self.context['request']
        return request.user.get_full_name()

    def update(self, instance, validated_data):
        # retrieve the User
        user_data = validated_data.pop('user', None)
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)

        # retrieve Profile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user.save()
        instance.save()
        return instance


class CustomerSerializer(serializers.HyperlinkedModelSerializer):
    # profile_url = serializers.HyperlinkedIdentityField(
    #     view_name='profile-detail')
    customerprofile = CustomerProfileSerializer()
    class Meta:
        model = Customer
        depth = 1
        # fields = ('url', 'id', 'username', 'first_name', 'last_name', 'email',
        #           'is_superuser', 'is_staff', 'customerprofile')
        exclude =["user_permissions"]


class AgentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Agent
        depth = 1
        # fields = ['url', 'username', 'email', 'agentprofile']
        exclude =["user_permissions"]


class AgentProfileSerializer(serializers.HyperlinkedModelSerializer):
    user_url = serializers.HyperlinkedIdentityField(view_name='agent-detail')

    # user = serializers.ReadOnlyField(source='user.id')
    # id = serializers.IntegerField(source='pk', read_only=True)
    # username = serializers.CharField(source='user.username', read_only=True)
    # email = serializers.CharField(source='user.email')
    # first_name = serializers.CharField(source='user.first_name')
    # last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = AgentProfile
        depth = 1
        fields = ['url', 'user_url', 'name', 'location', 'phone_number', 'availability']

    def get_full_name(self, obj):
        request = self.context['request']
        return request.user.get_full_name()

    def update(self, instance, validated_data):
        # retrieve the User
        user_data = validated_data.pop('agent', None)
        for attr, value in user_data.items():
            setattr(instance.agent, attr, value)

        # retrieve Profile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user.save()
        instance.save()
        return instance


class CustomerProfileSerializer(serializers.HyperlinkedModelSerializer):
    userId = serializers.ReadOnlyField(source='customer.id')
    id = serializers.IntegerField(source='pk', read_only=True)
    username = serializers.CharField(source='customer.username', read_only=True)
    email = serializers.CharField(source='customer.email')
    first_name = serializers.CharField(source='customer.first_name')
    last_name = serializers.CharField(source='customer.last_name')

    class Meta:
        model = CustomerProfile
        depth = 1
        fields = ['url', 'id', 'userId', 'username', 'email', 'first_name', 'last_name', 'location', 'phone_number']

    def get_full_name(self, obj):
        request = self.context['request']
        return request.user.get_full_name()

    def update(self, instance, validated_data):
        # retrieve the User
        user_data = validated_data.pop('customer', None)
        for attr, value in user_data.items():
            setattr(instance.agent, attr, value)

        # retrieve Profile
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.user.save()
        instance.save()
        return instance


from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['role'] = user.role
        return token


# Register Serializer
class RegisterAgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        if validated_data['role'] is None:
            validated_data['role'] = User.Role.CUSTOMER

        user = User.objects.create(email=validated_data['email'],
                                   name=validated_data['name']
                                   )
        user.set_password(validated_data['password'])
        user.save()
        return user
