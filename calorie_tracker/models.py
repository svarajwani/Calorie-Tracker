from django.db import models

# Create your models here.
class FoodItem(models.Model):
    id=models.IntegerField(primary_key=True)
    name=models.CharField(max_length=50)
    servingSize=models.CharField(max_length=50)
    servingUnits=models.CharField(max_length=50, default="")
    calories=models.DecimalField(max_digits=5, decimal_places=2)
    numberOfServings=models.DecimalField(max_digits=5, decimal_places=2)
    protein=models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    carbs=models.DecimalField(max_digits=5, decimal_places=2, default=0.0)
    fat=models.DecimalField(max_digits=5, decimal_places=2, default=0.0)


    def __str__(self):
        return self.name


