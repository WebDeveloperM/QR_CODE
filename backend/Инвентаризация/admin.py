from django.contrib import admin
from .models import *

# Register your models here.


admin.site.register(Department)
admin.site.register(ComputerAgent)
admin.site.register(ProgramLicense)


@admin.register(Compyuter)
class CompyuterAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'seal_number',
        'departament',
        'warehouse_manager',
        'type_compyuter',
        'motherboard',
        'motherboard_model',
        'CPU',
        'generation',
        'frequency',
        'HDD',
        'SSD',
        'disk_type',
        'RAM_type',
        'RAMSize',
        'GPU',
        'ipadresss',
        'internet',
        'mac_adress',
        'qr_image',
        'joinDate',
        'addedUser',
        'updatedUser',
        'updatedAt',
        'isActive',
    )

    fields = (
        'user',
        'seal_number',
        'departament',
        'warehouse_manager',
        'type_compyuter',
        'motherboard',
        'motherboard_model',
        'CPU',
        'generation',
        'frequency',
        'HDD',
        'SSD',
        'disk_type',
        'RAM_type',
        'RAMSize',
        'GPU',
        'ipadresss',
        'mac_adress',
        'scaner',
        'type_webcamera',
        'model_webcam',
        'program',
        'type_monitor',
        'internet',
        'slug',
        'isActive'
    )

    search_fields = ('seal_number', 'departament')

    def save_model(self, request, obj, form, change):
        if not obj.addedUser:
            obj.addedUser = request.user
        super().save_model(request, obj, form, change)


admin.site.register(TypeCompyuter)
admin.site.register(WarehouseManager)
admin.site.register(Motherboard)
admin.site.register(MotherboardModel)
admin.site.register(CPU)
admin.site.register(Generation)
admin.site.register(Frequency)
admin.site.register(HDD)
admin.site.register(SSD)
admin.site.register(RAMSize)
admin.site.register(GPU)
admin.site.register(TypeWebCamera)
admin.site.register(DiskType)
admin.site.register(RAMType)
admin.site.register(ModelWebCamera)
admin.site.register(Monitor)
admin.site.register(Printer)
admin.site.register(Scaner)
admin.site.register(Program)
admin.site.register(MFO)
