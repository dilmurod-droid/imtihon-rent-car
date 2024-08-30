from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from cars.views import UserLoginView, BookCarList, BookCarCreate, UserRegistrationView, CarList, CarCreate, CarDetail, \
    RecomCarList, RecomCarCreate

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('login/',UserLoginView.as_view(),name='login'),
    path('register/',UserRegistrationView.as_view(),name='register'),
    path('book/car',BookCarList.as_view(),name='book'),
    path('book/car/create', BookCarCreate.as_view(), name='bookcreate'),
    path('car/',CarList.as_view(),name='car'),
    path('car/create', CarCreate.as_view(), name='carcreate'),
    path('car/<int:pk>',CarDetail.as_view(),name='detail'),
    path('car/recommendation',RecomCarList.as_view(),name='recom'),
    path('car/recommendation', RecomCarCreate.as_view(), name='recom-create'),
]