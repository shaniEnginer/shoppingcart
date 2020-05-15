from django.contrib import admin


from .models import (Item ,
           
                OrderItem ,
                Order , 
                BilligAddress ,
                Payment ,
                Coupon , 
                Refund
                                 )




def make_refund_accepted( modeladmin , request , queryset):
    queryset.update( refund_requested =False ,refund_granted=True )


make_refund_accepted.short_descripition = 'update order to refund granted '

class  OrderAdmin(admin.ModelAdmin):


    list_display =[
        'user'  ,
        'orderd', 
        'being_delivered', 
        "received", 
        "refund_requested", 
        "refund_granted" , 
         "billing_address", 
        "payment", 
        "coupon"
    ]


    list_filter =[
        'orderd', 
        'being_delivered', 
        "received", 
        "refund_requested", 
        "refund_granted"
    
    ]
    list_display_links =[
        "billing_address", 
        "payment", 
        "coupon" , 
        'user'
    ]

    search_fields =[
        'user__username' , 
        'ref_code'
    ]

    actions = [make_refund_accepted , ]









admin.site.register(Item)
admin.site.register(OrderItem)
admin.site.register(Order , OrderAdmin)
admin.site.register(BilligAddress)
admin.site.register(Coupon)
admin.site.register(Payment)
admin.site.register(Refund)
