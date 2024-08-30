from django.contrib import admin

from cars.models import Car, BookCar, CarRecommendation

admin.site.register(Car)
admin.site.register(BookCar)
admin.site.register(CarRecommendation)