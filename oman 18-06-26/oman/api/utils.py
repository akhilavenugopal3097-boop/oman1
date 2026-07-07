# api/utils.py
from django.apps import apps
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from oman_app.models import BoostUsage

# ============================================
# COMPLETE CATEGORY MODEL MAPPING
# ============================================

CATEGORY_MODEL_MAP = {
    # Real Estate
    'land': 'Land',
    'villa': 'Villa',
    'commercial': 'Commercial',
    'farm': 'Farm',
    'apartment': 'Apartment',
    'factory': 'Factory',
    'complex': 'Complex',
    'clinic': 'Clinic',
    'hostel': 'Hostel',
    'office': 'Office',
    'shop': 'Shop',
    'cafe': 'Cafe',
    'staff': 'Staff',
    'warehouse': 'Warehouse',
    'townhouse': 'Townhouse',
    'fullfloors': 'Fullfloors',
    'showrooms': 'Showrooms',
    'wholebuilding': 'Wholebuilding',
    'supermarket': 'Supermarket',
    'foreign': 'Foreign',
    'shared': 'Shared',
    'suits': 'Suits',
    'chalet': 'Chalet',
    
    # Motors
    'automobile': 'Automobile',
    'motorcycle': 'Motorcycle',
    'scooter': 'Scooter',
    'quadbikes': 'Quadbikes',
    'helmetclothes': 'HelmetClothes',
    'heavyvehicle': 'HeavyVehicle',
    'boat': 'Boat',
    'autoaccessorypart': 'AutoAccessoryPart',
    'numberplate': 'NumberPlate',
    'junkcar': 'JunkCar',
    'tiresandcaps': 'TiresAndCaps',
    'drivingtraining': 'DrivingTraining',
    'carrepairmaintenance': 'CarRepairMaintenance',
    'sportscar': 'SportsCar',
    'part': 'Part',
    
    # Mobiles & Tablets
    'mobile': 'Mobile',
    'tablet': 'Tablet',
    'smartwatch': 'SmartWatch',
    'headset': 'Headset',
    'cover': 'Cover',
    'accessory': 'Accessory',
    'mobilesim': 'MobileSIM',
    'computer': 'Computer',
    'sound': 'Sound',
    
    # Classifieds & Goods
    'fashion': 'Fashion',
    'toys': 'Toys',
    'food': 'Food',
    'fitness': 'Fitness',
    'pet': 'Pet',
    'book': 'Book',
    'appliance': 'Appliance',
    'business': 'Business',
    'education': 'Education',
    'service': 'Service',
    
    # Listings
    'computerlisting': 'ComputerListing',
    'businessindustriallisting': 'BusinessIndustrialListing',
    'petlisting': 'PetListing',
    'sportslisting': 'SportsListing',
    'musicallisting': 'MusicalListing',
    'gaminglisting': 'GamingListing',
    'ticketvoucherlisting': 'TicketVoucherListing',
    'collectiblelisting': 'CollectibleListing',
    'bookslisting': 'BooksListing',
    'musiclisting': 'MusicListing',
    'dvdsmovieslisting': 'DVDsMoviesListing',
    'furniturehomegardenlisting': 'FurnitureHomeGardenListing',
    'babyitemslisting': 'BabyItemsListing',
    'toyslisting': 'ToysListing',
    'lostfoundlisting': 'LostFoundListing',
    'cameralisting': 'CameraListing',
    'jewelrylisting': 'JewelryListing',
    'homeappliancelisting': 'HomeApplianceListing',
    'clothingaccessorieslisting': 'ClothingAccessoriesListing',
    'electronicslisting': 'ElectronicsListing',
    
    # Services
    'autoservicelisting': 'AutoServiceListing',
    'consultancyservicelisting': 'ConsultancyServiceListing',
    'domesticservicelisting': 'DomesticServiceListing',
    'evententertainmentservicelisting': 'EventEntertainmentServiceListing',
    'healthwellbeingservicelisting': 'HealthWellbeingServiceListing',
    'homemaintenanceservicelisting': 'HomeMaintenanceServiceListing',
    'moversservicelisting': 'MoversServiceListing',
    'restorationservicelisting': 'RestorationServiceListing',
    'tutorsservicelisting': 'TutorsServiceListing',
    'webcomputerservicelisting': 'WebComputerServiceListing',
    'freelancersservicelisting': 'FreelancersServiceListing',
    'otherservicelisting': 'OtherServiceListing',
}

