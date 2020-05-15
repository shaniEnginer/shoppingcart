#imports @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@


from django.shortcuts import render , get_object_or_404 , redirect
from .models import( 
        
        Item , 
        Order ,
        OrderItem ,
        Payment ,
        BilligAddress ,
        Coupon , 
        Refund
            
        )
from django.views.generic import( 
           
            ListView , 
            DetailView , 
            View
)

from django.contrib.auth.models import User 
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ( 
    CheckOutForm ,
     CouponForm , 
     RefundForm
     )
 
from django.conf import settings
# end-imports @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@




###################################

# STRIPE PAYMENTS

import stripe
stripe.api_key = settings.STRIPE_KEY


###################################


import random
import string

def create_ref_code():
    ''.join(random.choices( string.ascii_lowercase , + string.digits , k=20)) 

class HomeView(ListView):
    model = Item 
    fields ='__all__'
    template_name='home-page.html'
    paginate_by = 10


class OrderSummery( LoginRequiredMixin, View):
    def get(self , *args , **kwargs):
        try:
            order = Order.objects.get(user = self.request.user , orderd = False)
            context={
                'object':order
            }
            return render( self.request , "order-summery.html" , context)
        except  ObjectDoesNotExist:
            messages.warning(self.request , "you dont hav an active ordr")
            # return redirect('order-summery')

        return render( self.request , "order-summery.html"  )




class ItemDetailView(DetailView):
    model = Item
    template_name ='product-page.html'









## ADD TO CART @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@login_required
def add_to_cart(request , slug):
    item = get_object_or_404(Item , slug = slug)
    # user  = User.objects.get(pk=1)
    user  = request.user

    order_item  , _ = OrderItem.objects.get_or_create(item=item , orderd= False , user = user)

    order_qs = Order.objects.filter(user = user , orderd= False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug = item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.warning( request , f" {order_item.item.title} item quantity was Updated to your cart by {order_item.quantity}   ")
            return redirect( 'order-summery')
        else:
            order.items.add(order_item)
            messages.info( request , f"{order_item.item.title} item was added to your cart ")
            return redirect( 'order-summery')
    else:
        orderd_date = timezone.now()
        order = Order.objects.create(user =  user ,orderd_date=orderd_date )
        order.items.add(order_item)
        messages.info( request , f" {order_item.item.title}this item was added to your cart ")
    return redirect('order-summery')




## REMOVE FROM CART @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@login_required
def remove_from_cart(request ,slug):
    user  = request.user
    item = get_object_or_404(Item , slug = slug)

    order_qs = Order.objects.filter(user = user , orderd= False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug = item.slug).exists():            
            order_item = OrderItem.objects.filter(
                        item=item ,
                        orderd= False ,
                        user = user )[0]
            order.items.remove(order_item)  
            messages.info( request , "this item was rmoved from  your cart ")
            return redirect('order-summery')
             
        else:
            messages.warning( request , " order dose not contain this item ")
     
            return redirect('product-view' ,slug=slug)

    else:
        #add a message saying user dosent have an order
        messages.info( request , "You dont have an active order")
        return redirect('product-view' ,slug=slug)






@login_required
def remove_single_item_from_cart(request ,slug):
    user  = request.user
    item = get_object_or_404(Item , slug = slug)

    order_qs = Order.objects.filter(user = user , orderd= False)
    if order_qs.exists():
        order = order_qs[0]
        # check if the order item is in the order
        if order.items.filter(item__slug = item.slug).exists():            
            order_item = OrderItem.objects.filter(
                        item=item ,
                        orderd= False ,
                        user = user )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)  
            messages.info( request , "this item quantity was updated ")
            return redirect('order-summery')
             
        else:
            messages.warning( request , " order dose not contain this item ")
            # add a message saying order dose not contain this item 
            return redirect('product-view' ,slug=slug)

    else:
        #add a message saying user dosent have an order
        messages.info( request , "You dont have an active order")
        return redirect('product-view' ,slug=slug)


class CheckoutView(View):

    def get(self , *args , **kwargs):

        try:
  
            order  = Order.objects.get(user = self.request.user , orderd= False)                
            form = CheckOutForm()
            context = {
                'form':form, 
                'order':order , 
                'couponform':CouponForm()
            }
            return render(self.request , 'checkout-page.html'  , context)

       
        except ObjectDoesNotExist:
            messages.error(self.request , "You dont have an active order ")
            return redirect('checkout-view'  )



    def post(self , *args , **kwargs):
        form = CheckOutForm(self.request.POST or None)

        try:
            order = Order.objects.get(user = self.request.user , orderd = False)

            # print(form)

            if form.is_valid():
                print("eathy 1")
                street_address = form.cleaned_data.get('street_address')   
                apartment_address = form.cleaned_data.get('apartment_address')   
                contries = form.cleaned_data.get('contries') 
                zip = form.cleaned_data.get('zip')   
                # TODO  Add functionality for these fields 
                same_billing_address = form.cleaned_data.get('same_billing_address')  
                save_info= form.cleaned_data.get('save_info')
                payment_option = form.cleaned_data.get('payment_option')
                print(street_address)
                billing_address = BilligAddress(
                    user = self.request.user, 
                    street_address = street_address, 
                    apartment_address = apartment_address, 
                    contries = contries, 
                    zip = zip )
                billing_address.save()
                order.billing_address = billing_address
                order.save()

                # TODO add a redirect to payment option


                if  payment_option == 'S':
                    messages.info( self.request, "form subbimted")
                    return redirect ('payment-view' , payment_options="stripe" )

                else:
                    return redirect ('payment-view' , payment_option="paypal" )
 
            else:
                print(form.errors)
                print(self.request.POST)
                messages.warning( self.request, "Invalid payment Option")
                return redirect ('checkout-view' )
        
        except  ObjectDoesNotExist:
            messages.warning(self.request , "you dont hav an active ordr")
            return redirect('/')

        









