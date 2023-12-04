from django.contrib import admin
from .models import *
from import_export.admin import ExportActionMixin
from import_export import resources
import csv


class CartResource(resources.ModelResource):
    class Meta:
        model = Cart
        fields = ('id', 'product', 'user_id', 'quantity',)


@admin.register(BotAdmin)
class BotAdminAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['title', 'user_id', 'created_at', 'updated_at']
    list_filter = ['title', 'user_id', 'created_at', 'updated_at']
    search_fields = ['title', 'user_id', 'created_at', 'updated_at']
    list_per_page = 10
    readonly_fields = ['status', ]


@admin.register(Category)
class CategoryAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['title', 'created_at', 'updated_at']
    search_fields = ['title', 'created_at', 'updated_at']
    list_per_page = 10


@admin.register(Product)
class ProductAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['title', 'description', 'price', 'category', 'image', 'created_at', 'updated_at']
    list_filter = ['title', 'description', 'price', 'category', 'image', 'created_at', 'updated_at']
    search_fields = ['title', 'description', 'price', 'category', 'image', 'created_at', 'updated_at']
    list_per_page = 10


@admin.register(Question)
class QuestionAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['user_id', 'question', 'message_id', 'answer', 'is_answered', 'created_at', 'updated_at']
    list_filter = ['user_id', 'question', 'message_id', 'answer', 'is_answered', 'created_at', 'updated_at']
    search_fields = ['user_id', 'question', 'message_id', 'answer', 'is_answered', 'created_at', 'updated_at']
    list_per_page = 10


from django.contrib import admin
from django.http import HttpResponse
from django.utils.encoding import smart_str
import csv


def export_selected_objects_as_csv(modeladmin, request, queryset):
    # Create response
    response = HttpResponse(content_type='text/xlsx')
    response['Content-Disposition'] = 'attachment; filename=exported_data.xlsx'

    # Create CSV writer
    writer = csv.writer(response, csv.excel)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional for Excel compatibility)
    fieldsss = ['get_catr_products','get_full_carts']
    header_row = [smart_str(modeladmin.model._meta.get_field(field).verbose_name.title()) for field in modeladmin.list_display if field not in fieldsss]+['Carts','Products','Count']
    writer.writerow(header_row)

    for obj in queryset:
        data_row = [smart_str(getattr(obj, field)) for field in modeladmin.list_display if field not in fieldsss]+[smart_str(obj.get_full_carts()),smart_str(obj.get_catr_products()),smart_str(obj.carts.count())]
        writer.writerow(data_row)

    return response


export_selected_objects_as_csv.short_description = "Export selected objects to Exsel"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    actions = [export_selected_objects_as_csv]
    list_display = ['user_id', 'get_full_carts', 'total_price', 'is_paid', 'is_finished', 'name', 'adress',
                    'created_at', 'updated_at']
    list_filter = ['user_id', 'total_price', 'is_paid', 'is_finished', 'name', 'adress', 'created_at', 'updated_at']
    search_fields = ['user_id', 'total_price', 'is_paid', 'is_finished', 'name', 'adress', 'created_at', 'updated_at']
    list_per_page = 10


@admin.register(Cart)
class CartAdmin(ExportActionMixin, admin.ModelAdmin):
    list_display = ['product', 'user_id', 'quantity', 'created_at', 'updated_at']
    list_filter = ['product', 'user_id', 'quantity', 'created_at', 'updated_at']
    search_fields = ['product', 'user_id', 'quantity', 'created_at', 'updated_at']
    list_per_page = 10



