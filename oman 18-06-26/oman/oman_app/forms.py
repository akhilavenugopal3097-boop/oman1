from .models import *
from django import forms

class adminform(forms.Form):
    username=forms.CharField(max_length=50)
    password=forms.CharField()


from django.core.exceptions import ValidationError
from .models import CustomUser  # Make sure to import your CustomUser model

class CustomUserRegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email'
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']  # Add email to fields list
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        }

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.lower()
        # Exclude the current user from the uniqueness check
            if CustomUser.objects.filter(username__iexact=username).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            raise ValidationError("Passwords do not match.")
        
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Hash the password
        user.email = self.cleaned_data['email']  # Save the email
        if commit:
            user.save()
        return user


from django import forms
from django.core.exceptions import ValidationError
from .models import CustomUser

class CustomUserProfileForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        label='Email'
    )
    # New: first_name and last_name fields (required)
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        label='First Name'
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        label='Last Name'
    )

    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone', 
            'address', 'dob', 'nationality', 'gender', 'image', 'whatsapp'
        ]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number', 'maxlength': '8', 'pattern': '\d{8}'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Address', 'rows': 3}),
            'dob': forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Date of Birth', 'type': 'date'}),
            'nationality': forms.Select(attrs={'class': 'form-select', 'id': 'nationality'}),
            'gender': forms.Select(attrs={'class': 'form-control'}, choices=[('', 'Select Gender'), ('Male', 'Male'), ('Female', 'Female')]),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'whatsapp': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'WhatsApp Number', 'maxlength': '8', 'pattern': '\d{8}'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make nationality a choice field
        self.fields['nationality'].widget = forms.Select(attrs={'class': 'form-select', 'id': 'nationality'})
        
        # If instance has whatsapp, strip the country code for display
        if self.instance and self.instance.whatsapp:
            initial_whatsapp = self.instance.whatsapp
            # Remove +968 if present
            if initial_whatsapp and initial_whatsapp.startswith('+968'):
                self.initial['whatsapp'] = initial_whatsapp[4:]
            elif initial_whatsapp and initial_whatsapp.startswith('968'):
                self.initial['whatsapp'] = initial_whatsapp[3:]

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = username.lower()
        # Exclude the current user from the uniqueness check
            if CustomUser.objects.filter(username__iexact=username).exclude(pk=self.instance.pk).exists():
                raise ValidationError("A user with this username already exists.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("A user with this email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            cleaned_phone = ''.join(filter(str.isdigit, phone))
            if len(cleaned_phone) != 8:
                raise ValidationError("Phone number must be exactly 8 digits.")
            return cleaned_phone
        return phone

    def clean_whatsapp(self):
        whatsapp = self.cleaned_data.get('whatsapp')
        if whatsapp:
            cleaned_whatsapp = ''.join(filter(str.isdigit, whatsapp))
            if len(cleaned_whatsapp) != 8:
                raise ValidationError("WhatsApp number must be exactly 8 digits.")
            return '+968' + cleaned_whatsapp
        return whatsapp

    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Ensure phone is stored without country code
        if user.phone:
            user.phone = ''.join(filter(str.isdigit, user.phone))
        
        # first_name and last_name are already set by the form's cleaned_data
        # because they are in Meta.fields and we have no custom clean method for them
        
        if commit:
            user.save()
        return user
    
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Username'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )


from django import forms
from django.core.exceptions import ValidationError
from oman_app.models import CustomUser  # Adjusted import to reference your custom user model
from django.contrib.auth.forms import PasswordResetForm

class CustomPasswordResetForm(PasswordResetForm):
    username = forms.CharField(max_length=150, required=True, label="Username")
    
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        username = cleaned_data.get("username")

        # Check if a user with both the email and username exists
        if email and username:
            try:
                user = CustomUser.objects.get(email=email, username=username)  # Use CustomUser model
            except CustomUser.DoesNotExist:
                raise ValidationError("No user found with the provided email and username combination.")
        return cleaned_data

class nearbylocationForm(forms.ModelForm):
    class Meta:
        model = NearbyLocation
        fields = '__all__'

class mainamenitiesForm(forms.ModelForm):
    class Meta:
        model = MainAmenities
        fields = '__all__'

class additionalamenitiesForm(forms.ModelForm):
    class Meta:
        model = AdditionalAmenities
        fields = '__all__'


from django import forms
from .models import Land, NearbyLocation

class LandForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Land
        fields = [
            'property_title', 
            'price', 
            'plot_area', 
            'description', 'payment_method',
            'city',
            'latitude',
            'longitude',
            'images',
            'listing_type',  
            'zoned_for',
            'lister_type',  
            'property_mortgage',
            'facade',
            'rental_period',
            'nearby_location',  # Added nearby locations
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'listing_type': forms.Select(choices=Land.LISTING_TYPE_CHOICES),
        }



class Villaform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Villa
        fields = [
            'property_title', 
            'price', 
            'plot_area',
            'surface_area', 
            'bedrooms','payment_method',
            'bathrooms',
            'description',
            'building',  # Added building age
            'city',
            'latitude',
            'longitude', 
            'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
            'facade',  # Added facade choices
            'furnished',  # Added furnished choice
            'images',
            'listing_type',
            'rental_period',
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'floors',
        ]
        
class categoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__'

class jobcategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategory
        fields = '__all__'

class advertisementForm(forms.ModelForm):
    class Meta:
        model = Advertisement
        fields = '__all__'

class userForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = '__all__'

class regionForm(forms.ModelForm):
    class Meta:
        model = Region
        fields = '__all__'

class GovernateForm(forms.ModelForm):
    class Meta:
        model = Governate
        fields = '__all__'

class DistrictForm(forms.ModelForm):
    class Meta:
        model = District
        fields = '__all__'

class CitiesForm(forms.ModelForm):
    class Meta:
        model = Cities
        fields = '__all__'



class CommercialForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Commercial
        fields = [
            'property_title',
            'price',
            'plot_area',
            'surface_area',
            'description',
            'city',
            'latitude','payment_method',
            'longitude',
           
            'images',
            'listing_type',  # Add this field
            
            'furnished',  # Added furnished choice
            'property',
           
             
            'lister_type',  # Added Agent or Landlord selection
            
            'property_mortgage',  # Added mortgage Yes/No
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'floors',
            
            'rental_period',
        ]

class FarmForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Farm
        fields = [
            'property_title',
            'price',
            'surface_area',
            'plot_area',
            'city',
            'latitude',
            'longitude',
            'description',
            'images',
            'listing_type',  # Add this field
            'bedrooms',
            'bathrooms',
            'building',  # Added building age
            'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
            'facade',  # Added facade choices
            'furnished',  # Added furnished choice
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'rental_period','payment_method',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

class ChaletForm(forms.ModelForm):
    class Meta:
        model = Chalet
        fields = [
            'property_title',
            'price',
            'location',
            'plot_area',
            'bedrooms',
            'bathrooms',
            'description',
            'amenities',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'proximity_to_activities',
            'tenancy_information',
            'contact_details',
            'additional_information',
            'listing_type',  # Add this field
            'images',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'amenities': forms.Textarea(attrs={'rows': 3}),
            'proximity_to_activities': forms.Textarea(attrs={'rows': 3}),
            'contact_details': forms.Textarea(attrs={'rows': 3}),
            'additional_information': forms.Textarea(attrs={'rows': 3}),
        }

class FashionForm(forms.ModelForm):
    class Meta:
        model = Fashion
        fields = [
            'brand', 
            'category', 
            'size', 
            'gender', 
            'color', 
            'material',
            'condition', 
            'price', 
            'location', 
            'description',
            'regions',
             'cities',
             'latitude',
             'longitude',
            'contact_details',  # Assuming you add 'contact_details' field for fashion items
            
            'images',
        ]

class ToysForm(forms.ModelForm):
    class Meta:
        model = Toys
        fields = [
            'category', 
            'product_name',
            'brand', 
            'platform', 
            'age_group', 
            'condition', 
            'price', 
            'location', 
            'images',
            'description',
            'regions',
            'cities',
            'latitude',
            'longitude',
           
        ]

class FoodForm(forms.ModelForm):
    class Meta:
        model = Food
        fields = [
            'product_name',
            'product_type',
            'brand',
            'quantity',
            'expiration_date',
            'price',
            'location',
            'dietary_info',
            'images',
            'description',
            'regions',
            'cities',
            'latitude',
            'longitude',
        ]

class FitnessForm(forms.ModelForm):
    class Meta:
        model = Fitness
        fields = [
            'product_name',
            'category',
            'brand',
            'description',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'condition',
            'price',
            'warranty_status',
            'location',
            'images',
            ]
        
class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['pet_type', 'breed', 'age', 'price', 'vaccinated', 'location', 'images','description','regions','cities','latitude','longitude','pet_name']

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['category', 'genre', 'condition', 'price', 'location', 'images','description',
            'regions',
            'cities',
            'latitude',
            'longitude',
            'book_name',]

class ApplianceForm(forms.ModelForm):
    class Meta:
        model = Appliance
        fields = ['appliance_type', 'brand', 'model_number', 'condition', 'warranty_status', 'price', 'location', 'images','regions','description',
            'cities',
            'latitude',
            'longitude',
            'product_name',]



class BusinessForm(forms.ModelForm):
    class Meta:
        model = Business
        fields = ['category', 'brand', 'condition', 'price', 'warranty_status', 'location', 'description','regions','cities','latitude','longitude','images']
        
class EducationForm(forms.ModelForm):
    class Meta:
        model = Education
        fields = ['course_type', 'subject', 'duration', 'price', 'location', 'instructor_name', 'qualification', 'experience', 'description','regions','cities','latitude','longitude','images']
       

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['service_type', 'provider_name', 'price_range', 'contact_info', 'location', 'description','regions','cities','latitude','longitude','images']

class MobileForm(forms.ModelForm):
  
    class Meta:
        model = Mobile
        fields = [
            'brand', 'model_number', 'year', 'color', 
            'storage_capacity', 'listing_type', 'provide',
            'price', 'condition', 'description', 'city',
            'latitude', 'longitude','images','accompaniments','title',
        ]
        widgets = {
            'color': forms.Select(choices=Mobile.COLOR_CHOICES),
            'listing_type': forms.Select(choices=Mobile.LISTING_TYPE_CHOICES),
            'provide': forms.Select(choices=Mobile.PROVIDE_CHOICES),
            'accompaniments': forms.Select(choices=Mobile.ACCOMPANIMENT_CHOICES),
            'storage_capacity': forms.Select(choices=Mobile.STORAGE_CHOICES),
            'condition': forms.Select(choices=Mobile.condition.field.choices),
        }
       

class TabletForm(forms.ModelForm):
    class Meta:
        model = Tablet
        fields = [
            'brand', 'model_number', 'description',
            'color', 'storage_capacity', 'screen_size','age',
            'listing_type', 'provide', 'price', 'condition',
            'city', 'latitude', 'longitude','accompaniments','title',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }

class SmartWatchForm(forms.ModelForm):
    class Meta:
        model = SmartWatch
        fields = [
            'brand', 'description', 
            'listing_type', 'provide', 'price', 'condition',
            'city', 'latitude', 'longitude','title'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
        }



class HeadsetForm(forms.ModelForm):

    class Meta:
        model = Headset
        fields = [
            'title','description', 'listing_type', 'provide',
            'price', 'condition', 'city', 'latitude', 'longitude',
            'images',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'latitude': forms.HiddenInput(),
            'longitude': forms.HiddenInput(),
        }


class CoverForm(forms.ModelForm):
    class Meta:
        model = Cover
        fields = [
            'title', 'description', 'listing_type', 'provide',
            'price', 'condition', 'city', 'latitude', 'longitude',
            'images', 
        ]
        widgets = {
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Enter description'}),
           
            
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Longitude'}),
            
        }

class AccessoryForm(forms.ModelForm):
    class Meta:
        model = Accessory
        fields = [
            'type', 'title', 'description', 'listing_type', 'provide', 
            'price', 'condition', 'city', 'latitude', 'longitude'  # Add latitude/longitude
        ]
        widgets = {
            'type': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'listing_type': forms.Select(attrs={'class': 'form-control'}),
            'provide': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
        }

class MobileSIMForm(forms.ModelForm):
    class Meta:
        model = MobileSIM
        fields = [
    'operator', 'title', 'description', 'listing_type', 'provide',
    'price', 'city', 'latitude', 'longitude', 
]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
           
        }

        
class CompanyRegistrationForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ['company_name', 'company_type', 'trade_license', 'contact_name', 'logo', 'website', 'description','company_size','email','industry','phone','instagram','youtube','linkedin','facebook',
             'city',
             'latitude',
             'longitude']
    
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
    
    def save(self, commit=True):
        instance = super().save(commit=False)
        if self.user:
            instance.user = self.user  # Assign the logged-in user
        if commit:
            instance.save()
        return instance



class JobPostForm(forms.ModelForm):
    class Meta:
        model = JobPost
        fields = [
            "title", "description", "job_type", "job_category", 
            "salary_range",  "number_of_vacancies", 
            "contact_email", "qualifications", "skills_required", 
            "experience_required", "application_deadline", "experience_required",  # choices dropdown
            "gender",               # choices dropdown
            "nationality",  "working_hours",        # choices dropdown
            "working_days",         # choices dropdown
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
            "qualifications": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "skills_required": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "application_deadline": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "job_type": forms.Select(attrs={"class": "form-select"}),
            "job_category": forms.Select(attrs={"class": "form-select"}),
            "experience_required": forms.Select(attrs={"class": "form-select"}),
            "gender": forms.Select(attrs={"class": "form-select"}),
            "nationality": forms.Select(attrs={"class": "form-select"}),
            "working_hours": forms.Select(attrs={"class": "form-select"}),
            "working_days": forms.Select(attrs={"class": "form-select"}),
           
        }


class JobApplicationForm(forms.ModelForm):
    class Meta:
        model = JobApplication
        fields = ['name', 'email', 'phone', 'resume']
        widgets = {
            'name': forms.TextInput(attrs={
                'id': 'name', 
                'name': 'name', 
                'required': True, 
                'type': 'text'
            }),
            'email': forms.EmailInput(attrs={
                'id': 'email', 
                'name': 'email', 
                'required': True, 
                'type': 'email'
            }),
            'phone': forms.TextInput(attrs={
                'id': 'phone', 
                'name': 'phone', 
                'type': 'text'
            }),
            'resume': forms.ClearableFileInput(attrs={
                'id': 'resume', 
                'name': 'resume', 
                'type': 'file'
            }),
        }
        labels = {
            'name': 'Full Name',
            'email': 'Email',
            'phone': 'Phone Number',
            'resume': 'Upload Resume',
        }



import os
    
class ChatForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']

from datetime import datetime
class CarForm(forms.ModelForm):
    interior_options = forms.ModelMultipleChoiceField(
        queryset=InteriorOptions.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    exterior_options = forms.ModelMultipleChoiceField(
        queryset=ExteriorOptions.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    technology_options = forms.ModelMultipleChoiceField(
        queryset=TechnologyOptions.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Automobile
        fields = [
            'make', 'name', 'year', 'body_type', 'fuel_type',
            'engine_capacity', 'transmission', 'interior_color',
            'exterior_color', 'price', 'listing_type', 'city',
            'latitude', 'longitude', 'description', 'condition',
            'payment_method', 'regional_spec', 'vin_chassis_number',
            'interior_options', 'exterior_options', 'technology_options',
            'rental_period', 'car_license_status', 'insurance_type',
            'horsepower', 'seats', 'warranty', 'cylinders', 'doors',
            'kilometers', 'lister_type','title'
        ]

        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'year': forms.NumberInput(attrs={
                'min': 1900, 
                'max': datetime.now().year + 1,
                'placeholder': 'e.g., 2023'
            }),
            
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'lister_type': forms.Select(attrs={
        'class': 'form-select'
    }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Make fields not required
        optional_fields = [
            'payment_method', 'rental_period', 'vin_chassis_number',
            'engine_capacity', 'horsepower', 'kilometers', 'seats',
            'doors', 'cylinders', 'warranty', 'car_license_status',
            'insurance_type', 'latitude', 'longitude'
        ]
        
        for field in optional_fields:
            self.fields[field].required = False
            
        self.fields['lister_type'].initial = 'dealer'
        
        # Set current year as default for year field
        self.fields['year'].initial = datetime.now().year

    # ---------------------------
    #        VALIDATIONS
    # ---------------------------

    def clean_year(self):
        year = self.cleaned_data.get('year')
        current_year = datetime.now().year
        if year and (year < 1900 or year > current_year + 1):
            raise forms.ValidationError(
                f"Year must be between 1900 and {current_year + 1}"
            )
        return year

    def clean_engine_capacity(self):
        capacity = self.cleaned_data.get('engine_capacity')

        ENGINE_CAPACITY_CHOICES = [
        '0-499', '500-999', '1000-1499', '1500-1999',
        '2000-2499', '2500-2999', '3000-3999',
        '4000-4999', '5000-5999', '6000+'
        ]

        if capacity and capacity not in ENGINE_CAPACITY_CHOICES:
            raise forms.ValidationError("Invalid engine capacity range.")

        return capacity


    def clean_kilometers(self):
        km = self.cleaned_data.get('kilometers')
        return km   # no numeric comparison because value is string


    def clean_vin_chassis_number(self):
        vin = self.cleaned_data.get("vin_chassis_number")
        
        if vin:  # Only validate if not empty
            queryset = Automobile.objects.filter(vin_chassis_number=vin)
            
            # Exclude current instance if updating
            if self.instance and self.instance.pk:
                queryset = queryset.exclude(pk=self.instance.pk)
                
            if queryset.exists():
                raise forms.ValidationError(
                    "This VIN/Chassis Number is already registered."
                )
        return vin

    def clean(self):
        cleaned_data = super().clean()
        listing_type = cleaned_data.get('listing_type')
        rental_period = cleaned_data.get('rental_period')
        payment_method = cleaned_data.get('payment_method')

        # Validate rental fields based on listing type
        if listing_type == 'rent':
            if not rental_period:
                self.add_error('rental_period', 
                    "Rental period is required for rental listings."
                )
        else:
            if rental_period:
                self.add_error('rental_period',
                    "Rental period should only be specified for rental listings."
                )

        return cleaned_data
    
class BikeForm(forms.ModelForm):
    class Meta:
        model = Motorcycle
        fields = [
            'make',  'model', 'year', 'body_type', 
            'engine_capacity', 'price', 'condition', 'description', 
            'payment_method', 'images', 'listing_type',
            'city','lister_type',
            'latitude', 'longitude', 'kilometers','title'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'year': forms.NumberInput(attrs={'min': 1900, 'max': timezone.now().year}),
            'engine_capacity': forms.NumberInput(attrs={'min': 0}),
            
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'body_type': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.RadioSelect(),
            'listing_type': forms.RadioSelect(),
            'lister_type': forms.Select(attrs={
                'class': 'form-select searchable'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required fields
        self.fields['payment_method'].required = False
        self.fields['kilometers'].required = False
        self.fields['city'].required = False
        
    

    def clean_kilometers(self):
        km = self.cleaned_data.get('kilometers')
        return km   # no numeric comparison because value is string


    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be positive")
        return price
    
class ScooterForm(forms.ModelForm):
    class Meta:
        model = Scooter
        fields = [
            'make',  'model', 'year', 
            'engine_capacity', 'price', 'condition', 'description', 
            'payment_method', 'images', 'listing_type',
            'city','lister_type',
            'latitude', 'longitude', 'kilometers','title','fuel_type'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'condition': forms.RadioSelect(),
            'listing_type': forms.RadioSelect(),
            'lister_type': forms.Select(attrs={
                'class': 'form-select searchable'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Set required fields
        self.fields['payment_method'].required = False
        self.fields['kilometers'].required = False
        self.fields['city'].required = False
        
    

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is not None and price <= 0:
            raise forms.ValidationError("Price must be positive")
        return price
  
from django import forms
from .models import HelmetClothes


class HelmetClothesForm(forms.ModelForm):
    class Meta:
        model = HelmetClothes
        fields = [
            'title',
            'helmetcloth_type',
            'listing_type',
            'condition',
            'price',
            'payment_method',
            'rental_period',
            'lister_type',
            'provide_delivery',
            'description',
            'city',
            'latitude',
            'longitude',
        ]

        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Full-Face Helmet'
            }),

            'helmetcloth_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'listing_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            # ✅ DROPDOWN CONDITION
            'condition': forms.Select(attrs={
                'class': 'form-select'
            }),

            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01'
            }),

            'payment_method': forms.Select(attrs={
                'class': 'form-select'
            }),

            'rental_period': forms.Select(attrs={
                'class': 'form-select'
            }),

            'lister_type': forms.Select(attrs={
                'class': 'form-select'
            }),

            'provide_delivery': forms.Select(attrs={
                'class': 'form-select'
            }),

            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3
            }),

            'city': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Conditional fields
        self.fields['payment_method'].required = False
        self.fields['rental_period'].required = False

        # Force empty labels (important for selects)
        self.fields['condition'].empty_label = "Select Condition"
        self.fields['listing_type'].empty_label = "Select Listing Type"
        self.fields['helmetcloth_type'].empty_label = "Select Gear Type"





class CarRepairMaintenanceForm(forms.ModelForm):

    class Meta:
        model = CarRepairMaintenance
        fields = [
            'category', 'title', 'description', 'price',
            'city', 'latitude', 'longitude',
            'images', 
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select'}),
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Describe the service'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price (OMR)'
            }),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Latitude'
            }),
            'longitude': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Longitude'
            }),
        }


