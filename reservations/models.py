from django.db import models
from django.utils.safestring import mark_safe


class PhotoList(models.Model):
    picture = models.ImageField("Фото")
    room = models.ForeignKey('Rooms', verbose_name="Номер", null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Фотография Номера"
        verbose_name_plural = "Фотографии нормера"


class Rooms(models.Model):
    title = models.CharField("Номер", max_length=35, null=False)
    description = models.TextField("Описание")
    price = models.IntegerField("Цена")
    """viewPhotoList выводит картинки в просмотр"""

    def viewPhotolist(self):
        try:
            return mark_safe(u'<a href="../../../../media/{0}" target="_blank"><img src="../../../../media/{0}" '
                             u'width="120"/></a>'.format(self.photolist_set.all()[0].picture))
        except IndexError:
            return 'Нет фото'

    viewPhotolist.short_description = 'фотографии номера'

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Номер"
        verbose_name_plural = "Номера"


class Reservations(models.Model):
    start = models.DateField("Начало брони")
    end = models.DateField("Конец брони")
    price = models.IntegerField("Цена")
    room = models.ForeignKey(Rooms, verbose_name="Номер", on_delete=models.PROTECT)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = "Бронь"
        verbose_name_plural = "Брони"


class Persons(models.Model):
    name = models.CharField("Имя", max_length=35)
    age = models.PositiveSmallIntegerField()
    family = models.ForeignKey('Guests', verbose_name="Участники", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Человек"
        verbose_name_plural = "Люди"


class Guests(models.Model):
    last_name = models.CharField("Фамилия", max_length=35)
    count = models.PositiveSmallIntegerField("Количество человек")
    reservation = models.OneToOneField(Reservations, verbose_name="Номер брони", on_delete=models.CASCADE)

    def room_num(self):
        return self.reservation.room.description

    def __str__(self):
        return self.last_name

    class Meta:
        verbose_name = "Гость"
        verbose_name_plural = "Постояльцы"

    room_num.short_description = 'Номер'
# Create your models here.
