from django import forms
from django.contrib import admin
from django.contrib.admin import AdminSite
from django.db.models import Q

from .models import PhotoList, Persons, Rooms, Reservations, Guests


class GuestsAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'reservation', 'room_num')

    class GuestsForm(forms.ModelForm):
        class Meta:
            model = Guests
            fields = ('last_name', 'reservation', 'count')

        def clean_end(self):
            if self.cleaned_data['start'] > self.cleaned_data['end']:
                raise forms.ValidationError("Указаны не возможные даты")
            elif self.cleaned_data['start'] == self.cleaned_data['end']:
                raise forms.ValidationError("Нельзя забронировать номер на один день, мы же не дешёвый мотель!")
            else:
                return self.cleaned_data['end']

    class PersonsInline(admin.StackedInline):
        model = Persons

    inlines = [PersonsInline]


class ReservationsAdmin(admin.ModelAdmin):
    class Media:
        js = ("price.js",)

    class GuestsInline(admin.StackedInline):
        model = Guests
        # fields = '__all__'

    class ReservationsForm(forms.ModelForm):
        class Meta:
            model = Reservations
            fields = ('start', 'end', 'price', 'room')

        def clean_end(self):
            if self.cleaned_data['start'] > self.cleaned_data['end']:
                raise forms.ValidationError("Указаны не возможные даты")
            elif self.cleaned_data['start'] == self.cleaned_data['end']:
                raise forms.ValidationError("Нельзя забронировать номер на один день, мы же не дешёвый мотель!")
            else:
                return self.cleaned_data['end']

        def clean_room(self):
            resevated = Reservations.objects.all().filter(room=self.cleaned_data['room'], start__range=(
                self.cleaned_data['start'], self.cleaned_data['end']))
            if resevated.count() > 0:
                raise forms.ValidationError(
                    "Этот номер забронирован с " + str(resevated[0].start) + " по " + str(resevated[0].start))

            resevated1 = Reservations.objects.all().filter(room=self.cleaned_data['room'], end__range=(
                self.cleaned_data['start'], self.cleaned_data['end']))
            if resevated1.count() > 0:
                raise forms.ValidationError("Этот номер забронирован до " + str(resevated1[0].end))
            return self.cleaned_data['room']

        def clean_price(self):
            self.cleaned_data['price'] = self.cleaned_data['room'].price * (
                    self.cleaned_data['end'] - self.cleaned_data['start']).days
            return self.cleaned_data['price']

    def save_model(self, request, obj, form, change):
        obj.price = form.cleaned_data['room'].price * (form.cleaned_data['end'] - form.cleaned_data['start']).days
        obj.save()

    inlines = [GuestsInline]
    form = ReservationsForm
    fields = (("start", "end"), "room", "price",)
    readonly_fields = ('price',)


class RoomsAdmin(admin.ModelAdmin):  # Определяет особенности работы с моделью Rooms
    class PhotoListInline(admin.TabularInline):  # Внутренний класс для добовления фотографий номера
        model = PhotoList

    fields = ('title', 'description', 'price')
    list_display = ('title', 'viewPhotolist')
    inlines = [PhotoListInline]


admin.AdminSite.site_header = 'Управение гостиничным комплексом \"Отец Роман\"'  # Сверху в админке будет написано

# регистрация моделей
admin.site.register(Guests, GuestsAdmin)
admin.site.register(Rooms, RoomsAdmin)
admin.site.register(Persons)
admin.site.register(Reservations, ReservationsAdmin)