class QuadbikesForm(forms.ModelForm):
    class Meta:
        model = Quadbikes
        fields = [
            'description', 'payment_method', 'city',
            'latitude', 'longitude', 
            'price', 'condition',
            'images','types','title'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'required': True}),
            'price': forms.NumberInput(attrs={'step': '0.01', 'required': True}),
            'condition': forms.Select(attrs={'required': True}),
            'city': forms.Select(attrs={'required': False}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['payment_method'].required = False

class JunkCarForm(forms.ModelForm):
    class Meta:
        model = JunkCar
        fields = [
            'name', 'condition', 'price', 'description',
            'city', 'latitude', 'longitude','listing_type'
        ]


class AutoAccessoryPartForm(forms.ModelForm):
    class Meta:
        model = AutoAccessoryPart
        fields = [
            'main_category','sub_category','name','description','city','latitude','longitude',
            'condition', 'payment_method', 'provide','price',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
        }

class HeavyVehicleForm(forms.ModelForm):
    class Meta:
        model = HeavyVehicle
        fields = [
            'name', 'description',  'year', 'price', 'condition',
             'payment_method', 'city', 'latitude', 'longitude',
            'images', 'listing_type', 'main_type', 'sub_type', 'model', 'bus_model','rental_period'
        ]
class BoatForm(forms.ModelForm):
    class Meta:
        model = Boat
        fields = [
            'name', 'description', 
            'boat_type', 'lister_type', 'payment_method',
            'listing_type',  'price', 'condition',
             'city', 'latitude', 'longitude','rental_period',
            'images'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'latitude': forms.NumberInput(attrs={'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'step': 'any'}),
        }
class TiresAndCapsForm(forms.ModelForm):
    class Meta:
        model = TiresAndCaps
        fields = [
            'tire_type', 'size', 'brand', 'description', 'price', 'provide',
            'condition', 'payment_method', 'city', 'latitude', 'longitude','title'
        ]

class NumberPlateForm(forms.ModelForm):
    class Meta:
        model = NumberPlate
        fields = [
            'number', 'price', 'description', 'payment_method',
            'city', 'latitude', 'longitude','listing_type','letter_english', 'letter_arabic', 'plate_type' , 'seller_name','title', 'usage_type',
        ]


from django import forms
from .models import UploadedImage

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = UploadedImage
        fields = ['image']

from django import forms
from .models import DrivingTraining

class DrivingTrainingForm(forms.ModelForm):
    class Meta:
        model = DrivingTraining
        fields = [
            'trainer_name', 'trainer_gender', 'transmission', 'price',
            'body_type', 'model_year', 'description', 'city',
            'latitude', 'longitude',
             'location', 'language', 'about_instructor', 'images','payment_method','title'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'about_instructor': forms.Textarea(attrs={'rows': 3}),
        }

# -------------------------------------------------------------

class ApartmentForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  
        required=False
    )
    class Meta:
        model = Apartment
        fields = [
            'property_title',
            'price',
            'plot_area',
            'city',
            'latitude',
            'longitude',
            'description',
            'property_mortgage',
            'listing_type',
            'floors',
            'images',
            'building',  
            'lister_type',  
            'property_mortgage',  
            'facade', 
            'furnished', 
            'nearby_location',
            'additional_amenities',
            'main_amenities', 
            'bedrooms',
            'bathrooms',
            'rental_period',
            'payment_method',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }

class FactoryForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Factory
        fields = [
            'property_title',
            'price',
            'plot_area',
            'city',
            'latitude',
            'longitude',
            'description',
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'images',
            'rental_period','payment_method',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }




class ComplexForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Complex
        fields = [
            'property_title',
            'price',
            'plot_area',
            'city',
            'latitude',
            'longitude',
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'images',
            'property',
            'surface_area',
            'nearby_location','payment_method',
            'additional_amenities',
            'main_amenities',
            'floors','rental_period',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }

class ClinicForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Clinic
        fields = [
            'property_title',
            'price',
            'plot_area',
            'city',
            'latitude',
            'longitude',
            'furnished', 
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'images',
            'property','payment_method',
            'floors','rental_period',
            ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }

class HostelForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Hostel
        fields = [
            'property_title',
            'price',
            'plot_area',
            'city',
            'latitude',
            'longitude',
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'images',
            'property','payment_method',
            'bedrooms',
            'floors',
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'furnished', 'rental_period',
            
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }



class OfficeForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Office
        fields = [
            'property_title',
            'price',
            'plot_area',
            'city',
            'latitude',
            'longitude',
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'images',
            'property',
            'floors',
            'nearby_location',
            'additional_amenities','payment_method',
            'main_amenities',
            'furnished','rental_period',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }



class ShopForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Shop
        fields = [
            'property_title',
            'price',
            'plot_area',
            'city',
            'latitude',
            'longitude',
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection            
            'images',
            'nearby_location',
            'additional_amenities','payment_method',
            'main_amenities','rental_period',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }

class CafeForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        
        model = Cafe
        fields = [
            'property_title',
            'price',
            'plot_area',
             'city',
             'latitude',
             'longitude',
            
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            
            
            'images',
            'property',           
            'nearby_location','payment_method',
            'additional_amenities',
            'main_amenities','rental_period',      
            
            
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }


class StaffForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Staff
        fields = [
            'property_title',
            'price',
            'plot_area',
             'city',
             'latitude',
             'longitude',
            
            'description',
            'property_mortgage','payment_method',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            
            'images',
            'property',
            'bedrooms',
            
            'floors','rental_period',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }



class WarehouseForm(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Warehouse
        fields = [
            'property_title',
            'price',
            'plot_area',
             'city',
             'latitude',
             'longitude',
            'description',
            'property_mortgage',
            'listing_type',
            'lister_type',  # Added Agent or Landlord selection
            'nearby_location',
            'additional_amenities',
            'main_amenities','payment_method',
            'images',
            'property','rental_period',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            
        }

class Townhouseform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Townhouse
        fields = [
            'property_title', 
            'price', 
            'plot_area', 
            'surface_area', 'payment_method',
            'bedrooms',
            'bathrooms',
            'floors',
            'description',
            'building',  # Added building age
             'city',
             'latitude',
             'longitude', 
              'lister_type',  # Added Agent or Landlord selection
            
            'property_mortgage',  # Added mortgage Yes/No
            'facade',  # Added facade choices
             'furnished',  # Added furnished choice
            'nearby_location',
            'additional_amenities',
            'main_amenities',
             
            'images',
            'listing_type','rental_period',
            
        ]




class Fullfloorsform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Fullfloors
        fields = [
            'property_title', 
            'price', 
            'plot_area', 
            'floors',
            'description',
            'city',
            'latitude',
            'longitude', 
            'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
            'property','payment_method',
            
            'nearby_location',
            'additional_amenities',
            'main_amenities',
            'images',
            'listing_type','rental_period',
            
        ]

class Showroomsform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Showrooms
        fields = [
            'property_title', 
            'price', 
            'plot_area', 
            'description',
             'city',
             'latitude','payment_method',
             'longitude', 
              'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
           'property', 
            'nearby_location',
            'additional_amenities',
            'main_amenities', 
            'images',
            'listing_type','rental_period',
            
        ]
class Wholebuildingform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Wholebuilding
        fields = [
            'property_title', 
            'price', 
            'plot_area',
            'surface_area', 
            'floors',
            'building',  # Added building age
            'nearby_location',
            'description',
            'facade',
           'city',
            'latitude','payment_method',
            'longitude', 
            'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
            'property', 
            'images',
            'listing_type','rental_period',
        ]

class Supermarketform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    main_amenities = forms.ModelMultipleChoiceField(
        queryset=MainAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    additional_amenities = forms.ModelMultipleChoiceField(
        queryset=AdditionalAmenities.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Supermarket
        fields = [
            'property_title', 
            'price', 
            'plot_area', 
            'nearby_location',
            'additional_amenities',
            'main_amenities', 
            'description',
            'city','payment_method',
            'latitude',
            'longitude', 
            'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
            'property',  
            'images',
            'listing_type','rental_period',
            
        ]
class Foreignform(forms.ModelForm):
    nearby_location = forms.ModelMultipleChoiceField(
        queryset=NearbyLocation.objects.all(),
        widget=forms.CheckboxSelectMultiple,  # This allows checkboxes for selection
        required=False
    )
    class Meta:
        model = Foreign
        fields = [
            'property_title', 
            'price', 
            'country', 
            'description',
            'city','payment_method',
            'nearby_location',
            'latitude',
            'longitude', 
            'lister_type',  # Added Agent or Landlord selection
            'property_mortgage',  # Added mortgage Yes/No
            'estate_type',
            'images',
            'listing_type',  'rental_period', 
        ]


class Sharedform(forms.ModelForm):
    
    class Meta:
        model = Shared
        fields = [
            'property_title', 
            'price', 
            
            'description',
           
            'city',
            'latitude','payment_method',
            'longitude', 
            
            'furnished',  # Added furnished choice
            'images',
            'listing_type',
            'rental_period',
            
        ]


class Suitsform(forms.ModelForm):
    
    class Meta:
        model = Suits
        fields = [
            'property_title', 
            'price', 
            
            'description',
           
            'city',
            'latitude',
            'longitude', 'payment_method',
            
            'furnished',  # Added furnished choice
            'images',
            'listing_type',
            'rental_period',
            
        ]

# ------------------------------------------------------Motors------------------------------------------------------------
from django import forms
from .models import Part

class PartForm(forms.ModelForm):
    types = forms.ChoiceField(choices=[
        ('batteries', 'Batteries'),
        ('bodyparts', 'Body Parts'),
        ('mechanical', 'Mechanical Parts'),
        ('spareparts', 'Spare Parts'),
        ('other', 'Other'),
    ], required=True)

    class Meta:
        model = Part
        fields = [
            'name', 'description', 'price', 'regions', 'cities', 'latitude', 'longitude', 
            'provide', 'condition', 'subtype', 'images',
        ]
      

class SportsCarForm(forms.ModelForm):  # Renamed
    class Meta:
        model = SportsCar  # Updated model reference
        fields = [
            'make', 'year', 'description',
            'bodytype', 'top_speed', 'top_speed_unit',
            'acceleration', 'drivetrain',
            'regions', 'cities',
            'rental_period', 'rental_price',
            'horsepower', 'torque',
            'images', 'latitude', 'longitude'
        ]


class interioroptionsForm(forms.ModelForm):
    class Meta:
        model = InteriorOptions
        fields = '__all__'

class exterioroptionsForm(forms.ModelForm):
    class Meta:
        model = ExteriorOptions
        fields = '__all__'

class technologyoptionsForm(forms.ModelForm):
    class Meta:
        model = TechnologyOptions
        fields = '__all__'




# ---------------------------------------------------------------Other Category-----------------------------------------------------------
class ComputerListingForm(forms.ModelForm):
    class Meta:
        model = ComputerListing
        fields = [
            # Common fields
            "category", "description", "listing_type", "condition", "price",
            "city", "latitude", "longitude", "images",
            
            # Category-specific fields
            "brand", "operating_system", "processor_brand", "processor_type",
            "component_type", "component_title",
            "accessory_type",
            "peripheral_brand", "screen_size","title",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
            "city": forms.Select(attrs={'class': 'form-select'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all category-specific fields not required initially
        for field in ['brand', 'operating_system', 'processor_brand', 'processor_type',
                     'component_type', 'component_title', 'accessory_type',
                     'peripheral_brand', 'screen_size']:
            self.fields[field].required = False

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")

        # Validate images
        images = self.files.getlist('images')
        if not images:
            self.add_error('images', 'At least one image is required.')

        # Validate based on category
        if category == "computers":
            required_fields = ["brand", "operating_system", "processor_brand", "processor_type"]
            for field in required_fields:
                if not cleaned_data.get(field):
                    self.add_error(field, f"This field is required for Computers category.")

        elif category == "components":
            if not cleaned_data.get("component_type"):
                self.add_error("component_type", "This field is required for Components.")
            if not cleaned_data.get("component_title"):
                self.add_error("component_title", "This field is required for Components.")

        elif category == "accessories":
            if not cleaned_data.get("accessory_type"):
                self.add_error("accessory_type", "This field is required for Accessories.")

        elif category == "peripherals":
            if not cleaned_data.get("peripheral_brand"):
                self.add_error("peripheral_brand", "This field is required for Peripherals.")
            if not cleaned_data.get("screen_size"):
                self.add_error("screen_size", "This field is required for Peripherals.")

        return cleaned_data
    
class BusinessIndustrialListingForm(forms.ModelForm):
    class Meta:
        model = BusinessIndustrialListing
        fields = [
            "category", "description", "listing_type", "service_type", "price",
            "city", "latitude", "longitude","title",
            "condition", "usage",   # ✅ added new fields
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "price": forms.NumberInput(attrs={"step": "0.01"}),
            "city": forms.Select(attrs={'class': 'form-select'}),
            "condition": forms.Select(attrs={'class': 'form-select'}),  # dropdown
            "usage": forms.Select(attrs={'class': 'form-select'}),      # dropdown
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['service_type'].required = False  # default not required

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        service_type = cleaned_data.get("service_type")

        # Only required for Retail & Services
        if category == "retail_services" and not service_type:
            self.add_error("service_type", "This field is required for Retail & Services.")

        return cleaned_data


BREED_DATA = {
    "cats": ["persian", "siamese", "maine_coon", "ragdoll", "british_shorthair", "sphynx", "bengal", 
             "american_shorthair", "scottish_fold", "oriental_shorthair", "norwegian_forest", 
             "turkish_van", "himalayan", "devon_rex", "exotic_shorthair"],
    "dogs": ["labrador", "german_shepherd", "golden_retriever", "beagle", "bulldog", "pomeranian", 
             "poodle", "rottweiler", "doberman", "shih_tzu", "chihuahua", "husky", "corgi", 
             "dachshund", "boxer"],
}

class PetListingForm(forms.ModelForm):

    accept_exchange = forms.ChoiceField(
        choices=[('', 'Select'), ('True', 'Yes'), ('False', 'No')],
        required=False
    )

    class Meta:
        model = PetListing
        fields = [
            "category", "pet_type", "breed", "name", "age",
            "accessory_type", "condition", "accept_exchange",
            "listing_type", "price", "description",
            "city", "latitude", "longitude","title",
        ]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make all fields not required by default
        for field in self.fields:
            self.fields[field].required = False
        # Except these which are always required
        self.fields['category'].required = True
        self.fields['description'].required = True
        self.fields['city'].required = True
        self.fields['latitude'].required = True
        self.fields['longitude'].required = True

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        pet_type = cleaned_data.get("pet_type")
        listing_type = cleaned_data.get("listing_type")

        # 🔹 Convert accept_exchange string to boolean
        accept_exchange = cleaned_data.get("accept_exchange")
        if accept_exchange == "True":
            cleaned_data["accept_exchange"] = True
        elif accept_exchange == "False":
            cleaned_data["accept_exchange"] = False
        else:
            cleaned_data["accept_exchange"] = None

        # 🔹 Adoption / Lost & Found rules
        if category in ['free_adoption', 'lost_found']:
            for field in ['pet_type', 'name', 'age']:
                if not cleaned_data.get(field):
                    self.add_error(field, f"This field is required for {category.replace('_', ' ')}")

            # Breed required only if pet_type has breed list
            if pet_type and pet_type in BREED_DATA and BREED_DATA[pet_type]:
                if not cleaned_data.get("breed"):
                    self.add_error("breed", "Breed is required for the selected pet type.")

        # 🔹 Accessories rules - FIXED: Changed 'accessories' to 'pet_accessories'
        if category == 'pet_accessories':
            for field in ['accessory_type', 'condition', 'listing_type']:
                if not cleaned_data.get(field):
                    self.add_error(field, f"{field.replace('_', ' ').capitalize()} is required for accessories")

            if listing_type == "sale" and not cleaned_data.get("price"):
                self.add_error("price", "Price is required for accessories listed for sale.")

        return cleaned_data
class SportsListingForm(forms.ModelForm):
    class Meta:
        model = SportsListing
        fields = [
            'category',
            'subcategory',
            'condition',
            'listing_type',
            'price',
            'description',
            'city',
            "latitude", "longitude",
            'images','title',
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'subcategory': forms.Select(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'listing_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price in OMR'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write details here...'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
        }

    def _init_(self, *args, **kwargs):
        super()._init_(*args, **kwargs)
        
class MusicalListingForm(forms.ModelForm):
    PROVIDE_CHOICES = [
        (True, 'Yes'),
        (False, 'No'),
    ]

    provide = forms.ChoiceField(
        choices=PROVIDE_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Provide"
    )

    class Meta:
        model = MusicalListing
        fields = [
            'category', 'subcategory', 'type', 'condition', 'listing_type',
            'age', 'usage', 'condition_detail', 'provide',
            'price', 'description', 'city', 'latitude', 'longitude',
            'images', 
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'category-select'}),
            'subcategory': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specify if category is Other', 'id': 'subcategory-input'}),
            'type': forms.TextInput(attrs={'class': 'form-control'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'listing_type': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.Select(attrs={'class': 'form-control'}),
            'usage': forms.Select(attrs={'class': 'form-control'}),
            'condition_detail': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
           
        }

    def __init__(self, *args, **kwargs):
        super(MusicalListingForm, self).__init__(*args, **kwargs)
        # Make subcategory optional, show only if 'Other' selected
        self.fields['subcategory'].required = False
        self.fields['subcategory'].widget.attrs['style'] = 'display:none;'

class GamingListingForm(forms.ModelForm):
    # Convert provide to a boolean dropdown
    provide = forms.ChoiceField(
        choices=[('True', 'Yes'), ('False', 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Provide?"
    )

    class Meta:
        model = GamingListing
        fields = [
            'category',
            'subcategory',
            'type',
            'condition',
            'age',
            'usage',
            'package',
            'rating',
            'listing_type',
            'provide',
            'price','title',
            'description',
            'city',
            'latitude',
            'longitude',
            # images & videos are handled manually
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'gamingCategory'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'gamingSubcategory'}),
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., PS5, Gaming Chair'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.Select(attrs={'class': 'form-control'}),
            'usage': forms.Select(attrs={'class': 'form-control'}),
            'package': forms.Select(attrs={'class': 'form-control'}),
            'rating': forms.Select(attrs={'class': 'form-control'}),
            'listing_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'OMR'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_provide(self):
        """Convert string choice to boolean."""
        val = self.cleaned_data.get('provide')
        return val == 'True'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamic subcategory based on selected category
        if 'category' in self.data:
            category = self.data.get('category')
        elif self.instance.pk:
            category = self.instance.category
        else:
            category = None

        if category:
            self.fields['subcategory'].choices = GamingListing.get_subcategory_choices(category)
        else:
            self.fields['subcategory'].choices = []

class TicketVoucherListingForm(forms.ModelForm):
    class Meta:
        model = TicketVoucherListing
        fields = [
            'subcategory',
            'price',
            'description',
            'city',
            'latitude',
            'longitude',
            'provide','title',
            'other_options','number_of_tickets'
        ]
        widgets = {
            'subcategory': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price in OMR'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the ticket, voucher, or event details...'}),
            'city': forms.Select(attrs={'class': 'form-control', 'required': True}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Latitude', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Longitude', 'step': '0.000001'}),
            'provide': forms.Select(attrs={'class': 'form-control'}),
            'other_options': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Extra details like seat info, date, terms, etc.'}),
        }

class CollectibleListingForm(forms.ModelForm):
    provide = forms.ChoiceField(
        choices=[('True', 'Yes'), ('False', 'No')],
        widget=forms.Select(attrs={'class': 'form-control'}),
        label="Provide?"
    )

    class Meta:
        model = CollectibleListing
        fields = [
            'category', 'subcategory', 'type',
            'condition', 'age', 'usage',
            'listing_type', 'provide',
            'price', 'description',
            'city', 'latitude', 'longitude',
            # images handled manually in the template
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'collectibleCategory'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'collectibleSubcategory'}),
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Specific Item Type'}),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.Select(attrs={'class': 'form-control'}),
            'usage': forms.Select(attrs={'class': 'form-control'}),
            'listing_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
        }

    def clean_provide(self):
        val = self.cleaned_data['provide']
        return val == 'True'  # convert string to boolean

class BooksListingForm(forms.ModelForm):
    class Meta:
        model = BooksListing
        fields = [
            'category',
            'subcategory',
            'type',          # Hardcover / Paperback
            'condition',     
            'age',
            'usage',
            'listing_type',
            'price','title',
            'city',
            'latitude',
            'longitude',
            # images and videos handled separately
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control', 'id': 'booksCategory'}),
            'subcategory': forms.Select(attrs={'class': 'form-control', 'id': 'booksSubcategory'}),
            'type': forms.Select(attrs={'class': 'form-control'}, choices=[('Hardcover','Hardcover'), ('Paperback','Paperback')]),
            'condition': forms.Select(attrs={'class': 'form-control'}),
            'age': forms.Select(attrs={'class': 'form-control'}),
            'usage': forms.Select(attrs={'class': 'form-control'}),
            'listing_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
        }

class MusicListingForm(forms.ModelForm):
    class Meta:
        model = MusicListing
        fields = [
            'category',
            'subcategory',
            'type',
            'duration',
            'condition',
            'age',
            'usage',
            'listing_type',
            'price',
            'city',
            'latitude',
            'longitude',
            'title',
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-select', 'id': 'musicCategory', 'required': True}),
            'subcategory': forms.Select(attrs={'class': 'form-select', 'id': 'musicSubcategory'}),
            'type': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter music title or type'}),
            'duration': forms.Select(attrs={'class': 'form-select'}),
            'condition': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'age': forms.Select(attrs={'class': 'form-select'}),
            'usage': forms.Select(attrs={'class': 'form-select'}),
            'listing_type': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter price in OMR'}),
            'city': forms.Select(attrs={'class': 'form-select', 'required': True}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
        }

class DVDsMoviesListingForm(forms.ModelForm):
    class Meta:
        model = DVDsMoviesListing
        fields = [
            "category",
            "subcategory",
            "type",
            "condition",
            "age",
            "usage",
            "rating",
            "listing_type",
            "price",
            "city",
            "latitude",
            "longitude",
            "other_options",
        ]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select", "id": "dvdsCategory", "required": True}),
            "subcategory": forms.Select(attrs={"class": "form-select", "id": "dvdsSubcategory"}),
            "type": forms.TextInput(attrs={"class": "form-control", "placeholder": "Movie / Series Title"}),
            "condition": forms.Select(attrs={"class": "form-select"}),
            "age": forms.Select(attrs={"class": "form-select"}),
            "usage": forms.Select(attrs={"class": "form-select"}),
            "rating": forms.Select(attrs={"class": "form-select"}),
            "listing_type": forms.Select(attrs={"class": "form-select", "required": True}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "Enter Price in OMR"}),
            "city": forms.Select(attrs={"class": "form-select", "required": True}),
            "latitude": forms.NumberInput(attrs={"class": "form-control", "step": "0.000001", "placeholder": "Latitude"}),
            "longitude": forms.NumberInput(attrs={"class": "form-control", "step": "0.000001", "placeholder": "Longitude"}),
            "other_options": forms.Textarea(attrs={"class": "form-control", "rows": 2, "placeholder": "Special Edition, Subtitles, Region Code, etc."}),
        }

class FurnitureHomeGardenListingForm(forms.ModelForm):
    class Meta:
        model = FurnitureHomeGardenListing
        fields = [
            "category", "subcategory", "condition",
            "age", "usage",
            "title", "description", "listing_type", "price",
            "city", "latitude", "longitude", 
        ]
        widgets = {
            "category": forms.Select(attrs={"class": "form-select", "required": True}),
            "subcategory": forms.Select(attrs={"class": "form-select", "required": True}),
            "condition": forms.Select(attrs={"class": "form-select"}),
            "age": forms.Select(attrs={"class": "form-select"}),
            "usage": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={
                "class": "form-control", 
                "placeholder": "Enter listing title", 
                "required": True
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control", 
                "rows": 3, 
                "placeholder": "Describe the item"
            }),
            "listing_type": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={
                "class": "form-control", 
                "step": "0.01", 
                "placeholder": "Enter price in OMR"
            }),
            "city": forms.Select(attrs={"class": "form-select"}),
            "latitude": forms.NumberInput(attrs={
                "class": "form-control", 
                "step": "0.000001", 
                "placeholder": "Latitude"
            }),
            "longitude": forms.NumberInput(attrs={
                "class": "form-control", 
                "step": "0.000001", 
                "placeholder": "Longitude"
            }),
        }

class BabyItemsListingForm(forms.ModelForm):
    class Meta:
        model = BabyItemsListing
        fields = [
            "category",
            "subcategory",  # new field
            "title",
            "description",
            "condition",
            "age",           # new field
            "usage",         # new field
            "listing_type",
            "price",
            "city",
            "latitude",
            "longitude",
        ]
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01"}),
            "latitude": forms.NumberInput(attrs={"class": "form-control", "step": "0.000001"}),
            "longitude": forms.NumberInput(attrs={"class": "form-control", "step": "0.000001"}),
            "category": forms.Select(attrs={"class": "form-select", "id": "category"}),
            "subcategory": forms.Select(attrs={"class": "form-select", "id": "subcategory"}),
            "condition": forms.Select(attrs={"class": "form-select"}),
            "age": forms.Select(attrs={"class": "form-select"}),
            "usage": forms.Select(attrs={"class": "form-select"}),
            "listing_type": forms.Select(attrs={"class": "form-select"}),
            "city": forms.Select(attrs={"class": "form-select"}),
        }

class ToysListingForm(forms.ModelForm):
    class Meta:
        model = ToysListing
        fields = [
            "category",
            "condition",
            "usage",
            "age",
            "title",
            "description",
            "listing_type",
            "price",
            "city",
            "latitude",
            "longitude",
        ]
        widgets = {
            "condition": forms.Select(attrs={"class": "form-select"}),
            "usage": forms.Select(attrs={"class": "form-select"}),
            "age": forms.Select(attrs={"class": "form-select"}),
            "main_category": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Listing Title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Describe the toy..."}),
            "listing_type": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "Price in OMR"}),
            "latitude": forms.HiddenInput(),
            "longitude": forms.HiddenInput(),
            "city": forms.Select(attrs={"class": "form-select"}),
        }