class PaymentView(View):
    def get(self , *args , **kwargs):

        order =Order.objects.get(user = self.request.user , orderd = False)

        context = {
            'order':order
        }
        return render(self.request , 'payment.html' , context)


    def post(self , *args , **kwargs):
        token = self.request.POST.get('stripeToken')
        order =Order.objects.get(user = self.request.user , orderd = False)
        amount =  int(order.get_total() *100)      
        try:
            print(token)
            print(amount)
            charge = stripe.Charge.create(
            amount=amount,
            currency="usd",
            source=token,
            )


        
            #  save the payment 
            payment =  Payment()
            payment.stripe_charge_id = charge.id
            payment.user = self.request.user
            payment.amount = order.get_total() 
            payment.save()

            #  assign the payment to the Order 



            order_items = order.items.all()
            order_items.updated(orderd = True)
            for item  in order_items:
                item.save()







            order.orderd =True
            order.payment = payment
            order.ref_code =create_ref_code
            order.save()
            messages.success(self.request ,  " your order was successfull ")
            return redirect('/')
        except stripe.error.CardError as e:
            # Since it's a decline, stripe.error.CardError will be caught

            body  = e.json_body()
            err = body.get('error' , {})
            messages.error( self.request , f"{err.get('message')}")


            # print('Status is: %s' % e.http_status)
            # print('Type is: %s' % e.error.type)
            # print('Code is: %s' % e.error.code)
            # print('Param is: %s' % e.error.param)
            # print('Message is: %s' % e.error.message)

        except stripe.error.RateLimitError as e:
            messages.error( self.request , "Rate Limmit error ")
            return redirect('/')


        except stripe.error.InvalidRequestError as e:
            messages.error( self.request , f"Invalid parms")
            return redirect('/')



        except stripe.error.AuthenticationError as e:
            messages.error( self.request , f" Not authenticated ")
            return redirect('/')


        except stripe.error.APIConnectionError as e:
            messages.error( self.request , f"Network erro")
            return redirect('/')


        except stripe.error.StripeError as e:
            messages.error( self.request , f"Somethig went wrong , you were not charged , Please try again")
            return redirect('/')


        except Exception as e:
        # Something else happened, completely unrelated to Stripe
            messages.error( self.request , "Some serious error has been occured we have been notified")
            return redirect('/')





def get_coupon_shortcut(request  , code):


    try:
         coupon = Coupon.objects.get(code = code)

        
    except ObjectDoesNotExist:
        messages.error(request , "ivalid coupon ")
        return redirect('checkout-view'  )
    
    return coupon

class Addcupon(View):


    def post( self   , *args , **kwargs):

        form =  CouponForm(self.request.POST , None)
        if form.is_valid():

            try:
                code = form.cleaned_data.get('code')

                order  = Order.objects.get(user = self.request.user , orderd= False)
                order.coupon =  get_coupon_shortcut(request = request , code = code)
                order.save()

                messages.success(self.request , "Successfully Added Coupon  ")
                return redirect('checkout-view')

            
            except ObjectDoesNotExist:
                messages.error(self.request , "You dont have an active order ")
                return redirect('checkout-view'  )


 





class RequestRefundView(View):

    def post(self , *args , **kwargs):
        form = RefundForm( self.request.POST  or None)

        if form.is_valid():
            code  = form.cleaned_data.get('ref_code')
            message  = form.cleaned_data.get('message')
            email  = form.cleaned_data.get('email')
            try:
                order = Order.objects.get( ref_code = code)
                order.refund_requested = True
                order.save()
                
                refund = Refund()
                refund.order = order
                refund.reason = message
                refund.email = email
                refund.save()

                messages.warning( self.request , " your request was received    ")
                return redirect("refund")

            except ObjectDoesNotExist:
                messages.warning( self.request , " invalid refrenec code    ")
                return redirect("refund")





    def get(self ,*args , **kwargs ):


        form =RefundForm()
        context={
            'form':form
        }

        return render(self.request , 'request_refund.html' , context)
        














































































# def ProductView(request):
#     return render(request , 'product-page.html' ,{})



# def HomeView(request):
#     context ={ 'items':Item.objects.all()}
#     # print(Item.objects.all())
#     return render(request , 'home-page.html' ,context)
