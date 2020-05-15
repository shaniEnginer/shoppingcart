from django.urls import path 

from django.conf import settings

from django.conf.urls.static import static
from .views import (HomeView ,

                ItemDetailView ,
                CheckoutView ,
                add_to_cart ,
                remove_from_cart,
                OrderSummery,
                remove_single_item_from_cart , 
                PaymentView ,
                 Addcupon , 
                 RequestRefundView
                )

# app_name='core'

urlpatterns= [

    path('' ,  HomeView.as_view() , name='home'),
    path('product/<slug>' ,  ItemDetailView.as_view() , name='product-view'),
    path('checkout/' ,  CheckoutView.as_view() , name='checkout-view') ,
    path('add-to-cart/<slug>' ,add_to_cart , name='add_to_cart' ),
    path('remove-from-cart/<slug>' ,remove_from_cart , name='remove_from_cart' ),
    path('order-summery/' ,OrderSummery.as_view() , name='order-summery' ),
    path('remove-item-from-cart/<slug>' ,remove_single_item_from_cart , name='remove-item-from-cart' ) , 
    path('payment/<payment_options>/' , PaymentView.as_view() , name='payment-view'),
    path('add_cupon/' , Addcupon.as_view() , name='add_cupon'), 
    path('request-refund/' , RequestRefundView.as_view() , name='refund')

            ]



if settings.DEBUG:
    urlpatterns += static( settings.MEDIA_URL , document_root = settings.MEDIA_ROOT )