class LostFoundListingForm(forms.ModelForm):
  

    class Meta:
        model = LostFoundListing
        fields = [
            'title',  # Add this
            'category',
            'description',
            'listing_type',
            'city',
            'latitude',
            'longitude',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter listing title'}), 
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'listing_type': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
        }



from django import forms
from .models import CameraListing


class CameraListingForm(forms.ModelForm):
    class Meta:
        model = CameraListing
        fields = [
            "main_category", "sub_category", "brand", "title", "description",
            "condition", "usage", "age", "warranty",
            "listing_type", "price",
            "city", "latitude", "longitude",
        ]
        widgets = {
            "main_category": forms.Select(attrs={
                "class": "form-select", "id": "main_category_camera"
            }),
            "sub_category": forms.Select(attrs={
                "class": "form-select", "id": "sub_category_camera"
            }),
            "brand": forms.Select(attrs={
                "class": "form-select", "id": "brand_camera"
            }),
            "title": forms.TextInput(attrs={
                "class": "form-control", "placeholder": "Enter listing title"
            }),
            "description": forms.Textarea(attrs={
                "class": "form-control", "rows": 3,
                "placeholder": "Describe the camera or accessory"
            }),
            "condition": forms.Select(attrs={"class": "form-select"}),
            "usage": forms.Select(attrs={"class": "form-select"}),
            "age": forms.Select(attrs={"class": "form-select"}),
            "warranty": forms.Select(attrs={"class": "form-select"}),
            "listing_type": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={
                "class": "form-control", "step": "0.01",
                "placeholder": "Enter price in OMR"
            }),
            "city": forms.Select(attrs={"class": "form-select"}),
            "latitude": forms.NumberInput(attrs={
                "class": "form-control", "step": "0.000001"
            }),
            "longitude": forms.NumberInput(attrs={
                "class": "form-control", "step": "0.000001"
            }),
        }

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
    

