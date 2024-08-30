from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.shortcuts import render
from rest_framework import status, generics, viewsets
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from cars.models import BookCar, Car, CarRecommendation
from cars.serializers import UserLoginSerializer, BookCarSerializer, UserRegistrationSerializer, CarSerializer, \
    BookCarCreateSerializer, CarCreateSerializer, CarRecommendationSerializer, CarRecommendationCreateSerializer

User = get_user_model()

class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            tokens = serializer.get_tokens(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class UserRegistrationView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        response_data = {
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

class BookCarList(generics.ListAPIView):
    queryset = BookCar.objects.all()
    serializer_class = BookCarSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return BookCar.objects.filter(user=user)
class BookCarCreate(generics.CreateAPIView):
    queryset = BookCar.objects.all()
    serializer_class = BookCarCreateSerializer
    permission_classes = [IsAuthenticated]

class CarList(generics.ListAPIView):
    queryset = Car.objects.filter(is_active=True)
    serializer_class = CarSerializer
    permission_classes = [AllowAny]
class CarDetail(generics.RetrieveAPIView):
    queryset = Car.objects.filter(is_active=True)
    serializer_class = CarSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        obj.increment_views()
        return obj
class CarCreate(generics.CreateAPIView):
    queryset = Car.objects.all()
    serializer_class = CarCreateSerializer
    permission_classes = [IsAuthenticated]
class RecomCarList(generics.ListAPIView):
    queryset = CarRecommendation.objects.all()
    serializer_class = CarRecommendationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if CarRecommendation.objects.filter(user=user).exists():
            return CarRecommendation.objects.filter(user=user)
        else:
            return Car.objects.filter(is_active=True).order_by('-views')
class RecomCarCreate(generics.CreateAPIView):
    queryset = CarRecommendation.objects.all()
    serializer_class = CarRecommendationCreateSerializer
    permission_classes = [IsAuthenticated]