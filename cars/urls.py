from django.urls import path
from . import views


urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path('cars/', views.cars_list, name='cars_list'),
    path('cars/novo/', views.car_create, name='car_create'),
    path('cars/<int:pk>/editar/', views.car_update, name='car_update'),
    path('cars/<int:pk>/excluir/', views.car_delete, name='car_delete'),

    path('vendidos/', views.sold_cars_list, name='sold_cars_list'),
    path('vendidos/nova-venda/', views.sale_create, name='sale_create'),

    path('financeiro/', views.financial_view, name='financial'),

    path('documentacao/', views.documentation_list, name='documentation_list'),
    path('documentacao/novo/', views.document_create, name='document_create'),

    path('estoque/', views.inventory_view, name='inventory'),
    path('configuracoes/', views.settings_view, name='settings_view'),
    path('financeiro/notas/<int:pk>/', views.invoice_document_detail, name='invoice_document_detail'),
]