class JewelryListingForm(forms.ModelForm):
    class Meta:
        model = JewelryListing
        fields = [
            "main_category", "sub_category", "title", "description",
            "condition", "usage", "age", "warranty",
            "listing_type", "price",
            "city", "latitude", "longitude",
        ]
        widgets = {
            "main_category": forms.Select(attrs={"class": "form-select", "id": "main_category_jewelry"}),
            "sub_category": forms.Select(attrs={"class": "form-select", "id": "sub_category_jewelry"}),
            
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter listing title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3, "placeholder": "Describe the item"}),
            "condition": forms.Select(attrs={"class": "form-select"}),
            "usage": forms.Select(attrs={"class": "form-select"}),
            "age": forms.Select(attrs={"class": "form-select"}),
            "warranty": forms.Select(attrs={"class": "form-select"}),
            "listing_type": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "step": "0.01", "placeholder": "Enter price in OMR"}),
            "city": forms.Select(attrs={"class": "form-select"}),
            "latitude": forms.NumberInput(attrs={"class": "form-control", "step": "0.000001"}),
            "longitude": forms.NumberInput(attrs={"class": "form-control", "step": "0.000001"}),
        }

    def save(self, commit=True, user=None):
        instance = super().save(commit=False)
        if user:
            instance.user = user
        if commit:
            instance.save()
        return instance
    

