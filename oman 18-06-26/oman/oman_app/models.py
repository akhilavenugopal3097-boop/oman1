from django.db import models
from django.utils import timezone
from PIL import Image, ImageDraw, ImageFont
import os
from django.conf import settings
from PIL import Image, ImageOps
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import datetime


from django.db import models

class AdvertisementCategory(models.TextChoices):
    HOME = 'home', 'Home'  # 👈 added this
    MOTORS = 'motors', 'Motors'
    REAL_ESTATE = 'real_estate', 'Real Estate'
    JOB = 'job', 'Jobs'
    OTHER_CLASSIFIED = 'other_classified', 'Other Classified'
    MOBILES = 'mobiles', 'Mobiles'
    SERVICES = 'services', 'Services'

class Advertisement(models.Model):
    category = models.CharField(
        max_length=20,
        choices=AdvertisementCategory.choices,
        default=AdvertisementCategory.HOME  # 👈 optional: make home default
    )
    image = models.ImageField(upload_to='advertisements/')
    url = models.URLField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_category_display()} Advertisement {self.id}"
    
    def toggle_active(self):
        """Toggle the is_active status"""
        self.is_active = not self.is_active
        self.save()
        return self.is_active
    
    class Meta:
        ordering = ['-uploaded_at']


class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)
 
    def __str__(self):
        return self.name

    
