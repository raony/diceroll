from django.shortcuts import render
from dicerollapp.forms import NewDiceroll

def home(request):
    return render(request, 'diceroll/home.html', {'form' : NewDiceroll()})