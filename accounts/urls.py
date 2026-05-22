from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [

    path(
        '',
        views.login_page,
        name='login'
    ),

    path(
        'register/',
        views.register_page,
        name='register'
    ),

    path(
        'dashboard/',
        views.dashboard,
        name='dashboard'
    ),

    path(
        'logout/',
        LogoutView.as_view(next_page='login'),
        name='logout'
    ),
    path('add-product/', views.add_product, name='add_product'),
    path('receiving/', views.receiving_page, name='receiving'),
    path('putaway/', views.putaway_page, name='putaway'),
    path('inventory/', views.inventory_page, name='inventory'),
    path('picking/', views.picking_page, name='picking'),
    path('packing/', views.packing_page, name='packing'),
    path('shipping/', views.shipping_page, name='shipping'),
    path('logout/', views.logout_page, name='logout'),
  
   

]