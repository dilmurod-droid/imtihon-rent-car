from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
import re


class Car(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    image = models.ImageField(upload_to="cars/")
    state = models.CharField(max_length=500)
    car_number = models.CharField(max_length=8)
    car_year = models.IntegerField()
    car_oil = models.CharField(max_length=255)
    price = models.IntegerField()
    views = models.IntegerField(default=0)
    is_active=models.BooleanField(default=True)
    def increment_views(self):
        self.views += 1
        self.save()
    def __str__(self):
        return f"{self.name} - {self.car_number}"

class BookCar(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    car=models.ManyToManyField(Car)
    def __str__(self):
        return f"{self.user} - {self.car}"


class CarRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked_cars = models.ManyToManyField(Car, related_name='recommended_to')

    def __str__(self):
        liked_car_names = ', '.join([car.name for car in self.liked_cars.all()])
        return f"{self.user} likes: {liked_car_names}"