CATEGORY_DISPLAY = {
    'land': 'Land',
    'villa': 'Villa',
    'commercial': 'Commercial Property',
    'farm': 'Farm',
    'apartment': 'Apartment',
    'factory': 'Factory',
    'complex': 'Complex',
    'clinic': 'Clinic',
    'hostel': 'Hostel',
    'office': 'Office',
    'shop': 'Shop',
    'cafe': 'Cafe',
    'staff': 'Staff Accommodation',
    'warehouse': 'Warehouse',
    'townhouse': 'Townhouse',
    'fullfloors': 'Full Floors',
    'showrooms': 'Showrooms',
    'wholebuilding': 'Whole Building',
    'supermarket': 'Supermarket',
    'foreign': 'Foreign Property',
    'shared': 'Shared Rooms',
    'suits': 'Hotel Apartments',
    'chalet': 'Chalet',
    'automobile': 'Car',
    'motorcycle': 'Motorcycle',
    'scooter': 'Scooter',
    'quadbikes': 'Quad Bike',
    'helmetclothes': 'Helmet & Clothes',
    'heavyvehicle': 'Heavy Vehicle',
    'boat': 'Boat',
    'autoaccessorypart': 'Auto Accessory',
    'numberplate': 'Number Plate',
    'junkcar': 'Junk Car',
    'tiresandcaps': 'Tires & Caps',
    'drivingtraining': 'Driving Training',
    'carrepairmaintenance': 'Car Repair',
    'mobile': 'Mobile Phone',
    'tablet': 'Tablet',
    'smartwatch': 'Smart Watch',
    'headset': 'Headset',
    'cover': 'Cover',
    'accessory': 'Accessory',
    'mobilesim': 'Mobile SIM',
    'computer': 'Computer',
    'sound': 'Sound System',
    'fashion': 'Fashion',
    'toys': 'Toys',
    'food': 'Food',
    'fitness': 'Fitness',
    'pet': 'Pet',
    'book': 'Book',
    'appliance': 'Appliance',
    'business': 'Business Equipment',
    'education': 'Education',
    'service': 'Service',
    'computerlisting': 'Computer Listing',
    'businessindustriallisting': 'Business & Industrial',
    'petlisting': 'Pet Listing',
    'sportslisting': 'Sports',
    'musicallisting': 'Musical Instrument',
    'gaminglisting': 'Gaming',
    'ticketvoucherlisting': 'Ticket & Voucher',
    'collectiblelisting': 'Collectible',
    'bookslisting': 'Books',
    'musiclisting': 'Music',
    'dvdsmovieslisting': 'DVDs & Movies',
    'furniturehomegardenlisting': 'Furniture',
    'babyitemslisting': 'Baby Items',
    'toyslisting': 'Toys',
    'lostfoundlisting': 'Lost & Found',
    'cameralisting': 'Camera',
    'jewelrylisting': 'Jewelry',
    'homeappliancelisting': 'Home Appliance',
    'clothingaccessorieslisting': 'Clothing',
    'electronicslisting': 'Electronics',
    'autoservicelisting': 'Auto Service',
    'consultancyservicelisting': 'Consultancy',
    'domesticservicelisting': 'Domestic Service',
    'evententertainmentservicelisting': 'Event Service',
    'healthwellbeingservicelisting': 'Health Service',
    'homemaintenanceservicelisting': 'Home Maintenance',
    'moversservicelisting': 'Movers',
    'restorationservicelisting': 'Restoration',
    'tutorsservicelisting': 'Tutors',
    'webcomputerservicelisting': 'Web Service',
    'freelancersservicelisting': 'Freelancers',
    'otherservicelisting': 'Other Service',
}


