from django.contrib import admin
from .models import Board

# Register your models here.
class BoardAdmin(admin.ModelAdmin):
    pass
    def __str__(self):
        list_display=('idx','ip')
        return self.idx

admin.site.register(Board, BoardAdmin)