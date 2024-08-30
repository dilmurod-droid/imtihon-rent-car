import re

from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import Car, BookCar, CarRecommendation
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
User = get_user_model()


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class CarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}  # Ensure 'user' is not required in the input

    def validate(self, attrs):
        pattern = r'^\d{2}[A-Z]\d{3}[A-Z]{2}$'
        car_number = attrs.get('car_number')
        if re.match(pattern, car_number):
            return attrs
        else:
            raise serializers.ValidationError("Davlat raqami noto'g'ri formatda.")

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user  # Automatically get the user from the request
        validated_data['user'] = user
        car = Car.objects.create(**validated_data)
        return car

class BookCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCar
        fields = ['car','user']
class BookCarCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCar
        fields = ['car','user']

    def validate(self, data):
        cars = data.get('car', [])
        for car in cars:
            if not car.is_active:
                raise ValidationError(f"Car with id {car.id} is not available for booking.")
        return data

    def create(self, validated_data):
        cars = validated_data.pop('car')
        bookcar = BookCar.objects.create(**validated_data)
        bookcar.car.set(cars)
        return bookcar
class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','password','email',]
    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.password = make_password(password)
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    return user
                else:
                    raise serializers.ValidationError('User account is disabled.')
            else:
                raise serializers.ValidationError('Invalid login credentials.')
        else:
            raise serializers.ValidationError('Must include "username" and "password".')

    def get_tokens(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
class CarRecommendationCreateSerializer(serializers.ModelSerializer):
    recommended_cars = serializers.SerializerMethodField()

    class Meta:
        model = CarRecommendation
        fields = ['user', 'liked_cars', 'recommended_cars']
class CarRecommendationSerializer(serializers.ModelSerializer):
    recommended_cars = serializers.SerializerMethodField()

    class Meta:
        model = CarRecommendation
        fields = ['recommended_cars']

    def get_recommended_cars(self, obj):
        viewed_cars = Car.objects.filter(views__gte=5)
        recommended_cars = viewed_cars
        return CarSerializer(recommended_cars.distinct(), many=True).data