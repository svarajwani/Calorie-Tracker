from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.cache import cache
from fatsecret import Fatsecret
import requests


from .forms import FoodSearchForm, NumberOfServingsForm
from .models import FoodItem

consumer_key =  "02d2b47e52014d1f8e5db815be740d43"
consumer_secret = "252b5f1c78904660b505fa03ae487b60"
fs = Fatsecret(consumer_key, consumer_secret)

def test_keys():
    print(f"API_KEY: {settings.API_KEY}")
    print(f"FATSECRET_KEY: {settings.FATSECRET_KEY}")

# Create your views here.

def index(request):

    results = []
    form = FoodSearchForm(request.GET)
    data = None
    request.session['food_cart'] = []
    if form.is_valid():
        query = form.cleaned_data["foodName"]

        try:
            results = fs.foods_search(query, page_number=1, max_results=15)


        except Exception as error:
            print(error)

    
    return render(request, "search.html", { 'form': form, 'results': results })

#def addFood(request, food_id):


def food(request, food_id):
    food_item = None
    # if not FoodItem.objects.filter(id=food_id).exists():
    #         createFoodItem(request, food_id)

    food_item = fs.food_get(food_id)

    id = food_item["food_id"]

    name = food_item["food_name"]

    serving_data = food_item["servings"]["serving"]
    if isinstance(serving_data, list):
        serving = serving_data[0]
    else:
        serving = serving_data

    servingSize = serving.get("metric_serving_amount", serving.get("serving_description"))
    servingUnits = serving.get("metric_serving_unit", "")
    calories = serving.get("calories")
    protein = serving.get("protein")
    carbs = serving.get("carbohydrate")
    fat = serving.get("fat")
    
    # food_item = FoodItem.objects.get(pk=food_id)
    # food_name = food_item.name
    # food_calories = int(food_item.calories)
    # serving_size = food_item.servingSize
    # serving_units = food_item.servingUnits


    form = form = NumberOfServingsForm(request.POST)

    if request.method == "POST":
        if form.is_valid():
            servings = form.cleaned_data["numberOfServings"]
            createFoodItem(request, food_id, servings)
            try:
                return redirect('totals')
            except Exception as error:
                print(error)

    return render(request, "food.html", 
        {
            'food_name': name, 
            'food_calories': calories, 
            'serving_size': servingSize, 
            'serving_units': servingUnits, 
            'form': form,
            'protein': int(float(protein)),
            'carbs': int(float(carbs)),
            'fat': int(float(fat))
        })

def createFoodItem(request, food_id, servings):
    food_item = fs.food_get(food_id)

    id = food_item["food_id"] 

    name = food_item["food_name"]

    serving_data = food_item["servings"]["serving"]
    if isinstance(serving_data, list):
        serving = serving_data[0]
    else:
        serving = serving_data

    servingSize = serving.get("metric_serving_amount", serving.get("serving_description"))
    servingUnits = serving.get("metric_serving_unit", "")
    calories = serving.get("calories")

    protein = serving.get("protein")
    carbs = serving.get("carbohydrate")
    fat = serving.get("fat")

    food_item_instance, created = FoodItem.objects.update_or_create(
        id=id,
        defaults = {
            'name': name,
            'servingSize': servingSize,
            'servingUnits': servingUnits,
            'calories': calories,
            'numberOfServings': servings,
            'protein': protein,
            'carbs': carbs,
            'fat': fat,
        }
    )

    return HttpResponse("Food item created successfully.")

def totals(request):
    cart = FoodItem.objects.all()
    totalCalories = 0
    totalProtein = 0
    totalCarbs = 0
    totalFat = 0
    for item in cart:
        totalCalories += int(item.calories * item.numberOfServings)
        totalProtein += int(item.protein * item.numberOfServings)
        totalCarbs += int(item.carbs * item.numberOfServings)
        totalFat += int(item.fat * item.numberOfServings)
    # print(cart)
    return render(request, "totals.html", 
        {
            "cart": cart, 
            "totalCalories": totalCalories,
            "totalProtein": totalProtein,
            "totalCarbs": totalCarbs,
            "totalFat": totalFat,
        })

def delete(request, food_id=None):
    object = get_object_or_404(FoodItem, pk=food_id)
    object.delete()
    return redirect('totals')