from django import forms
from .models import HomeApplianceListing

from django import forms
from .models import HomeApplianceListing, HomeApplianceImage, HomeApplianceVideo


class HomeApplianceListingForm(forms.ModelForm):
    class Meta:
        model = HomeApplianceListing
        fields = [
            # Core
            "main_category", "subcategory", "title", "description",
            "condition", "usage", "age", "warranty", "brand",
            "listing_type", "price",
            # Location
            "city", "latitude", "longitude",
            # Subcategory-specific (all included, frontend decides visibility)
            "ac_brand", "cooling_power", "heating_type",
            "dishwasher_brand", "place_settings",
            "gas_cylinder_brand", "gas_cylinder_weight",
            "humidifier_brand", "room_size",
            "oven_brand", "oven_type",
            "range_model", "energy_input",
            "fridge_brand", "number_of_doors",
            "washer_brand", "access_location", "capacity",
            "water_cooler_brand", "cooling_capacity",
            "power_watts", "capacity_liters", "appliance_type", "toaster_slots",
            "power_source", "cooking_area", "number_of_burners",
            "capacity_quarts", "lawnmower_type", "psi",
            "wattage", "max_weight",
        ]
        widgets = {
            "main_category": forms.Select(attrs={"class": "form-select", "id": "mainCategory"}),
            "subcategory": forms.Select(attrs={"class": "form-select", "id": "subCategory"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter title"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "condition": forms.Select(attrs={"class": "form-select"}),
            "usage": forms.Select(attrs={"class": "form-select"}),
            "age": forms.Select(attrs={"class": "form-select"}),
            "warranty": forms.Select(attrs={"class": "form-select"}),
            "brand": forms.TextInput(attrs={"class": "form-control"}),
            "listing_type": forms.Select(attrs={"class": "form-select"}),
            "price": forms.NumberInput(attrs={"class": "form-control", "placeholder": "Enter price"}),
            "city": forms.Select(attrs={"class": "form-select"}),
            "latitude": forms.NumberInput(attrs={"class": "form-control", "step": "any"}),
            "longitude": forms.NumberInput(attrs={"class": "form-control", "step": "any"}),
            # Category-specific widgets
            "ac_brand": forms.TextInput(attrs={"class": "form-control"}),
            "cooling_power": forms.TextInput(attrs={"class": "form-control"}),
            "dishwasher_brand": forms.TextInput(attrs={"class": "form-control"}),
            "place_settings": forms.NumberInput(attrs={"class": "form-control"}),
            "gas_cylinder_brand": forms.TextInput(attrs={"class": "form-control"}),
            "gas_cylinder_weight": forms.TextInput(attrs={"class": "form-control"}),
            "humidifier_brand": forms.TextInput(attrs={"class": "form-control"}),
            "room_size": forms.NumberInput(attrs={"class": "form-control"}),
            "oven_brand": forms.TextInput(attrs={"class": "form-control"}),
            "oven_type": forms.Select(attrs={"class": "form-select"}),
            "range_model": forms.TextInput(attrs={"class": "form-control"}),
            "energy_input": forms.Select(attrs={"class": "form-select"}),
            "fridge_brand": forms.TextInput(attrs={"class": "form-control"}),
            "number_of_doors": forms.TextInput(attrs={"class": "form-control"}),
            "washer_brand": forms.TextInput(attrs={"class": "form-control"}),
            "access_location": forms.Select(attrs={"class": "form-select"}),
            "capacity": forms.Select(attrs={"class": "form-select"}),
            "water_cooler_brand": forms.TextInput(attrs={"class": "form-control"}),
            "cooling_capacity": forms.NumberInput(attrs={"class": "form-control"}),
            "power_watts": forms.NumberInput(attrs={"class": "form-control"}),
            "capacity_liters": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "appliance_type": forms.TextInput(attrs={"class": "form-control"}),
            "toaster_slots": forms.NumberInput(attrs={"class": "form-control"}),
            "power_source": forms.Select(attrs={"class": "form-select"}),
            "cooking_area": forms.NumberInput(attrs={"class": "form-control"}),
            "number_of_burners": forms.NumberInput(attrs={"class": "form-control"}),
            "capacity_quarts": forms.NumberInput(attrs={"class": "form-control"}),
            "lawnmower_type": forms.Select(attrs={"class": "form-select"}),
            "psi": forms.NumberInput(attrs={"class": "form-control"}),
            "wattage": forms.NumberInput(attrs={"class": "form-control"}),
            "max_weight": forms.NumberInput(attrs={"class": "form-control"}),
        }



from django import forms
from .models import ClothingAccessoriesListing, ClothingAccessoriesImage, ClothingAccessoriesVideo

class ClothingAccessoriesListingForm(forms.ModelForm):
    
    
    class Meta:
        model = ClothingAccessoriesListing
        fields = [
            'main_category', 'subcategory', 'title', 'description', 'brand',
            'size', 'condition', 'age', 'usage', 'listing_type', 'price',
            'city', 'latitude', 'longitude'
        ]
        widgets = {
            'main_category': forms.Select(attrs={'class': 'form-select', 'id': 'main_category_clothing'}),
            'subcategory': forms.Select(attrs={'class': 'form-select', 'id': 'sub_category_clothing'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter listing title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the item'}),
            'brand': forms.Select(attrs={'class': 'form-select', 'id': 'brandSelect'}),
            'size': forms.Select(attrs={'class': 'form-select', 'id': 'sizeSelect'}),
            'condition': forms.Select(attrs={'class': 'form-select'}),
            'age': forms.Select(attrs={'class': 'form-select'}),
            'usage': forms.Select(attrs={'class': 'form-select'}),
            'listing_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter price in OMR'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.000001'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make certain fields not required initially
        self.fields['subcategory'].required = False
        self.fields['brand'].required = False
        self.fields['size'].required = False
        self.fields['condition'].required = False
        self.fields['age'].required = False
        self.fields['usage'].required = False
        self.fields['price'].required = False
        
        # Set empty labels
        self.fields['main_category'].empty_label = "Select Category"
        self.fields['subcategory'].empty_label = "Select Sub Category"
        self.fields['brand'].empty_label = "Select Brand"
        self.fields['size'].empty_label = "Select Size"
        self.fields['condition'].empty_label = "Select Condition"
        self.fields['age'].empty_label = "Select Age"
        self.fields['usage'].empty_label = "Select Usage"
        self.fields['listing_type'].empty_label = "Select Type"
        self.fields['city'].empty_label = "Select City"
    
    def clean(self):
        cleaned_data = super().clean()
        listing_type = cleaned_data.get('listing_type')
        price = cleaned_data.get('price')
        main_category = cleaned_data.get('main_category')
        subcategory = cleaned_data.get('subcategory')
        
        # Price is required for "For Sale" listings
        if listing_type == 'sale' and price is None:
            self.add_error('price', 'Price is required for "For Sale" listings.')
        
        # Validate that subcategory belongs to the selected main category
        if main_category and subcategory:
            valid_subcategories = [choice[0] for choice in ClothingAccessoriesListing.SUBCATEGORY_CHOICES.get(main_category, [])]
            if subcategory not in valid_subcategories:
                self.add_error('subcategory', 'Invalid subcategory for the selected main category.')
        
        return cleaned_data
    
    



class ElectronicsListingForm(forms.ModelForm):
    class Meta:
        model = ElectronicsListing
        fields = [
            'main_category', 'subcategory', 'brand', 'title', 'description',
            'tv_model', 'tv_resolution', 'tv_screen_size', 'tv_mount_type',
            'condition', 'age', 'usage', 'listing_type', 'price', 'warranty',
            'city', 'latitude', 'longitude',
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'price': forms.NumberInput(attrs={'step': '0.01'}),
            'latitude': forms.NumberInput(attrs={'step': '0.000001'}),
            'longitude': forms.NumberInput(attrs={'step': '0.000001'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(ElectronicsListingForm, self).__init__(*args, **kwargs)
        # Example: optionally make some fields required based on context
        self.fields['main_category'].required = True
        self.fields['title'].required = True
        self.fields['listing_type'].required = True

    def save(self, commit=True):
        # Override save to handle ManyToMany relationships for images/videos
        instance = super().save(commit=False)
        
        return instance
   


# ----------------------------------------------------------Services-----------------------------------------------------------------

class AutoServiceListingForm(forms.ModelForm):

    class Meta:
        model = AutoServiceListing
        fields = [
            'title',
            'description',
            'service_type',
            'city',
            'price',
            'latitude',
            'longitude',
            'images',
           
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price in OMR'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
        }


# Save helper for handling ManyToMany uploads
def save_autoservice_form(form, user):
    """
    Custom save method to handle image/video uploads properly
    """
    service = form.save(commit=False)
    service.user = user
    service.save()


    service.save()
    return service


class ConsultancyServiceListingForm(forms.ModelForm):

    class Meta:
        model = ConsultancyServiceListing
        fields = [
            'title',
            'description',
            'service_type',
            'price',
            'city',
            'latitude',
            'longitude',
    
            'images',
            
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter consultancy title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price in OMR'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),

        }


# Helper function to save with images/videos
def save_consultancy_form(form, user):
    """
    Custom save method to handle image/video uploads properly
    """
    consultancy = form.save(commit=False)
    consultancy.user = user
    consultancy.save()

    consultancy.save()
    return consultancy



class DomesticServiceListingForm(forms.ModelForm):
    class Meta:
        model = DomesticServiceListing
        fields = [
            'title', 
            'description', 
            'service_type', 
            'price', 
            'city', 
            'latitude', 
            'longitude', 
            'images', 
           
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Service Description', 'rows': 4}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Service Price in OMR'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Longitude'}),
            
        }



class EventEntertainmentServiceForm(forms.ModelForm):
    class Meta:
        model = EventEntertainmentServiceListing
        fields = [
            'title',
            'description',
            'service_type',
            'price',
            'city',
            'latitude',
            'longitude',
            'images',
            
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Service Description', 'rows': 4}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Service Price in OMR'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Longitude'}),
            
        }

class HealthWellbeingServiceForm(forms.ModelForm):
    class Meta:
        model = HealthWellbeingServiceListing
        fields = [
            'title',
            'description',
            'service_type',
            'price',
            'city',
            'latitude',
            'longitude',
            'images',
            
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Service Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Service Description', 'rows': 4}),
            'service_type': forms.Select(attrs={'class': 'form-control'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Service Price in OMR'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Longitude'}),
           
        }



class HomeMaintenanceServiceListingForm(forms.ModelForm):
    class Meta:
        model = HomeMaintenanceServiceListing
        fields = ['title', 'description', 'service_type', 'price', 'city', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter service title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your service'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.000001}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.000001}),
        }

class MoversServiceListingForm(forms.ModelForm):
    class Meta:
        model = MoversServiceListing
        fields = ['title', 'description', 'service_type', 'price', 'city', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter service title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your service'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.000001}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.000001}),
        }

class RestorationServiceListingForm(forms.ModelForm):
    class Meta:
        model = RestorationServiceListing
        fields = ['title', 'description', 'service_type', 'price', 'city', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter service title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your service'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.000001}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.000001}),
        }

class TutorsServiceListingForm(forms.ModelForm):
    class Meta:
        model = TutorsServiceListing
        fields = ['title', 'description', 'service_type', 'price', 'city', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter service title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your service'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.000001}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.000001}),
        }


class WebComputerServiceListingForm(forms.ModelForm):
    class Meta:
        model = WebComputerServiceListing
        fields = ['title', 'description', 'service_type', 'price', 'city', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter service title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your service'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.000001}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.000001}),
        }



class FreelancersServiceListingForm(forms.ModelForm):
    class Meta:
        model = FreelancersServiceListing
        fields = ['title', 'description', 'price', 'city', 'latitude', 'longitude']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter service title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe your service'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.01}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.000001}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 0.000001}),
        }


class OtherServiceListingForm(forms.ModelForm):
  

    class Meta:
        model = OtherServiceListing
        fields = [
            'title',
            'description',
            'service_type',
            'price',
            'city',
            'latitude',
            'longitude',
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter service title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Describe the service'}),
            'service_type': forms.Select(attrs={'class': 'form-select'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter price (optional)'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any'}),
        }


class JobSeekerForm(forms.ModelForm):
    # Add skills as a multiple choice field
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'skills-select'}),
        required=False,
        label="Skills"
    )
    
    class Meta:
        model = JobSeeker
        fields = [
            'headline',
            'phone_number',
            'cover_letter',
            'gender',
            'nationality',
            'current_company',
            'notice_period',
            'visa_status',
            'expected_salary',
            'work_experience',
            'education_level',
            'commitment',
            'city',
            'latitude',
            'longitude',
            'skills',  # Add skills to fields
        ]
        widgets = {
            'headline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your professional headline'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'cover_letter': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Write your cover letter'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'nationality': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your nationality'}),
            'current_company': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Current company (optional)'}),
            'notice_period': forms.Select(attrs={'class': 'form-select'}),
            'visa_status': forms.Select(attrs={'class': 'form-select'}),
            'expected_salary': forms.Select(attrs={'class': 'form-select'}),
            'work_experience': forms.Select(attrs={'class': 'form-select'}),
            'education_level': forms.Select(attrs={'class': 'form-select'}),
            'commitment': forms.Select(attrs={'class': 'form-select'}),
            'city': forms.Select(attrs={'class': 'form-select'}),
            'latitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Latitude'}),
            'longitude': forms.NumberInput(attrs={'class': 'form-control', 'step': 'any', 'placeholder': 'Longitude'}),
        }

class JobSeekerProfileForm(forms.ModelForm):
    profile_skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(),
        widget=forms.SelectMultiple(attrs={'class': 'form-select', 'id': 'profile-skills-select'}),
        required=False,
        label="Skills for this Category"
    )
    
    class Meta:
        model = JobSeekerProfile
        fields = ['job_category', 'resume', 'profile_skills']
        widgets = {
            'job_category': forms.Select(attrs={'class': 'form-select'}),
            'resume': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

# New form for adding custom skills
class CustomSkillForm(forms.Form):
    skill_name = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter a new skill',
            'id': 'new-skill-input'
        }),
        label="Add New Skill"
    )


# --------------------------------------------------FAQ--------------------------------------------------------------


from django import forms
from .models import FAQ

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['question', 'answer', 'is_active']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
            'answer': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }