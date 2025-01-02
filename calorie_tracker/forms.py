from django import forms

class FoodSearchForm(forms.Form):
    foodName = forms.CharField(label="Enter a food", required=False,
                           widget= forms.TextInput
                           (attrs={
                               'name': 'foodName',
                               'placeholder':'ex. Apple',
                               'required': 'True',
                               'class': "shadow border-black rounded w-full py-2 px-3 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                            }))

class NumberOfServingsForm(forms.Form):
    numberOfServings = forms.DecimalField(label="Number of servings: ", max_digits=5, decimal_places=2, required=False,
                            widget= forms.NumberInput
                           (attrs={
                               'name': 'servings',
                               'placeholder':'ex. 2',
                               'required': 'True',
                               'class': "shadow border-black rounded w-full py-1 px-1 text-gray-700 leading-tight focus:outline-none focus:shadow-outline",
                            }))