class Governate(models.Model):
    name = models.CharField(max_length=100, unique=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    
    def __str__(self):
        return self.name    

class District(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    governate = models.ForeignKey(Governate, on_delete=models.CASCADE, related_name='districts')
    
    def __str__(self):
        return f"{self.name} ({self.governate.name})"

class Cities(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='cities')
    def __str__(self):
        return f"{self.name} ({self.district.name}, {self.district.governate.name})" 

    
    
class Category(models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, help_text="Enter the Font Awesome class for the icon, e.g., 'fas fa-tshirt'.")
    def _str_(self):
        return self.name

class Subcategory(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subcategories')
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.category.name} - {self.name}"
    
class JobCategory(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(
        upload_to='job_categories/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name


class NearbyLocation(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Location Name")

    def __str__(self):
        return self.name


class MainAmenities(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Amenity Name")

    def __str__(self):
        return self.name


class AdditionalAmenities(models.Model):
    name = models.CharField(max_length=255, unique=True, verbose_name="Amenity Name")

    def __str__(self):
        return self.name

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

from django.db import models
from django.conf import settings

class Land(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),

    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent')
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    FACADE_CHOICES = [
        ('northern', 'Northern'),
        ('southern', 'Southern'),
        ('eastern', 'Eastern'),
        ('western', 'Western'),
        ('northeast', 'Northeast'),
        ('southeast', 'Southeast'),
        ('northwest', 'Northwest'),
        ('southwest', 'Southwest'),

    ]
    ZONED_FOR_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('farm', 'Farm'),
        ('industrial', 'Industrial'),
        ('mixed use', 'Mixed Use')
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='lands'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    image = models.ImageField(upload_to='land/', verbose_name="Main Image")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='land')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    plot_area = models.CharField(max_length=100, verbose_name="Land Area")
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    # New field for listing type
    listing_type = models.CharField(
        max_length=10,
        choices=LISTING_TYPE_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    
    
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    facade = models.CharField(
        max_length=10, 
        choices=FACADE_CHOICES, 
        verbose_name="Facade"
    )
    zoned_for = models.CharField(
        max_length=100, 
        choices=ZONED_FOR_CHOICES, 
        verbose_name="Zoned For"
    )
    nearby_location = models.ManyToManyField(NearbyLocation) 
    images = models.ManyToManyField(
        'LandImage', 
        blank=True, 
        related_name='land', 
        verbose_name="Images"
    )
    
    videos = models.ManyToManyField(
        'LandVideo', 
        blank=True, 
        related_name='land', 
        verbose_name="Videos"
    )

class LandImage(models.Model):
    image = models.ImageField(upload_to='land/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class LandVideo(models.Model):
    video = models.FileField(upload_to='land/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
   
#villa    
class Villa(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    BEDROOM_CHOICES =[
            ('studio', 'Studio'),
            ('1', '1 Bed'),
            ('2', '2 Beds'),
            ('3', '3 Beds'),
            ('4', '4 Beds'),
            ('5', '5 Beds'),
            ('6+', '6+ Beds'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    BUILDING_AGE_CHOICES = [
        ('under_construction', 'Under Construction'),
        ('0-11_months', '0-11 Months'),
        ('1-5_years', '1-5 Years'),
        ('6-9_years', '6-9 Years'),
        ('10-19_years', '10-19 Years'),
        ('20+_years', '20+ Years'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    FACADE_CHOICES = [
        ('northern', 'Northern'),
        ('southern', 'Southern'),
        ('eastern', 'Eastern'),
        ('western', 'Western'),
        ('northeast', 'Northeast'),
        ('southeast', 'Southeast'),
        ('northwest', 'Northwest'),
        ('southwest', 'Southwest'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='villas'
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    image = models.ImageField(upload_to='villa/', verbose_name="Main Image")
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    
    FLOOR_CHOICES = [
        ('basement_floor', 'Basement Floor'),
    ('semiground_floor', 'Semi Ground Floor'),
    ('ground_floor', 'Ground Floor'),
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),
    ('3_floor', '3 Floors'),
    ('4_floor', '4 Floors'),
    ('5_floor', '5 Floors'),
    ('6_floor', '6 Floors'),
    ('7_floor', '7 Floors'),
    ('8_floor', '8 Floors'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )

    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='villa')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Land Area")
    surface_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    bedrooms = models.CharField(
        max_length=10,
        choices=BEDROOM_CHOICES,
        verbose_name="Number of Bedrooms"
    )
    bathrooms = models.CharField(
        max_length=10,
        choices=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6+', '6+'),
        ],
        verbose_name="Number of Bathrooms"
    )
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    building = models.CharField(max_length=20, choices=BUILDING_AGE_CHOICES,default='under_construction',  verbose_name="Building Age")
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    
    
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    facade = models.CharField(
    max_length=10,
    choices=FACADE_CHOICES,
    null=True,
    blank=True
    )

    images = models.ManyToManyField(
        'VillaImage', 
        blank=True, 
        related_name='villa', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'VillaVideo', 
        blank=True, 
        related_name='villa', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class VillaImage(models.Model):
    image = models.ImageField(upload_to='villa/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"
    
class VillaVideo(models.Model):
    video = models.FileField(upload_to='villa/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    

class Commercial(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]

    PROPERTY_CHOICES = [
        ('complete', 'Ready to Occupy'),
        ('under_construction', 'Under Construction'),
            ]
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='commercial'
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='commercial')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Land Area (sq ft/m²)")
    surface_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    FLOOR_CHOICES = [
    ('basement_floor', 'Basement Floor'),
    ('semiground_floor', 'Semi Ground Floor'),
    ('ground_floor', 'Ground Floor'),
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),
    ('3_floor', '3 Floors'),
    ('4_floor', '4 Floors'),
    ('5_floor', '5 Floors'),
    ('6_floor', '6 Floors'),
    ('7_floor', '7 Floors'),
    ('8_floor', '8 Floors'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
]
    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sale',
        verbose_name="Listing Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    images = models.ManyToManyField(
        'ComImage', 
        blank=True, 
        related_name='Commercial', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ComVideo',
        blank=True,
        related_name='Commercial',
        verbose_name="Videos"
    )
    
    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)


class ComImage(models.Model):
    image = models.ImageField(upload_to='Commercial/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class ComVideo(models.Model):
    video = models.FileField(upload_to='Commercial/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"


class Farm(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    BUILDING_AGE_CHOICES = [
        ('under_construction', 'Under Construction'),
        ('0-11_months', '0-11 Months'),
        ('1-5_years', '1-5 Years'),
        ('6-9_years', '6-9 Years'),
        ('10-19_years', '10-19 Years'),
        ('20+_years', '20+ Years'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    FACADE_CHOICES = [
        ('northern', 'Northern'),
        ('southern', 'Southern'),
        ('eastern', 'Eastern'),
        ('western', 'Western'),
        ('northeast', 'Northeast'),
        ('southeast', 'Southeast'),
        ('northwest', 'Northwest'),
        ('southwest', 'Southwest'),

    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='farm'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    surface_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    BEDROOM_CHOICES =[
            ('studio', 'Studio'),
            ('1', '1 Bed'),
            ('2', '2 Beds'),
            ('3', '3 Beds'),
            ('4', '4 Beds'),
            ('5', '5 Beds'),
            ('6+', '6+ Beds'),
    ]
    bedrooms = models.CharField(
        max_length=10,
        choices=BEDROOM_CHOICES,
        verbose_name="Number of Bedrooms"
    )
    bathrooms = models.CharField(
        max_length=10,
        choices=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6+', '6+'),
        ],
        verbose_name="Number of Bathrooms"
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='farm')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Land Area")
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities) 
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    building = models.CharField(max_length=20, choices=BUILDING_AGE_CHOICES,default='under_construction',  verbose_name="Building Age")
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period")
    
    
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    facade = models.CharField(
        max_length=10, 
        choices=FACADE_CHOICES, 
        verbose_name="Facade"
    )

    images = models.ManyToManyField(
        'FarmImage', 
        blank=True, 
        related_name='Farm', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'FarmVideo',
        blank=True,
        related_name='Farm',
        verbose_name="Videos"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class FarmImage(models.Model):
    image = models.ImageField(upload_to='Farm/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class FarmVideo(models.Model):
    video = models.FileField(upload_to='Farm/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

class Chalet(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='chalet'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Plot Area")
    bedrooms = models.IntegerField(verbose_name="Number of Bedrooms")
    bathrooms = models.IntegerField(verbose_name="Number of Bathrooms")
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    amenities = models.TextField(verbose_name="Amenities (e.g., Fireplace, Jacuzzi, Sauna)")
    proximity_to_activities = models.TextField(verbose_name="Proximity to Skiing/Outdoor Activities")
    tenancy_information = models.CharField(
        max_length=100, 
        choices=[('rented', 'Rented'), ('owner_occupied', 'Owner Occupied')], 
        verbose_name="Tenancy Information"
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    contact_details = models.TextField(verbose_name="Contact Details")
    additional_information = models.TextField(verbose_name="Additional Information")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'ChaletImage', 
        blank=True, 
        related_name='Chalet', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ChaletVideo',
        blank=True,
        related_name='Chalet',
        verbose_name="Videos"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class ChaletImage(models.Model):
    image = models.ImageField(upload_to='Chalet/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class ChaletVideo(models.Model):
    video = models.FileField(upload_to='Chalet/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"


    
#Job
class Job(models.Model):
    JOB_TYPE_CHOICES = [
    ('full_time', 'Full-time'), 
    ('part_time', 'Part-time'), 
    ('freelance', 'Freelance'), 
    ('contract', 'Contract'), 
    ('temporary', 'Temporary')
]
    job_title = models.CharField(max_length=255, verbose_name="Job Title")
    company_name = models.CharField(max_length=255, verbose_name="Company Name")
    job_type = models.CharField(
        max_length=50, 
        choices=JOB_TYPE_CHOICES,
        verbose_name="Job Type"
    )
    industry = models.CharField(
        max_length=50, 
        choices=[('IT', 'IT'), ('marketing', 'Marketing'), ('finance', 'Finance'), ('designing', 'Designing')], 
        verbose_name="Industry"
    )
    experience_level = models.CharField(
        max_length=50, 
        choices=[('entry', 'Entry-level'), ('mid', 'Mid-level'), ('senior', 'Senior')], 
        verbose_name="Experience Level"
    )
    salary_range = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salary Range (OMR)")
    education_level = models.CharField(
        max_length=50, 
        choices=[('diploma', 'Diploma'), ('bachelor', 'Bachelor\'s'), ('postgraduate', 'Post Graduate'), ('phd', 'PHD')], 
        verbose_name="Education Level"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    skills_required = models.TextField(verbose_name="Skills Required")
    description = models.TextField(max_length=1000,verbose_name="Property Description")


  

class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name="Skill Name")
    
    def __str__(self):
        return self.name

  
class JobSeeker(models.Model):
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ]
    
    NOTICE_PERIOD_CHOICES = [
        ('immediately', 'Immediately'),
        ('less_than_2_weeks', 'Less than 2 Weeks'),
        ('one_month', 'One Month'),
        ('more_than_one_month', 'More than One Month'),
    ]
    
    VISA_STATUS_CHOICES = [
        ('not_applicable', 'Not Applicable'),
        ('business', 'Business'),
        ('employment', 'Employment'),
        ('residence', 'Residence'),
        ('spouse', 'Spouse'),
        ('student', 'Student'),
        ('tourist', 'Tourist'),
        ('visit', 'Visit'),
    ]
    
    EXPECTED_SALARY_CHOICES = [
        ('negotiable', 'Negotiable'),
        ('less_than_2000', 'Less than 2000'),
        ('2000_3999', '2000-3999'),
        ('4000_5999', '4000-5999'),
        ('6000_7999', '6000-7999'),
        ('8000_11999', '8000-11999'),
        ('12000_19999', '12000-19999'),
        ('20000_plus', '20000+'),
    ]
    
    WORK_EXPERIENCE_CHOICES = [
        ('0_1', '0-1 years'),
        ('1_2', '1-2 years'),
        ('2_5', '2-5 years'),
        ('5_10', '5-10 years'),
        ('10_15', '10-15 years'),
        ('15_plus', '15+ years'),
    ]
    
    EDUCATION_LEVEL_CHOICES = [
        ('noschool', 'No Formal Education'),
        ('basic', 'Basic Education (Grades 1–10)'),
        ('secondary', 'General Secondary (Grades 11–12)'),
        ('vocational', 'Vocational / Technical Certificate'),
        ('diploma', 'Diploma (Higher College of Technology / Colleges of Applied Sciences)'),
        ('bachelor', 'Bachelor’s Degree'),
        ('master', 'Master’s Degree'),
        ('phd', 'Doctorate (PhD)'),
    ]
    
    COMMITMENT_CHOICES = [
        ('full_time', 'Full-Time'),
        ('part_time', 'Part-Time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
        ('other', 'Other'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,  # <- use this instead of auth.User
        on_delete=models.CASCADE,
        related_name='jobseeker'
    )

    # Basic Info
    headline = models.CharField(max_length=255, verbose_name="Headline")
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number")
    cover_letter = models.TextField(verbose_name="Cover Letter")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, verbose_name="Gender")
    nationality = models.CharField(max_length=255, verbose_name="Nationality")
    current_company = models.CharField(max_length=255, verbose_name="Current Company", blank=True, null=True)
    
    # Documents
    is_completed = models.BooleanField(default=False)
    
    # Job Preferences
    notice_period = models.CharField(max_length=20, choices=NOTICE_PERIOD_CHOICES, verbose_name="Notice Period")
    visa_status = models.CharField(max_length=20, choices=VISA_STATUS_CHOICES, verbose_name="Visa Status")
    expected_salary = models.CharField(max_length=20, choices=EXPECTED_SALARY_CHOICES, verbose_name="Expected Salary")
    work_experience = models.CharField(max_length=20, choices=WORK_EXPERIENCE_CHOICES, verbose_name="Work Experience")
    education_level = models.CharField(max_length=20, choices=EDUCATION_LEVEL_CHOICES, verbose_name="Education Level")
    commitment = models.CharField(max_length=20, choices=COMMITMENT_CHOICES, verbose_name="Commitment", blank=True, null=True)

    skills = models.ManyToManyField(Skill, blank=True, related_name='jobseekers', verbose_name="Skills")
    

    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='jobseekers')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)


    def __str__(self):
        return self.headline

class JobSeekerProfile(models.Model):
    jobseeker = models.ForeignKey(JobSeeker, on_delete=models.CASCADE, related_name="profiles")
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/', verbose_name="Upload CV")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Add profile-specific skills
    profile_skills = models.ManyToManyField(Skill, blank=True, related_name='jobseeker_profiles', verbose_name="Profile Skills")
     
    class Meta:
        unique_together = ['jobseeker', 'job_category']
    
    def __str__(self):
        return f"{self.jobseeker.user.email} - {self.job_category.name}"



# authenticated user
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django_countries.fields import CountryField
from django.core.validators import RegexValidator
from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, phone=None, password=None, **extra_fields):
        if not username:
            raise ValueError('Username is required')
        if not email:
            raise ValueError('Email is required')
        if not first_name:
            raise ValueError('First name is required')
        if not last_name:
            raise ValueError('Last name is required')
        
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('user_type', 'admin')
        return self.create_user(username, email, first_name, last_name, None, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('regular', 'Regular User'),
        ('agent', 'Agent'),
        ('admin', 'Admin'),
        ('subadmin', 'Sub-Admin'),
    )
    
    # Basic required fields
    username = models.CharField(
        max_length=25,
        unique=True,
        validators=[RegexValidator(r'^\S+$', 'Username cannot contain spaces.')]
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, unique=True, null=True, blank=True)  # optional

    # Compulsory fields for registration
    first_name = models.CharField(max_length=150)  # no null=True, no blank=True
    last_name = models.CharField(max_length=150)   # no null=True, no blank=True
    
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(null=True, blank=True)
    date_joined = models.DateTimeField(default=timezone.now)
    
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='regular')
    is_approved = models.BooleanField(default=False)
    
    # optional profile fields
    whatsapp = models.CharField(max_length=15, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    is_chat_blocked = models.BooleanField(default=False)
    chat_blocked_at = models.DateTimeField(blank=True, null=True)
    is_suspended = models.BooleanField(default=False)
    suspended_at = models.DateTimeField(blank=True, null=True)
    suspension_reason = models.TextField(blank=True, null=True)
    nationality = CountryField(blank=True, null=True)
    gender = models.CharField(max_length=10, choices=[('Male','Male'),('Female','Female'),('Other','Other')], blank=True, null=True)
    image = models.ImageField(upload_to='user/images/', blank=True, null=True)
    is_exclusive_contact = models.BooleanField(
        default=False,
        help_text="This account's contact details show on all approved exclusive listings."
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'first_name', 'last_name']   # phone is optional, but name fields are required

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def save(self, *args, **kwargs):
        if self.user_type != 'agent':
            self.is_approved = True
        if self.is_staff or self.is_superuser:
            self.is_active = True
            self.is_approved = True
        super().save(*args, **kwargs)

    def can_login(self):
        if self.is_suspended:
            return False
        if self.user_type == 'agent':
            return self.is_active and self.is_approved
        return self.is_active
    
    @property
    def followers_count(self):
        return self.followers.count()
    
    @property
    def following_count(self):
        return self.following.count()
    
    @property
    def total_views(self):
        """Count only unique logged-in users who viewed the profile"""
        return self.profile_views.values('viewer').distinct().count()
    
    @property
    def unique_views(self):
        """Count unique logged-in users who viewed the profile"""
        return self.profile_views.values('viewer').distinct().count()
    
    def is_following(self, user):
        """Check if current user is following the given user"""
        return self.following.filter(following=user).exists()
    
    def follow(self, user):
        """Follow a user"""
        if self != user and not self.is_following(user):
            UserFollow.objects.create(follower=self, following=user)
            return True
        return False
    
    def unfollow(self, user):
        """Unfollow a user"""
        if self != user and self.is_following(user):
            UserFollow.objects.filter(follower=self, following=user).delete()
            return True
        return False
    
    def get_followers(self):
        """Get all followers"""
        return [follow.follower for follow in self.followers.all()]
    
    def get_following(self):
        """Get all users this user is following"""
        return [follow.following for follow in self.following.all()]

# models.py

class RecentlyViewed(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='recently_viewed')
    content_type = models.CharField(max_length=50)  # e.g., 'car', 'property', 'mobile', etc.
    object_id = models.PositiveIntegerField()
    category = models.CharField(max_length=50)  # 'Motors', 'Properties', 'Electronics', etc.
    viewed_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-viewed_at']
        unique_together = ['user', 'content_type', 'object_id']
    
    def __str__(self):
        return f"{self.user.username} viewed {self.content_type} {self.object_id}"
    
from django.db import models
from django.utils import timezone

class UserFollow(models.Model):
    follower = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='following'
    )
    following = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='followers'
    )
    created_at = models.DateTimeField(default=timezone.now)
    
    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.follower} follows {self.following}"
    
class UserProfileView(models.Model):
    viewer = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='viewed_profiles',
        null=True,
        blank=True
    )
    profile_owner = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='profile_views'
    )
    viewed_at = models.DateTimeField(default=timezone.now)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    
    class Meta:
        ordering = ['-viewed_at']
    
    def __str__(self):
        viewer_name = self.viewer.username if self.viewer else 'Anonymous'
        return f"{viewer_name} viewed {self.profile_owner.username}"


# Fashion model
class Fashion(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='fashion'
    )
    product_name=models.TextField(max_length=250)
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    name=models.TextField(max_length=250)
    category = models.CharField(
        max_length=50, 
        choices=[
            ('clothing', 'Clothing'), 
            ('footwear', 'Footwear'), 
            ('accessories', 'Accessories')
        ], 
        verbose_name="Category"
    )
    brand = models.CharField(max_length=100, verbose_name="Brand")
    size = models.CharField(
        max_length=10, 
        choices=[('S', 'Small'), ('M', 'Medium'), ('L', 'Large'), ('XL', 'XL')], 
        verbose_name="Size"
    )
    gender = models.CharField(
        max_length=10, 
        choices=[('male', 'Male'), ('female', 'Female'), ('unisex', 'Unisex')], 
        verbose_name="Gender"
    )
    color = models.CharField(max_length=50, verbose_name="Color")
    material = models.CharField(max_length=100, verbose_name="Material")
    condition = models.CharField(
        max_length=10, 
        choices=[('used', 'Used'), ('like_new', 'Like New')], 
        verbose_name="Condition"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    contact_details = models.TextField(verbose_name="Contact Details")
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'FashionImage', 
        blank=True, 
        related_name='fashion', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'FashionVideo', 
        blank=True, 
        related_name='fashion', 
        verbose_name="Videos"
    )
class FashionImage(models.Model):
    image = models.ImageField(upload_to='Fashion/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"
    
class FashionVideo(models.Model):
    video = models.FileField(upload_to='Fashion/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

class Toys(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='toys'
    )
    product_name = models.CharField(max_length=250)
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    category = models.CharField(
        max_length=50, 
        choices=[('video_games', 'Video Games'), ('consoles', 'Consoles'), ('toys', 'Toys')], 
        verbose_name="Category"
    )
    brand = models.CharField(max_length=100, verbose_name="Brand")
    platform = models.CharField(
        max_length=20, 
        choices=[('ps5', 'PS5'), ('xbox', 'Xbox'), ('pc', 'PC')], 
        verbose_name="Gaming Platform"
    )
    age_group = models.CharField(
        max_length=20, 
        choices=[
            ('3-5_years', '3-5 years'), 
            ('6-10_years', '6-10 years'), 
            ('11-16_years', '11-16 years'), 
            ('above_16_years', 'Above 16 years')
        ], 
        verbose_name="Age Group"
    )
    condition = models.CharField(
        max_length=11, 
        choices=[('new', 'New'), ('used', 'Used'), ('refurbished', 'Refurbished')], 
        verbose_name="Condition"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'ToysImage', 
        blank=True, 
        related_name='toys', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ToysVideo', 
        blank=True, 
        related_name='toys', 
        verbose_name="Videos"
    )


    

#Food and Supplements
class Food(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='food'
    )
    product_type = models.CharField(
        max_length=50, 
        choices=[
            ('food', 'Food'), 
            ('vitamin', 'Vitamin'), 
            ('herbal', 'Herbal Supplements'), 
            ('protein', 'Protein Supplements'), 
            ('fatty_acids', 'Fatty Acids & Omega-3s')
        ], 
        verbose_name="Product Type"
    )
    product_name=models.TextField(max_length=250)
    brand = models.CharField(max_length=100, verbose_name="Brand")
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    created_at = models.DateTimeField(default=timezone.now)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Quantity (grams/liters/capsules)")
    expiration_date = models.DateField(verbose_name="Expiration Date")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    dietary_info = models.TextField(verbose_name="Dietary Information (e.g., Gluten-Free, Vegan)")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'FoodImage', 
        blank=True, 
        related_name='food', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'FoodVideo', 
        blank=True, 
        related_name='food', 
        verbose_name="Videos"
    )

class FoodImage(models.Model):
    image = models.ImageField(upload_to='Food/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
    
class FoodVideo(models.Model):
    video = models.FileField(upload_to='Food/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

    

# SportsFitness model
class Fitness(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='fitness'
    )
    category = models.CharField(
        max_length=50, 
        choices=[
            ('equipment', 'Equipment'), 
            ('apparel', 'Apparel'), 
            ('team_sports', 'Team Sports'), 
            ('individual_sports', 'Individual Sports'), 
            ('athletics', 'Athletics/Track and Field')
        ], 
        verbose_name="Category"
    )
    product_name=models.TextField(max_length=250)
    brand = models.CharField(max_length=100, verbose_name="Brand")
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    created_at = models.DateTimeField(default=timezone.now)
    condition = models.CharField(
        max_length=11, 
        choices=[('new', 'New'), ('used', 'Used')], 
        verbose_name="Condition"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    warranty_status = models.CharField(
        max_length=10, 
        choices=[('yes', 'Yes'), ('no', 'No')], 
        verbose_name="Warranty Status"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'FitnessImage', 
        blank=True, 
        related_name='fitness', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'FitnessVideo', 
        blank=True, 
        related_name='fitness', 
        verbose_name="Videos"
    )

class FitnessImage(models.Model):
    image = models.ImageField(upload_to='Fitness/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
    
class FitnessVideo(models.Model):
    video = models.FileField(upload_to='Fitness/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

#Pets
class Pet(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='pet'
    )
    pet_type = models.CharField(
        max_length=50, 
        choices=[
            ('dog', 'Dog'), 
            ('cat', 'Cat'), 
            ('fish', 'Fish'), 
            ('rabbit', 'Rabbit'), 
            ('hamster', 'Hamster'), 
            ('hedgehog', 'Hedgehog'), 
            ('bird', 'Lovebird'), 
            ('tortoise', 'Tortoise')
        ], 
        verbose_name="Pet Type"
    )
    pet_name=models.TextField(max_length=250)
    breed = models.CharField(max_length=100, verbose_name="Breed")
    created_at = models.DateTimeField(default=timezone.now)
    age = models.IntegerField(verbose_name="Age (months/years)")
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    vaccinated = models.CharField(
        max_length=3, 
        choices=[('yes', 'Yes'), ('no', 'No')], 
        verbose_name="Vaccination Status"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'PetImage', 
        blank=True, 
        related_name='pet', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'PetVideo', 
        blank=True, 
        related_name='pet', 
        verbose_name="Videos"
    )

    
class Book(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='book'
    )
    category = models.CharField(
        max_length=50, 
        choices=[
            ('fiction', 'Fiction'), 
            ('non_fiction', 'Non-Fiction'), 
            ('children_books', 'Children’s Books'), 
            ('graphic_novels', 'Graphic Novels and Comics'), 
            ('poetry', 'Poetry'), 
            ('textbooks', 'Textbooks and Educational Materials'), 
            ('arts_crafts', 'Arts and Crafts'), 
            ('music', 'Music'), 
            ('photography', 'Photography')
        ], 
        verbose_name="Category"
    )
    book_name=models.TextField(max_length=250)
    genre = models.CharField(max_length=100, verbose_name="Genre (for books)")
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    condition = models.CharField(
        max_length=11, 
        choices=[('new', 'New'), ('used', 'Used')], 
        verbose_name="Condition"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'BookImage', 
        blank=True, 
        related_name='book', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'BookVideo', 
        blank=True, 
        related_name='book', 
        verbose_name="Videos"
    )

class BookImage(models.Model):
    image = models.ImageField(upload_to='Book/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
    
class BookVideo(models.Model):
    video = models.FileField(upload_to='Book/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

# Home Appliance model
class Appliance(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='appliance'
    )
    appliance_type = models.CharField(
        max_length=100, 
        choices=[
            ('refrigerator', 'Refrigerator'), 
            ('washing_machine', 'Washing Machine'), 
            ('oven', 'Oven'), 
            ('microwave', 'Microwave'), 
            ('clothes_dryer', 'Clothes Dryer'), 
            ('vacuum_cleaner', 'Vacuum Cleaner'), 
            ('air_conditioner', 'Air Conditioner')
        ], 
        verbose_name="Appliance Type"
    )
    product_name=models.TextField(max_length=250)
    image = models.ImageField(upload_to='Home Appliances/', verbose_name="Home Appliance Image")
    brand = models.CharField(max_length=100, verbose_name="Brand")
    created_at = models.DateTimeField(default=timezone.now)
    model_number = models.CharField(max_length=100, verbose_name="Model Number")
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    condition = models.CharField(
        max_length=11,  # Increased max_length to 11
        choices=[('new', 'New'), ('used', 'Used'), ('refurbished', 'Refurbished')], 
        verbose_name="Condition"
    )
    warranty_status = models.CharField(
        max_length=10, 
        choices=[('yes', 'Yes'), ('no', 'No')], 
        verbose_name="Warranty Status"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'ApplianceImage', 
        blank=True, 
        related_name='appliance', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ApplianceVideo', 
        blank=True, 
        related_name='appliance', 
        verbose_name="Videos"
    )

class ApplianceImage(models.Model):
    image = models.ImageField(upload_to='Appliance/images/', verbose_name="Image")

    def _str_(self):
        return f"Image {self.id}"
    
class ApplianceVideo(models.Model):
    video = models.FileField(upload_to='Appliance/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

# ----------------------------------------------------community---------------------------------------------------------

#Business Equipments
class Business(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='business'
    )
    category = models.CharField(
        max_length=50, 
        choices=[
            ('computers', 'Computers and Accessories'), 
            ('furniture', 'Office Furniture'), 
            ('telecommunication', 'Telecommunication Equipment'), 
            ('office_supplies', 'Office Supplies'), 
            ('audio_visual', 'Audio-Visual Equipment'), 
            ('storage_solutions', 'Storage Solutions')
        ], 
        verbose_name="Category"
    )
    product_name=models.TextField(max_length=250)
    brand = models.CharField(max_length=100, verbose_name="Brand")
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    created_at = models.DateTimeField(default=timezone.now)
    condition = models.CharField(max_length=11, 
        choices=[('new', 'New'), ('used', 'Used'), ('refurbished', 'Refurbished')], 
        verbose_name="Condition"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    warranty_status = models.CharField(
        max_length=10, 
        choices=[('yes', 'Yes'), ('no', 'No')], 
        verbose_name="Warranty Status"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'BusinessImage', 
        blank=True, 
        related_name='business', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'BusinessVideo', 
        blank=True, 
        related_name='business', 
        verbose_name="Videos"
    )

    def __str__(self):
        return self.brand

class BusinessImage(models.Model):
    image = models.ImageField(upload_to='Business/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class BusinessVideo(models.Model):
    video = models.FileField(upload_to='Business/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    


#Education & Training
class Education(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='education'
    )
    course_type = models.CharField(
        max_length=50, 
        choices=[
            ('online', 'Online Learning'), 
            ('in_person', 'In-person'), 
            ('bootcamp', 'Coding Bootcamps')
        ], 
        verbose_name="Course Type"
    )
    subject = models.CharField(max_length=100, verbose_name="Course Subject")
    duration = models.IntegerField(verbose_name="Duration (weeks/months)")
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Course Fee (OMR)")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    instructor_name = models.CharField(max_length=255, verbose_name="Instructor Name")
    qualification = models.CharField(max_length=255, verbose_name="Instructor Qualification")
    experience = models.TextField(verbose_name="Instructor Experience")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'EducationImage', 
        blank=True, 
        related_name='education', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'EducationVideo', 
        blank=True, 
        related_name='education', 
        verbose_name="Videos"
    )

    def __str__(self):
        return self.subject

class EducationImage(models.Model):
    image = models.ImageField(upload_to='Education/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class EducationVideo(models.Model):
    video = models.FileField(upload_to='Education/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"


# Service Provider
class Service(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='service'
    )
    service_type = models.CharField(
        max_length=50, 
        choices=[
            ('cleaning', 'Cleaning'), 
            ('maintenance', 'Maintenance'), 
            ('consulting', 'Consulting'), 
            ('legal', 'Legal Services'), 
            ('human_resources', 'Human Resources Services'), 
            ('medical', 'Medical Services'), 
            ('fitness', 'Fitness Services')
        ], 
        verbose_name="Service Type"
    )
    provider_name = models.CharField(max_length=255, verbose_name="Service Provider Name")
    price_range = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price Range (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    contact_info = models.TextField(verbose_name="Contact Information")
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'ServiceImage', 
        blank=True, 
        related_name='service', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ServiceVideo', 
        blank=True, 
        related_name='service', 
        verbose_name="Videos"
    )

    def __str__(self):
        return self.provider_name

class ServiceImage(models.Model):
    image = models.ImageField(upload_to='Service/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
    
class ServiceVideo(models.Model):
    video = models.FileField(upload_to='Service/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    

# --------------------------------------------------------Mobile -----------------------------------------

# Computer and Mobile model
class Mobile(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted')
    ]
    PROVIDE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No')
    ]
    CONDITION_CHOICES = [
        ('brand_new', 'Brand New'),
        ('damaged', 'Damaged'),
        ('used_excellent', 'Used - Excellent'),
        ('used_good', 'Used - Good')
    ]
    COLOR_CHOICES = [
        ('black', 'Black'),
        ('blue', 'Blue'),
        ('brown', 'Brown'),
        ('gold', 'Gold'),
        ('green', 'Green'),
        ('grey', 'Grey'),
        ('maroon', 'Maroon'),
        ('orange', 'Orange'),
        ('pearl_white', 'Pearl White'),
        ('pink', 'Pink'),
        ('purple', 'Purple'),
        ('red', 'Red'),
        ('rose_gold', 'Rose Gold'),
        ('silver', 'Silver'),
        ('turquoise', 'Turquoise'),
        ('white', 'White'),
        ('yellow', 'Yellow'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    
  
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='mobile'
    )
    
    brand = models.CharField(max_length=100, verbose_name="Brand")
    description = models.TextField(max_length=1000,verbose_name="Property Description")

    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )
    model_number = models.CharField(max_length=100, verbose_name="Model Number")
    created_at = models.DateTimeField(default=timezone.now)
    year = models.CharField(max_length=100,verbose_name="Year of Manufacture",default='2012')
    color = models.CharField(max_length=20, choices=COLOR_CHOICES,default='black')
    STORAGE_CHOICES = [
        ('4GB', '4GB'),
        ('8GB', '8GB'),
        ('16GB', '16GB'),
        ('32GB', '32GB'),
        ('64GB', '64GB'),
        ('128GB', '128GB'),
        ('256GB', '256GB'),
        ('512GB', '512GB'),
        ('1TB', '1TB'),
        ('2TB', '2TB'),
    ]
    
    storage_capacity = models.CharField(
        max_length=20,
        choices=STORAGE_CHOICES,
        default='128GB'  
    )
    ACCOMPANIMENT_CHOICES = [
        ('box', 'Original Box'),
        ('charger', 'Charger'),
        ('headset', 'Headset'),
    ]
    accompaniments = models.CharField(
        max_length=100,
        blank=True,
        choices=ACCOMPANIMENT_CHOICES,
        default='box'  
    )
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES,default='sale')
    provide = models.CharField(max_length=3, choices=PROVIDE_CHOICES,default='yes')
    
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(
        max_length=100, 
        choices=CONDITION_CHOICES, 
        verbose_name="Condition"
    )
    
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='mobiles')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'MobileImage', 
        blank=True, 
        related_name='mobile', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'MobileVideo', 
        blank=True, 
        related_name='mobile', 
        verbose_name="Videos"
    )
   

    def __str__(self):
        return self.brand

class MobileImage(models.Model):
    image = models.ImageField(upload_to='Mobile/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"
    
class MobileVideo(models.Model):
    video = models.FileField(upload_to='Mobile/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"


class Tablet(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted')
    ]

    PROVIDE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No')
    ]

    COLOR_CHOICES = [
        ('black', 'Black'), ('blue', 'Blue'), ('brown', 'Brown'), ('gold', 'Gold'),
        ('green', 'Green'), ('grey', 'Grey'), ('maroon', 'Maroon'), ('orange', 'Orange'),
        ('pearl_white', 'Pearl White'), ('pink', 'Pink'), ('purple', 'Purple'),
        ('red', 'Red'), ('rose_gold', 'Rose Gold'), ('silver', 'Silver'),
        ('turquoise', 'Turquoise'), ('white', 'White'), ('yellow', 'Yellow'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    SCREEN_SIZE_CHOICES = [
        ('5', '5 inch'), ('5.5', '5.5 inch'), ('6', '6 inch'), ('6.9', '6.9 inch'),
        ('7', '7 inch'), ('7.7', '7.7 inch'), ('7.9', '7.9 inch'), ('8', '8 inch'),
        ('8.4', '8.4 inch'), ('8.7', '8.7 inch'), ('8.9', '8.9 inch'), ('9.4', '9.4 inch'),
        ('9.7', '9.7 inch'), ('10', '10 inch'), ('10.1', '10.1 inch'), ('10.2', '10.2 inch'),
        ('10.4', '10.4 inch'), ('10.5', '10.5 inch'), ('10.8', '10.8 inch'), ('10.9', '10.9 inch'),
        ('10.95', '10.95 inch'), ('11', '11 inch'), ('11.6', '11.6 inch'), ('12', '12 inch'),
        ('12.2', '12.2 inch'), ('12.3', '12.3 inch'), ('12.4', '12.4 inch'), ('12.5', '12.5 inch'),
        ('12.9', '12.9 inch'), ('13.3', '13.3 inch'), ('14', '14 inch'), ('17.3', '17.3 inch'),
        ('18.4', '18.4 inch'),
    ]
    ACCOMPANIMENT_CHOICES = [
        ('box', 'Original Box'),
        ('charger', 'Charger'),
        ('headset', 'Headset'),
    ]
    accompaniments = models.CharField(
        max_length=100,
        blank=True,
        choices=ACCOMPANIMENT_CHOICES,
        default='box'  
    )

    CONDITION_CHOICES = [
        ('brand_new', 'Brand New'),
        ('damaged', 'Damaged'),
        ('used_excellent', 'Used - Excellent'),
        ('used_good', 'Used - Good')
    ]

    # Fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='tablets'
    )

    brand = models.CharField(max_length=100, verbose_name="Brand")
    model_number = models.CharField(max_length=100, verbose_name="Model Number")

    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    color = models.CharField(max_length=20, choices=COLOR_CHOICES)
    STORAGE_CHOICES = [
        ('4GB', '4GB'),
        ('8GB', '8GB'),
        ('16GB', '16GB'),
        ('32GB', '32GB'),
        ('64GB', '64GB'),
        ('128GB', '128GB'),
        ('256GB', '256GB'),
        ('512GB', '512GB'),
        ('1TB', '1TB'),
        ('2TB', '2TB'),
    ]
    
    storage_capacity = models.CharField(
        max_length=20,
        choices=STORAGE_CHOICES,
        default='128GB'  
    )
    screen_size = models.CharField(
        max_length=10,
        choices=SCREEN_SIZE_CHOICES,
        blank=True,
        null=True,
        verbose_name="Screen Size (only for tablets)"
    )
    AGE_CHOICES = [
        ('brand_new', 'Brand New'),
        ('0_1_year', '0-1 Year'),
        ('2_3_year', '2-3 Year'),
        ('more_than_3_year', 'More Than 3 Year')
    ]
    age = models.CharField(
        max_length=20,
        choices=AGE_CHOICES,
        default='brand_new',
        verbose_name="Age"
    )

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    provide = models.CharField(max_length=3, choices=PROVIDE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(max_length=100, choices=CONDITION_CHOICES, verbose_name="Condition")

    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='tablets')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )

    images = models.ManyToManyField(
        'TabletImage',
        blank=True,
        related_name='tablet',
        verbose_name="Images"
    )

    videos = models.ManyToManyField(
        'TabletVideo',
        blank=True,
        related_name='tablet',
        verbose_name="Videos"
    )
    

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.brand} {self.model_number}"


class TabletImage(models.Model):
    image = models.ImageField(upload_to='Tablet/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class TabletVideo(models.Model):
    video = models.FileField(upload_to='Tablet/videos/', verbose_name="Video")

    def __str__(self):
        return f"Tablet Video {self.id}"


class SmartWatch(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted')
    ]

    PROVIDE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No')
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    CONDITION_CHOICES = [
        ('brand_new', 'Brand New'),
        ('damaged', 'Damaged'),
        ('used_excellent', 'Used - Excellent Condition'),
        ('used_good', 'Used - Good Condition')
    ]
    

    # Fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='smartwatches'
    )

    brand = models.CharField(max_length=100, verbose_name="Brand")
    description = models.TextField(max_length=1000,verbose_name="Description")
    title = models.CharField(max_length=255, verbose_name="Title" ,default='Apple brandnew white smartwatch')

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    provide = models.CharField(max_length=3, choices=PROVIDE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(max_length=100, choices=CONDITION_CHOICES, verbose_name="Condition")

    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='smartwatches')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )

    images = models.ManyToManyField(
        'SmartWatchImage',
        blank=True,
        related_name='smartwatch',
        verbose_name="Images"
    )

    videos = models.ManyToManyField(
        'SmartWatchVideo',
        blank=True,
        related_name='smartwatch',
        verbose_name="Videos"
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.brand} {self.model_number}"


class SmartWatchImage(models.Model):
    image = models.ImageField(upload_to='SmartWatch/images/', verbose_name="Image")

   # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class SmartWatchVideo(models.Model):
    video = models.FileField(upload_to='SmartWatch/videos/', verbose_name="Video")

    def __str__(self):
        return f"SmartWatch Video {self.id}"
    
class Headset(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted')
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    PROVIDE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No')
    ]

    CONDITION_CHOICES = [
        ('brand_new', 'Brand New'),
        ('damaged', 'Damaged'),
        ('used_excellent', 'Used - Excellent Condition'),
        ('used_good', 'Used - Good Condition')
    ]
    # Fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='headsets'
    )

    title = models.CharField(max_length=255, verbose_name="Title")
    
    description = models.TextField(max_length=1000,verbose_name="Description")

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    provide = models.CharField(max_length=3, choices=PROVIDE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(max_length=100, choices=CONDITION_CHOICES, verbose_name="Condition")

    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='headsets')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )

    images = models.ManyToManyField(
        'HeadsetImage',
        blank=True,
        related_name='headset',
        verbose_name="Images"
    )

    videos = models.ManyToManyField(
        'HeadsetVideo',
        blank=True,
        related_name='headset',
        verbose_name="Videos"
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} - {self.brand}"


class HeadsetImage(models.Model):
    image = models.ImageField(upload_to='headsets/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class HeadsetVideo(models.Model):
    video = models.FileField(upload_to='headsets/videos/', verbose_name="Video")

    def __str__(self):
        return f"Headset Video {self.id}"

class Cover(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted')
    ]

    PROVIDE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No')
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    CONDITION_CHOICES = [
        ('brand_new', 'Brand New'),
        ('damaged', 'Damaged'),
        ('used_excellent', 'Used - Excellent Condition'),
        ('used_good', 'Used - Good Condition')
    ]
    # Fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='covers'
    )

    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(max_length=1000,verbose_name="Description")

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    provide = models.CharField(max_length=3, choices=PROVIDE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(max_length=100, choices=CONDITION_CHOICES, verbose_name="Condition")

    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='covers')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )

    images = models.ManyToManyField(
        'CoverImage',
        blank=True,
        related_name='cover',
        verbose_name="Images"
    )

    videos = models.ManyToManyField(
        'CoverVideo',
        blank=True,
        related_name='cover',
        verbose_name="Videos"
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title


class CoverImage(models.Model):
    image = models.ImageField(upload_to='covers/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class CoverVideo(models.Model):
    video = models.FileField(upload_to='covers/videos/', verbose_name="Video")

    def __str__(self):
        return f"Cover Video {self.id}"

class Accessory(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    PROVIDE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    CONDITION_CHOICES = [
        ('brand_new', 'Brand New'),
        ('damaged', 'Damaged'),
        ('used_excellent', 'Used - Excellent Condition'),
        ('used_good', 'Used - Good Condition')
    ]

    TYPE_CHOICES = [
        ('charger', 'Charger'),
        ('sparepart', 'Spare Part'),
        ('accessory', 'Accessory'),
    ]

    # Common Fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accessories'
    )

    type = models.CharField(max_length=20, choices=TYPE_CHOICES, verbose_name="Item Type")

    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(max_length=1000,verbose_name="Description")

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    provide = models.CharField(max_length=3, choices=PROVIDE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(max_length=100, choices=CONDITION_CHOICES, verbose_name="Condition")

    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='accessories')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    images = models.ManyToManyField(
        'AccessoryImage',
        blank=True,
        related_name='accessory',
        verbose_name="Images"
    )

    videos = models.ManyToManyField(
        'AccessoryVideo',
        blank=True,
        related_name='accessory',
        verbose_name="Videos"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_type_display()} - {self.title}"


class AccessoryImage(models.Model):
    image = models.ImageField(upload_to='accessory/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class AccessoryVideo(models.Model):
    video = models.FileField(upload_to='accessory/videos/', verbose_name="Video")

    def __str__(self):
        return f"Cover Video {self.id}"

from django.core.validators import RegexValidator
class MobileSIM(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted'),
    ]

    PROVIDE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]

    MOBILE_OPERATOR_CHOICES = [
    ('omantel', 'Omantel'),
    ('ooredoo', 'Ooredoo'),
    ('vodafone', 'Vodafone Oman'),
    ('friendi', 'FRiENDi mobile'),
    ('renna', 'Renna Mobile'),
    ('redbull', 'RedBull MOBILE'),
]


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='mobilesims'
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    oman_number = models.CharField(
    max_length=8,
    validators=[
        RegexValidator(
            regex=r'^\d{8}$',
            message="Enter a valid 8-digit number."
        )
    ],
    verbose_name="Oman Mobile Number"
    )

    operator = models.CharField(max_length=20, choices=MOBILE_OPERATOR_CHOICES, verbose_name="Mobile Operator")
    

    title = models.CharField(max_length=255, verbose_name="Title")
    description = models.TextField(max_length=1000,verbose_name="Description")

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    provide = models.CharField(max_length=3, choices=PROVIDE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")

    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='mobilesims')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )



    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.get_operator_display()} - {self.oman_number}"




class Computer(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='computer'
    )
    product_name=models.TextField(max_length=250)
    brand = models.CharField(max_length=100, verbose_name="Brand")
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    model_number = models.CharField(max_length=100, verbose_name="Model Number")
    operating_system = models.CharField(
        max_length=50, 
        choices=[
            ('windows', 'Windows'),
            ('macOS', 'macOS'),
            ('linux', 'Linux'),
            ('other', 'Other')
        ], 
        verbose_name="Operating System"
    )
    screen_size = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Screen Size (inches)")
    storage_capacity = models.IntegerField(verbose_name="Storage Capacity (GB)")
    ram_size = models.IntegerField(verbose_name="RAM Size (GB)")
    processor = models.CharField(max_length=100, verbose_name="Processor Type")
    graphics_card = models.CharField(max_length=100, verbose_name="Graphics Card", null=True, blank=True)
    battery_life = models.CharField(max_length=50, verbose_name="Battery Life (hours)", null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(
        max_length=11, 
        choices=[
            ('new', 'New'),
            ('used', 'Used'),
            ('refurbished', 'Refurbished')
        ], 
        verbose_name="Condition"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'ComputerImage', 
        blank=True, 
        related_name='computer', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ComputerVideo', 
        blank=True, 
        related_name='computer', 
        verbose_name="Videos"
    )

    def __str__(self):
        return self.brand



class Sound(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout')
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='sound'
    )
    product_name=models.TextField(max_length=250)
    brand = models.CharField(max_length=100, verbose_name="Brand")
    model_number = models.CharField(max_length=100, verbose_name="Model Number")
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    connectivity = models.CharField(
        max_length=50, 
        choices=[
            ('bluetooth', 'Bluetooth'),
            ('wifi', 'Wi-Fi'),
            ('aux', 'AUX'),
            ('usb', 'USB'),
            ('other', 'Other')
        ], 
        verbose_name="Connectivity"
    )
    output_power = models.CharField(max_length=50, verbose_name="Output Power (e.g., 20W)")
    channels = models.CharField(max_length=50, verbose_name="Audio Channels (e.g., 2.1, 5.1)", null=True, blank=True)
    has_smart_assistant = models.BooleanField(default=False, verbose_name="Smart Assistant Support")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(
        max_length=11, 
        choices=[
            ('new', 'New'),
            ('used', 'Used'),
            ('refurbished', 'Refurbished')
        ], 
        verbose_name="Condition"
    )
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Batinah'),
        ('DA', 'Dakhiliyah'),
        ('SH', 'Sharqiyah'),
        ('BR', 'Buraimi'),
        ('ZU', 'Zufar'),
        ('MW', 'Musandam'),
        ('WR', 'Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    cities=models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    location=models.TextField(max_length=250)
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'DeviceImage', 
        blank=True, 
        related_name='sound', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'SoundVideo', 
        blank=True, 
        related_name='sound', 
        verbose_name="Videos"
    )

    def __str__(self):
        return self.brand
   
class DeviceImage(models.Model):
    image = models.ImageField(upload_to='Mobile/devices/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
    
class SoundVideo(models.Model):
    video = models.FileField(upload_to='Mobile/devices/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
                                                                                                                                                                                               
                                                                                                                                                                                              
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

class Favorite(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Using the custom user model from settings
        on_delete=models.CASCADE,
        related_name='favorites'  # You can change the related name as needed
    )
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def _str_(self):
        return f"{self.user} - {self.content_object}"


class Company(models.Model):
    COMPANY_TYPES = [
        ('private', 'Private'),
        ('partnership', 'Partnership'),
        ('civil_company', 'Civil Company'),
        ('public', 'Public'),
    ]

    INDUSTRIES = [
        ('agriculture', 'Agriculture'),
        ('accounting', 'Accounting'),
        ('it', 'IT'),
        ('education', 'Education'),
        ('healthcare', 'Healthcare'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='companies'
    )
    company_name = models.CharField(max_length=255,unique=True)
    company_type = models.CharField(max_length=20, choices=COMPANY_TYPES)
    trade_license = models.CharField(max_length=50)
    contact_name = models.CharField(max_length=255)
    linkedin = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    industry = models.CharField(max_length=50, choices=INDUSTRIES)
    company_size = models.PositiveIntegerField()
    phone = models.CharField(max_length=20)
    logo = models.ImageField(upload_to='company_logos/')
    website = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    description = models.TextField()
    email = models.EmailField()
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="City")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    
    def __str__(self):
        return self.company_name
    

class JobPost(models.Model):
    EXPERIENCE_CHOICES = [
        ("none", "No Experience Required"),
        ("newbie", "Newbie"),
        ("1-2", "1-2 Years"),
        ("3-5", "3-5 Years"),
        ("6-10", "6-10 Years"),
        ("11-15", "11-15 Years"),
        ("15+", "15+ Years"),
    ]

    GENDER_CHOICES = [
        ("any", "Any"),
        ("male", "Male"),
        ("female", "Female"),
    ]

    NATIONALITY_CHOICES = [
        ("citizen", "Citizen"),
        ("non-citizen", "Non-Citizen"),
    ]

    QUALIFICATION_CHOICES = [
        ("noschool", "No Formal Education"),
        ("basic", "Basic Education (Grades 1–10)"),
        ("secondary", "General Secondary (Grades 11–12)"),
        ("vocational", "Vocational / Technical Certificate"),
        ("diploma", "Diploma (Higher College of Technology / Colleges of Applied Sciences)"),
        ("bachelor", "Bachelor’s Degree"),
        ("master", "Master’s Degree"),
        ("phd", "Doctorate (PhD)"),
    ]

    WORKING_DAYS_CHOICES = [
        ("2", "2 days / week"),
        ("3", "3 days / week"),
        ("4", "4 days / week"),
        ("5", "5 days / week"),
        ("6", "6 days / week"),
        ("7", "7 days / week"),
    ]

    WORKING_HOUR_CHOICES = [
        ("fixed", "Fixed Working Hours"),
        ("shift", "Shift"),
        ("hourly", "Hourly"),
    ]

    VACANCY_CHOICES = [
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("6+", "6+"),
    ]
    JOB_CHOICES = [
            ("full-time", "Full-time"),
            ("part-time", "Part-time"),
            ("contract", "Contract"),
            ("temporary", "Temporary"),
            ("freelance", "Freelance"),
            ("internship", "Internship"),
    ]
    title = models.CharField(max_length=200, help_text="Job Title (e.g., Software Developer)")
    description = models.TextField(help_text="Detailed description of the role, responsibilities, and expectations.")
    job_type = models.CharField(
        max_length=50,choices=JOB_CHOICES, 
        default="full-time",
    )
    job_category = models.ForeignKey(JobCategory, on_delete=models.CASCADE, related_name="job_posts")
    salary_range = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Salary Range")
   
    number_of_vacancies = models.CharField(max_length=3, choices=VACANCY_CHOICES, default="1")
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact_email = models.EmailField()
    qualifications = models.CharField(max_length=50, choices=QUALIFICATION_CHOICES, default="secondary")
    skills_required = models.TextField()
    experience_required = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, default="none")
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="any")
    nationality = models.CharField(max_length=20, choices=NATIONALITY_CHOICES, default="non-citizen")
    application_deadline = models.DateField()
    working_hours = models.CharField(max_length=20, choices=WORKING_HOUR_CHOICES, default="fixed")  # ✅ back to original style
    working_days = models.CharField(max_length=10, choices=WORKING_DAYS_CHOICES, default="5")
    posted_on = models.DateTimeField(auto_now_add=True)
    

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jobs"
    )

    def __str__(self):
        return self.title

class JobApplication(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Link to the custom user model
        on_delete=models.CASCADE,  # Delete applications if the user is deleted
        related_name='job_applications',  # Related name for reverse access
        verbose_name="User"
    )
    job = models.ForeignKey(
        JobPost,
        on_delete=models.CASCADE,
        related_name='applications',
        verbose_name="Job"
    )
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, verbose_name="Full Name")
    email = models.EmailField(verbose_name="Email Address")
    phone = models.CharField(max_length=15, verbose_name="Phone Number")
    resume = models.FileField(upload_to='resumes/', verbose_name="Upload Resume")
    applied_on = models.DateTimeField(auto_now_add=True, verbose_name="Applied On")

    def __str__(self):
        return f"{self.name} ({self.email})"


# models.py
from django.conf import settings
from django.db import models
from django.utils.timezone import now

class ChatMessage(models.Model):
    # Add this field to uniquely identify each product chat session
    chat_session_id = models.CharField(max_length=100, blank=True, null=True, db_index=True)
    
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    message = models.TextField()
    timestamp = models.DateTimeField(default=now)
    is_read = models.BooleanField(default=False)
    is_admin_chat = models.BooleanField(default=False)
    
    # Product reference - REQUIRED for product chats
    product_id = models.IntegerField(null=True, blank=True)
    product_type = models.CharField(max_length=20, null=True, blank=True)
    
    # New fields for delete functionality
    is_deleted_for_everyone = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['chat_session_id']),
            models.Index(fields=['sender', 'receiver', 'product_id', 'product_type']),
        ]
    
    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} - {self.message[:30]}"
    
    def save(self, *args, **kwargs):
        # Generate chat_session_id if we have product info
        if self.product_id and self.product_type and self.sender and self.receiver:
            # Create a unique session ID for this specific product chat
            # Format: user1_user2_producttype_productid (sorted so it's always the same)
            user_ids = sorted([str(self.sender.id), str(self.receiver.id)])
            self.chat_session_id = f"{user_ids[0]}_{user_ids[1]}_{self.product_type}_{self.product_id}"
        super().save(*args, **kwargs)
    
    def delete_for_user(self, user):
        """Soft delete for a specific user"""
        DeletedMessage.objects.get_or_create(
            message=self,
            deleted_by=user
        )
    
    def delete_for_everyone(self):
        """Delete message for everyone"""
        self.is_deleted_for_everyone = True
        self.deleted_at = now()
        self.message = "[This message has been deleted]"
        self.save(update_fields=['is_deleted_for_everyone', 'deleted_at', 'message'])
    
    def is_deleted_for_user(self, user):
        """Check if message is deleted for a specific user"""
        if self.is_deleted_for_everyone:
            return True
        return DeletedMessage.objects.filter(
            message=self,
            deleted_by=user
        ).exists()


class BlockedUser(models.Model):
    """Model to track blocked users"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='blocked_users'
    )
    blocked_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='blocked_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'blocked_user')
        indexes = [
            models.Index(fields=['user', 'blocked_user']),
        ]
        
    def __str__(self):
        return f"{self.user} blocked {self.blocked_user}"


class DeletedMessage(models.Model):
    """Model to track messages deleted by users"""
    message = models.ForeignKey('ChatMessage', on_delete=models.CASCADE, related_name='deletions')
    deleted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    deleted_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('message', 'deleted_by')
        indexes = [
            models.Index(fields=['message', 'deleted_by']),
        ]
    
    def __str__(self):
        return f"Message {self.message.id} deleted by {self.deleted_by.username}"
    
class Automobile(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]

    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    LISTER_TYPE_CHOICES = [
    ('owner', 'Owner'),
    ('dealer', 'Dealer'),
   ]
    CYLINDER_CHOICES = [
    ('4', '4 Cylinders'),
    ('6', '6 Cylinders'),
    ('8', '8 Cylinders'),
    ('8+', '8+ Cylinders'),
    ]
    REGIONAL_SPEC_CHOICES = [
    ('gcc', 'GCC'),
    ('gccoman', 'GCC(Oman)'),
    ('american', 'American'),
    ('canadian', 'Canadian'),
    ('euro', 'European'),
    ('japanese', 'Japanese'),
    ('korean', 'Korean'),
    ('chinese', 'Chinese'),
    ('other', 'Other'),
]

    DOOR_CHOICES = [
    ('2', '2 Doors'),
    ('3', '3 Doors'),
    ('4', '4 Doors'),
    ('5+', '5+ Doors'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
   

    BODY_TYPE_CHOICES = [
        ('bus_van', 'Bus - Van'),
        ('convertible', 'Convertible'),
        ('coupe', 'Coupe'),
        ('hatchback', 'HatchBack'),
        ('pickup', 'PickUp'),
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('truck', 'Truck'),
    ]

    LICENSE_STATUS_CHOICES = [
        ('licensed', 'Licensed'),
        ('not_licensed', 'Not Licensed')
    ]
    WARRANTY_CHOICES = [
    ('yes', 'Yes'),
    ('no', 'No'),
    ('does not apply', 'N/A'),
]


    INSURANCE_TYPE_CHOICES = [
        ('comprehensive', 'Comprehensive Insurance'),
        ('compulsory', 'Compulsory Insurance'),
        ('none', 'Not Insured')
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    COLOR_CHOICES = [
        ('black', 'Black'),
        ('white', 'White'),
        ('gray', 'Gray'),
        ('silver', 'Silver'),
        ('red', 'Red'),
        ('blue', 'Blue'),
        ('navy', 'Navy Blue'),
        ('green', 'Green'),
        ('beige', 'Beige'),
        ('brown', 'Brown'),
        ('yellow', 'Yellow'),
        ('orange', 'Orange'),
        ('maroon', 'Maroon'),
        ('gold', 'Gold'),
        ('purple', 'Purple'),
        ('pink', 'Pink'),
        ('skyblue', 'Sky Blue'),
        ('champagne', 'Champagne'),
        ('burgundy', 'Burgundy'),
        ('turquoise', 'Turquoise'),
    ]

    KM_CHOICES = [
    ('1000-9999', '1,000 - 9,999 km'),
    ('10000-19999', '10,000 - 19,999 km'),
    ('20000-29999', '20,000 - 29,999 km'),
    ('30000-39999', '30,000 - 39,999 km'),
    ('40000-49999', '40,000 - 49,999 km'),
    ('50000-59999', '50,000 - 59,999 km'),
    ('60000-69999', '60,000 - 69,999 km'),
    ('70000-79999', '70,000 - 79,999 km'),
    ('80000-89999', '80,000 - 89,999 km'),
    ('90000-99999', '90,000 - 99,999 km'),
    ('100000-119999', '100,000 - 119,999 km'),
    ('120000-139999', '120,000 - 139,999 km'),
    ('140000-159999', '140,000 - 159,999 km'),
    ('160000-179999', '160,000 - 179,999 km'),
    ('180000-199999', '180,000 - 199,999 km'),
    ('200000+', '200,000+ km'),
    ]




    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cars')
    name = models.CharField(max_length=100, verbose_name="Name")
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )
    
    make = models.CharField(max_length=100, verbose_name="Car Manufacturer")
    SEAT_CHOICES = [
    ("2", "2 Seats"),
    ("3", "3 Seats"),
    ("4", "4 Seats"),
    ("5", "5 Seats"),
    ("6", "6 Seats"),
    ("7", "7 Seats"),
    ("8", "8 Seats"),
    ("8+", "8+ Seats"),
    ]

    seats = models.CharField(
    max_length=5,
    choices=SEAT_CHOICES,
    null=True,
    blank=True,
    verbose_name="Number of Seats"
    )

    year = models.PositiveIntegerField(
        verbose_name="Year of Manufacture",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year + 1)
        ]
    )
    doors = models.CharField(max_length=3,choices=DOOR_CHOICES,verbose_name="Number of Doors",null=True,blank=True, default='2')
    cylinders = models.CharField( max_length=3,choices=CYLINDER_CHOICES,verbose_name="Number of Cylinders",null=True,blank=True
    )
    kilometers = models.CharField(
    max_length=20,
    choices=KM_CHOICES,
    verbose_name="Kilometers",
    null=True,
    blank=True
    )


    lister_type = models.CharField(max_length=10,choices=LISTER_TYPE_CHOICES,verbose_name="Lister Type",default='dealer')
    warranty = models.CharField(max_length=20,choices=WARRANTY_CHOICES,null=True,blank=True,verbose_name="Warranty",default='yes')

    body_type = models.CharField(
        max_length=50,
        choices=BODY_TYPE_CHOICES,
        verbose_name="Car Body Type"
    )

    created_at = models.DateTimeField(default=timezone.now)

    fuel_type = models.CharField(
        max_length=50,
        choices=[
            ('petrol', 'Petrol'),
    ('diesel', 'Diesel'),
    ('hybrid', 'Hybrid'),
    ('electric', 'Electric'), 
        ],
        verbose_name="Fuel Type"
    )

    transmission = models.CharField(
        max_length=50,
        choices=[('automatic', 'Automatic'), ('manual', 'Manual')],
        verbose_name="Transmission Type"
    )

    interior_color = models.CharField(
        max_length=50,
        choices=COLOR_CHOICES,
        verbose_name="Interior Color"
    )

    exterior_color = models.CharField(
        max_length=50,
        choices=COLOR_CHOICES,
        verbose_name="Exterior Color"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")

    listing_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES, default='sale', verbose_name="Listing Type")
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='automobiles')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    description = models.TextField(max_length=1000,verbose_name="Description")

    condition = models.CharField(
        max_length=10,
        choices=[('new', 'New'), ('used', 'Used')],
        verbose_name="Condition"
    )

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    ENGINE_CAPACITY_CHOICES = [
    ('0-499', '0–499 cc'),
    ('500-999', '500–999 cc'),
    ('1000-1499', '1000–1499 cc'),
    ('1500-1999', '1500–1999 cc'),
    ('2000-2499', '2000–2499 cc'),
    ('2500-2999', '2500–2999 cc'),
    ('3000-3999', '3000–3999 cc'),
    ('4000-4999', '4000–4999 cc'),
    ('5000-5999', '5000–5999 cc'),
    ('6000+', '6000+ cc'),
    ]

    engine_capacity = models.CharField(
    max_length=20,
    choices=ENGINE_CAPACITY_CHOICES,
    verbose_name="Engine Capacity",
    null=True,
    blank=True
    )

    
    HORSEPOWER_CHOICES = [
    ("0-99", "0–99 HP"),
    ("100-199", "100–199 HP"),
    ("200-299", "200–299 HP"),
    ("300-399", "300–399 HP"),
    ("400+", "400+ HP"),
    ]

    horsepower = models.CharField(
    max_length=20,
    choices=HORSEPOWER_CHOICES,
    null=True,
    blank=True,
    verbose_name="Horsepower (HP)"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )

    regional_spec = models.CharField(
        max_length=20,
        choices=REGIONAL_SPEC_CHOICES,
        default='gcc',
        verbose_name="Regional Specification"
    )

    vin_chassis_number = models.CharField(
        max_length=250,
        verbose_name="VIN/Chassis Number",
        blank=True,
        null=True,
        unique=True
    )
    interior_options = models.ManyToManyField(
        'InteriorOptions',
        blank=True,
        related_name='automobiles',
        verbose_name="Interior Options"
    )
    exterior_options = models.ManyToManyField(
        'ExteriorOptions',
        blank=True,
        related_name='cars',
        verbose_name="Exterior Options"
    )
    technology_options = models.ManyToManyField(
        'TechnologyOptions',
        blank=True,
        related_name='cars',
        verbose_name="Technology Options"
    )

    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )

    car_license_status = models.CharField(
        max_length=20,
        choices=LICENSE_STATUS_CHOICES,
        verbose_name="Car License Status",
        null=True,
        blank=True
    )

    insurance_type = models.CharField(
        max_length=20,
        choices=INSURANCE_TYPE_CHOICES,
        verbose_name="Insurance Type",
        null=True,
        blank=True
    )
   
    images = models.ManyToManyField(
        'AutomobileImage', 
        blank=True, 
        related_name='automobile', 
        verbose_name="Images"
    )

    videos = models.ManyToManyField(
        'AutomobileVideo', 
        blank=True, 
        related_name='automobile', 
        verbose_name="Videos"
    )

class AutomobileImage(models.Model):
    image = models.ImageField(upload_to='automobile/images/', verbose_name="Image")

     # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class AutomobileVideo(models.Model):
    video = models.FileField(upload_to='automobile/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
  

class Motorcycle(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    LISTER_TYPE_CHOICES = [
    ('owner', 'Owner'),
    ('dealer', 'Dealer'),
   ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    BODY_TYPE_CHOICES = [
        ('adventure', 'Adventure'),
        ('budgy', 'Budgy'),
        ('cruiser', 'Cruiser'),
        ('offroad', 'Offroad'),
        ('scooter', 'Scooter'),
        ('sport', 'Sport'),
        ('street', 'Street'),
        ('tricycle', 'Tricycle'),
        ('other', 'Other'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='motorcycles'
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    make = models.CharField(max_length=100, verbose_name="Manufacturer")
    model = models.CharField(max_length=100, verbose_name="Model")
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )
    created_at = models.DateTimeField(default=timezone.now)
    year = models.PositiveIntegerField(
        verbose_name="Year of Manufacture",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year + 1)
        ]
    )
    description = models.TextField(max_length=1000,verbose_name="Description")
    KILOMETER_CHOICES = [
        ('0-5k', '0 - 5,000 km'),
        ('5k-10k', '5,000 - 10,000 km'),
        ('10k-20k', '10,000 - 20,000 km'),
        ('20k-30k', '20,000 - 30,000 km'),
        ('30k-40k', '30,000 - 40,000 km'),
        ('40k-50k', '40,000 - 50,000 km'),
        ('50k-75k', '50,000 - 75,000 km'),
        ('75k-100k', '75,000 - 100,000 km'),
        ('100k-150k', '100,000 - 150,000 km'),
        ('150k-200k', '150,000 - 200,000 km'),
        ('200k+', '200,000 km and above'),
    ]

    kilometers = models.CharField(
        max_length=20,
        choices=KILOMETER_CHOICES,
        null=True,
        blank=True,
        verbose_name="Kilometers"
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='motorcycle')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    body_type = models.CharField(
        max_length=50,
        choices=BODY_TYPE_CHOICES,
        verbose_name="Car Body Type"
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sale',
        verbose_name="Listing Type"
    )
    ENGINE_CAPACITY_CHOICES = [
        ('11-250', '11 – 250 cc'),
        ('250-499', '250 – 499 cc'),
        ('500-599', '500 – 599 cc'),
        ('600-749', '600 – 749 cc'),
        ('750-999', '750 – 999 cc'),
        ('1000+', '1000 cc and above'),
    ]

    engine_capacity = models.CharField(
        max_length=20,
        choices=ENGINE_CAPACITY_CHOICES,
        null=True,
        blank=True,
        verbose_name="Engine Capacity (cc)"
    )
    lister_type = models.CharField(max_length=10,choices=LISTER_TYPE_CHOICES,verbose_name="Lister Type",default='dealer')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(
        max_length=10,
        choices=[('new', 'New'), ('used', 'Used')],
        verbose_name="Condition"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'MotorcycleImage', 
        blank=True, 
        related_name='motorcycle', 
        verbose_name="Images"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )
    videos = models.ManyToManyField(
        'MotorcycleVideo', 
        blank=True, 
        related_name='motorcycle', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class MotorcycleImage(models.Model):
    image = models.ImageField(upload_to='Motorcycle/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class MotorcycleVideo(models.Model):
    video = models.FileField(upload_to='Motorcycle/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    
class Scooter(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    LISTER_TYPE_CHOICES = [
    ('owner', 'Owner'),
    ('dealer', 'Dealer'),
   ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    FUEL_TYPE_CHOICES = [
        ('petrol', 'Petrol'),
        ('electric', 'Electric'),
    ]
    fuel_type = models.CharField(
        max_length=20,
        choices=FUEL_TYPE_CHOICES,
        null=True,
        blank=True,
        verbose_name="Fuel Type"
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='scooter'
    )
    make = models.CharField(max_length=100, verbose_name="Manufacturer")
    model = models.CharField(max_length=100, verbose_name="Model")
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )
    created_at = models.DateTimeField(default=timezone.now)
    year = models.PositiveIntegerField(
        verbose_name="Year of Manufacture",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year + 1)
        ]
    )
    description = models.TextField(max_length=1000,verbose_name="Description")
    KILOMETER_CHOICES = [
        ('0-5k', '0 - 5,000 km'),
        ('5k-10k', '5,000 - 10,000 km'),
        ('10k-20k', '10,000 - 20,000 km'),
        ('20k-30k', '20,000 - 30,000 km'),
        ('30k-40k', '30,000 - 40,000 km'),
        ('40k-50k', '40,000 - 50,000 km'),
        ('50k-75k', '50,000 - 75,000 km'),
        ('75k-100k', '75,000 - 100,000 km'),
        ('100k-150k', '100,000 - 150,000 km'),
        ('150k-200k', '150,000 - 200,000 km'),
        ('200k+', '200,000 km and above'),
    ]

    kilometers = models.CharField(
        max_length=20,
        choices=KILOMETER_CHOICES,
        null=True,
        blank=True,
        verbose_name="Kilometers"
    )
    lister_type = models.CharField(max_length=10,choices=LISTER_TYPE_CHOICES,verbose_name="Lister Type",default='dealer')
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='scooter')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sale',
        verbose_name="Listing Type"
    )
    ENGINE_CAPACITY_CHOICES = [
        ('11-250', '11 – 250 cc'),
        ('250-499', '250 – 499 cc'),
        ('500-599', '500 – 599 cc'),
        ('600-749', '600 – 749 cc'),
        ('750-999', '750 – 999 cc'),
        ('1000+', '1000 cc and above'),
    ]

    engine_capacity = models.CharField(
        max_length=20,
        choices=ENGINE_CAPACITY_CHOICES,
        null=True,
        blank=True,
        verbose_name="Engine Capacity (cc)"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(
        max_length=10,
        choices=[('new', 'New'), ('used', 'Used')],
        verbose_name="Condition"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'ScooterImage', 
        blank=True, 
        related_name='scooter', 
        verbose_name="Images"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )
    videos = models.ManyToManyField(
        'ScooterVideo', 
        blank=True, 
        related_name='scooter', 
        verbose_name="Videos"
    )


class ScooterImage(models.Model):
    image = models.ImageField(upload_to='Scooter/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class ScooterVideo(models.Model):
    video = models.FileField(upload_to='Scooter/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    

class Quadbikes(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    PRODUCT_CHOICES = [
        ('quadbikes','Quad Bikes'),
        ('buggies', 'Buggies'),
        ('atv', 'ATV'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='quadbikes'
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=1000,verbose_name="Description")
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='quadbikes')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    types = models.CharField(
        max_length=10,
        choices=PRODUCT_CHOICES,
        default='quadbikes',
        verbose_name="Product Type"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(
        max_length=10,
        choices=[('new', 'New'), ('used', 'Used')],
        verbose_name="Condition"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'QuadbikesImage', 
        blank=True, 
        related_name='quadbikes', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'QuadbikesVideo', 
        blank=True, 
        related_name='quadbikes', 
        verbose_name="Videos"
    )


class QuadbikesImage(models.Model):
    image = models.ImageField(upload_to='Quadbikes/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class QuadbikesVideo(models.Model):
    video = models.FileField(upload_to='Quadbikes/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    

class CarRepairMaintenance(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
    ]

    CATEGORY_CHOICES = [
        ('maintenance_repair', 'Car Maintenance & Repair'),
        ('towing', 'Towing'),
        ('car_wash', 'Car Wash'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='car_repair_maintenance'
    )
    category = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='maintenance_repair',
        verbose_name="Service Category"
    )
    title = models.CharField(max_length=255, verbose_name="Service Title")
    description = models.TextField(max_length=1000,verbose_name="Description")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    city = models.ForeignKey(
        Cities,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='car_repair_maintenance'
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Service Status"
    )
    created_at = models.DateTimeField(default=timezone.now)

    # Media fields
    images = models.ManyToManyField(
        'CarRepairImage',
        blank=True,
        related_name='car_repair_maintenance',
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'CarRepairVideo',
        blank=True,
        related_name='car_repair_maintenance',
        verbose_name="Videos"
    )

    class Meta:
        verbose_name = "Car Repair & Maintenance"
        verbose_name_plural = "Car Repair & Maintenance Listings"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_category_display()} - {self.title}"


class CarRepairImage(models.Model):
    image = models.ImageField(upload_to='CarRepairMaintenance/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class CarRepairVideo(models.Model):
    video = models.FileField(upload_to='CarRepairMaintenance/videos/', verbose_name="Video")

    def __str__(self):
        return f"CarRepair Video {self.id}"
 
class HelmetClothes(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    PRODUCT_CHOICES = [
        ('helmet', 'Helmet'),
        ('clothes', 'Clothes'),
    ]
    LISTER_TYPE_CHOICES = [
        ('owner', 'Owner'),
        ('dealer', 'Dealer'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='helmetclothes'
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    created_at = models.DateTimeField(default=timezone.now)

    # NEW: Title field (missing earlier)
    title = models.CharField(max_length=255, verbose_name="Item Title")

    description = models.TextField(max_length=1000,verbose_name="Description")

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        null=True, blank=True,
        verbose_name="Payment Method"
    )

    city = models.ForeignKey(
        Cities, on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='helmetclothes'
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type",
        default='dealer'
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sale',
        verbose_name="Listing Type"
    )
    helmetcloth_type = models.CharField(
        max_length=10,
        choices=PRODUCT_CHOICES,
        default='helmet',
        verbose_name="Product Type"
    )
    price = models.DecimalField(
        max_digits=10, decimal_places=2,
        verbose_name="Price (OMR)"
    )
    condition = models.CharField(
        max_length=10,
        choices=[('new', 'New'), ('used', 'Used')],
        verbose_name="Condition"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )
    images = models.ManyToManyField(
        'HelmetClothesImage',
        blank=True, related_name='helmetclothes',
        verbose_name="Images"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True, blank=True,
        verbose_name="Rental Period"
    )

    # NEW: Provide delivery option
    provide_delivery = models.CharField(
        max_length=3,
        choices=[('yes', 'Yes'), ('no', 'No')],
        default='no',
        verbose_name="Provide Delivery?"
    )

    videos = models.ManyToManyField(
        'HelmetClothesVideo',
        blank=True, related_name='helmetclothes',
        verbose_name="Videos"
    )

    def __str__(self):
        return self.title

class HelmetClothesImage(models.Model):
    image = models.ImageField(upload_to='HelmetClothes/images/', verbose_name="Image")

     # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class HelmetClothesVideo(models.Model):
    video = models.FileField(upload_to='HelmetClothes/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    
class JunkCar(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    CONDITION_CHOICES = [
        ('damaged', 'Damaged'),
    ('not_working', 'Not Working'),
    ('scrap', 'Scrap'),
    ('accident', 'Accident'),
    ('engine_problem', 'Engine Problem'),
    ('transmission_problem', 'Transmission Problem'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted')
    ]
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sale',
        verbose_name="Listing Type"
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]
    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='junk_cars'
    )
    name = models.CharField(max_length=100, verbose_name="Title")
    
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, verbose_name="Condition")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Expected Price / Scrap Value")
    description = models.TextField(max_length=1000,verbose_name="Description", blank=True)

    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="City")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )

    images = models.ManyToManyField(
        'JunkCarImage',
        blank=True,
        related_name='junkcar',
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'JunkCarVideo',
        blank=True,
        related_name='junkcar',
        verbose_name="Videos"
    )

    def __str__(self):
        return self.name

class JunkCarImage(models.Model):
    image = models.ImageField(upload_to='JunkCar/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class JunkCarVideo(models.Model):
    video = models.FileField(upload_to='JunkCar/videos/', verbose_name="Video")

    def __str__(self):
        return f"JunkCar Video {self.id}"

class AutoAccessoryPart(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='auto_accessory_parts'
    )

    MAIN_CATEGORY_CHOICES = [     
        ('car_parts', 'Car/4x4 Parts'),
        ('apparel_merch', 'Apparel, Merchandise & Accessories'),
        ('motorcycle_parts', 'Motorcycle Parts'),
        ('tools', 'Automotive Tools'),
        ('boat_parts', 'Boat Parts'),
        ('other_vehicle', 'Other Vehicle Parts'),
    ]

    SUB_CATEGORY_CHOICES = [
        ('wheels_tires', 'Wheels/Tires'),
        ('brakes', 'Brakes'),
        ('exterior_parts', 'Exterior Parts'),
        ('interior_parts', 'Interior Parts'),
        ('exhaust', 'Exhaust/Air Intake'),
        ('suspension', 'Suspension'),
        ('engine_computer', 'Engine & Computer Parts'),
        ('lighting', 'Lighting'),
        ('batteries', 'Batteries'),
        ('car_other', 'Other'),
        ('car_accessories', 'Car/4x4 Accessories'),
        ('apparel', 'Apparel'),
        ('motorcycle_accessories', 'Motorcycle Accessories'),
        ('merch_other', 'Other'),
        ('motorcycle_accessories', 'Accessories'),
        ('body_frame', 'Body & Frame'),
        ('engine_components', 'Engines & Components'),
        ('motorcycle_wheels', 'Wheels Tires'),
        ('tools', 'Automotive Tools'),
        ('boat_body', 'Body Parts & Accessories'),
        ('boat_engine', 'Engine Parts'),
        ('other_vehicle', 'Other Vehicle Parts'),
    ]

    main_category = models.CharField(max_length=50, choices=MAIN_CATEGORY_CHOICES,default='car_parts')
    sub_category = models.CharField(max_length=50, choices=SUB_CATEGORY_CHOICES,default='wheels_tires')
    name = models.CharField(max_length=100)
    description = models.TextField()
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="City")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    CONDITION_CHOICES = [
        ('used', 'Used'),
        ('like_new', 'Like New'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted')
    ]
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sale',
        verbose_name="Listing Type"
    )
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='cash', null=True, blank=True)

    PROVIDE_DELIVERY_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    provide = models.CharField(max_length=3, choices=PROVIDE_DELIVERY_CHOICES, default='no')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending'
    )

    created_at = models.DateTimeField(default=timezone.now)

    images = models.ManyToManyField(
        'AutoAccessoryPartImage', 
        blank=True, 
        related_name='parts_images'
    )
    videos = models.ManyToManyField(
        'AutoAccessoryPartVideo', 
        blank=True, 
        related_name='parts_videos'
    )

    def __str__(self):
        return f"{self.name} - {self.get_main_category_display()} - {self.get_sub_category_display()}"


class AutoAccessoryPartImage(models.Model):
    image = models.ImageField(upload_to='auto_accessory_parts/images/')
    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class AutoAccessoryPartVideo(models.Model):
    video = models.FileField(upload_to='auto_accessory_parts/videos/')
    def __str__(self):
        return f"Video {self.id}"

class HeavyVehicle(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used')
    ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]
   
    MAIN_TYPE_CHOICES = [
        ('trucks', 'Trucks'), ('buses', 'Buses'), ('forklifts', 'Forklifts'),
        ('trailers', 'Trailers'), ('cranes', 'Cranes'), ('tankers', 'Tankers'),
        ('parts_engines', 'Parts & Engines'), ('aircrafts', 'Aircrafts'), ('other', 'Other Vehicles'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    rental_period = models.CharField(
        max_length=20,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        help_text="Rental period applicable if listing type is rent"
    )

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='heavy_vehicles')
    name = models.CharField(max_length=255)
    description = models.TextField()
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="City")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    year = models.PositiveIntegerField(
        verbose_name="Year of Manufacture",
        validators=[
            MinValueValidator(1900),
            MaxValueValidator(datetime.now().year + 1)
        ]
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES)
    listing_type = models.CharField(max_length=10, choices=TRANSACTION_CHOICES, default='sale')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    main_type = models.CharField(max_length=50, choices=MAIN_TYPE_CHOICES,default='trucks')
    sub_type = models.CharField(max_length=100,default='Cab-Chassis')
    model = models.CharField(max_length=100, blank=True, null=True, help_text="Model (for trucks/trailers)")
    bus_model = models.CharField(max_length=100, blank=True, null=True, help_text="Bus model (for buses)")

    images = models.ManyToManyField('HeavyVehicleImage', blank=True, related_name='heavyvehicle')
    videos = models.ManyToManyField('HeavyVehicleVideo', blank=True, related_name='heavyvehicle')


class HeavyVehicleImage(models.Model):
    image = models.ImageField(upload_to='heavyvehicle/images/')
    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class HeavyVehicleVideo(models.Model):
    video = models.FileField(upload_to='heavyvehicle/videos/')
    def __str__(self):
        return f"Video {self.id}"
    
class Boat(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
        ('refurbished', 'Refurbished')
    ]
    LISTER_TYPE_CHOICES = [
    ('owner', 'Owner'),
    ('dealer', 'Dealer'),
   ]
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]

    BOAT_TYPE_CHOICES = [
        ('boats', 'Boats'),
        ('yachts', 'Yachts'),
        ('jet_skis', 'Jet Skis'),
        ('canoes', 'Canoes'),
        ('kayaks', 'Kayaks'),
        ('paddle_boats', 'Paddle Boats'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='boats'
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    boat_type = models.CharField(
        max_length=50,
        choices=BOAT_TYPE_CHOICES,
        verbose_name="Boat Type",
        default='boats'
    )
    lister_type = models.CharField(max_length=10,choices=LISTER_TYPE_CHOICES,verbose_name="Lister Type",default='dealer')
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sale',
        verbose_name="Listing Type"
    )
    
    name = models.CharField(max_length=255, verbose_name="Boat Name")
    description = models.TextField(max_length=1000,verbose_name="Description")
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="City")
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Price (OMR)")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, verbose_name="Condition")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Approval Status")

    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )

    images = models.ManyToManyField(
        'BoatImage',
        blank=True,
        related_name='boat',
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'BoatVideo',
        blank=True,
        related_name='boat',
        verbose_name="Videos"
    )

    def __str__(self):
        return self.name


class BoatImage(models.Model):
    image = models.ImageField(upload_to='boat/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class BoatVideo(models.Model):
    video = models.FileField(upload_to='boat/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    
class TiresAndCaps(models.Model):
    TIRE_TYPE_CHOICES = [
        ('tyres', 'Tyres'),
        ('rims', 'Rims'),
        ('set_wheels_rims_tyres', 'Set of Wheels, Rims and Tyres'),
        ('automotive_caps', 'Automotive Caps'),
    ]

    SIZE_CHOICES = [
        ('10', '10'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'),
        ('16', '16'), ('17', '17'), ('17.5', '17.5'), ('18', '18'), ('19', '19'),
        ('20', '20'), ('21', '21'), ('22', '22'), ('22.5', '22.5'), ('23', '23'),
        ('25', '25'), ('30', '30'), ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tire_type = models.CharField(max_length=50, choices=TIRE_TYPE_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, blank=True, null=True)
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )
    brand = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    provide = models.CharField(max_length=3, choices=[('yes', 'Yes'), ('no', 'No')])
    condition = models.CharField(max_length=10, choices=[('used', 'Used'), ('like_new', 'Like New')])
    payment_method = models.CharField(max_length=20, choices=[('cash', 'Cash'), ('installments', 'Installments')], null=True, blank=True)
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    images = models.ManyToManyField('TiresAndCapsImage', blank=True)
    videos = models.ManyToManyField('TiresAndCapsVideo', blank=True)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def display_tire_type(self):
      return self.get_tire_type_display()


class TiresAndCapsImage(models.Model):
    image = models.ImageField(upload_to='tires_caps/images/')
    
    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class TiresAndCapsVideo(models.Model):
    video = models.FileField(upload_to='tires_caps/videos/')

from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator


class NumberPlate(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='number_plates'
    )

    class PlateType(models.TextChoices):
        MOTORCYCLE = "motorcycle", _("Motorcycle")
        CAR = "car", _("Car")

    class PlateUsage(models.TextChoices):
        PRIVATE = "private", _("Private")
        COMMERCIAL = "commercial", _("Commercial")

    TRANSACTION_CHOICES = [
        ('sale', 'Sale'),
        ('wanted', 'Wanted')
    ]

    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sale',
        verbose_name="Listing Type"
    )

    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    number = models.CharField(
    max_length=5,
    
    validators=[
        RegexValidator(
            regex=r'^\d{1,5}$',
            message="Enter up to 5 digits only."
        )
    ],
    verbose_name="Plate Number"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Price (OMR)"
    )

    # ✅ ONLY CAPITAL LETTERS ALLOWED
    letter_english = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[A-Z ]+$',
                message="Only uppercase English letters (A–Z) are allowed."
            )
        ],
        verbose_name="English Letter"
    )

    letter_arabic = models.CharField(
        max_length=10,
        verbose_name="Arabic Letter"
    )

    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )

    plate_type = models.CharField(
        max_length=20,
        choices=PlateType.choices,
        verbose_name="Vehicle Type"
    )

    # ✅ NEW FIELD: Commercial / Private
    usage_type = models.CharField(
        max_length=20,
        choices=PlateUsage.choices,
        verbose_name="Plate Usage Type"
    )

    seller_name = models.CharField(max_length=100)

    description = models.TextField(max_length=1000,verbose_name="Description")

    city = models.ForeignKey(
        Cities,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="City"
    )

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=[
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected')
        ],
        default='pending',
        verbose_name="Approval Status"
    )

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.number} - {self.plate_type} ({self.usage_type})"

    def get_plate_design(self):
        return f"[ {self.letter_arabic} | {self.letter_english} | {self.number} | {self.plate_type} ]"
    
    def save(self, *args, **kwargs):
        if self.letter_english:
            self.letter_english = self.letter_english.upper()
        super().save(*args, **kwargs)



class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image uploaded at {self.uploaded_at}"



class DrivingTraining(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='driving_trainings'
    )

    trainer_name = models.CharField(max_length=255)
    trainer_gender = models.CharField(
        max_length=10, 
        choices=[('Male', 'Male'), ('Female', 'Female')]
    )
    transmission = models.CharField(
        max_length=10, 
        choices=[('Automatic', 'Automatic'), ('Manual', 'Manual')]
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )
    body_type = models.CharField(
        max_length=20, 
        choices=[('Sedan', 'Sedan'), ('Hatchback', 'Hatchback'), ('Small Truck', 'Small Truck'), ('Large Truck', 'Large Truck'), ('Motorcycle', 'Motorcycle')]
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    model_year = models.PositiveIntegerField()
    created_at = models.DateTimeField(default=timezone.now)
    description = models.TextField(max_length=1000,verbose_name="Description")
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='drivingtraining')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    location = models.TextField(max_length=250, blank=True, null=True)

    status = models.CharField(
        max_length=20,
        choices=[('pending', 'Pending'), ('approved', 'Approved'), ('rejected', 'Rejected')],
        default='pending',
        verbose_name="Approval Status"
    )
    language = models.CharField(max_length=100)
    about_instructor = models.TextField()
    images = models.ManyToManyField(
        'DrivingTrainingImage', 
        blank=True, 
        related_name='driving_training', 
        verbose_name="Images"
    )

    def __str__(self):
        return f"{self.trainer_name} - {self.body_type} ({self.model_year})"


class DrivingTrainingImage(models.Model):
    image = models.ImageField(upload_to='driving_training/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"
    


class Apartment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    BUILDING_AGE_CHOICES = [
        ('under_construction', 'Under Construction'),
        ('0-11_months', '0-11 Months'),
        ('1-5_years', '1-5 Years'),
        ('6-9_years', '6-9 Years'),
        ('10-19_years', '10-19 Years'),
        ('20+_years', '20+ Years'),
    ]
    
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    FACADE_CHOICES = [
        ('northern', 'Northern'),
        ('southern', 'Southern'),
        ('eastern', 'Eastern'),
        ('western', 'Western'),
        ('northeast', 'Northeast'),
        ('southeast', 'Southeast'),
        ('northwest', 'Northwest'),
        ('southwest', 'Southwest'),

    ]
    BEDROOM_CHOICES =[
            ('studio', 'Studio'),
            ('1', '1 Bed'),
            ('2', '2 Beds'),
            ('3', '3 Beds'),
            ('4', '4 Beds'),
            ('5', '5 Beds'),
            ('6+', '6+ Beds'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='apartment'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='apartment')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    bedrooms = models.CharField(
        max_length=10,
        choices=BEDROOM_CHOICES,
        verbose_name="Number of Bedrooms"
    )
    bathrooms = models.CharField(
        max_length=10,
        choices=[
            ('1', '1 Bath'),
            ('2', '2 Baths'),
            ('3', '3 Baths'),
            ('4', '4 Baths'),
            ('5', '5 Baths'),
            ('6+', '6+ Baths'),
        ],
        verbose_name="Number of Bathrooms"
    )
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    FLOOR_CHOICES = [
         ('basement_floor', 'Basement Floor'),
    ('1_floor', '1st Floor'),
    ('2_floor', '2nd Floor'),
    ('3_floor', '3rd Floor'),
    ('4_floor', '4th Floor'),
    ('5_floor', '5th Floor'),
    ('6_floor', '6th Floor'),
    ('7_floor', '7th Floor'),
    ('8_floor', '8th Floor'),
    ('9_floor', '9th Floor'),
    ('10_floor', '10th Floor'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    building = models.CharField(max_length=20, choices=BUILDING_AGE_CHOICES,default='under_construction',  verbose_name="Building Age")
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )  
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    nearby_location = models.ManyToManyField(NearbyLocation, related_name='apartments') 
    main_amenities = models.ManyToManyField(MainAmenities, related_name='apartments')
    additional_amenities = models.ManyToManyField(AdditionalAmenities, related_name='apartments')
    facade = models.CharField(
        max_length=10, 
        choices=FACADE_CHOICES, 
        verbose_name="Facade"
    )
    images = models.ManyToManyField(
        'ApartmentImage', 
        blank=True, 
        related_name='Apartment', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ApartmentVideo',
        blank=True,
        related_name='Apartment',
        verbose_name="Videos"
    )

    def __str__(self):
        return self.property_title
    
   
class ApartmentImage(models.Model):
    image = models.ImageField(upload_to='Apartment/images/', verbose_name="Image")
    
    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class ApartmentVideo(models.Model):
    video = models.FileField(upload_to='Apartment/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    
class Factory(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]

    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='factory'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities) 
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='factory')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'FactoryImage', 
        blank=True, 
        related_name='Factory', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'FactoryVideo',
        blank=True,
        related_name='Factory',
        verbose_name="Videos"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class FactoryImage(models.Model):
    image = models.ImageField(upload_to='Factory/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class FactoryVideo(models.Model):
    video = models.FileField(upload_to='Factory/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    

class Complex(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Ready to Occupy'),
        ('under_construction', 'Under Construction'),
            ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='complex'
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='complex')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="land Area")
    surface_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    FLOOR_CHOICES = [
    ('basement_floor', 'Basement Floor'),
    ('semiground_floor', 'Semi Ground Floor'),
    ('ground_floor', 'Ground Floor'),
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),
    ('3_floor', '3 Floors'),
    ('4_floor', '4 Floors'),
    ('5_floor', '5 Floors'),
    ('6_floor', '6 Floors'),
    ('7_floor', '7 Floors'),
    ('8_floor', '8 Floors'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
]
    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sale',
        verbose_name="Listing Type"
    )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'ComplexImage', 
        blank=True, 
        related_name='Complex', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ComplexVideo',
        blank=True,
        related_name='Complex',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
  

class ComplexImage(models.Model):
    image = models.ImageField(upload_to='Complex/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class ComplexVideo(models.Model):
    video = models.FileField(upload_to='Complex/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    
class Clinic(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Ready to Occupy'),
        ('under_construction', 'Under Construction'),
            ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='clinic'
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='clinic')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
   
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    FLOOR_CHOICES = [
    ('basement_floor', 'Basement Floor'),
    ('semiground_floor', 'Semi Ground Floor'),
    ('ground_floor', 'Ground Floor'),
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),
    ('3_floor', '3 Floors'),
    ('4_floor', '4 Floors'),
    ('5_floor', '5 Floors'),
    ('6_floor', '6 Floors'),
    ('7_floor', '7 Floors'),
    ('8_floor', '8 Floors'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
]
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'ClinicImage', 
        blank=True, 
        related_name='Clinic', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ClinicVideo',
        blank=True,
        related_name='Clinic',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class ClinicImage(models.Model):
    image = models.ImageField(upload_to='Clinic/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class ClinicVideo(models.Model):
    video = models.FileField(upload_to='Clinic/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    
class Hostel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    BEDROOM_CHOICES =[
            ('studio', 'Studio'),
            ('1', '1 Bed'),
            ('2', '2 Beds'),
            ('3', '3 Beds'),
            ('4', '4 Beds'),
            ('5', '5 Beds'),
            ('6+', '6+ Beds'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Ready to Occupy'),
        ('under_construction', 'Under Construction'),
            ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Hostel'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)
    bedrooms = models.CharField(
        max_length=10,
        choices=BEDROOM_CHOICES,
        verbose_name="Number of Bedrooms"
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='hostel')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    FLOOR_CHOICES = [
    ('basement_floor', 'Basement Floor'),
    ('semiground_floor', 'Semi Ground Floor'),
    ('ground_floor', 'Ground Floor'),
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),
    ('3_floor', '3 Floors'),
    ('4_floor', '4 Floors'),
    ('5_floor', '5 Floors'),
    ('6_floor', '6 Floors'),
    ('7_floor', '7 Floors'),
    ('8_floor', '8 Floors'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'HostelImage', 
        blank=True, 
        related_name='Hostel', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'HostelVideo',
        blank=True,
        related_name='Hostel',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class HostelImage(models.Model):
    image = models.ImageField(upload_to='Hostel/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class HostelVideo(models.Model):
    video = models.FileField(upload_to='Hostel/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    


class Office(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Ready to Occupy'),
        ('under_construction', 'Under Construction'),
            ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Office'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)
    
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='office')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
   
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    FLOOR_CHOICES = [
    ('basement_floor', 'Basement Floor'),
    ('semiground_floor', 'Semi Ground Floor'),
    ('ground_floor', 'Ground Floor'),
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),
    ('3_floor', '3 Floors'),
    ('4_floor', '4 Floors'),
    ('5_floor', '5 Floors'),
    ('6_floor', '6 Floors'),
    ('7_floor', '7 Floors'),
    ('8_floor', '8 Floors'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'OfficeImage', 
        blank=True, 
        related_name='Office', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'OfficeVideo',
        blank=True,
        related_name='Office',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class OfficeImage(models.Model):
    image = models.ImageField(upload_to='Office/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class OfficeVideo(models.Model):
    video = models.FileField(upload_to='Office/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    

class Shop(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Shop'
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)
    
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='shop')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
   
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    images = models.ManyToManyField(
        'ShopImage', 
        blank=True, 
        related_name='Shop', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ShopVideo',
        blank=True,
        related_name='Shop',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
   
    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class ShopImage(models.Model):
    image = models.ImageField(upload_to='Shop/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class ShopVideo(models.Model):
    video = models.FileField(upload_to='Shop/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    

class Cafe(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Ready to Occupy'),
        ('under_construction', 'Under Construction'),
            ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Cafe'
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='cafe')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
   
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    images = models.ManyToManyField(
        'CafeImage', 
        blank=True, 
        related_name='Cafe', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'CafeVideo',
        blank=True,
        related_name='Cafe',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class CafeImage(models.Model):
    image = models.ImageField(upload_to='Cafe/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class CafeVideo(models.Model):
    video = models.FileField(upload_to='Cafe/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    


class Staff(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    BEDROOM_CHOICES =[
            ('studio', 'Studio'),
            ('1', '1 Bed'),
            ('2', '2 Beds'),
            ('3', '3 Beds'),
            ('4', '4 Beds'),
            ('5', '5 Beds'),
            ('6+', '6+ Beds'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Ready to Occupy'),
        ('under_construction', 'Under Construction'),
            ]
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Staff'
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    bedrooms = models.CharField(
        max_length=10,
        choices=BEDROOM_CHOICES,
        verbose_name="Number of Bedrooms"
    )
    
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Plot Area")
   
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    FLOOR_CHOICES = [
    ('basement_floor', 'Basement Floor'),
    ('semiground_floor', 'Semi Ground Floor'),
    ('ground_floor', 'Ground Floor'),
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),
    ('3_floor', '3 Floors'),
    ('4_floor', '4 Floors'),
    ('5_floor', '5 Floors'),
    ('6_floor', '6 Floors'),
    ('7_floor', '7 Floors'),
    ('8_floor', '8 Floors'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )

  
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    images = models.ManyToManyField(
        'StaffImage', 
        blank=True, 
        related_name='Staff', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'StaffVideo',
        blank=True,
        related_name='Staff',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class StaffImage(models.Model):
    image = models.ImageField(upload_to='Staff/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class StaffVideo(models.Model):
    video = models.FileField(upload_to='Staff/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    


class Warehouse(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Ready to Occupy'),
        ('under_construction', 'Under Construction'),
            ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Warehouse'
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    created_at = models.DateTimeField(default=timezone.now)
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='warehouse')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'WarehouseImage', 
        blank=True, 
        related_name='Warehouse', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'WarehouseVideo',
        blank=True,
        related_name='Warehouse',
        verbose_name="Videos"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )

    def __str__(self):
        return self.property_title
    
    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class WarehouseImage(models.Model):
    image = models.ImageField(upload_to='Warehouse/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class WarehouseVideo(models.Model):
    video = models.FileField(upload_to='Warehouse/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"

class Townhouse(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    BEDROOM_CHOICES =[
            ('studio', 'Studio'),
            ('1', '1 Bed'),
            ('2', '2 Beds'),
            ('3', '3 Beds'),
            ('4', '4 Beds'),
            ('5', '5 Beds'),
            ('6+', '6+ Beds'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    BUILDING_AGE_CHOICES = [
        ('under_construction', 'Under Construction'),
        ('0-11_months', '0-11 Months'),
        ('1-5_years', '1-5 Years'),
        ('6-9_years', '6-9 Years'),
        ('10-19_years', '10-19 Years'),
        ('20+_years', '20+ Years'),
    ]
    
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    FACADE_CHOICES = [
        ('northern', 'Northern'),
        ('southern', 'Southern'),
        ('eastern', 'Eastern'),
        ('western', 'Western'),
        ('northeast', 'Northeast'),
        ('southeast', 'Southeast'),
        ('northwest', 'Northwest'),
        ('southwest', 'Southwest'),

    ]
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Townhouse'
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='townhouse')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Land Area")
    surface_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    FLOOR_CHOICES = [
    ('basement_floor', 'Basement Floor'),
    ('semiground_floor', 'Semi Ground Floor'),
    ('ground_floor', 'Ground Floor'),
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),
    ('3_floor', '3 Floors'),
    ('4_floor', '4 Floors'),
    ('5_floor', '5 Floors'),
    ('6_floor', '6 Floors'),
    ('7_floor', '7 Floors'),
    ('8_floor', '8 Floors'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    bedrooms = models.CharField(
        max_length=10,
        choices=BEDROOM_CHOICES,
        verbose_name="Number of Bedrooms"
    )
    bathrooms = models.CharField(
        max_length=10,
        choices=[
            ('1', '1'),
            ('2', '2'),
            ('3', '3'),
            ('4', '4'),
            ('5', '5'),
            ('6+', '6+'),
        ],
        verbose_name="Number of Bathrooms"
    )
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )
    building = models.CharField(max_length=20, choices=BUILDING_AGE_CHOICES,default='under_construction',  verbose_name="Building Age")
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sale',
        verbose_name="Listing Type"
    )
    
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    
    
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    facade = models.CharField(
        max_length=10, 
        choices=FACADE_CHOICES, 
        verbose_name="Facade"
    )

    images = models.ManyToManyField(
        'TownhouseImage', 
        blank=True, 
        related_name='Townhouse', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'TownhouseVideo', 
        blank=True, 
        related_name='Townhouse', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class TownhouseImage(models.Model):
    image = models.ImageField(upload_to='Townhouse/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"
    
class TownhouseVideo(models.Model):
    video = models.FileField(upload_to='Townhouse/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"



class Fullfloors(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Ready to Occupy'),
        ('under_construction', 'Under Construction'),
            ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
   

    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Fullfloors'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='fullfloors')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    FLOOR_CHOICES = [
    ('basement_floor', 'Basement Floor'),
    ('semiground_floor', 'Semi Ground Floor'),
    ('ground_floor', 'Ground Floor'),
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),
    ('3_floor', '3 Floors'),
    ('4_floor', '4 Floors'),
    ('5_floor', '5 Floors'),
    ('6_floor', '6 Floors'),
    ('7_floor', '7 Floors'),
    ('8_floor', '8 Floors'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
    ]
    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor'  # Fixed
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )
    
    
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
   
    images = models.ManyToManyField(
        'FullfloorsImage', 
        blank=True, 
        related_name='Fullfloors', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'FullfloorsVideo', 
        blank=True, 
        related_name='Fullfloors', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class FullfloorsImage(models.Model):
    image = models.ImageField(upload_to='Fullfloors/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"
    
class FullfloorsVideo(models.Model):
    video = models.FileField(upload_to='Fullfloors/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    



class Showrooms(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Ready to Occupy'),
        ('under_construction', 'Under Construction'),
            ]
   
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities)  
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Showrooms'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='showrooms')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    
    
   
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )
    
    
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
   
    images = models.ManyToManyField(
        'ShowroomsImage', 
        blank=True, 
        related_name='Showrooms', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ShowroomsVideo', 
        blank=True, 
        related_name='Showrooms', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class ShowroomsImage(models.Model):
    image = models.ImageField(upload_to='Showrooms/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"
    
class ShowroomsVideo(models.Model):
    video = models.FileField(upload_to='Showrooms/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    
class Wholebuilding(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    PROPERTY_CHOICES = [
        ('complete', 'Ready to Occupy'),
        ('under_construction', 'Under Construction'),
            ]
    BUILDING_AGE_CHOICES = [
        ('under_construction', 'Under Construction'),
        ('0-11_months', '0-11 Months'),
        ('1-5_years', '1-5 Years'),
        ('6-9_years', '6-9 Years'),
        ('10-19_years', '10-19 Years'),
        ('20+_years', '20+ Years'),
    ]
    FACADE_CHOICES = [
        ('northern', 'Northern'),
        ('southern', 'Southern'),
        ('eastern', 'Eastern'),
        ('western', 'Western'),
        ('northeast', 'Northeast'),
        ('southeast', 'Southeast'),
        ('northwest', 'Northwest'),
        ('southwest', 'Southwest'),

    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Wholebuilding'
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    nearby_location = models.ManyToManyField(NearbyLocation) 
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='wholebuilding')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Land Area")
    surface_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    FLOOR_CHOICES = [
    ('basement_floor', 'Basement Floor'),
    ('semiground_floor', 'Semi Ground Floor'),
    ('ground_floor', 'Ground Floor'),
    ('1_floor', '1 Floor'),
    ('2_floor', '2 Floors'),
    ('3_floor', '3 Floors'),
    ('4_floor', '4 Floors'),
    ('5_floor', '5 Floors'),
    ('6_floor', '6 Floors'),
    ('7_floor', '7 Floors'),
    ('8_floor', '8 Floors'),
    ('lastfloorwith_roof', 'Last Floor with Roof'),
]

    floors = models.CharField(
       max_length=250,
       choices=FLOOR_CHOICES,
       default='1_floor' 
    )  
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        ) 
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )
    building = models.CharField(max_length=20, choices=BUILDING_AGE_CHOICES,default='under_construction',  verbose_name="Building Age")
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    facade = models.CharField(
        max_length=10, 
        choices=FACADE_CHOICES, 
        verbose_name="Facade"
    )
   
    images = models.ManyToManyField(
        'WholebuildingImage', 
        blank=True, 
        related_name='Wholebuilding', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'WholebuildingVideo', 
        blank=True, 
        related_name='Wholebuilding', 
        verbose_name="Videos"
    )


    
class WholebuildingImage(models.Model):
    image = models.ImageField(upload_to='Wholebuilding/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"
    
class WholebuildingVideo(models.Model):
    video = models.FileField(upload_to='Wholebuilding/videos/', verbose_name="Video")

    def _str_(self):
        return f"Video {self.id}"
    
class Supermarket(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    PROPERTY_CHOICES = [
        ('complete', 'Ready to Occupy'),
        ('under_construction', 'Under Construction'),
            ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Supermarket'
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    nearby_location = models.ManyToManyField(NearbyLocation) 
    main_amenities = models.ManyToManyField(MainAmenities)
    additional_amenities = models.ManyToManyField(AdditionalAmenities) 
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='supermarket')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    plot_area = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Surface Area")
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    property = models.CharField(
        max_length=20,
        choices=PROPERTY_CHOICES,
         default='under_construction', 
        verbose_name="Property Status"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'SupermarketImage', 
        blank=True, 
        related_name='Supermarket', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'SupermarketVideo', 
        blank=True, 
        related_name='Supermarket', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class SupermarketImage(models.Model):
    image = models.ImageField(upload_to='Supermarket/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"
    
class SupermarketVideo(models.Model):
    video = models.FileField(upload_to='Supermarket/videos/', verbose_name="Video")

    def _str_(self):
        return f"Video {self.id}"
    
class Foreign(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout','Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    TRANSACTION_CHOICES = [
        ('sell', 'Sale'),
        ('rent', 'Rent'),
    ]
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
        ]
    
    LISTER_TYPE_CHOICES = [
        ('agent', 'Agent'),
        ('landlord', 'Landlord'),
    ]
    PROPERTY_MORTGAGE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    ESTATE_TYPE_CHOICES = [
        ('apartment', 'Apartment'),
        ('chalets', 'Chalets - Summer Houses'),
        ('commercial', 'Commercial'),
        ('farm', 'Farm'),
        ('land', 'Land'),
        ('villa', 'Villa House'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    nearby_location = models.ManyToManyField(NearbyLocation) 
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Foreign'
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='foreign')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    country = CountryField(blank_label="Select Country")
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='sell',
        verbose_name="Listing Type"
    )
    lister_type = models.CharField(
        max_length=10,
        choices=LISTER_TYPE_CHOICES,
        verbose_name="Lister Type"
    )
    estate_type = models.CharField(
        max_length=20,
        choices=ESTATE_TYPE_CHOICES,
         default='apartment', 
        verbose_name="Estate Type"
    )
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
        )
    property_mortgage = models.CharField(
        max_length=3, 
        choices=PROPERTY_MORTGAGE_CHOICES, 
        default='no', 
        verbose_name="Property Mortgage"
    )
    images = models.ManyToManyField(
        'ForeignImage', 
        blank=True, 
        related_name='Foreign', 
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'ForeignVideo', 
        blank=True, 
        related_name='Foreign', 
        verbose_name="Videos"
    )
    
class ForeignImage(models.Model):
    image = models.ImageField(upload_to='Foreign/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"
    
class ForeignVideo(models.Model):
    video = models.FileField(upload_to='Foreign/videos/', verbose_name="Video")

    def _str_(self):
        return f"Video {self.id}"
    
class Shared(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    
    TRANSACTION_CHOICES = [
        ('rent', 'Rent'),
    ]
    
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='shared'
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='shared')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='rent',
        verbose_name="Listing Type"
    )
    
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )
    
    images = models.ManyToManyField(
        'SharedImage', 
        blank=True, 
        related_name='Shared', 
        verbose_name="Images"
    )
    
    videos = models.ManyToManyField(
        'SharedVideo', 
        blank=True, 
        related_name='Shared', 
        verbose_name="Videos"
    )
    
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class SharedImage(models.Model):
    image = models.ImageField(upload_to='Shared/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"
    
class SharedVideo(models.Model):
    video = models.FileField(upload_to='Shared/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"



    
class Suits(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
        ('exclusive', 'Exclusive'),  # ADDED: For approved exclusive listings
        ('pending_exclusive', 'Pending Exclusive'),
    ]
    
    TRANSACTION_CHOICES = [
        ('rent', 'Rent'),
    ]
    
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    FURNISHED_CHOICES = [
        ('furnished', 'Furnished'),
        ('semi_furnished', 'Semi-Furnished'),
        ('unfurnished', 'Unfurnished'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    admin_verified = models.BooleanField(default=False, verbose_name="Admin Verified for Exclusive")
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Suits'
    )
    
    property_title = models.CharField(max_length=255, verbose_name="Property Title")
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    
    city = models.ForeignKey(Cities, on_delete=models.SET_NULL, null=True, blank=True, related_name='suits')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    description = models.TextField(max_length=1000,verbose_name="Property Description")
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    
    listing_type = models.CharField(
        max_length=10,
        choices=TRANSACTION_CHOICES,
        default='rent',
        verbose_name="Listing Type"
    )
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('installments', 'Installments'),
    ]

    payment_method = models.CharField(
        max_length=20,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
        null=True,
        blank=True,
        verbose_name="Payment Method"
    )
    
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        null=True,
        blank=True,
        verbose_name="Rental Period"
    )
    
    images = models.ManyToManyField(
        'SuitsImage', 
        blank=True, 
        related_name='Suits', 
        verbose_name="Images"
    )
    
    videos = models.ManyToManyField(
        'SuitsVideo', 
        blank=True, 
        related_name='Suits', 
        verbose_name="Videos"
    )
    
    furnished = models.CharField(
        max_length=20, 
        choices=FURNISHED_CHOICES, 
        default='unfurnished', 
        verbose_name="Furnished"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class SuitsImage(models.Model):
    image = models.ImageField(upload_to='Suits/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"
    
class SuitsVideo(models.Model):
    video = models.FileField(upload_to='Suits/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
# ----------------------------------------------------------------------Motors---------------------------------------------------  


    

    
    

    

   
class Part(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    TYPES_CHOICES = [
        ('batteries', 'Batteries'),
        ('bodyparts', 'Body Parts'),
        ('mechanical', 'Mechanical Parts'),
        ('spareparts', 'Spare Parts'),
        ('other', 'Other'),
    ]
    SUBTYPE_CHOICES = {
        'batteries': [('batteries', 'Batteries'), ('hybrid', 'Hybrid')],
        'bodyparts': [('exterior', 'Exterior Parts'), ('interior', 'Interior Parts'), ('light', 'Light'), ('other', 'Other')],
        'mechanical': [
            ('brakes', 'Brakes'), ('chips', 'Computer Chips'), ('engines', 'Engines'),
            ('filters', 'Filters'), ('mechanical', 'Mechanical Parts'), ('oil', 'Oil'),
            ('suspensions', 'Suspensions'), ('transmission', 'Transmission'), ('other', 'Other')
        ],
        'spareparts': [
            ('coolers', 'Coolers'), ('headers', 'Headers'), ('sport_filters', 'Sport Filters'),
            ('steering_wheel', 'Steering Wheel'), ('turbo', 'Turbo Supercharge'), ('other', 'Other')
        ]
    }
    PROVIDE_DELIVERY_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    condition = models.CharField(
        max_length=10, 
        choices=[('used', 'Used'), ('like_new', 'Like New')], 
        verbose_name="Condition"
    )

    
   
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='Part'
    )
    
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")
    types = models.CharField(max_length=20, choices=TYPES_CHOICES, default='other')
    subtype = models.CharField(max_length=20)
    
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'  
    )
    
    cities = models.TextField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    description = models.TextField(max_length=1000,verbose_name="Description")
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='pending', 
        verbose_name="Approval Status"
    )
    provide = models.CharField(
        max_length=3, 
        choices=PROVIDE_DELIVERY_CHOICES, 
        default='no', 
        verbose_name="Delivery"
    )
    
   
    
    images = models.ManyToManyField(
        'PartImage', 
        blank=True, 
        related_name='Part', 
        verbose_name="Images"
    )
    
    videos = models.ManyToManyField(
        'PartVideo', 
        blank=True, 
        related_name='Part', 
        verbose_name="Videos"
    )
    
   

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)
    
class PartImage(models.Model):
    image = models.ImageField(upload_to='Carpart/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"
    
class PartVideo(models.Model):
    video = models.FileField(upload_to='Carpart/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"
    


    
class SportsCar(models.Model):
    # Status choices
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout')
    ]
    
    # Rental period choices
    RENTAL_PERIOD_CHOICES = [
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    # Vehicle specific body types
    BODYTYPE_CHOICES = [
        ('coupe', 'Coupe'),
        ('convertible', 'Convertible'),
        ('targa', 'Targa'),
        ('roadster', 'Roadster'),
        ('supercar', 'Supercar'),
        ('hypercar', 'Hypercar'),
        ('track', 'Track Car'),
        ('gt', 'Grand Tourer'),
    ]
    
    # Performance measurement units
    TOP_SPEED_UNITS = [
        ('kmh', 'km/h'),
        ('mph', 'mph'),
    ]
    
    make = models.CharField(max_length=100, verbose_name="Manufacturer")
    year = models.PositiveIntegerField(verbose_name="Year")
    description = models.TextField(max_length=1000,verbose_name="Description")
    
    # Region choices for Oman
    REGION_CHOICES = [
        ('MS', 'Muscat'),
        ('DH', 'Dhofar'),
        ('BT', 'Al Batinah'),
        ('DA', 'Al Dakhiliya'),
        ('SH', 'Al Sharqiya'),
        ('BR', 'Al Buraimi'),
        ('ZU', 'Al Dhahirah'),
        ('MW', 'Musandam'),
        ('WR', 'Al Wusta'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='SportsCar'
    )

    # Body type field with specific choices
    bodytype = models.CharField(
        max_length=100, 
        choices=BODYTYPE_CHOICES,
        verbose_name="Vehicle Body Type"
    )
    
    # Performance fields
    top_speed = models.PositiveIntegerField(
        verbose_name="Top Speed",
        null=True,
        blank=True
    )
    
    top_speed_unit = models.CharField(
        max_length=5,
        choices=TOP_SPEED_UNITS,
        default='kmh',
        verbose_name="Top Speed Unit"
    )
    
    acceleration = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Acceleration Time",
        null=True,
        blank=True
    )
    
    
    
    drivetrain = models.CharField(
        max_length=20,
        choices=[
            ('rwd', 'Rear-Wheel Drive'),
            ('fwd', 'Front-Wheel Drive'),
            ('awd', 'All-Wheel Drive'),
            ('4wd', 'Four-Wheel Drive'),
        ],
        default='rwd',
        verbose_name="Drivetrain"
    )
    
    # Location fields
    regions = models.CharField(
        max_length=250,
        choices=REGION_CHOICES,
        default='MS'
    )
    
    cities = models.CharField(
        max_length=250,
        verbose_name="City"
    )
    
    latitude = models.FloatField(
        null=True,
        blank=True
    )
    
    longitude = models.FloatField(
        null=True,
        blank=True
    )
    
    # Rental details
    rental_period = models.CharField(
        max_length=10,
        choices=RENTAL_PERIOD_CHOICES,
        verbose_name="Rental Period"
    )
    
    rental_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Rental Price"
    )
    
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )
    
    # Engine specifications
    horsepower = models.PositiveIntegerField(
        verbose_name="Horsepower",
        null=True,
        blank=True
    )
    
    torque = models.PositiveIntegerField(
        verbose_name="Torque (Nm)",
        null=True,
        blank=True
    )
    

    
    # Media fields
    images = models.ManyToManyField(
        'SportsCarImage', 
        blank=True, 
        related_name='sports_car', 
        verbose_name="Images"
    )
    
    videos = models.ManyToManyField(
        'SportsCarVideo', 
        blank=True, 
        related_name='sports_car', 
        verbose_name="Videos"
    )

    def get_region_display(self):
        return dict(self.REGION_CHOICES).get(self.regions, self.regions)

class SportsCarImage(models.Model):
    image = models.ImageField(upload_to='sports_cars/images/', verbose_name="Image")

    def __str__(self):
        return f"Image {self.id}"

class SportsCarVideo(models.Model):
    video = models.FileField(upload_to='sports_cars/videos/', verbose_name="Video")

    def __str__(self):
        return f"Video {self.id}"




from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class ProductReport(models.Model):
    REPORT_REASONS = [
        ('abuse', 'Report Abuse'),
        ('sold', 'Listing Sold'),
        ('duplicate', 'Duplicate Listing'),
        ('inappropriate', 'Inappropriate Listing'),
        ('wrong_category', 'Wrong Category'),
        ('incorrect_pictures', 'Incorrect Pictures'),
        ('incorrect_pricing', 'Incorrect Pricing'),
        ('fraud', 'Fraud'),
        ('other', 'Other'),
    ]
    
    REPORT_STATUS = [
        ('pending', 'Pending Review'),
        ('under_review', 'Under Review'),
        ('resolved', 'Resolved'),
        ('dismissed', 'Dismissed'),
        ('action_taken', 'Action Taken'),
    ]
    
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reports_made'
    )
    reason = models.CharField(max_length=30, choices=REPORT_REASONS)
    description = models.TextField(blank=True, help_text="Optional additional explanation.")
    created_at = models.DateTimeField(auto_now_add=True)
    
    # NEW FIELDS
    status = models.CharField(max_length=20, choices=REPORT_STATUS, default='pending')
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviews_done'
    )
    reviewed_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, help_text="Admin notes about this report")
    action_taken = models.CharField(max_length=100, blank=True, help_text="What action was taken")

    # Generic relation
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    reported_object = GenericForeignKey('content_type', 'object_id')

    def __str__(self):
        return f"{self.reported_object} reported as {self.get_reason_display()}"



# ---------------------------------------------Motors Design----------------------------------------


class InteriorOptions(models.Model):
    name = models.CharField(max_length=255, verbose_name="Location Name")
    def __str__(self):
        return self.name     
   

    
class ExteriorOptions(models.Model):
    name = models.CharField(max_length=255, verbose_name="Location Name")
    def __str__(self):
        return self.name  
    
class TechnologyOptions(models.Model):
    name = models.CharField(max_length=255, verbose_name="Location Name")
    def __str__(self):
        return self.name 
    



# ---------------------------------------------------------------Other Category------------------------------------------------------------
from django.db import models
from django.conf import settings
from django.utils import timezone


class ComputerListing(models.Model):
    # ------------------------
    # Common Choices
    # ------------------------
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted'),
    ]

    CONDITION_CHOICES = [
        ('brand_new', 'Brand New'),
        ('used_excellent', 'Used - Excellent Condition'),
        ('used_good', 'Used - Good Condition'),
        ('damaged', 'Damaged'),
    ]

    CATEGORY_CHOICES = [
        ('computers', 'Computers'),
        ('components', 'Computer Components'),
        ('accessories', 'Accessories'),
        ('networking', 'Networking & Communication'),
        ('software', 'Software'),
        ('mining', 'Mining Rigs & Components (CryptoCurrency)'),
        ('pos', 'POS Machine & Parts'),
        ('peripherals', 'Monitors, Printers & Other Peripherals'),
    ]

    # ------------------------
    # Common Fields
    # ------------------------
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='computer_listings'
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    description = models.TextField(max_length=1000,verbose_name="Description")
    created_at = models.DateTimeField(default=timezone.now)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price (OMR)")

    city = models.ForeignKey(
        'Cities', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='computer_listings'
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    images = models.ManyToManyField('ComputerImage', blank=True, related_name='listings')
    videos = models.ManyToManyField('ComputerVideo', blank=True, related_name='listings')

    # ------------------------
    # Extra Fields per Category
    # ------------------------

    # ✅ For Computers
    brand = models.CharField(max_length=100, blank=True, null=True)
    operating_system = models.CharField(max_length=100, blank=True, null=True)
    processor_brand = models.CharField(max_length=100, blank=True, null=True)
    processor_type = models.CharField(max_length=100, blank=True, null=True)

    # ✅ For Computer Components
    COMPONENT_CHOICES = [
        ('batteries', 'Batteries'),
        ('case', 'Case'),
        ('chargers', 'Chargers & Cables'),
        ('disk_reader', 'Disk Reader'),
        ('fans', 'Fans and Cooling'),
        ('gpu', 'Graphics Card'),
        ('motherboard', 'Motherboard'),
        ('psu', 'Power Supply'),
        ('processor', 'Processor'),
        ('ram', 'RAM'),
        ('sound_card', 'Sound Card'),
        ('other', 'Other'),
    ]
    component_type = models.CharField(max_length=50, choices=COMPONENT_CHOICES, blank=True, null=True)
    component_title = models.CharField(max_length=200, blank=True, null=True)

    # ✅ For Accessories
    ACCESSORY_CHOICES = [
        ('audio', 'Audio & Headsets'),
        ('keyboard', 'Keyboard'),
        ('laptop_bag', 'Laptop Bag'),
        ('mouse', 'Mouse'),
        ('printing_paper', 'Printing Paper'),
        ('webcam', 'Webcam'),
        ('other', 'Other'),
    ]
    accessory_type = models.CharField(max_length=50, choices=ACCESSORY_CHOICES, blank=True, null=True)

    # ✅ For Monitors, Printers & Peripherals
    peripheral_brand = models.CharField(max_length=100, blank=True, null=True)
    screen_size = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.category} - {self.description[:30]}"


class ComputerImage(models.Model):
    image = models.ImageField(upload_to='computers/images/')

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class ComputerVideo(models.Model):
    video = models.FileField(upload_to='computers/videos/')

    def __str__(self):
        return f"Video {self.id}"

class BusinessIndustrialListing(models.Model):
  
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sale', 'For Sale'),
        ('wanted', 'Wanted'),
    ]

    

    CATEGORY_CHOICES = [
        ('business_sale', 'Businesses for Sale'),
        ('construction', 'Construction'),
        ('food_beverage', 'Food & Beverage'),
        ('industrial_supplies', 'Industrial Supplies'),
        ('office_furniture', 'Office Furniture & Equipment'),
        ('manufacturing', 'Manufacturing'),
        ('electrical_equipment', 'Electrical Equipment'),
        ('retail_services', 'Retail & Services'),  # 👈 important for service_type
    ]

    SERVICE_TYPE_CHOICES = [
        ('movers_packers', 'Movers - Packers'),
        ('home_care', 'Home Care Services'),
        ('appliances_repair', 'Appliances Repair Services'),
        ('home_repair', 'Home Repair'),
        ('cleaning', 'Cleaning Services'),
        ('towing', 'Towing Services'),
        ('car_maintenance', 'Car Maintenance And Repair'),
        ('doors_windows', 'Doors - Windows Maintenance'),
        ('transport_delivery', 'Transportation & Delivery Services'),
        ('carpentry', 'Carpentry and Furniture Maintenance'),
        ('water_tanks', 'Water Tanks'),
        ('welding', 'Blacksmith & Welding Services'),
        ('travel_tourism', 'Travel - Tourism'),
        ('interior_design', 'Interior Design Services'),
        ('mobile_repair', 'Mobile & Tablet Repair Services'),
        ('plumbing', 'Plumbing Services'),
        ('painting', 'Painting Services'),
        ('upholstery', 'Upholstery Services'),
        ('kitchen_install', 'Kitchen Installation'),
        ('design_printing', 'Design & Printing Services'),
        ('events', 'Events Services'),
        ('pest_control', 'Pest Control'),
        ('business_services', 'Business Services'),
        ('electrical_services', 'Electrical Services'),
        ('marketing', 'Marketing & Advertising'),
        ('accounting', 'Accounting & Finance'),
        ('gardening', 'Gardening Services'),
        ('computer_repair', 'Computer Repair Services'),
        ('general_repair', 'General Repair Services'),
        ('medical', 'Medical Services'),
        ('legal', 'Legal Services'),
        ('tiles_flooring', 'Tiles & Flooring Services'),
        ('beauty', 'Beauty & Personal Care'),
        ('video_games_repair', 'Video Games Repair Services'),
        ('car_cleaning', 'Car Cleaning Services'),
        ('bathroom_install', 'Bathroom Installation'),
        ('other', 'Other Services'),
    ]
    CONDITION_CHOICES = [
        ('flawless', 'Flawless'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]

    USAGE_CHOICES = [
        ('never_used', 'Never Used'),
        ('used_once', 'Used Once'),
        ('light_usage', 'Light Usage'),
        ('normal_usage', 'Normal Usage'),
        ('heavy_usage', 'Heavy Usage'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='business_industrial_listings'
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    service_type = models.CharField(  # ✅ only for retail & services
        max_length=100,
        choices=SERVICE_TYPE_CHOICES,
        blank=True,
        null=True
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Price (OMR)")
    description = models.TextField(max_length=1000,verbose_name="Description")

    city = models.ForeignKey(
        'Cities',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='business_industrial_listings'
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    condition = models.CharField(
        max_length=50,
        choices=CONDITION_CHOICES,
        default='excellent',   # ✅ default value
        verbose_name="Condition"
    )
    usage = models.CharField(
        max_length=50,
        choices=USAGE_CHOICES,
        default='never_used',  # ✅ default value
        verbose_name="Usage"
    )

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    images = models.ManyToManyField('BusinessIndustrialImage', blank=True, related_name='listings')
    videos = models.ManyToManyField('BusinessIndustrialVideo', blank=True, related_name='listings')

    def __str__(self):
        return f"{self.get_category_display()} - {self.description[:30]}"


class BusinessIndustrialImage(models.Model):
    image = models.ImageField(upload_to='business_industrial/images/')

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class BusinessIndustrialVideo(models.Model):
    video = models.FileField(upload_to='business_industrial/videos/')

    def __str__(self):
        return f"Video {self.id}"




class PetListing(models.Model):
    # ------------------------
    # Common Choices
    # ------------------------
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted'),
    ]

    CATEGORY_CHOICES = [
        ('free_adoption', 'Pets for Free Adoption'),
        ('pet_accessories', 'Pet Accessories'),
        ('lost_found', 'Lost & Found Pets'),
    ]

    PET_TYPE_CHOICES = [
        ('cats', 'Cats'), ('dogs', 'Dogs'), ('parrots', 'Parrots'), ('pigeons', 'Pigeons'),
        ('chickens', 'Chickens'), ('sheep', 'Sheep'), ('goats', 'Goats'), ('horses', 'Horses'),
        ('camels', 'Camels'), ('birds', 'Birds'), ('fish', 'Fish'), ('turtles', 'Turtles'),
        ('rabbits', 'Rabbits'), ('hamsters', 'Hamsters'), ('cows', 'Cows'),
    ]
    
    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]

    ACCESSORY_TYPE_CHOICES = [
        ('collar', 'Collar'), ('leash', 'Leash'), ('toys', 'Toys'), ('cage', 'Cage'),
        ('food', 'Food'), ('bedding', 'Bedding'), ('clothes', 'Clothes'), ('other', 'Other'),
    ]
    AGE_CHOICES = [
        ('0-12', '0-12 months'),
        ('13-24', '13-24 months'),
        ('25-36', '25-36 months'),
        ('37-48', '37-48 months'),
        ('4plus', 'More than 4 years'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pet_listings'
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    # Pet fields (for adoption and lost/found)
    pet_type = models.CharField(max_length=20, choices=PET_TYPE_CHOICES, blank=True, null=True)
    breed = models.CharField(max_length=50, blank=True, null=True)  # Removed invalid choices
    name = models.CharField(max_length=100, blank=True, null=True)
    age = models.CharField(
    max_length=10,
    choices=AGE_CHOICES,
    default='13-24',
    blank=True,
    null=True
    )
    accessory_type = models.CharField(max_length=50, choices=ACCESSORY_TYPE_CHOICES, blank=True, null=True)
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, blank=True, null=True)
    accept_exchange = models.BooleanField(default=False)

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Price (OMR)")
    description = models.TextField(max_length=1000,verbose_name="Description")

    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='pet_listings')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    images = models.ManyToManyField('PetImage', blank=True, related_name='listings')
    videos = models.ManyToManyField('PetVideo', blank=True, related_name='listings')

    def __str__(self):
        return f"{self.get_category_display()} - {self.name or 'Unnamed'}"


class PetImage(models.Model):
    image = models.ImageField(upload_to='pets/images/')
    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class PetVideo(models.Model):
    video = models.FileField(upload_to='pets/videos/')
    def __str__(self):
        return f"Video {self.id}"

class SportsListing(models.Model):

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]

    AGE_CHOICES = [
        ('0-12', '0-12 months'),
        ('13-24', '13-24 months'),
        ('25-36', '25-36 months'),
        ('37-48', '37-48 months'),
        ('4plus', 'More than 4 years'),
    ]

    CATEGORY_CHOICES = [
        ('cycling', 'Cycling'),
        ('exercise_equipment', 'Exercise Equipment'),
        ('water_sports', 'Water Sports'),
        ('camping_hiking', 'Camping & Hiking'),
        ('golf', 'Golf'),
        ('indoor_sports', 'Indoor Sports'),
        ('team_sports', 'Team Sports'),
        ('tennis_racquet', 'Tennis & Racquet Sports'),
        ('winter_sports', 'Winter Sports'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sports_listings'
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=100, blank=True, null=True)

    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, blank=True, null=True)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=10, choices=AGE_CHOICES, default='13-24', blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Price (OMR)")
    description = models.TextField(max_length=1000,verbose_name="Description", blank=True, null=True)

    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='sports_listings')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    images = models.ManyToManyField('SportsImage', blank=True, related_name='listings')
    videos = models.ManyToManyField('SportsVideo', blank=True, related_name='listings')

    def _str_(self):
        return f"{self.get_category_display()} - {self.price or 'No Price'}"


class SportsImage(models.Model):
    image = models.ImageField(upload_to='sports/images/')

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class SportsVideo(models.Model):
    video = models.FileField(upload_to='sports/videos/')

    def _str_(self):
        return f"Video {self.id}"

class MusicalListing(models.Model):
  
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted'),
    ]

    CONDITION_CHOICES = [
        ('new', 'New'),
        ('used', 'Used'),
    ]

    CATEGORY_CHOICES = [
        ('guitars', 'Guitars'),
        ('pianos', 'Pianos, Keyboards & Organs'),
        ('percussion', 'Percussion'),
        ('string', 'String Instruments'),
        ('wind', 'Wind Instruments'),
        ('dj_recording', 'DJ & Recording Equipment'),
        ('other', 'Other'),  
    ]

    AGE_CHOICES = [
         ('brand_new', 'Brand New'),
    ('1_2_years', '1-2 years'),
    ('3_5_years', '3-5 years'),
    ('6_10_years', '6-10 years'),
    ('10_plus', '10+ years'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    USAGE_CHOICES = [
        ('never_used', 'Never Used'),
        ('used_once', 'Used Once'),
        ('light_usage', 'Light Usage'),
        ('normal', 'Normal Usage'),
        ('heavy', 'Heavy Usage'),
    ]

    CONDITION_DETAIL_CHOICES = [
        ('flawless', 'Flawless'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='musical_instrument_listings'
    )

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=100, blank=True, null=True, help_text="Specify if category is 'Other'")  # New subcategory

    type = models.CharField(max_length=100, blank=True, null=True, help_text="Specific instrument type, e.g., Acoustic Guitar, Digital Piano")
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, blank=True, null=True)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, blank=True, null=True)

    age = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True, null=True)  # New field
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True, null=True)  # New field
    condition_detail = models.CharField(max_length=20, choices=CONDITION_DETAIL_CHOICES, blank=True, null=True)  # New field

    provide = models.BooleanField(default=False, help_text="Provide? (Yes/No)")

    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Price (OMR)")
    description = models.TextField(max_length=1000,verbose_name="Description", blank=True, null=True)
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='musical_instrument_listings')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    images = models.ManyToManyField('MusicalInstrumentImage', blank=True, related_name='listings')
    videos = models.ManyToManyField('MusicalInstrumentVideo', blank=True, related_name='listings')

    def __str__(self):
        return f"{self.get_category_display()} - {self.price or 'No Price'}"


class MusicalInstrumentImage(models.Model):
    image = models.ImageField(upload_to='musical_instruments/images/')

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class MusicalInstrumentVideo(models.Model):
    video = models.FileField(upload_to='musical_instruments/videos/')

    def __str__(self):
        return f"Video {self.id}"



class GamingListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    CONDITION_CHOICES = [
        ('flawless', 'Flawless'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]

    AGE_CHOICES = [
        ('brand_new', 'Brand New'),
        ('1_year', '1 Year'),
        ('2_years', '2 Years'),
        ('3_years', '3 Years'),
        ('4_years', '4 Years'),
        ('5_years', '5 Years'),
        ('6_10_years', '6-10 Years'),
        ('10_plus', '10+ Years'),
    ]

    USAGE_CHOICES = [
        ('never_used', 'Never Used'),
        ('used_once', 'Used Once'),
        ('light_usage', 'Light Usage'),
        ('normal', 'Normal Usage'),
        ('heavy', 'Heavy Usage'),
    ]

    PACKAGE_CHOICES = [
        ('system_controllers', 'Gaming System + Controllers'),
        ('system_games', 'Gaming System + Games'),
        ('system_games_controllers', 'Gaming System + Games & Controllers'),
        ('system_only', 'Gaming System Only'),
    ]

    RATING_CHOICES = [
        ('EC', 'Early Child'),
        ('E', 'Everyone'),
        ('E10+', 'Everyone 10+'),
        ('T', 'Teens'),
        ('M', 'Mature'),
        ('RP', 'Rating Pending'),
    ]

    CATEGORY_CHOICES = [
        ('gaming_systems', 'Gaming Systems'),
        ('video_games', 'Video Games'),
        ('gaming_accessories', 'Gaming Accessories'),
    ]

    GAMING_SYSTEM_SUBCATEGORY_CHOICES = [
        ('playstation_5', 'PlayStation 5'),
    ('playstation_4', 'PlayStation 4'),
    ('playstation_3', 'PlayStation 3'),
    ('playstation_2', 'PlayStation 2'),
    ('playstation_1', 'PlayStation'),
    ('ps_vita', 'PS Vita'),
    ('psp', 'PSP'),

    ('xbox_series_x', 'Xbox Series X|S'),
    ('xbox_one', 'Xbox One'),
    ('xbox_360', 'Xbox 360'),

    ('nintendo_switch', 'Nintendo Switch'),
    ('nintendo_wii', 'Nintendo Wii'),
    ('nintendo_ds', 'Nintendo DS'),
    ('nintendo_64', 'Nintendo 64'),
    ('nintendo_gamecube', 'Nintendo GameCube'),
    ('nintendo_nes', 'Nintendo NES'),
    ('super_nintendo', 'Super Nintendo'),

    ('gaming_pc', 'Gaming PC'),
    ('handheld_console', 'Handheld Consoles (Steam Deck, etc.)'),
    ('retro_console', 'Retro Consoles'),
    ('arcade_machine', 'Arcade Machines'),
    ('other', 'Other'),
    ]

    VIDEO_GAME_SUBCATEGORY_CHOICES = [
        # PlayStation
    ('playstation_5', 'PlayStation 5'),
    ('playstation_4', 'PlayStation 4'),
    ('playstation_3', 'PlayStation 3'),
    ('playstation_2', 'PlayStation 2'),
    ('playstation_1', 'PlayStation'),
    ('ps_vita', 'PS Vita'),
    ('psp', 'PSP'),

    # Xbox
    ('xbox_series_x', 'Xbox Series X|S'),
    ('xbox_one', 'Xbox One'),
    ('xbox_360', 'Xbox 360'),

    # Nintendo
    ('nintendo_switch_2', 'Nintendo Switch 2'),
    ('nintendo_switch', 'Nintendo Switch'),
    ('nintendo_wii', 'Nintendo Wii'),
    ('nintendo_ds', 'Nintendo DS'),
    ('nintendo_64', 'Nintendo 64'),
    ('nintendo_gamecube', 'Nintendo GameCube'),
    ('nintendo_nes', 'Nintendo NES'),
    ('super_nintendo', 'Super Nintendo'),

    # Other Platforms
    ('pc', 'PC'),
    ('other', 'Other'),

    # Broad Game Categories
    ('ps_games', 'PlayStation Games'),
    ('xbox_games', 'Xbox Games'),
    ('nintendo_games', 'Nintendo Games'),
    ('pc_games', 'PC Games'),
    ('vr_games', 'VR Games'),
    ('mobile_games', 'Mobile Games'),
    ('collector_games', 'Collector’s Editions'),
    ('digital_codes', 'Digital Codes / Gift Cards'),
    ('board_games', 'Board & Card Games'),
    ]

    ACCESSORY_SUBCATEGORY_CHOICES = [
        # Consoles & Systems
    ('playstation_5', 'PlayStation 5'),
    ('playstation_4', 'PlayStation 4'),
    ('playstation_3', 'PlayStation 3'),
    ('playstation_2', 'PlayStation 2'),
    ('playstation_1', 'PlayStation'),
    ('ps_vita', 'PS Vita'),
    ('psp', 'PSP'),

    ('xbox_one', 'Xbox One'),
    ('xbox_360', 'Xbox 360'),

    ('nintendo_switch', 'Nintendo Switch'),
    ('nintendo_wii', 'Nintendo Wii'),
    ('nintendo_ds', 'Nintendo DS'),
    ('nintendo_64', 'Nintendo 64'),
    ('nintendo_gamecube', 'Nintendo GameCube'),
    ('nintendo_nes', 'Nintendo NES'),
    ('super_nintendo', 'Super Nintendo'),

    ('pc', 'PC'),
    ('other_systems', 'Other'),

    # Accessories
    ('controllers', 'Controllers & Gamepads'),
    ('headsets', 'Gaming Headsets'),
    ('keyboards', 'Keyboards'),
    ('mice', 'Gaming Mice'),
    ('mousepads', 'Mouse Pads'),
    ('chairs', 'Gaming Chairs'),
    ('desks', 'Gaming Desks'),
    ('cables_chargers', 'Cables & Chargers'),
    ('vr_accessories', 'VR Accessories'),
    ('other_accessories', 'Other'),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='gaming_listings')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Type (e.g., PS5, Xbox, Gaming Chair)")
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )

    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True, null=True)
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True, null=True)
    package = models.CharField(max_length=50, choices=PACKAGE_CHOICES, blank=True, null=True)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, blank=True, null=True)

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, blank=True, null=True)
    provide = models.BooleanField(default=False, help_text="Provide? (Yes/No)")

    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Price (OMR)")
    description = models.TextField(max_length=1000,verbose_name="Description", blank=True, null=True)
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='gaming_listings')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)
    images = models.ManyToManyField('GamingImage', blank=True, related_name='listings')
    videos = models.ManyToManyField('GamingVideo', blank=True, related_name='listings')

    def __str__(self):
        return f"{self.get_category_display()} - {self.price or 'No Price'}"

    # ------------------------
    # Helper Methods
    # ------------------------
    @staticmethod
    def get_subcategory_choices(category):
        if category == 'gaming_systems':
            return GamingListing.GAMING_SYSTEM_SUBCATEGORY_CHOICES
        elif category == 'video_games':
            return GamingListing.VIDEO_GAME_SUBCATEGORY_CHOICES
        elif category == 'gaming_accessories':
            return GamingListing.ACCESSORY_SUBCATEGORY_CHOICES
        return []

class GamingImage(models.Model):
    image = models.ImageField(upload_to='gaming/images/')

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class GamingVideo(models.Model):
    video = models.FileField(upload_to='gaming/videos/')

    def __str__(self):
        return f"Video {self.id}"


class TicketVoucherListing(models.Model):
    # ------------------------
    # Common Choices
    # ------------------------
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    CATEGORY_CHOICES = [
        ('tickets_vouchers', 'Tickets & Vouchers'),
    ]

    SUBCATEGORY_CHOICES = [
        ('concerts', 'Concerts'),
        ('sporting_events', 'Sporting Events'),
        ('travel', 'Travel'),
        ('events', 'Events'),
        ('movies_theater', 'Movies & Theater'),
        ('activities_attractions', 'Activities & Attractions'),
        ('vouchers_giftcards', 'Vouchers & Gift Cards'),
        ('others', 'Other'),
    ]
    TICKET_NUMBER_CHOICES = [
        ('single', 'Single Ticket'),
        ('pair', 'Pair Tickets'),
        ('3', '3 Tickets'),
        ('4', '4 Tickets'),
        ('4_plus', '4+ Tickets'),
    ]

    PROVIDE_CHOICES = [
        ('yes', 'Yes'),
        ('no', 'No'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    # ------------------------
    # Core Fields
    # ------------------------
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='ticketvoucher_listings'
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='tickets_vouchers')
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, blank=True, null=True)

    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Price (OMR)")
    description = models.TextField(max_length=1000,verbose_name="Description", blank=True, null=True)
    number_of_tickets = models.CharField(max_length=10, choices=TICKET_NUMBER_CHOICES, blank=True, null=True)
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='ticketvoucher_listings')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    provide = models.CharField(max_length=3, choices=PROVIDE_CHOICES, default='no')

    other_options = models.TextField(blank=True, null=True, help_text="Extra details (e.g. seat info, date, terms, etc.)")

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    images = models.ManyToManyField('TicketVoucherImage', blank=True, related_name='listings')
    videos = models.ManyToManyField('TicketVoucherVideo', blank=True, related_name='listings')

    def __str__(self):
        return f"{self.get_subcategory_display()} - {self.price or 'No Price'}"


class TicketVoucherImage(models.Model):
    image = models.ImageField(upload_to='tickets_vouchers/images/')

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class TicketVoucherVideo(models.Model):
    video = models.FileField(upload_to='tickets_vouchers/videos/')

    def __str__(self):
        return f"TicketVoucherVideo {self.id}"


class CollectibleListing(models.Model):
    # ------------------------
    # Common Choices
    # ------------------------
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted'),
    ]
    CONDITION_CHOICES = [
        ('flawless', 'Flawless'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]

    AGE_CHOICES = [
        ('brand_new', 'Brand New'),
        ('1_year', '1 Year'),
        ('2_years', '2 Years'),
        ('3_years', '3 Years'),
        ('4_years', '4 Years'),
        ('5_years', '5 Years'),
        ('6_10_years', '6-10 Years'),
        ('10_plus', '10+ Years'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    USAGE_CHOICES = [
        ('never_used', 'Never Used'),
        ('used_once', 'Used Once'),
        ('light_usage', 'Light Usage'),
        ('normal', 'Normal Usage'),
        ('heavy', 'Heavy Usage'),
    ]

    CATEGORY_CHOICES = [
        ('antiques', 'Antiques'),
        ('art', 'Art'),
        ('decorations', 'Decorations'),
        ('pens_writing_instruments', 'Pens & Writing Instruments'),
        ('memorabilia', 'Memorabilia'),
        ('rocks_fossils_artifacts', 'Rocks / Fossils / Artifacts'),
        ('other', 'Other'),
    ]

    SUBCATEGORY_CHOICES = [
        # Antiques
        ('antiquities', 'Antiquities'),
        ('books_maps', 'Books & Maps'),
        ('decorations_antiques', 'Decorations'),
        ('furniture', 'Furniture'),
        ('machines_tools', 'Machines, Instruments & Tools'),
        ('other_antiques', 'Other'),

        # Art
        ('drawings', 'Drawings'),
        ('paintings', 'Paintings'),
        ('photography', 'Photography'),
        ('statues', 'Statues'),
        ('other_art', 'Other'),

        # Decorations
        ('domestic_decorations', 'Domestic Decorations'),
        ('linens_textiles', 'Linens/Textiles'),
        ('outdoor_decoration', 'Outdoor Decoration'),
        ('wall_hangings', 'Wall Hangings'),
        ('other_decorations', 'Other'),

        # Pens & Writing Instruments
        ('calligraphy', 'Calligraphy'),
        ('pens', 'Pens'),
        ('sets', 'Sets'),
        ('typewriters', 'Typewriters'),
        ('other_pens', 'Other'),

        # Memorabilia
        ('cultural_memorabilia', 'Cultural Memorabilia'),
        ('historical_memorabilia', 'Historical Memorabilia'),
        ('limited_edition_memorabilia', 'Limited Edition Memorabilia'),
        ('military_memorabilia', 'Military Memorabilia'),
        ('religious_memorabilia', 'Religious Memorabilia'),
        ('sports_memorabilia', 'Sports Memorabilia'),
        ('other_memorabilia', 'Other'),

        # Rocks / Fossils / Artifacts
        ('artifacts', 'Artifacts'),
        ('fossils', 'Fossils'),
        ('petrified_wood', 'Petrified Wood'),
        ('rocks_crystals_minerals', 'Rocks, Crystals & Minerals'),
        ('other_rocks', 'Other'),

        # Other
        ('other', 'Other'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='collectible_listings'
    )

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Type / Specific Item")

    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True, null=True)
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True, null=True)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, blank=True, null=True)
    provide = models.BooleanField(default=False, help_text="Provide? (Yes/No)")

    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Price (OMR)")
    description = models.TextField(max_length=1000,verbose_name="Description", blank=True, null=True)

    # ------------------------
    # Location
    # ------------------------
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='collectible_listings')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # ------------------------
    # Status & Timestamps
    # ------------------------
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    # ------------------------
    # Media
    # ------------------------
    images = models.ManyToManyField('CollectibleImage', blank=True, related_name='listings')
    videos = models.ManyToManyField('CollectibleVideo', blank=True, related_name='listings')

    def __str__(self):
        return f"{self.get_category_display()} - {self.price or 'No Price'}"


class CollectibleImage(models.Model):
    image = models.ImageField(upload_to='collectibles/images/')

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class CollectibleVideo(models.Model):
    video = models.FileField(upload_to='collectibles/videos/')

    def __str__(self):
        return f"Video {self.id}"

class BooksListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted'),
    ]

    CONDITION_CHOICES = [
        ('flawless', 'Flawless'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]

    AGE_CHOICES = [
        ('brand_new', 'Brand New'),
        ('1_year', '1 Year'),
        ('2_years', '2 Years'),
        ('3_years', '3 Years'),
        ('4_years', '4 Years'),
        ('5_years', '5 Years'),
        ('6_10_years', '6-10 Years'),
        ('10_plus', '10+ Years'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    USAGE_CHOICES = [
        ('never_used', 'Never Used'),
        ('used_once', 'Used Once'),
        ('light_usage', 'Light Usage'),
        ('normal', 'Normal Usage'),
        ('heavy', 'Heavy Usage'),
    ]

    CATEGORY_CHOICES = [
        ('textbooks', 'Textbooks'),
        ('nonfiction', 'Nonfiction'),
        ('fiction', 'Fiction'),
        ('children_books', "Children's Books"),
        ('book_accessories', 'Book Accessories'),
        ('digital_ebooks', 'Digital / E-books'),
        ('audiobooks', 'Audiobooks'),
        ('stationery', 'Stationery'),
    ]

    SUBCATEGORY_CHOICES = [
        # Textbooks
        ('a_levels', 'A Levels / High School'),
        ('primary_school', 'Primary School'),
        ('secondary_school', 'Secondary School'),
        ('university', 'University'),

        # Nonfiction
        ('business_science_tech', 'Business/Science/Technology'),
        ('cook_books', 'Cook Books'),
        ('history_biography', 'History/Biography'),
        ('how_to_books', 'How-To Books'),
        ('picture_books', 'Picture Books'),
        ('religious_books', 'Religious Books'),
        ('self_help', 'Self Help / Motivational Books'),
        ('sports_health', 'Sports/Health Books'),
        ('travel_books', 'Travel Books'),
        ('other_nonfiction', 'Other'),

        # Fiction
        ('action_adventure', 'Action/Adventure'),
        ('classics', 'Classics'),
        ('fantasy_scifi', 'Fantasy/Sci Fi'),
        ('humor', 'Humor'),
        ('mystery_thriller', 'Mystery/Thriller'),
        ('romance', 'Romance'),
        ('other_fiction', 'Other'),

        # Children's Books
        ('coloring_activity', 'Coloring/Activity Books'),
        ('educational_books', 'Educational Books'),
        ('fiction_cb', 'Fiction'),
        ('nonfiction_cb', 'Nonfiction'),
        ('picture_popup_books', 'Picture/Pop Up Books'),
        ('other_cb', 'Other'),

        # Book Accessories
        ('book_lights', 'Book Lights'),
        ('daily_planners', 'Daily Planners'),
        ('diaries_notebooks', 'Diaries/Note Books'),
        ('other_accessories', 'Other'),
    ]

    # Core Fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='books_listings')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, blank=True, null=True)
    type = models.CharField(max_length=50, blank=True, null=True, verbose_name="Type / Hardcover/Paperback")
    title = models.CharField(
        max_length=200,
        verbose_name="Listing Title"
    )
    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True, null=True)
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True, null=True)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Price (OMR)")

    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    images = models.ManyToManyField('BooksImage', blank=True, related_name='listings')
    videos = models.ManyToManyField('BooksVideo', blank=True, related_name='listings')

    def __str__(self):
        return f"{self.get_category_display()} - {self.price or 'No Price'}"


class BooksImage(models.Model):
    image = models.ImageField(upload_to='books/images/')
    
    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class BooksVideo(models.Model):
    video = models.FileField(upload_to='books/videos/')

class MusicListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted'),
    ]

    CONDITION_CHOICES = [
        ('flawless', 'Flawless'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]

    AGE_CHOICES = [
        ('brand_new', 'Brand New'),
        ('1_year', '1 Year'),
        ('2_years', '2 Years'),
        ('3_years', '3 Years'),
        ('4_years', '4 Years'),
        ('5_years', '5 Years'),
        ('6_10_years', '6-10 Years'),
        ('10_plus', '10+ Years'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    USAGE_CHOICES = [
        ('never_used', 'Never Used'),
        ('used_once', 'Used Once'),
        ('light_usage', 'Light Usage'),
        ('normal', 'Normal Usage'),
        ('heavy', 'Heavy Usage'),
    ]

    CATEGORY_CHOICES = [
        ('vinyl', 'Vinyl'),
        ('cds', 'CDs'),
        ('cassettes', 'Cassettes'),
        ('digital', 'Digital'),
    ]

    SUBCATEGORY_CHOICES = [
       
        # CDs genres
        ('cds_classical', 'Classical'),
        ('cds_country', 'Country'),
        ('cds_jazz', 'Jazz'),
        ('cds_latin', 'Latin'),
        ('cds_metal', 'Metal'),
        ('cds_rnb_soul_funk', 'R&B / Soul / Funk'),
        ('cds_arabic', 'Arabic'),
        ('cds_rock_indie', 'Rock & Indie Rock'),

        # Cassettes genres
        ('cass_classical', 'Classical'),
        ('cass_country', 'Country'),
        ('cass_jazz', 'Jazz'),
        ('cass_latin', 'Latin'),
        ('cass_metal', 'Metal'),
        ('cass_rnb_soul_funk', 'R&B / Soul / Funk'),
        ('cass_arabic', 'Arabic'),
        ('cass_rock_indie', 'Rock & Indie Rock'),

        # Digital genres
        ('digital_classical', 'Classical'),
        ('digital_country', 'Country'),
        ('digital_jazz', 'Jazz'),
        ('digital_latin', 'Latin'),
        ('digital_metal', 'Metal'),
        ('digital_rnb_soul_funk', 'R&B / Soul / Funk'),
        ('digital_arabic', 'Arabic'),
        ('digital_rock_indie', 'Rock & Indie Rock'),
    ]

    DURATION_CHOICES = [
        ('album', 'Album'),
        ('ep', 'EP'),
        ('box_set', 'Box Set'),
        ('single', 'Single'),
        ('other', 'Other'),
    ]

    # Core Fields
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='music_listings')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, blank=True, null=True)

    title = models.CharField(max_length=255, verbose_name="Title" ,default='Vinyl')

    type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Type / Title")
    duration = models.CharField(max_length=20, choices=DURATION_CHOICES, blank=True, null=True)

    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True, null=True)
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True, null=True)

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Price (OMR)")

    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    images = models.ManyToManyField('MusicImage', blank=True, related_name='listings')
    videos = models.ManyToManyField('MusicVideo', blank=True, related_name='listings')

    def __str__(self):
        return f"{self.get_category_display()} - {self.price or 'No Price'}"


class MusicImage(models.Model):
    image = models.ImageField(upload_to='music/images/')
    
    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class MusicVideo(models.Model):
    video = models.FileField(upload_to='music/videos/')

class DVDsMoviesListing(models.Model):
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted'),
    ]

    CATEGORY_CHOICES = [
        ('dvd', 'DVD'),
        ('digital', 'Digital'),
        ('vhs', 'VHS'),
        ('other_formats', 'Other Formats'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    SUBCATEGORY_CHOICES = [
        ('action_adventure', 'Action, Adventure'),
        ('animation', 'Animation'),
        ('children_family', 'Children & Family'),
        ('comedy', 'Comedy'),
        ('concert_music', 'Concert/Music'),
        ('documentary', 'Documentary Film'),
        ('drama', 'Drama'),
        ('horror', 'Horror'),
        ('mystery_suspense', 'Mystery/Suspense'),
        ('series', 'Series'),
        ('sports', 'Sports'),
        ('other_genre', 'Other Genre'),
    ]

    CONDITION_CHOICES = [
        ('flawless', 'Flawless'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]

    AGE_CHOICES = [
        ('brand_new', 'Brand New'),
        ('1_year', '1 Year'),
        ('2_years', '2 Years'),
        ('3_years', '3 Years'),
        ('4_years', '4 Years'),
        ('5_years', '5 Years'),
        ('6_10_years', '6-10 Years'),
        ('10_plus', '10+ Years'),
    ]

    USAGE_CHOICES = [
        ('never_used', 'Never Used'),
        ('used_once', 'Used Once'),
        ('light_usage', 'Light Usage'),
        ('normal', 'Normal Usage'),
        ('heavy', 'Heavy Usage'),
    ]

    RATING_CHOICES = [
        ('G', 'G'),
        ('PG', 'PG'),
        ('PG13', 'PG-13'),
        ('R', 'R'),
        ('NC17', 'NC-17'),
        ('Unrated', 'Unrated'),
        ('Other', 'Other'),
    ]

    # ------------------------
    # Core Fields
    # ------------------------
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='dvds_movies_listings')
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=50, choices=SUBCATEGORY_CHOICES, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True, verbose_name="Title / Type")

    condition = models.CharField(max_length=10, choices=CONDITION_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True, null=True)
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True, null=True)
    rating = models.CharField(max_length=10, choices=RATING_CHOICES, blank=True, null=True)

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True, verbose_name="Price (OMR)")

    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    other_options = models.TextField(blank=True, null=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(default=timezone.now)

    images = models.ManyToManyField('DVDsMoviesImage', blank=True, related_name='listings')
    videos = models.ManyToManyField('DVDsMoviesVideo', blank=True, related_name='listings')

    def __str__(self):
        return f"{self.get_category_display()} - {self.price or 'No Price'}"


class DVDsMoviesImage(models.Model):
    image = models.ImageField(upload_to='DVD/images/')


class DVDsMoviesVideo(models.Model):
    video = models.FileField(upload_to='DVD/videos/')

class FurnitureHomeGardenListing(models.Model):
 
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted'),
    ]

    # Updated Condition Choices
    CONDITION_CHOICES = [
        ('flawless', 'Flawless'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]

    AGE_CHOICES = [
        ('brand_new', 'Brand New'),
        ('1_year', '1 Year'),
        ('2_years', '2 Years'),
        ('3_years', '3 Years'),
        ('4_years', '4 Years'),
        ('5_years', '5 Years'),
        ('6_10_years', '6-10 Years'),
        ('10_plus', '10+ Years'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    USAGE_CHOICES = [
        ('never_used', 'Never Used'),
        ('used_once', 'Used Once'),
        ('light_usage', 'Light Usage'),
        ('normal', 'Normal Usage'),
        ('heavy', 'Heavy Usage'),
    ]

    CATEGORY_CHOICES = [
        ('furniture', 'Furniture'),
        ('home_accessories', 'Home Accessories'),
        ('garden_outdoor', 'Garden & Outdoor'),
        ('lighting_fans', 'Lighting & Fans'),
        ('rugs_carpets', 'Rugs & Carpets'),
        ('curtains_blinds', 'Curtains & Blinds'),
        ('tools_home_improvement', 'Tools & Home Improvement'),
    ]
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="furniture_home_garden_listings"
    )

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=100, blank=True, null=True)

    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True, null=True)
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True, null=True)

    title = models.CharField(max_length=150, verbose_name="Listing Title")
    description = models.TextField(blank=True, null=True)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES, blank=True, null=True)

    price = models.DecimalField(
        max_digits=12, decimal_places=2,
        blank=True, null=True,
        verbose_name="Price (OMR)"
    )

    # Location
    city = models.ForeignKey("Cities", on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # System fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now)

    # Media
    images = models.ManyToManyField("FurnitureHomeGardenImage", blank=True, related_name="listings")
    videos = models.ManyToManyField("FurnitureHomeGardenVideo", blank=True, related_name="listings")

    def __str__(self):
        return f"{self.title} ({self.get_main_category_display()}) - {self.price or 'No Price'}"


class FurnitureHomeGardenImage(models.Model):
    image = models.ImageField(upload_to="furniture_home_garden/images/")
    
    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class FurnitureHomeGardenVideo(models.Model):
    video = models.FileField(upload_to="furniture_home_garden/videos/")


class BabyItemsListing(models.Model):
    # ------------------------
    # Common Choices
    # ------------------------
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('soldout', 'Soldout'),
    ]

    LISTING_TYPE_CHOICES = [
        ('sell', 'Sale'),
        ('wanted', 'Wanted'),
    ]

    CONDITION_CHOICES = [
        ('flawless', 'Flawless'),
        ('excellent', 'Excellent'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('poor', 'Poor'),
    ]

    AGE_CHOICES = [
        ('brand_new', 'Brand New'),
        ('1_year', '1 Year'),
        ('2_years', '2 Years'),
        ('3_years', '3 Years'),
        ('4_years', '4 Years'),
        ('5_years', '5 Years'),
        ('6_10_years', '6-10 Years'),
        ('10_plus', '10+ Years'),
    ]

    USAGE_CHOICES = [
        ('never_used', 'Never Used'),
        ('used_once', 'Used Once'),
        ('light_usage', 'Light Usage'),
        ('normal', 'Normal Usage'),
        ('heavy', 'Heavy Usage'),
    ]

    CATEGORY_CHOICES = [
        ('strollers_car_seats', 'Strollers & Car Seats'),
        ('nursery_furniture', 'Nursery Furniture & Accessories'),
        ('baby_gear', 'Baby Gear'),
        ('baby_toys', 'Baby Toys'),
        ('feeding', 'Feeding'),
        ('safety_health', 'Safety & Health'),
        ('bath_diapers', 'Bath & Diapers'),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="baby_items_listings"
    )

    category = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES
    )
    SUBCATEGORY_CHOICES = [
    # Strollers & Car Seats
    ('car_seat_accessories', 'Car Seat Accessories'),
    ('infant_car_seats', 'Infant Car Seats'),
    ('jogging_strollers', 'Jogging Strollers'),
    ('pram_strollers', 'Pram Strollers'),
    ('standard_strollers', 'Standard Strollers'),
    ('stroller_accessories', 'Stroller Accessories'),
    ('toddler_car_seats', 'Toddler Car Seats'),
    ('travel_system_strollers', 'Travel System Strollers'),

    # Nursery Furniture
    ('baby_dressers', 'Baby Dressers'),
    ('bassinets_cradles_rockers', 'Bassinets, Cradles & Rockers'),
    ('changing_tables', 'Changing Tables'),
    ('cribs', 'Cribs'),
    ('nursery_bedding', 'Nursery Bedding'),
    ('nursery_decor_accessories', 'Nursery Decor & Accessories'),
    ('nursery_furniture_sets', 'Nursery Furniture Sets'),

    # Baby Gear
    ('backpacks_carriers', 'Backpacks & Carriers'),
    ('chairs', 'Chairs'),
    ('jumping_exercisers', 'Jumping Exercisers'),
    ('swings', 'Swings'),
    ('walkers', 'Walkers'),

    # Feeding
    ('baby_food_processor', 'Baby Food Processor'),
    ('bibs', 'Bibs'),
    ('booster_high_chairs', 'Booster/High Chairs'),
    ('bottles', 'Bottles'),
    ('dishes_utensils', 'Dishes & Utensils'),
    ('nursing_pillows', 'Nursing Pillows'),
    ('pacifiers', 'Pacifiers'),

    # Safety & Health
    ('baby_house_car_proofing', 'Baby House & Car Proofing'),
    ('baby_monitors', 'Baby Monitors'),
    ('baby_thermometers', 'Baby Thermometers'),
    ('locks_latches', 'Locks & Latches'),

    # Bath & Diapers
    ('bath_tubs', 'Bath Tubs'),
    ('diaper_bins', 'Diaper Bins'),
    ('diapers_wipes', 'Diapers & Wipes'),
    ('lotions_powders_shampoos', 'Lotions, Powders & Shampoos'),
    ('potties', 'Potties'),

    # Toys
    ('educational_toys', 'Educational Toys'),
    ('soft_toys', 'Soft Toys'),
    ('activity_centers', 'Activity Centers'),

    ('other', 'Other'),
]


    # NEW: Subcategory field (blank for form until selected via JS)
    subcategory = models.CharField(
    max_length=50,
    choices=SUBCATEGORY_CHOICES,
    blank=True,
    null=True
)


    condition = models.CharField(
        max_length=20, 
        choices=CONDITION_CHOICES, 
        blank=True, null=True
    )

    age = models.CharField(
        max_length=20, 
        choices=AGE_CHOICES, 
        blank=True, null=True
    )

    usage = models.CharField(
        max_length=20, 
        choices=USAGE_CHOICES, 
        blank=True, null=True
    )

    title = models.CharField(max_length=150, verbose_name="Listing Title")
    description = models.TextField(blank=True, null=True)

    listing_type = models.CharField(
        max_length=10, 
        choices=LISTING_TYPE_CHOICES, 
        blank=True, null=True
    )

    price = models.DecimalField(
        max_digits=12, decimal_places=2, 
        blank=True, null=True, 
        verbose_name="Price (OMR)"
    )

    # Location
    city = models.ForeignKey("Cities", on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # System fields
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now)

    # Media
    images = models.ManyToManyField("BabyItemsImage", blank=True, related_name="listings")
    videos = models.ManyToManyField("BabyItemsVideo", blank=True, related_name="listings")

    def __str__(self):
        return f"{self.title} ({self.get_main_category_display()}) - {self.price or 'No Price'}"


class BabyItemsImage(models.Model):
    image = models.ImageField(upload_to="baby_items/images/")
    
    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class BabyItemsVideo(models.Model):
    video = models.FileField(upload_to="baby_items/videos/")

class ToysListing(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("soldout", "Soldout"),
    ]

    LISTING_TYPE_CHOICES = [
        ("sale", "Sale"),
        ("wanted", "Wanted"),
    ]

    CONDITION_CHOICES = [
        ("new", "New"),
        ("used", "Used"),
        ("flawless", "Flawless"),
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("average", "Average"),
        ("poor", "Poor"),
    ]

    USAGE_CHOICES = [
        ("never_used", "Never Used"),
        ("used_once", "Used Once"),
        ("light_usage", "Light Usage"),
        ("normal", "Normal Usage"),
        ("heavy", "Heavy Usage"),
    ]

    AGE_CHOICES = [
        ("brand_new", "Brand New"),
        ("1_year", "1 Year"),
        ("2_years", "2 Years"),
        ("3_years", "3 Years"),
        ("4_years", "4 Years"),
        ("5_years", "5 Years"),
        ("6_10_years", "6-10 Years"),
        ("10_plus", "10+ Years"),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    # ------------------------
    # Main Category Choices
    # ------------------------
    CATEGORY_CHOICES = [
        ("electronic_remote", "Electronic & Remote Control Toys"),
        ("action_figures", "Action Figures & Toy Vehicles"),
        ("outdoor_toys", "Outdoor Toys & Structures"),
        ("hobbies", "Hobbies"),
        ("pretend_play", "Pretend Play & Preschool Toys"),
        ("educational", "Educational Toys"),
        ("dolls", "Dolls & Stuffed Animals"),
        ("games_puzzles", "Games & Puzzles"),
        ("classic_vintage", "Classic & Vintage Toys"),
        ("building", "Building Toys"),
    ]

    # ------------------------
    # Fields
    # ------------------------
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="toys_listings",
    )

    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)

    condition = models.CharField(
        max_length=20, choices=CONDITION_CHOICES, blank=True, null=True
    )

    usage = models.CharField(
        max_length=20, choices=USAGE_CHOICES, blank=True, null=True
    )

    age = models.CharField(
        max_length=20, choices=AGE_CHOICES, blank=True, null=True
    )

    title = models.CharField(max_length=150, verbose_name="Listing Title")
    description = models.TextField(blank=True, null=True)

    listing_type = models.CharField(
        max_length=10, choices=LISTING_TYPE_CHOICES, blank=True, null=True
    )

    price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        verbose_name="Price (OMR)",
    )

    # Location
    city = models.ForeignKey("Cities", on_delete=models.SET_NULL, null=True, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # System fields
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="pending"
    )
    created_at = models.DateTimeField(default=timezone.now)

    # Media
    images = models.ManyToManyField(
        "ToysImage", blank=True, related_name="listings"
    )
    videos = models.ManyToManyField(
        "ToysVideo", blank=True, related_name="listings"
    )

    def __str__(self):
        return f"{self.title} - {self.price or 'No Price'}"


class ToysImage(models.Model):
    image = models.ImageField(upload_to="toys/images/")
    
    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"

class ToysVideo(models.Model):
    video = models.FileField(upload_to="toys/videos/")




class LostFoundListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('found', 'Found'),
    ]

    LISTING_TYPE_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
    ]

    CATEGORY_CHOICES = [
        ('jewelry', 'Jewelry, Watches & Sunglasses'),
        ('keys', 'Keys'),
        ('mobile_phone', 'Mobile Phone'),
        ('passport', 'Passport & Documents'),
        ('pets', 'Pets'),
        ('wallet', 'Wallet'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='lost_found_listings'
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    title = models.CharField(max_length=200, verbose_name="Title")
    
    description = models.TextField(max_length=1000,verbose_name="Description", blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)

    city = models.ForeignKey(
        'Cities', on_delete=models.SET_NULL, null=True, blank=True,
        related_name='lost_found_listings'
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    images = models.ManyToManyField('LostFoundImage', blank=True, related_name='listings')
    videos = models.ManyToManyField('LostFoundVideo', blank=True, related_name='listings')

    def __str__(self):
        return f"{self.category} - {self.description[:30]}"

class LostFoundImage(models.Model):
    image = models.ImageField(upload_to='lostfound/images/')

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class LostFoundVideo(models.Model):
    video = models.FileField(upload_to='lostfound/videos/')

    def __str__(self):
        return f"Video {self.id}"



class CameraListing(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("soldout", "Soldout"),
    ]

    LISTING_TYPE_CHOICES = [
        ("sale", "For Sale"),
        ("wanted", "Wanted"),
    ]

    CONDITION_CHOICES = [
        ("flawless", "Flawless"),
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("average", "Average"),
        ("poor", "Poor"),
    ]

    USAGE_CHOICES = [
        ("never_used", "Never Used"),
        ("used_once", "Used Once"),
        ("light_usage", "Light Usage"),
        ("normal", "Normal Usage"),
        ("heavy", "Heavy Usage"),
    ]

    AGE_CHOICES = [
        ("brand_new", "Brand New"),
        ("1_year", "1 Year"),
        ("2_years", "2 Years"),
        ("3_years", "3 Years"),
        ("4_years", "4 Years"),
        ("5_years", "5 Years"),
        ("6_10_years", "6-10 Years"),
        ("10_plus", "10+ Years"),
    ]

    WARRANTY_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
        ("not_apply", "Do Not Apply"),
    ]

    MAIN_CATEGORY_CHOICES = [
        ("digital_cameras", "Digital Cameras"),
        ("lenses_filters_lighting", "Lenses, Filters & Lighting"),
        ("professional_equipment", "Professional Equipment"),
        ("camera_accessories", "Camera Accessories"),
        ("tripods_stands", "Tripods & Stands"),
        ("camcorders", "Camcorders"),
        ("film_cameras", "Film Cameras"),
        ("binoculars_telescopes", "Binoculars / Telescopes"),
        ("camcorder_accessories", "Camcorder Accessories"),
        ("camera_drones", "Camera Drones"),
    ]

    # Core fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="camera_listings"
    )
    main_category = models.CharField(max_length=50, choices=MAIN_CATEGORY_CHOICES)
    sub_category = models.CharField(max_length=100, blank=True, null=True)  # will hold sub-categories dynamically
    brand = models.CharField(max_length=100, blank=True, null=True)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True, null=True)
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True, null=True)
    warranty = models.CharField(max_length=10, choices=WARRANTY_CHOICES, blank=True, null=True)

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Location
    city = models.ForeignKey(
        "Cities",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="camera_listings"
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Status & timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now)

    # Media
    images = models.ManyToManyField("CameraImage", blank=True, related_name="listings")
    videos = models.ManyToManyField("CameraVideo", blank=True, related_name="listings")

    def __str__(self):
        return f"{self.title} ({self.get_main_category_display()})"


class CameraImage(models.Model):
    image = models.ImageField(upload_to="cameras/images/")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class CameraVideo(models.Model):
    video = models.FileField(upload_to="cameras/videos/")

    def __str__(self):
        return f"Video {self.id}"





class JewelryListing(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("soldout", "Soldout"),
    ]

    LISTING_TYPE_CHOICES = [
        ("sale", "For Sale"),
        ("wanted", "Wanted"),
    ]

    CONDITION_CHOICES = [
        ("flawless", "Flawless"),
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("average", "Average"),
        ("poor", "Poor"),
    ]

    USAGE_CHOICES = [
        ("never_used", "Never Used"),
        ("used_once", "Used Once"),
        ("light_usage", "Light Usage"),
        ("normal", "Normal Usage"),
        ("heavy", "Heavy Usage"),
    ]

    AGE_CHOICES = [
        ("brand_new", "Brand New"),
        ("1_year", "1 Year"),
        ("2_years", "2 Years"),
        ("3_years", "3 Years"),
        ("4_years", "4 Years"),
        ("5_years", "5 Years"),
        ("6_10_years", "6-10 Years"),
        ("10_plus", "10+ Years"),
    ]

    WARRANTY_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
        ("not_apply", "Do Not Apply"),
    ]

    MAIN_CATEGORY_CHOICES = [
        ("watches", "Watches"),
        ("womens_jewelry", "Women's Jewelry"),
        ("mens_jewelry", "Men's Jewelry"),
        ("loose_diamonds_gems", "Loose Diamonds & Gems"),
        ("other", "Other"),
    ]

    # Core fields
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="jewelry_listings"
    )
    main_category = models.CharField(max_length=50, choices=MAIN_CATEGORY_CHOICES)
    sub_category = models.CharField(max_length=100, blank=True, null=True)  # dynamic by main category
    

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True, null=True)
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True, null=True)
    warranty = models.CharField(max_length=10, choices=WARRANTY_CHOICES, blank=True, null=True)
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Location
    city = models.ForeignKey(
        "Cities",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="jewelry_listings"
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Status & timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now)

    # Media
    images = models.ManyToManyField("JewelryImage", blank=True, related_name="listings")
    videos = models.ManyToManyField("JewelryVideo", blank=True, related_name="listings")

    def __str__(self):
        return f"{self.title} ({self.get_main_category_display()})"


class JewelryImage(models.Model):
    image = models.ImageField(upload_to="jewelry/images/")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class JewelryVideo(models.Model):
    video = models.FileField(upload_to="jewelry/videos/")

    def __str__(self):
        return f"Video {self.id}"


class HomeApplianceListing(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("soldout", "Soldout"),
    ]

    LISTING_TYPE_CHOICES = [
        ("sale", "For Sale"),
        ("wanted", "Wanted"),
    ]

    CONDITION_CHOICES = [
        ("flawless", "Flawless"),
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("average", "Average"),
        ("poor", "Poor"),
        ("used", "Used"),
    ]

    USAGE_CHOICES = [
        ("never_used", "Never Used"),
        ("used_once", "Used Once"),
        ("light_usage", "Light Usage"),
        ("normal", "Normal Usage"),
        ("heavy", "Heavy Usage"),
    ]

    AGE_CHOICES = [
        ("brand_new", "Brand New"),
        ("1_year", "1 Year"),
        ("2_years", "2 Years"),
        ("3_years", "3 Years"),
        ("4_years", "4 Years"),
        ("5_years", "5 Years"),
        ("6_10_years", "6-10 Years"),
        ("10_plus", "10+ Years"),
    ]

    WARRANTY_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
        ("not_apply", "Do Not Apply"),
    ]

    MAIN_CATEGORY_CHOICES = [
        ("large_white_goods", "Large Appliances / White Goods"),
        ("small_kitchen", "Small Kitchen Appliances"),
        ("outdoor_appliances", "Outdoor Appliances"),
        ("small_bathroom", "Small Bathroom Appliances"),
        ("beauty_spa", "Beauty, Spa & Sauna Appliances"),
        ("irons_sewing", "Irons & Sewing Machines"),
        ("vacuums_floor", "Vacuums & Floor Care"),
        ("other", "Other"),
    ]

    SUBCATEGORY_CHOICES = {
        "large_white_goods": [
            ("air_conditioners", "Air Conditioners"),
            ("dishwashers", "Dishwashers"),
            ("gas_cylinders", "Gas Cylinders"),
            ("humidifiers_purifiers", "Humidifiers & Air Purifiers"),
            ("ovens_microwaves", "Ovens & Microwaves"),
            ("ranges_cooking", "Ranges & Cooking Appliances"),
            ("refrigerators_freezers", "Refrigerators & Freezers"),
            ("washers_dryers", "Washers & Dryers"),
            ("water_coolers", "Water Coolers"),
            ("other", "Other"),
        ],
        "small_kitchen": [
            ("blenders_juicers", "Blenders & Juicers"),
            ("bread_machines", "Bread Machines"),
            ("coffee_espresso", "Coffee & Espresso Appliances"),
            ("fryers", "Fryers"),
            ("hot_plates_grills", "Hot Plates & Grills"),
            ("kettles", "Kettles"),
            ("processors_mixers_grinders", "Processors, Mixers & Grinders"),
            ("slow_cookers_steamers", "Slow Cookers & Steamers"),
            ("toasters", "Toasters"),
            ("other", "Other"),
        ],
        "outdoor_appliances": [
            ("blowers", "Blowers"),
            ("charcoal_grills", "Charcoal Grills"),
            ("gas_grills", "Gas Grills"),
            ("ice_chests", "Ice Chests"),
            ("lawnmowers", "Lawnmowers"),
            ("power_tools", "Power Tools"),
            ("pressure_washers", "Pressure Washers"),
            ("other", "Other"),
        ],
        "small_bathroom": [
            ("hair_dryers", "Hair Dryers, Curlers & Straighteners"),
            ("massagers", "Massagers & Foot Spa"),
            ("scales", "Scales"),
            ("shavers_trimmers", "Shavers & Trimmers"),
            ("other", "Other"),
        ],
    }

    HEATING_TYPE_CHOICES = [
        ("cooling", "Cooling"),
        ("cooling_heating", "Cooling / Heating"),
        ("heating", "Heating"),
    ]
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="home_appliance_listings",
    )
    main_category = models.CharField(max_length=50, choices=MAIN_CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=100, blank=True, null=True)

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True, null=True)
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True, null=True)
    warranty = models.CharField(max_length=10, choices=WARRANTY_CHOICES, blank=True, null=True)

    brand = models.CharField(max_length=100, blank=True, null=True)
    # Air Conditioners
    cooling_power = models.CharField(max_length=50, blank=True, null=True)
    heating_type = models.CharField(max_length=50, choices=HEATING_TYPE_CHOICES, blank=True, null=True)
    # Dishwashers
    place_settings = models.IntegerField(blank=True, null=True)

    # Gas Cylinders
    gas_cylinder_weight = models.CharField(max_length=50, blank=True, null=True)

    # Humidifiers & Air Purifiers
    room_size = models.IntegerField(blank=True, null=True)  # in m²

    # Ovens & Microwaves
    oven_type = models.CharField(
        max_length=50,
        choices=[
            ("air_fryers", "Air Fryers"),
            ("microwaves_with_oven_grill", "Microwaves with Oven & Grill"),
            ("solo_microwaves", "Solo Microwaves"),
            ("solo_ovens", "Solo Ovens"),
            ("toaster_ovens", "Toaster Ovens"),
            ("toasters", "Toasters"),
        ],
        blank=True,
        null=True
    )

    # Ranges & Cooking Appliances
    range_model = models.CharField(max_length=100, blank=True, null=True)
    energy_input = models.CharField(
        max_length=20,
        choices=[("electric", "Electric"), ("electric_gas", "Electric & Gas"), ("gas", "Gas")],
        blank=True,
        null=True
    )

    # Refrigerators & Freezers
    number_of_doors = models.CharField(max_length=10, blank=True, null=True)

    # Washers & Dryers
    access_location = models.CharField(
        max_length=20,
        choices=[("front_load", "Front Load"), ("top_load", "Top Load")],
        blank=True,
        null=True
    )
    capacity = models.CharField(
        max_length=10,
        choices=[("7", "7"), ("8", "8"), ("9", "9"), ("10", "10"), ("11", "11"), ("12", "12"), ("12+", "12+")],
        blank=True,
        null=True
    )

    # Water Coolers
    cooling_capacity = models.IntegerField(blank=True, null=True)  # in L/hr

    # Small Kitchen Appliances
    power_watts = models.IntegerField(blank=True, null=True)
    capacity_liters = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    appliance_type = models.CharField(max_length=100, blank=True, null=True)  # Generic type field
    toaster_slots = models.IntegerField(blank=True, null=True)

    # Outdoor Appliances
    power_source = models.CharField(
        max_length=20,
        choices=[("electric", "Electric"), ("gas", "Gas"), ("battery", "Battery")],
        blank=True,
        null=True
    )
    cooking_area = models.IntegerField(blank=True, null=True)  # in sq. in.
    number_of_burners = models.IntegerField(blank=True, null=True)
    capacity_quarts = models.IntegerField(blank=True, null=True)
    lawnmower_type = models.CharField(
        max_length=20,
        choices=[
            ("push", "Push Mower"),
            ("self_propelled", "Self-Propelled"),
            ("riding", "Riding Mower"),
            ("electric", "Electric Mower")
        ],
        blank=True,
        null=True
    )
    psi = models.IntegerField(blank=True, null=True)  # Pressure for washers

    # Small Bathroom Appliances
    wattage = models.IntegerField(blank=True, null=True)
    max_weight = models.IntegerField(blank=True, null=True)  # for scales

    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)

    # Location
    city = models.ForeignKey(
        "Cities",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="home_appliance_listings",
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Status & timestamps
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(default=timezone.now)

    # Media
    images = models.ManyToManyField("HomeApplianceImage", blank=True, related_name="listings")
    videos = models.ManyToManyField("HomeApplianceVideo", blank=True, related_name="listings")

    # -----------------------
    # Subcategory Specific Fields
    # -----------------------

    # Air Conditioners
    ac_brand = models.CharField(max_length=100, blank=True, null=True)
    cooling_power = models.CharField(max_length=50, blank=True, null=True)

    # Dishwashers
    dishwasher_brand = models.CharField(max_length=100, blank=True, null=True)

    # Gas Cylinders
    gas_cylinder_brand = models.CharField(max_length=100, blank=True, null=True)
    gas_cylinder_weight = models.CharField(max_length=50, blank=True, null=True)

    # Humidifiers & Air Purifiers
    humidifier_brand = models.CharField(max_length=100, blank=True, null=True)

    # Ovens & Microwaves
    oven_brand = models.CharField(max_length=100, blank=True, null=True)
    oven_type = models.CharField(
        max_length=50,
        choices=[
            ("air_fryers", "Air Fryers"),
            ("microwaves_with_oven_grill", "Microwaves with Oven & Grill"),
            ("solo_microwaves", "Solo Microwaves"),
            ("solo_ovens", "Solo Ovens"),
            ("toaster_ovens", "Toaster Ovens"),
            ("toasters", "Toasters"),
        ],
        blank=True,
        null=True
    )

    # Ranges & Cooking Appliances
    range_model = models.CharField(max_length=100, blank=True, null=True)
    energy_input = models.CharField(
        max_length=20,
        choices=[("electric", "Electric"), ("electric_gas", "Electric & Gas"), ("gas", "Gas")],
        blank=True,
        null=True
    )

    # Refrigerators & Freezers
    fridge_brand = models.CharField(max_length=100, blank=True, null=True)
    number_of_doors = models.CharField(max_length=10, blank=True, null=True)

    # Washers & Dryers
    washer_brand = models.CharField(max_length=100, blank=True, null=True)
    access_location = models.CharField(
        max_length=20,
        choices=[("front_load", "Front Load"), ("top_load", "Top Load")],
        blank=True,
        null=True
    )
    capacity = models.CharField(
        max_length=10,
        choices=[("7", "7"), ("8", "8"), ("9", "9"), ("10", "10"), ("11", "11"), ("12", "12"), ("12+", "12+")],
        blank=True,
        null=True
    )

    # Water Coolers
    water_cooler_brand = models.CharField(max_length=100, blank=True, null=True)

    # Heating type (common field for some appliances)
    heating_type = models.CharField(max_length=50, choices=HEATING_TYPE_CHOICES, blank=True, null=True)

    def __str__(self):
        return f"{self.title} ({self.get_main_category_display()})"


class HomeApplianceImage(models.Model):
    image = models.ImageField(upload_to="home_appliances/images/")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class HomeApplianceVideo(models.Model):
    video = models.FileField(upload_to="home_appliances/videos/")

    def __str__(self):
        return f"Video {self.id}"




class ClothingAccessoriesListing(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("soldout", "Soldout"),
    ]

    LISTING_TYPE_CHOICES = [
        ("sale", "For Sale"),
        ("wanted", "Wanted"),
    ]

    CONDITION_CHOICES = [
        ("flawless", "Flawless"),
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("average", "Average"),
        ("poor", "Poor"),
        ("used", "Used"),
    ]

    USAGE_CHOICES = [
        ("never_used", "Never Used"),
        ("used_once", "Used Once"),
        ("light_usage", "Light Usage"),
        ("normal", "Normal Usage"),
        ("heavy", "Heavy Usage"),
    ]

    AGE_CHOICES = [
        ("brand_new", "Brand New"),
        ("1_year", "1 Year"),
        ("2_years", "2 Years"),
        ("3_years", "3 Years"),
        ("4_years", "4 Years"),
        ("5_years", "5 Years"),
        ("6_10_years", "6-10 Years"),
        ("10_plus", "10+ Years"),
    ]

    MAIN_CATEGORY_CHOICES = [
        ("shoes_footwear", "Shoes/Footwear"),
        ("clothing", "Clothing"),
        ("handbags_bags_wallets", "Handbags, Bags & Wallets"),
        ("mens_accessories", "Men's Accessories"),
        ("womens_accessories", "Women's Accessories"),
        ("luggage", "Luggage"),
        ("fragrances", "Fragrances"),
        ("wedding_apparel", "Wedding Apparel"),
        ("costumes_uniforms", "Costumes & Uniforms"),
        ("vintage_highend", "Vintage & Highend Clothing"),
        ("gifts_bouquet", "Gifts & Bouquet"),
        ("makeup_skincare", "Make up & Skin Care"),
        ("other", "Other"),
    ]

    SUBCATEGORY_CHOICES = {
        "shoes_footwear": [
            ("children_shoes", "Children's Shoes and Footwear"),
            ("mens_shoes", "Men's Shoes and Footwear"),
            ("unisex_shoes", "Unisex Shoes and Footwear"),
            ("womens_shoes", "Women's Shoes and Footwear"),
        ],
        "clothing": [
            ("children_clothing", "Children's Clothing"),
            ("mens_clothing", "Men's Clothing"),
            ("unisex_clothing", "Unisex Clothing"),
            ("womens_clothing", "Women's Clothing"),
        ],
        "handbags_bags_wallets": [
            ("athletic_bags", "Athletic Bags"),
            ("bags", "Bags"),
            ("briefcases", "Briefcases"),
            ("mens_wallets", "Men's Wallets"),
            ("womens_handbags", "Women's Handbags"),
            ("womens_wallets", "Women's Wallets"),
        ],
        "mens_accessories": [
            ("belts", "Belts"),
            ("gloves", "Gloves"),
            ("hats", "Hats"),
            ("sunglasses", "Sunglasses"),
            ("ties", "Ties"),
            ("other", "Other"),
        ],
        "womens_accessories": [
            ("belts", "Belts"),
            ("gloves", "Gloves"),
            ("hair_accessories", "Hair Accessories"),
            ("hats", "Hats"),
            ("sunglasses", "Sunglasses"),
            ("other", "Other"),
        ],
        "luggage": [
            ("backpacks", "Backpacks"),
            ("cases", "Cases"),
            ("duffel_bags", "Duffel Bags"),
            ("roller_luggage", "Roller Luggage"),
        ],
        "fragrances": [
            ("mens_fragrances", "Men's Fragrances"),
            ("unisex_fragrances", "Unisex Fragrances"),
            ("womens_fragrances", "Women's Fragrances"),
        ],
        "wedding_apparel": [
            ("children_wedding", "Children's Wedding Apparel"),
            ("mens_wedding", "Men's Wedding Apparel"),
            ("womens_wedding", "Women's Wedding Apparel"),
        ],
        "costumes_uniforms": [
            ("children_costumes", "Children's Costumes & Uniforms"),
            ("mens_costumes", "Men's Costumes & Uniforms"),
            ("unisex_costumes", "Unisex Costumes & Uniforms"),
            ("womens_costumes", "Women's Costumes & Uniforms"),
        ],
        "vintage_highend": [
            ("children_vintage", "Children's Vintage & Highend Clothing"),
            ("mens_vintage", "Men's Vintage & Highend Clothing"),
            ("unisex_vintage", "Unisex Vintage & Highend Clothing"),
            ("womens_vintage", "Women's Vintage & Highend Clothing"),
        ],
        "gifts_bouquet": [],
        "makeup_skincare": [],
        "other": [],
    }
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="clothing_accessories_listings",
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True, null=True)
    main_category = models.CharField(max_length=50, choices=MAIN_CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True, null=True)
    
    # Additional fields
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)

    # Location
    city = models.ForeignKey(
        "Cities",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clothing_accessories_listings",
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(default=timezone.now)

    # Media
    images = models.ManyToManyField("ClothingAccessoriesImage", blank=True, related_name="listings")
    videos = models.ManyToManyField("ClothingAccessoriesVideo", blank=True, related_name="listings")

    def __str__(self):
        return f"{self.title} ({self.get_main_category_display()})"


class ClothingAccessoriesImage(models.Model):
    image = models.ImageField(upload_to="clothing_accessories/images/")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class ClothingAccessoriesVideo(models.Model):
    video = models.FileField(upload_to="clothing_accessories/videos/")

    def __str__(self):
        return f"Video {self.id}"




class ElectronicsListing(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
        ("soldout", "Soldout"),
    ]

    LISTING_TYPE_CHOICES = [
        ("sale", "For Sale"),
        ("wanted", "Wanted"),
    ]

    CONDITION_CHOICES = [
        ("flawless", "Flawless"),
        ("excellent", "Excellent"),
        ("good", "Good"),
        ("average", "Average"),
        ("poor", "Poor"),
        ("used", "Used"),
    ]

    USAGE_CHOICES = [
        ("never_used", "Never Used"),
        ("used_once", "Used Once"),
        ("light_usage", "Light Usage"),
        ("normal", "Normal Usage"),
        ("heavy", "Heavy Usage"),
    ]

    AGE_CHOICES = [
        ("brand_new", "Brand New"),
        ("1_year", "1 Year"),
        ("2_years", "2 Years"),
        ("3_years", "3 Years"),
        ("4_years", "4 Years"),
        ("5_years", "5 Years"),
        ("6_10_years", "6-10 Years"),
        ("10_plus", "10+ Years"),
    ]

    WARRANTY_CHOICES = [
        ("yes", "Yes"),
        ("no", "No"),
        ("not_apply", "Do Not Apply"),
    ]

    MAIN_CATEGORY_CHOICES = [
        ("home_audio", "Home Audio & Turntables"),
        ("televisions", "Televisions"),
        ("dvd_theater", "DVD & Home Theater"),
        ("electronic_accessories", "Electronic Accessories"),
        ("gadgets", "Gadgets"),
        ("car_electronics", "Car Electronics"),
        ("projectors", "Projectors"),
        ("mp3_audio", "Mp3 Players and Portable Audio"),
        ("satellite_cable", "Satellite & Cable TV"),
        ("health_electronics", "Health Electronics"),
        ("smart_home", "Smart Home"),
        ("wearable_tech", "Wearable Technology"),
        ("other", "Other"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="electronics_listings"
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    main_category = models.CharField(max_length=50, choices=MAIN_CATEGORY_CHOICES)
    subcategory = models.CharField(max_length=100, blank=True, null=True)
    brand = models.CharField(max_length=100, blank=True, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    # Television specific fields
    tv_model = models.CharField(max_length=100, blank=True, null=True)
    tv_resolution = models.CharField(max_length=50, blank=True, null=True)
    tv_screen_size = models.CharField(max_length=20, blank=True, null=True)
    tv_mount_type = models.CharField(max_length=50, blank=True, null=True)

    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, blank=True, null=True)
    age = models.CharField(max_length=20, choices=AGE_CHOICES, blank=True, null=True)
    usage = models.CharField(max_length=20, choices=USAGE_CHOICES, blank=True, null=True)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE_CHOICES)
    price = models.DecimalField(max_digits=12, decimal_places=2, blank=True, null=True)
    warranty = models.CharField(max_length=20, choices=WARRANTY_CHOICES, blank=True, null=True)
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    # Location fields
    city = models.ForeignKey(
        "Cities",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="electronics_listings"
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    created_at = models.DateTimeField(default=timezone.now)

    # Media uploads
    images = models.ManyToManyField("ElectronicsImage", blank=True, related_name="listings")
    videos = models.ManyToManyField("ElectronicsVideo", blank=True, related_name="listings")

    def __str__(self):
        return f"{self.title} ({self.get_main_category_display()})"


class ElectronicsImage(models.Model):
    image = models.ImageField(upload_to="electronics/images/")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class ElectronicsVideo(models.Model):
    video = models.FileField(upload_to="electronics/videos/")

    def __str__(self):
        return f"Video {self.id}"

# ----------------------------------------------------Services----------------------------------------------------------------------


class AutoServiceListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive')
    ]

    SERVICE_TYPE_CHOICES = [
        ('ac_electrical', 'Air Condition & Electrical Repairing'),
        ('body_detailing', 'Body Detailing'),
        ('car_repair', 'Car Repair'),
        ('car_service', 'Car Service'),
        ('car_wash', 'Car Wash'),
        ('others', 'Others'),
        ('roadside_assistance', 'Roadside Assistance'),
        ('tyre_change', 'Tyre Change'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='auto_services'
    )

    title = models.CharField(max_length=200, verbose_name="Service Title")
    description = models.TextField(max_length=1000,verbose_name="Service Description")
    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPE_CHOICES,
        verbose_name="Type of Service"
    )
    created_at = models.DateTimeField(default=timezone.now)

    city = models.ForeignKey(
        'Cities',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='auto_services'
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    price = models.DecimalField(
    max_digits=10,
    decimal_places=2,
    null=True,
    blank=True,
    verbose_name="Service Price"
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )

    images = models.ManyToManyField(
        'AutoServiceImage',
        blank=True,
        related_name='auto_service',
        verbose_name="Images"
    )
    videos = models.ManyToManyField(
        'AutoServiceVideo',
        blank=True,
        related_name='auto_service',
        verbose_name="Videos"
    )

    def __str__(self):
        return f"{self.title} - {self.get_service_type_display()}"


class AutoServiceImage(models.Model):
    image = models.ImageField(upload_to='AutoServices/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class AutoServiceVideo(models.Model):
    video = models.FileField(upload_to='AutoServices/videos/', verbose_name="Video")

    def __str__(self):
        return f"AutoService Video {self.id}"
    


class ConsultancyServiceListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('business', 'Business Consultancy Services'),
        ('legal', 'Legal Consultancy Services'),
        ('financial', 'Loans & Financial Services'),
        ('translation', 'Translation Services'),
        ('visa', 'Visa Consultancy Services'),
        ('others', 'Other Consultancy Services'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='consultancy_services'
    )

    title = models.CharField(max_length=200, verbose_name="Service Title")
    description = models.TextField(max_length=1000,verbose_name="Service Description")

    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPE_CHOICES,
        verbose_name="Type of Consultancy Service"
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Service Price (OMR)"
    )

    created_at = models.DateTimeField(default=timezone.now)

    city = models.ForeignKey(
        'Cities',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='consultancy_services'
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )

    images = models.ManyToManyField(
        'ConsultancyServiceImage',
        blank=True,
        related_name='consultancy_service',
        verbose_name="Images"
    )

    videos = models.ManyToManyField(
        'ConsultancyServiceVideo',
        blank=True,
        related_name='consultancy_service',
        verbose_name="Videos"
    )

    def __str__(self):
        return f"{self.title} - {self.get_service_type_display()}"


class ConsultancyServiceImage(models.Model):
    image = models.ImageField(upload_to='ConsultancyServices/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class ConsultancyServiceVideo(models.Model):
    video = models.FileField(upload_to='ConsultancyServices/videos/', verbose_name="Video")

    def __str__(self):
        return f"Consultancy Service Video {self.id}"
    



class DomesticServiceListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('childcare', 'Childcare & Nannies'),
        ('cooks', 'Cooks'),
        ('gardeners', 'Gardeners & Outdoor Services'),
        ('maids', 'Maids'),
        ('pool', 'Pool Maintenance'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='domestic_services'
    )

    title = models.CharField(max_length=200, verbose_name="Service Title")
    description = models.TextField(max_length=1000,verbose_name="Service Description")

    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPE_CHOICES,
        verbose_name="Type of Domestic Service"
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Service Price (OMR)"
    )

    created_at = models.DateTimeField(default=timezone.now)

    city = models.ForeignKey(
        'Cities',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='domestic_services'
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )

    images = models.ManyToManyField(
        'DomesticServiceImage',
        blank=True,
        related_name='domestic_service',
        verbose_name="Images"
    )

    videos = models.ManyToManyField(
        'DomesticServiceVideo',
        blank=True,
        related_name='domestic_service',
        verbose_name="Videos"
    )

    def __str__(self):
        return f"{self.title} - {self.get_service_type_display()}"


class DomesticServiceImage(models.Model):
    image = models.ImageField(upload_to='DomesticServices/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class DomesticServiceVideo(models.Model):
    video = models.FileField(upload_to='DomesticServices/videos/', verbose_name="Video")

    def __str__(self):
        return f"Domestic Service Video {self.id}"


class EventEntertainmentServiceListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('caterers', 'Caterers'),
        ('party_rentals', 'Party Rentals & Supplies'),
        ('photography', 'Photography & Videography'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='event_services'
    )

    title = models.CharField(max_length=200, verbose_name="Service Title")
    description = models.TextField(max_length=1000,verbose_name="Service Description")

    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPE_CHOICES,
        verbose_name="Type of Event & Entertainment Service"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Service Price (OMR)"
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )

    created_at = models.DateTimeField(default=timezone.now)

    city = models.ForeignKey(
        'Cities',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='event_services'
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )

    images = models.ManyToManyField(
        'EventEntertainmentServiceImage',
        blank=True,
        related_name='event_service',
        verbose_name="Images"
    )

    videos = models.ManyToManyField(
        'EventEntertainmentServiceVideo',
        blank=True,
        related_name='event_service',
        verbose_name="Videos"
    )

    def __str__(self):
        return f"{self.title} - {self.get_service_type_display()}"


class EventEntertainmentServiceImage(models.Model):
    image = models.ImageField(upload_to='EventEntertainmentServices/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class EventEntertainmentServiceVideo(models.Model):
    video = models.FileField(upload_to='EventEntertainmentServices/videos/', verbose_name="Video")

    def __str__(self):
        return f"Event/Entertainment Service Video {self.id}"


class HealthWellbeingServiceListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('beauty_spa', 'Beauty & Spa Services'),
        ('counsellors', 'Counsellors & Therapists'),
        ('medical', 'Medical Services'),
        ('personal_trainers', 'Personal Trainers'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='health_services'
    )

    title = models.CharField(max_length=200, verbose_name="Service Title")
    description = models.TextField(max_length=1000,verbose_name="Service Description")

    service_type = models.CharField(
        max_length=50,
        choices=SERVICE_TYPE_CHOICES,
        verbose_name="Type of Health & Wellbeing Service"
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Service Price (OMR)"
    )

    created_at = models.DateTimeField(default=timezone.now)

    city = models.ForeignKey(
        'Cities',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='health_services'
    )
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Approval Status"
    )

    images = models.ManyToManyField(
        'HealthWellbeingServiceImage',
        blank=True,
        related_name='health_service',
        verbose_name="Images"
    )

    videos = models.ManyToManyField(
        'HealthWellbeingServiceVideo',
        blank=True,
        related_name='health_service',
        verbose_name="Videos"
    )

    def __str__(self):
        return f"{self.title} - {self.get_service_type_display()}"


class HealthWellbeingServiceImage(models.Model):
    image = models.ImageField(upload_to='HealthWellbeingServices/images/', verbose_name="Image")

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class HealthWellbeingServiceVideo(models.Model):
    video = models.FileField(upload_to='HealthWellbeingServices/videos/', verbose_name="Video")

    def __str__(self):
        return f"Health & Wellbeing Service Video {self.id}"
    
class HomeMaintenanceServiceListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('ac', 'AC Maintenance & Repair'),
        ('alarm', 'Alarm & Security'),
        ('carpenters', 'Carpenters'),
        ('electricians', 'Electricians'),
        ('general', 'General Maintenance'),
        ('handyman', 'Handyman'),
        ('interior', 'Interior Design & Architects'),
        ('painters', 'Painters'),
        ('pest_control', 'Pest Control'),
        ('plumbers', 'Plumbers'),
        ('renovations', 'Renovations & General Contracting'),
        ('smart_home', 'Smart Home Services'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='home_maintenance_services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='home_maintenance_services')
    latitude = models.FloatField(null=True, blank=True)
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    images = models.ManyToManyField('HomeMaintenanceServiceImage', blank=True, related_name='home_maintenance_service')
    videos = models.ManyToManyField('HomeMaintenanceServiceVideo', blank=True, related_name='home_maintenance_service')

    def __str__(self):
        return f"{self.title} - {self.get_service_type_display()}"


class HomeMaintenanceServiceImage(models.Model):
    image = models.ImageField(upload_to='HomeMaintenance/images/')

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class HomeMaintenanceServiceVideo(models.Model):
    video = models.FileField(upload_to='HomeMaintenance/videos/')

    def __str__(self):
        return f"Home Maintenance Video {self.id}"


class MoversServiceListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('deep_cleaning', 'Deep Cleaning & Disinfection Services'),
        ('movers_packers', 'Movers & Packers'),
        ('storage', 'Storage Services'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='movers_services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='movers_services')
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    images = models.ManyToManyField('MoversServiceImage', blank=True, related_name='movers_service')
    videos = models.ManyToManyField('MoversServiceVideo', blank=True, related_name='movers_service')

    def __str__(self):
        return f"{self.title} - {self.get_service_type_display()}"


class MoversServiceImage(models.Model):
    image = models.ImageField(upload_to='Movers/images/')

    def __str__(self):
        return f"Movers Image {self.id}"


class MoversServiceVideo(models.Model):
    video = models.FileField(upload_to='Movers/videos/')

    def __str__(self):
        return f"Movers Video {self.id}"


class RestorationServiceListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('electronic', 'Electronic Appliances Repair'),
        ('fridge', 'Fridge Repair'),
        ('furniture', 'Furniture & Sofa Repair'),
        ('it', 'IT Repair'),
        ('jewelry', 'Jewelry & Watches Repairs'),
        ('washing_machine', 'Washing Machine Repair'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='restoration_services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='restoration_services')
    latitude = models.FloatField(null=True, blank=True)
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    images = models.ManyToManyField('RestorationServiceImage', blank=True, related_name='restoration_service')
    videos = models.ManyToManyField('RestorationServiceVideo', blank=True, related_name='restoration_service')

    def __str__(self):
        return f"{self.title} - {self.get_service_type_display()}"


class RestorationServiceImage(models.Model):
    image = models.ImageField(upload_to='Restoration/images/')

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class RestorationServiceVideo(models.Model):
    video = models.FileField(upload_to='Restoration/videos/')

    def __str__(self):
        return f"Restoration Video {self.id}"


class TutorsServiceListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('arts_crafts', 'Arts & Crafts'),
        ('dance', 'Dance'),
        ('fitness_sport', 'Fitness and Sport'),
        ('languages', 'Languages'),
        ('music', 'Music'),
        ('others', 'Others'),
        ('professional_training', 'Professional Training Courses'),
        ('subject_tutors', 'Subject Tutors'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tutors_services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='tutors_services')
    latitude = models.FloatField(null=True, blank=True)
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    images = models.ManyToManyField('TutorsServiceImage', blank=True, related_name='tutors_service')
    videos = models.ManyToManyField('TutorsServiceVideo', blank=True, related_name='tutors_service')

    def __str__(self):
        return f"{self.title} - {self.get_service_type_display()}"


class TutorsServiceImage(models.Model):
    image = models.ImageField(upload_to='Tutors/images/')

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class TutorsServiceVideo(models.Model):
    video = models.FileField(upload_to='Tutors/videos/')

    def __str__(self):
        return f"Tutors Video {self.id}"


class WebComputerServiceListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive'),
    ]

    SERVICE_TYPE_CHOICES = [
        ('graphic_web', 'Graphic & Web Designers'),
        ('it_services', 'IT Services'),
        ('media_video', 'Media & Video Editing'),
        ('website_app', 'Website & App Development'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='web_computer_services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='web_computer_services')
    latitude = models.FloatField(null=True, blank=True)
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    created_at = models.DateTimeField(default=timezone.now)
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    images = models.ManyToManyField('WebComputerServiceImage', blank=True, related_name='web_computer_service')
    videos = models.ManyToManyField('WebComputerServiceVideo', blank=True, related_name='web_computer_service')

    def __str__(self):
        return f"{self.title} - {self.get_service_type_display()}"


class WebComputerServiceImage(models.Model):
    image = models.ImageField(upload_to='WebComputer/images/')

    def __str__(self):
        return f"WebComputer Image {self.id}"


class WebComputerServiceVideo(models.Model):
    video = models.FileField(upload_to='WebComputer/videos/')

    def __str__(self):
        return f"WebComputer Video {self.id}"

class FreelancersServiceListing(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive'),
    ]
    
    SERVICE_TYPE_CHOICES = [
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('hybrid', 'Hybrid'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='freelancers_services')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default='remote')
    city = models.ForeignKey('Cities', on_delete=models.SET_NULL, null=True, blank=True, related_name='freelancers_services')
    latitude = models.FloatField(null=True, blank=True)
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    images = models.ManyToManyField('FreelancersServiceImage', blank=True, related_name='freelancers_service')
    videos = models.ManyToManyField('FreelancersServiceVideo', blank=True, related_name='freelancers_service')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"


class FreelancersServiceImage(models.Model):
    image = models.ImageField(upload_to='Freelancers/images/')

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class FreelancersServiceVideo(models.Model):
    video = models.FileField(upload_to='Freelancers/videos/')

    def __str__(self):
        return f"Freelancers Video {self.id}"


class OtherServiceListing(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('laundry_services', 'Laundry & Dry Cleaning Services'),
        ('tailoring', 'Tailoring & Alterations'),
        ('event_planning', 'Event Planning & Coordination'),
        ('printing_services', 'Printing & Publishing Services'),
        ('logistics', 'Logistics & Delivery Services'),
        ('marketing', 'Marketing & Advertising Services'),
        ('carpet_cleaning', 'Carpet & Upholstery Cleaning'),
        ('elderly_care', 'Elderly Care Services'),
        ('travel_services', 'Travel & Tourism Services'),
        ('insurance_services', 'Insurance Services'),
        ('real_estate_services', 'Real Estate Services'),
        ('waste_management', 'Waste Management & Recycling'),
        ('solar_installation', 'Solar Panel Installation'),
        ('generator_services', 'Generator Services & Maintenance'),
        ('signage_services', 'Signage Services'),
        ('security_services', 'Security Guard Services'),
        ('artisan_crafts', 'Artisan & Craft Services'),
        ('equipment_rental', 'Equipment Rental Services'),
        ('landscaping', 'Landscaping Services'),
        ('language_services', 'Language Interpretation Services'),
        ('other', 'Other Specialized Services'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('inactive', 'Inactive'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='other_services'
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    city = models.ForeignKey(
        'Cities',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='other_services'
    )
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default='other')
    latitude = models.FloatField(null=True, blank=True)
    POSTING_METHOD_CHOICES = [
        ('normal', 'Normal Post'),
        ('boosted', 'Boosted Post'),
        # ('exclusive', 'Exclusive Request'),
    ]
    
    posting_method = models.CharField(
        max_length=20,
        choices=POSTING_METHOD_CHOICES,
        default='normal',
        verbose_name="Posting Method"
    )
    longitude = models.FloatField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )
    images = models.ManyToManyField(
        'OtherServiceImage',
        blank=True,
        related_name='other_service'
    )
    videos = models.ManyToManyField(
        'OtherServiceVideo',
        blank=True,
        related_name='other_service'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"
    
class OtherServiceImage(models.Model):
    image = models.ImageField(upload_to='other_services/images/')

    # Desired dimensions for the main image
    IMAGE_WIDTH = 800
    IMAGE_HEIGHT = 600

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save the original image first

        if self.image:
            image_path = self.image.path
            try:
                # Open the original image
                img = Image.open(image_path).convert("RGB")
                
                # Path to your logo file
                logo_path = os.path.join(settings.BASE_DIR, 'static/assets/images/ZoqoWhite-01.png')
                
                # Open and resize logo proportionally based on image size
                logo = Image.open(logo_path).convert("RGBA")
                
                # Calculate logo size as percentage of image width (e.g., 10-15% of image width)
                # This ensures logo scales with image resolution
                logo_width = int(img.width * 0.12)  # 12% of image width
                logo_height = int(logo_width * (75/300))  # Maintain aspect ratio (75:300)
                
                # Ensure minimum and maximum logo sizes
                logo_width = max(60, min(logo_width, 300))
                logo_height = max(15, min(logo_height, 75))
                
                logo = ImageOps.fit(logo, (logo_width, logo_height), method=Image.Resampling.LANCZOS)
                
                # Calculate position with proportional padding (5% of image size)
                padding_x = int(img.width * 0.03)  # 3% of image width
                padding_y = int(img.height * 0.03)  # 3% of image height
                
                position = (
                    img.width - logo.width - padding_x,
                    img.height - logo.height - padding_y
                )
                
                # Create a transparent layer for the logo
                logo_layer = Image.new("RGBA", img.size, (0, 0, 0, 0))
                logo_layer.paste(logo, position, logo)  # Use logo as mask for transparency
                
                # Convert main image to RGBA for composition
                img_rgba = img.convert("RGBA")
                
                # Combine original and logo
                watermarked = Image.alpha_composite(img_rgba, logo_layer)
                
                # Save with maximum quality
                if image_path.lower().endswith('.png'):
                    watermarked.save(image_path, quality=100, optimize=True)
                else:
                    watermarked.convert("RGB").save(image_path, quality=95, subsampling=0)
                
            except Exception as e:
                print(f"Error applying watermark: {e}")
                # If watermark fails, keep the original image
                Image.open(image_path).convert("RGB").save(image_path)

    def __str__(self):
        return f"Image {self.id}"


class OtherServiceVideo(models.Model):
    video = models.FileField(upload_to='other_services/videos/')

    def __str__(self):
        return f"Other Service Video {self.id}"



# -------------------------------------------------------FAQ-------------------------------------------------------------

from django.db import models

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question


# -------------------------------------------------------Blog--------------------------------------------------------------
from django.db import models

class Blog(models.Model):
    class Category(models.TextChoices):
        MOTORS = 'motors', 'Motors'
        REAL_ESTATE = 'real_estate', 'Real Estate'
        OTHER = 'other', 'Other'
        JOB = 'job', 'Job'
        MOBILES_TABLETS = 'mobiles_tablets', 'Mobiles and Tablets'
        SERVICE = 'service', 'Service'

    image = models.ImageField(upload_to='blogs/')
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Blogs"

# --------------------------------------------------------Banner Slider-----------------------------------------------------

from django.db import models

class BannerCategory(models.TextChoices):
    HOME = 'home', 'Home'
    MOTORS = 'motors', 'Motors'
    REAL_ESTATE = 'real_estate', 'Real Estate'
    JOB = 'job', 'Jobs'
    OTHER_CLASSIFIED = 'other_classified', 'Other Classified'
    MOBILES = 'mobiles', 'Mobiles'
    SERVICES = 'services', 'Services'

class Banner(models.Model):
    category = models.CharField(
        max_length=20,
        choices=BannerCategory.choices,
        default=BannerCategory.HOME
    )
    image = models.ImageField(upload_to='banners/')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_category_display()} Banner {self.id}"
    
    class Meta:
        ordering = ['-created_at']


# --------------------------------------------------------Sub Admins ----------------------------------------------------------
# Add this to your models.py after the CustomUser model
# Updated SubAdminPermission with all the sections you want to keep

from django.db import models
from django.contrib.auth import get_user_model
import json

CustomUser = get_user_model()


class SubAdminPermission(models.Model):
    """Model to store permissions for sub-admins only - admins have full access by default"""
    
    SECTION_CHOICES = [
        # Location Management
        ('governates', 'Governates'),
        ('districts', 'Districts'),
        ('cities', 'Cities'),
        
        # Amenities
        ('amenities', 'Amenities (Main, Additional, Nearby)'),
        
        # Motors Options
        ('interior_options', 'Interior Options'),
        ('exterior_options', 'Exterior Options'),
        ('technology_options', 'Technology Options'),
        
        # Content Management
        ('faq', 'FAQ Management'),
        ('blog', 'Blog Management'),
        ('banner', 'Banner Management'),
        
        # Advertisement
        ('advertisement', 'Advertisement Management'),
        
        # ===== ADS APPROVAL - SPLIT INTO 5 CATEGORIES =====
        ('ads_approval_properties', 'Ads Approval - Properties (Land, Villa, Commercial, etc.)'),
        ('ads_approval_vehicles', 'Ads Approval - Vehicles (Cars, Motorcycles, Boats, etc.)'),
        ('ads_approval_electronics', 'Ads Approval - Electronics & Mobile (Phones, Tablets, Computers, etc.)'),
        ('ads_approval_classifieds', 'Ads Approval - Classifieds & Listings (Fashion, Toys, Books, etc.)'),
        ('ads_approval_services', 'Ads Approval - Services (Auto, Domestic, Tutoring, etc.)'),
        
        # Companies
        ('companies', 'Company Management'),
        ('company_approval', 'Company Approval'),
        
        # Jobs
        ('job_posts', 'Job Posts'),
        ('job_categories', 'Job Categories'),
        
        # Reported Ads
        ('reported_ads', 'Reported Ads'),
        
        # User Related
        ('users_view', 'View Users'),
        ('user_reports', 'User Reports'),
        ('user_activity', 'User Activity Log'),
    ]

    name = models.CharField(max_length=100, help_text="Permission name")
    section = models.CharField(max_length=50, choices=SECTION_CHOICES, unique=True)
    description = models.TextField(blank=True, null=True)
    
    # Permission flags
    can_view = models.BooleanField(default=True, help_text="Can view this section")
    can_edit = models.BooleanField(default=False, help_text="Can edit/update items")
    can_delete = models.BooleanField(default=False, help_text="Can delete items")
    can_approve = models.BooleanField(default=False, help_text="Can approve/reject items")
    can_create = models.BooleanField(default=False, help_text="Can create new items")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['section']
        verbose_name = "Sub-Admin Permission"
        verbose_name_plural = "Sub-Admin Permissions"

    def __str__(self):
        return self.get_section_display()


class SubAdmin(models.Model):
    """Model for sub-admin users"""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='subadmin_profile'
    )
    created_by = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_subadmins'
    )
    permissions = models.ManyToManyField(
        SubAdminPermission,
        blank=True,
        related_name='subadmins'
    )
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True, help_text="Admin notes about this sub-admin")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Sub-Admin"
        verbose_name_plural = "Sub-Admins"

    def __str__(self):
        return f"{self.user.username} - Sub-Admin"

    def has_permission(self, section, action='view'):
        """
        Check if sub-admin has permission for a specific section and action
        """
        if not self.is_active:
            return False
            
        perms = self.permissions.filter(section=section)
        if not perms.exists():
            return False
            
        perm = perms.first()
        
        if action == 'view':
            return perm.can_view
        elif action == 'edit':
            return perm.can_edit
        elif action == 'delete':
            return perm.can_delete
        elif action == 'approve':
            return perm.can_approve
        elif action == 'create':
            return perm.can_create
        return False

    def get_permission_sections(self):
        """Return list of sections this sub-admin has access to"""
        return list(self.permissions.values_list('section', flat=True))
    
    def get_approval_categories(self):
        """Return list of approval categories this sub-admin can manage"""
        approval_categories = []
        if self.has_permission('ads_approval_properties', 'view'):
            approval_categories.append('properties')
        if self.has_permission('ads_approval_vehicles', 'view'):
            approval_categories.append('vehicles')
        if self.has_permission('ads_approval_electronics', 'view'):
            approval_categories.append('electronics')
        if self.has_permission('ads_approval_classifieds', 'view'):
            approval_categories.append('classifieds')
        if self.has_permission('ads_approval_services', 'view'):
            approval_categories.append('services')
        return approval_categories

from django.db import models
from django.core.validators import RegexValidator

class Offers(models.Model):
    # Simple validator: exactly 8 digits only
    phone_validator = RegexValidator(
        regex=r'^\d{8}$',
        message="Phone number must be exactly 8 digits"
    )
    
    image = models.ImageField(upload_to='offers/')
    
    phone_number = models.CharField(
        max_length=8, 
        validators=[phone_validator],
        help_text="Enter 8-digit phone number (e.g., 91234567)"
    )
    whatsapp_number = models.CharField(
        max_length=8, 
        blank=True, 
        null=True,
        validators=[phone_validator],
        help_text="Enter 8-digit WhatsApp number (optional)"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Offer {self.id}"
    
    def get_formatted_phone(self):
        """Returns formatted phone number (e.g., 9123 4567)"""
        if self.phone_number and len(self.phone_number) == 8:
            return f"{self.phone_number[:4]} {self.phone_number[4:]}"
        return self.phone_number
    
    def get_formatted_whatsapp(self):
        """Returns formatted WhatsApp number (e.g., 9123 4567)"""
        if self.whatsapp_number and len(self.whatsapp_number) == 8:
            return f"{self.whatsapp_number[:4]} {self.whatsapp_number[4:]}"
        return self.whatsapp_number


# models.py

from django.db import models
from django.utils import timezone
import random

class PhoneOTP(models.Model):
    phone = models.CharField(max_length=15)
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return timezone.now() < self.created_at + timezone.timedelta(minutes=5)

    @staticmethod
    def generate():
        return str(random.randint(100000, 999999))



# models.py
from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField  # For CKEditor 4
# OR for CKEditor 5:
# from ckeditor_5.fields import CKEditor5Field

class PrivacyPolicy(models.Model):
    """Model to store privacy policy versions"""
    title = models.CharField(max_length=200, default="Privacy Policy")
    content = RichTextField()  # Changed from models.TextField()
    # If using CKEditor 5:
    # content = CKEditor5Field(config_name='default')
    version = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-effective_date']
        verbose_name_plural = "Privacy Policies"
    
    def __str__(self):
        return f"{self.title} v{self.version}"
    
    def save(self, *args, **kwargs):
        # Ensure only one active policy at a time
        if self.is_active:
            PrivacyPolicy.objects.filter(is_active=True).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)


from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField  # Add this import

class TermsConditions(models.Model):
    """Model to store Terms and Conditions versions"""
    title = models.CharField(max_length=200, default="Terms and Conditions")
    content = RichTextField()  # Changed from models.TextField()
    version = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-effective_date']
        verbose_name_plural = "Terms and Conditions"
    
    def __str__(self):
        return f"{self.title} v{self.version}"
    
    def save(self, *args, **kwargs):
        if self.is_active:
            TermsConditions.objects.filter(is_active=True).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)



from django.db import models

class BusinessCollaboration(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class AboutUs(models.Model):
    """Model to store About Us content"""
    title = models.CharField(max_length=200, default="About Us")
    content = RichTextField()
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-effective_date']
        verbose_name_plural = "About Us"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.is_active:
            AboutUs.objects.filter(is_active=True).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)


class RefundPolicy(models.Model):
    """Model to store Refund Policy content"""
    title = models.CharField(max_length=200, default="Refund Policy")
    content = RichTextField()
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-effective_date']
        verbose_name_plural = "Refund Policies"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.is_active:
            RefundPolicy.objects.filter(is_active=True).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)


class ContactUs(models.Model):
    """Model to store Contact Us information"""
    title = models.CharField(max_length=200, default="Contact Us")
    content = RichTextField()
    is_active = models.BooleanField(default=True)
    effective_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-effective_date']
        verbose_name_plural = "Contact Us"
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.is_active:
            ContactUs.objects.filter(is_active=True).exclude(id=self.id).update(is_active=False)
        super().save(*args, **kwargs)



# -----------------------------------------------------PAYMOB----------------------------------------------------------
# ============================================================
# CREDIT SYSTEM MODELS - Add to your existing models.py
# ============================================================

from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import Sum, F
from django.utils import timezone
from datetime import timedelta

class CreditPackage(models.Model):
    """
    Available credit packages for purchase
    """
    PACKAGE_TYPES = [
        ('listing', 'Listing Credits'),
        ('boost_individual', 'Individual Boost'),
        ('boost_bulk', 'Bulk Boost'),
        ('business', 'Business Package'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Package Name")
    package_type = models.CharField(max_length=20, choices=PACKAGE_TYPES, verbose_name="Package Type")
    
    # Listing credits
    listing_credits = models.IntegerField(default=0, verbose_name="Number of Listing Credits")
    
    # Boost credits (for individual)
    boost_days = models.IntegerField(default=0, verbose_name="Boost Duration (Days)")
    boost_posts_count = models.IntegerField(default=1, verbose_name="Number of Posts to Boost")
    
    # Bulk boost specific
    is_bulk = models.BooleanField(default=False, verbose_name="Is Bulk Package")
    
    # Pricing
    price_omr = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Price (OMR)")
    vat_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=5.00, verbose_name="VAT %")
    
    # Validity
    validity_days = models.IntegerField(default=45, verbose_name="Credit Validity (Days)")
    
    # Business package specific
    is_business = models.BooleanField(default=False, verbose_name="Is Business Package")
    business_duration_days = models.IntegerField(default=365, verbose_name="Business Package Duration (Days)")
    
    # Display
    is_active = models.BooleanField(default=True, verbose_name="Is Active")
    display_order = models.IntegerField(default=0, verbose_name="Display Order")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    features = models.JSONField(default=list, blank=True, verbose_name="Features List")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['display_order', 'price_omr']
        verbose_name = "Credit Package"
        verbose_name_plural = "Credit Packages"
    
    def __str__(self):
        return f"{self.name} - {self.price_omr} OMR"
    
    def get_price_with_vat(self):
        """Calculate price including VAT"""
        return self.price_omr * (1 + self.vat_percentage / 100)
    
    def get_vat_amount(self):
        """Calculate VAT amount only"""
        return self.price_omr * (self.vat_percentage / 100)


class UserCredits(models.Model):
    """
    Track user's available credits
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='credits'
    )
    
    # Free tier (Phase 1)
    free_listings_total = models.IntegerField(default=30, verbose_name="Total Free Listings Allowed")
    free_listings_used = models.IntegerField(default=0, verbose_name="Free Listings Used")
    free_listings_expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Free Tier Expiry")
    
    # Purchased listing credits
    purchased_listing_credits = models.IntegerField(default=0, verbose_name="Purchased Listing Credits Available")
    
    # Boost credits (in days)
    boost_days_available = models.IntegerField(default=0, verbose_name="Boost Days Available")
    
    # Business package
    is_business_user = models.BooleanField(default=False, verbose_name="Is Business Package User")
    business_expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Business Package Expiry")
    
    # Statistics
    total_listings_created = models.IntegerField(default=0, verbose_name="Total Listings Created")
    total_boosts_used = models.IntegerField(default=0, verbose_name="Total Boosts Used")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "User Credits"
        verbose_name_plural = "User Credits"
    
    def __str__(self):
        return f"{self.user.username} - {self.available_listing_credits} listing credits"
    
    @property
    def available_free_listings(self):
        """Calculate remaining free listings"""
        return max(0, self.free_listings_total - self.free_listings_used)
    
    @property
    def available_listing_credits(self):
        """Total available listing credits (free + purchased)"""
        return self.available_free_listings + self.purchased_listing_credits
    
    def can_post_listing(self, posting_method='normal'):
        """Check if user can post a new listing"""
        if posting_method == 'exclusive':
            # Exclusive requires paid credits (cannot use free)
            return self.purchased_listing_credits > 0
        else:
            # Normal or boosted can use free or paid
            return self.available_listing_credits > 0
    
    def use_listing_credit(self, posting_method='normal'):
        """
        Use one listing credit
        Returns: (success, message)
        """
        if posting_method == 'exclusive':
            if self.purchased_listing_credits > 0:
                self.purchased_listing_credits -= 1
                self.total_listings_created += 1
                self.save()
                return True, "Used 1 purchased listing credit"
            else:
                return False, "No purchased listing credits available. Please buy a package."
        else:
            # Use free credits first
            if self.available_free_listings > 0:
                self.free_listings_used += 1
                self.total_listings_created += 1
                self.save()
                return True, f"Used 1 free listing credit ({self.free_listings_used}/{self.free_listings_total})"
            elif self.purchased_listing_credits > 0:
                self.purchased_listing_credits -= 1
                self.total_listings_created += 1
                self.save()
                return True, "Used 1 purchased listing credit"
            else:
                return False, "No listing credits available. Please buy a package."
    
    def use_boost_credit(self, days):
        """
        Use boost credits
        Returns: (success, message)
        """
        if self.boost_days_available >= days:
            self.boost_days_available -= days
            self.total_boosts_used += 1
            self.save()
            return True, f"Used {days} boost days. Remaining: {self.boost_days_available}"
        else:
            return False, f"Insufficient boost credits. Need {days} days, have {self.boost_days_available}"
    
    def add_listing_credits(self, amount):
        """Add purchased listing credits"""
        self.purchased_listing_credits += amount
        self.save()
    
    def add_boost_days(self, days):
        """Add boost days"""
        self.boost_days_available += days
        self.save()


class CreditTransaction(models.Model):
    """
    Log all credit transactions
    """
    TRANSACTION_TYPES = [
        ('purchase', 'Purchase'),
        ('usage', 'Usage'),
        ('refund', 'Refund'),
        ('expiry', 'Expiry'),
        ('bonus', 'Bonus'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='credit_transactions'
    )
    
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    
    # Related package (if purchase)
    package = models.ForeignKey(CreditPackage, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Amounts
    listing_credits_change = models.IntegerField(default=0, help_text="Positive = added, Negative = used")
    boost_days_change = models.IntegerField(default=0, help_text="Positive = added, Negative = used")
    
    # For purchase tracking
    payment_amount = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Related listing/boost (if usage)
    listing_id = models.IntegerField(null=True, blank=True)
    listing_type = models.CharField(max_length=100, null=True, blank=True)
    boost_duration = models.IntegerField(null=True, blank=True)
    
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Credit Transaction"
        verbose_name_plural = "Credit Transactions"
    
    def __str__(self):
        return f"{self.user.username} - {self.transaction_type} - {self.created_at.strftime('%Y-%m-%d')}"


class ListingUsage(models.Model):
    """
    Track which listing used which credit
    """
    LISTING_STATUS = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('deleted', 'Deleted'),
        ('sold', 'Sold'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listing_usages'
    )
    
    # Reference to the listing
    listing_type = models.CharField(max_length=100, verbose_name="Model Name")
    listing_id = models.IntegerField(verbose_name="Listing ID")
    
    # Credit source
    credit_source = models.CharField(max_length=20, choices=[
        ('free', 'Free Tier'),
        ('purchased', 'Purchased Credit'),
    ])
    
    # Status
    status = models.CharField(max_length=20, choices=LISTING_STATUS, default='active')
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(verbose_name="Expiry Date (45 days from creation)")
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = "Listing Usage"
        verbose_name_plural = "Listing Usages"
        indexes = [
            models.Index(fields=['listing_type', 'listing_id']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['user', 'status']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.listing_type} #{self.listing_id} - {self.status}"
    
    def is_expired(self):
        """Check if listing credit has expired"""
        return timezone.now() > self.expires_at
    
    def can_reuse(self):
        """Check if credit can be reused (deleted and not expired)"""
        return self.status == 'deleted' and not self.is_expired()


class BoostUsage(models.Model):
    """
    Track which ad is boosted and for how long
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='boost_usages'
    )
    
    # Reference to the listing
    listing_type = models.CharField(max_length=100, verbose_name="Model Name")
    listing_id = models.IntegerField(verbose_name="Listing ID")
    
    # Boost details
    boost_days = models.IntegerField(verbose_name="Boost Duration (Days)")
    boost_days_used = models.IntegerField(default=0, verbose_name="Boost Days Used")
    
    # Dates
    started_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(verbose_name="Boost Expiry Date")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Boost Usage"
        verbose_name_plural = "Boost Usages"
        indexes = [
            models.Index(fields=['listing_type', 'listing_id']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - Boost {self.listing_type} #{self.listing_id} - {self.boost_days} days"
    
    @property
    def days_remaining(self):
        """Calculate remaining boost days"""
        if not self.is_active:
            return 0
        remaining = max(0, (self.expires_at - timezone.now()).days)
        return remaining
    
    def is_boost_active(self):
        """Check if boost is still active"""
        return self.is_active and timezone.now() < self.expires_at
    
    def update_boost_status(self):
        """
        Update boost status based on expiry.
        If expired, set is_active=False and revert the listing's posting_method to 'normal'.
        """
        if self.is_active and timezone.now() > self.expires_at:
            self.is_active = False
            self.save(update_fields=['is_active'])
            
            # Revert the associated listing's posting_method to 'normal'
            from django.apps import apps
            try:
                # Capitalize model name (e.g., 'automobile' -> 'Automobile')
                model_name = self.listing_type.title()
                model = apps.get_model('oman_app', model_name)
                listing = model.objects.get(id=self.listing_id)
                if hasattr(listing, 'posting_method') and listing.posting_method == 'boosted':
                    listing.posting_method = 'normal'
                    listing.save(update_fields=['posting_method'])
            except Exception as e:
                # In production, use a logger instead of print
                print(f"Error reverting posting_method for {self.listing_type} #{self.listing_id}: {e}")
        
        return self.is_active

class PaymentTransaction(models.Model):
    """
    Store Paymob payment records
    """
    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payment_transactions'
    )
    
    # Package info
    package = models.ForeignKey(CreditPackage, on_delete=models.SET_NULL, null=True)
    
    # Paymob data
    payment_id = models.CharField(max_length=255, unique=True, null=True, blank=True, verbose_name="Paymob Transaction ID")
    order_id = models.CharField(max_length=255, null=True, blank=True)
    payment_token = models.CharField(max_length=255, null=True, blank=True)
    
    # Amounts
    amount_omr = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Amount (OMR)")
    vat_amount = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Total Amount (incl. VAT)")
    
    # Status
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Webhook data
    webhook_response = models.JSONField(default=dict, blank=True, verbose_name="Paymob Webhook Data")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "Payment Transaction"
        verbose_name_plural = "Payment Transactions"
    
    def __str__(self):
        return f"{self.user.username} - {self.payment_id} - {self.status}"


# ============================================================
# HELPER FUNCTIONS FOR CREDIT SYSTEM
# ============================================================

from decimal import Decimal
from django.utils import timezone
from datetime import timedelta

def get_or_create_user_credits(user):
    """Get or create UserCredits for a user"""
    credits, created = UserCredits.objects.get_or_create(user=user)
    
    # Set free tier expiry if not set (45 days from registration)
    if created and not credits.free_listings_expires_at:
        from django.utils import timezone
        credits.free_listings_expires_at = timezone.now() + timedelta(days=45)
        credits.save()
    
    return credits


def add_credits_to_user(user, package):
    """
    Add credits to user after successful purchase
    """
    credits = get_or_create_user_credits(user)
    
    # Create transaction record
    transaction = CreditTransaction.objects.create(
        user=user,
        transaction_type='purchase',
        package=package,
        listing_credits_change=package.listing_credits,
        boost_days_change=package.boost_days * package.boost_posts_count if package.boost_days else 0,
        payment_amount=package.get_price_with_vat(),
        description=f"Purchased {package.name}"
    )
    
    if package.package_type == 'listing':
        # Add listing credits
        credits.purchased_listing_credits += package.listing_credits
        credits.save()
        
    elif package.package_type in ['boost_individual', 'boost_bulk']:
        # Add boost days (total days = days * number of posts)
        total_boost_days = package.boost_days * package.boost_posts_count
        credits.boost_days_available += total_boost_days
        credits.save()
        transaction.boost_days_change = total_boost_days
        transaction.save()
        
    elif package.package_type == 'business':
        # Activate business package
        credits.is_business_user = True
        credits.business_expires_at = timezone.now() + timedelta(days=package.business_duration_days)
        credits.save()
    
    return credits


def check_and_expire_free_listings():
    """
    Cron job function: Expire free listings after 45 days
    Run this daily via celery or cron
    """
    expired_users = UserCredits.objects.filter(
        free_listings_expires_at__lte=timezone.now(),
        free_listings_used__lt=models.F('free_listings_total')
    )
    
    count = 0
    for credits in expired_users:
        # Mark remaining free listings as expired
        remaining = credits.free_listings_total - credits.free_listings_used
        if remaining > 0:
            CreditTransaction.objects.create(
                user=credits.user,
                transaction_type='expiry',
                listing_credits_change=-remaining,
                description=f"{remaining} free listing credits expired after 45 days"
            )
            credits.free_listings_total = credits.free_listings_used
            credits.save()
            count += 1
    
    return count


def expire_listing_credit(listing_usage_id):
    """
    Mark a listing credit as expired
    """
    try:
        usage = ListingUsage.objects.get(id=listing_usage_id)
        if not usage.is_expired() and usage.status == 'active':
            usage.status = 'expired'
            usage.save()
            
            # If it was a free credit, reduce free total
            if usage.credit_source == 'free':
                credits = get_or_create_user_credits(usage.user)
                credits.free_listings_total = max(0, credits.free_listings_total - 1)
                credits.save()
            
            return True
    except ListingUsage.DoesNotExist:
        pass
    return False

class UserPaymentRequest(models.Model):
    """When user wants to pay 25 OMR but has no credits - User initiates payment"""
    
    PAYMENT_STATUS = [
        ('pending', 'Pending Payment'),
        ('paid', 'Paid - Credits Added'),
        ('failed', 'Payment Failed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PAYMENT_METHOD_CHOICES = [
        ('paymob', 'Pay Online (Card)'),
        ('bank_transfer', 'Bank Transfer'),
        ('cash', 'Cash'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='user_payment_requests'
    )
    
    package = models.ForeignKey(CreditPackage, on_delete=models.SET_NULL, null=True, blank=True)
    
    # Payment details
    amount_omr = models.DecimalField(max_digits=10, decimal_places=3, default=25.000)
    vat_amount = models.DecimalField(max_digits=10, decimal_places=3, default=1.250)
    total_amount = models.DecimalField(max_digits=10, decimal_places=3, default=26.250)
    
    # Payment method
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    
    # For Paymob online payments
    payment_id = models.CharField(max_length=255, null=True, blank=True)
    payment_token = models.CharField(max_length=255, null=True, blank=True)
    
    # User message
    user_note = models.TextField(blank=True, null=True)
    
    # Admin verification (for bank transfer/cash)
    admin_verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='verified_payments'
    )
    admin_verified_at = models.DateTimeField(null=True, blank=True)
    admin_notes = models.TextField(blank=True, null=True)
    
    # Proof upload (for bank transfer)
    payment_proof = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)
    
    # ========== ADD THIS FIELD ==========
    pending_ad_data = models.TextField(blank=True, null=True, help_text="Stores ad data for publishing after payment")
    # ====================================
    
    # Status
    status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "User Payment Request"
        verbose_name_plural = "User Payment Requests"
    
    def __str__(self):
        return f"{self.user.username} - {self.total_amount} OMR - {self.status}"

class FixedAmountPackage(models.Model):
    """Fixed amount package for EXCLUSIVE listing payments - 1 OMR = 1 Credit"""
    
    name = models.CharField(max_length=100, default="25 OMR Credit Package")
    amount_omr = models.DecimalField(max_digits=10, decimal_places=3, default=25.000)
    listing_credits = models.IntegerField(default=25)  # 25 OMR = 25 credits
    boost_days = models.IntegerField(default=0)  # No boost days
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.amount_omr} OMR = {self.listing_credits} Credits"
    
    def get_price_with_vat(self):
        return self.amount_omr * Decimal('1.05')
    
    def get_vat_amount(self):
        return self.amount_omr * Decimal('0.05')

class ListingComment(models.Model):
    """
    Admin comments on listings for user feedback
    """
    listing_type = models.CharField(max_length=50)  # 'land', 'villa', 'automobile', etc.
    listing_id = models.PositiveIntegerField()
    
    # The user who owns the listing
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='listing_comments'
    )
    
    # Admin who wrote the comment
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admin_comments'
    )
    
    comment = models.TextField()
    is_read = models.BooleanField(default=False)
    requires_action = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['listing_type', 'listing_id']),
            models.Index(fields=['user', 'is_read']),
        ]
    
    def __str__(self):
        admin_name = self.admin.username if self.admin else 'Admin'
        return f"Comment on {self.listing_type} #{self.listing_id} by {admin_name}"
    
    def get_listing_object(self):
        """Get the actual listing object"""
        from django.apps import apps
        try:
            model = apps.get_model('oman_app', self.listing_type.title())
            return model.objects.get(id=self.listing_id)
        except:
            return None