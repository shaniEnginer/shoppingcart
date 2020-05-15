from django import forms

COUNTRIES=(

    ( 'P', 'pakistan'), 
    ( 'AF', 'Afghanstan'), 
    ( 'In', 'India'), 

      )
PAYMENT_CHOICES = (
    ('S' , 'Stripe' ), 
    ('P' , 'PayPal' ), 

     )

class CheckOutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class':'form-control' , 
        'placeholder':"1234 Main St", 
        'id':"address"
    }))
    apartment_address = forms.CharField( required =False  , widget=forms.TextInput(attrs={
         'id':"address-2", 
          'class':"form-control", 
          ' placeholder':"Apartment or uite"
    }))
    contries  = forms.ChoiceField( choices = COUNTRIES , widget=forms.Select(attrs={
        'class':'custom-select d-block w-100', 
        'id':'country'
    }))
    zip = forms.CharField(widget=forms.TextInput(attrs={
        "class":"form-control", 
        "placeholder":"Zip code of your state", 
         'id':"zip"
    }))
    same_billing_address = forms.BooleanField(widget=forms.CheckboxInput( ))
    save_info=forms.BooleanField(widget=forms.CheckboxInput( ))
    payment_option = forms.ChoiceField(widget= forms.RadioSelect , choices=PAYMENT_CHOICES)






class CouponForm(forms.Form):
        code = forms.CharField( widget=forms.TextInput(attrs={
            'class':'form-control', 
            'placeholder':'Promocode'
        }) )

class RefundForm(forms.Form):
        ref_code = forms.CharField( widget=forms.TextInput(attrs={
            'class':'form-control', 
            'placeholder':'refrence code'
        }) )

        message = forms.CharField( widget=forms.Textarea( attrs={
            'rows':4, 
                 'class':'form-control', 
            'placeholder':'state your Reaseon here'
        }))
        email = forms.CharField(
            widget=forms.TextInput(attrs={
                   'class':'form-control', 
            'placeholder':'Email'
            })
        )
