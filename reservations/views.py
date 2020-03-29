from django.shortcuts import render
from django.views.generic.base import View
from .models import Rooms, PhotoList
from django import forms

class IndexView(View):
    def get(self, request):
        rooms = Rooms.objects.all()
        return render(request, 'main.html', {'rooms': rooms})


"""
class AddReservationView(View):
    def get(self, request):
        return render(request, 'reserv.html')
    def post(self, request):
        return render(request, 'reserv.html', {'suc'})
"""


def addReservation(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        return render(request, 'result.html', {'name': name})
    else:
        form = ReservationForm()
        return render(request, 'reserve.html', {'form': form})


class ReservationForm(forms.Form):
    name = forms.CharField(label="Имя ", label_suffix="", widget=forms.TextInput(attrs={'class' : 'input'}))