def get_model_for_category(category):
    """Get model class for a given category key"""
    model_name = CATEGORY_MODEL_MAP.get(category.lower())
    if model_name:
        try:
            return apps.get_model('oman_app', model_name)
        except LookupError:
            return None
    return None


def get_category_display(category):
    """Get display name for a category"""
    return CATEGORY_DISPLAY.get(category.lower(), category.title())


def get_listing_title(item):
    """Get title from any listing item"""
    if hasattr(item, 'title') and item.title:
        return item.title
    elif hasattr(item, 'property_title') and item.property_title:
        return item.property_title
    elif hasattr(item, 'name') and item.name:
        return item.name
    elif hasattr(item, 'product_name') and item.product_name:
        return item.product_name
    elif hasattr(item, 'service_title') and item.service_title:
        return item.service_title
    elif hasattr(item, 'make') and hasattr(item, 'model'):
        return f"{item.make} {item.model}"
    elif hasattr(item, 'brand') and hasattr(item, 'model_number'):
        return f"{item.brand} {item.model_number}"
    return f"{item.__class__.__name__} #{item.id}"


def get_listing_price(item):
    """Get price from any listing item"""
    if hasattr(item, 'price') and item.price:
        return float(item.price)
    elif hasattr(item, 'rental_price') and item.rental_price:
        return float(item.rental_price)
    elif hasattr(item, 'price_range') and item.price_range:
        return float(item.price_range)
    return 0


def get_listing_image(item):
    """Get first image URL from any listing item"""
    if hasattr(item, 'images'):
        try:
            first_image = item.images.first()
            if first_image and hasattr(first_image, 'image'):
                return first_image.image.url
        except:
            pass
    
    if hasattr(item, 'image') and item.image:
        try:
            return item.image.url
        except:
            pass
    
    if hasattr(item, 'main_image') and item.main_image:
        try:
            return item.main_image.url
        except:
            pass
    
    return None


def get_listing_city(item):
    """Get city name from any listing item"""
    if hasattr(item, 'city') and item.city:
        city = item.city
        district = city.district if hasattr(city, 'district') else None
        governate = district.governate if district else None
        return {
            'id': city.id,
            'name': city.name,
            'district': district.name if district else None,
            'governate': governate.name if governate else None,
        }
    return None


def get_boosted_listings_all(limit=20):
    """Get boosted listings across all categories"""
    results = []
    
    for category_key in CATEGORY_MODEL_MAP.keys():
        model = get_model_for_category(category_key)
        if model:
            try:
                boost_ids = BoostUsage.objects.filter(
                    listing_type=category_key,
                    is_active=True,
                    expires_at__gt=timezone.now()
                ).values_list('listing_id', flat=True)
                
                if boost_ids:
                    items = model.objects.filter(
                        id__in=boost_ids,
                        status='approved'
                    ).order_by('-created_at')[:5]
                    
                    for item in items:
                        results.append({
                            'item': item,
                            'category': category_key,
                        })
            except:
                pass
    
    results.sort(key=lambda x: getattr(x['item'], 'created_at', timezone.now()), reverse=True)
    return results[:limit]


def get_favorite_product_data(favorite):
    """Get product data from a favorite object"""
    try:
        product = favorite.content_object
        if not product:
            return None
        
        model_name = product.__class__.__name__.lower()
        category_key = None
        
        for key, value in CATEGORY_MODEL_MAP.items():
            if value.lower() == model_name:
                category_key = key
                break
        
        if not category_key:
            category_key = model_name
        
        return {
            'id': product.id,
            'category': category_key,
            'category_display': get_category_display(category_key),
            'title': get_listing_title(product),
            'price': get_listing_price(product),
            'image': get_listing_image(product),
            'city': get_listing_city(product),
            'status': getattr(product, 'status', 'unknown'),
            'created_at': getattr(product, 'created_at', None),
            'favorite_id': favorite.id,
            'favorite_created_at': favorite.created_at,
        }
    except:
        return None