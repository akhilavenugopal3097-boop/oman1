from django import template
from ..models import *
import re

register = template.Library()

# Your existing filters...
@register.filter
def get_item(dictionary, key):
    """Get a value from a dictionary by key."""
    if hasattr(dictionary, 'get'):
        return dictionary.get(key, key)
    return key

@register.filter
def split(value, delimiter=","):
    """Split a string by delimiter."""
    if not value:
        return []
    return value.split(delimiter)

@register.filter
def replace(value, arg):
    """Replace parts of a string."""
    if not value or not arg:
        return value
    parts = arg.split(',')
    if len(parts) != 2:
        return value
    return value.replace(parts[0], parts[1])

@register.filter
def has_chat_with(user1, user2):
    """Check if two users have exchanged messages."""
    return ChatMessage.objects.filter(
        sender__in=[user1, user2],
        receiver__in=[user1, user2]
    ).exists()

# Format furnished value
@register.filter
def format_furnished(value):
    """Convert DB values like 'semi_furnished' to 'Semi Furnished'."""
    mapping = {
        'furnished': 'Furnished',
        'semi_furnished': 'Semi-Furnished',
        'unfurnished': 'Unfurnished',
    }
    return mapping.get(value, value.replace('_', ' ').title())

@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    request = context['request']
    params = request.GET.copy()

    for key, value in kwargs.items():
        if value is None or value == "":
            params.pop(key, None)
        else:
            params[key] = value

    return params.urlencode()

@register.filter
def remove_item(value, item_to_remove):
    """Remove item from comma-separated string or list"""
    if isinstance(value, str):
        items = value.split(',')
    else:
        items = list(value)
    
    items = [item.strip() for item in items if item.strip() != item_to_remove]
    return ','.join(items) if isinstance(value, str) else items

@register.filter
def contains_all(list_str, check_items):
    """Check if list contains all items from check_items."""
    items = list_str.split(',')
    check_items = check_items.split(',')
    return all(item in items for item in check_items)

@register.filter
def contains_city(regions_selected, city):
    region_city_mapping = {
        'muscat': ["Al Bustan", "Al Ghubrah", ...],  # all muscat cities
        'dhofar': ["Salalah", "Mirbat", ...],  # all dhofar cities
        # ... other regions
    }
    
    for region in regions_selected.split(','):
        if region and city in region_city_mapping.get(region, []):
            return True
    return False

@register.filter
def clean_city_name(city):
   
    if hasattr(city, 'name'):
        return city.name  
    return str(city)

@register.filter
def format_boat_type(value):
    return value.replace('_', ' ').title()

@register.filter
def format_body_type(value):
    return value.replace('_', ' ').title()

@register.filter
def format_tire_type(value):
    # Map of actual DB value to human-readable label
    tire_type_map = dict(TiresAndCaps.TIRE_TYPE_CHOICES)
    return tire_type_map.get(value, value)

@register.filter
def format_job_type(value):
    # Map of actual DB value to human-readable label
    job_type_map = dict(JobPost.JOB_CHOICES)
    return job_type_map.get(value, value)

@register.filter
def format_commitment(value):
    commitment_map = dict(JobSeeker.COMMITMENT_CHOICES)
    return commitment_map.get(value, value)

@register.filter
def format_expected_salary(value):
    expected_salary_map = dict(JobSeeker.EXPECTED_SALARY_CHOICES)
    return expected_salary_map.get(value, value)

@register.filter
def format_experience(value):
    # Map of actual DB value to human-readable label
    experience_map = dict(JobPost.EXPERIENCE_CHOICES)
    return experience_map.get(value, value)

@register.filter
def format_workexperience(value):
    # Map of actual DB value to human-readable label
    experience_map = dict(JobSeeker.WORK_EXPERIENCE_CHOICES)
    return experience_map.get(value, value)

@register.filter
def format_education_level(value):
    # Map of actual DB value to human-readable label
    education_level_map = dict(JobSeeker.EDUCATION_LEVEL_CHOICES)
    return education_level_map.get(value, value)

@register.filter
def format_qualifications(value):
    # Map of actual DB value to human-readable label
    qualifications_map = dict(JobPost.QUALIFICATION_CHOICES)
    return qualifications_map.get(value, value)

@register.filter
def format_working_days(value):
    # Map of actual DB value to human-readable label
    working_days_map = dict(JobPost.WORKING_DAYS_CHOICES)
    return working_days_map.get(value, value)


@register.filter
def format_job_category(value):
    try:
        category = JobCategory.objects.get(id=value)
        return category.name
    except JobCategory.DoesNotExist:
        return value


@register.filter
def format_working_hours(value):
    # Map of actual DB value to human-readable label
    working_hours_map = dict(JobPost.WORKING_HOUR_CHOICES)
    return working_hours_map.get(value, value)

@register.filter
def format_main_category(value, model_name=None):
    if model_name == 'autoaccessory':
        category_map = dict(AutoAccessoryPart.MAIN_CATEGORY_CHOICES)
    elif model_name == 'electronics':
        category_map = dict(ElectronicsListing.MAIN_CATEGORY_CHOICES)
    elif model_name == 'homeappliance':
        category_map = dict(HomeApplianceListing.MAIN_CATEGORY_CHOICES)
    elif model_name == 'clothing':
        category_map = dict(ClothingAccessoriesListing.MAIN_CATEGORY_CHOICES)
    elif model_name == 'jewelry':
        category_map = dict(JewelryListing.MAIN_CATEGORY_CHOICES)
    elif model_name == 'sports':
        category_map = dict(SportsListing.MAIN_CATEGORY_CHOICES)
    else:
        return value.replace('_', ' ').title()
    
    return category_map.get(value, value)


@register.filter
def format_main_type(value, model_name=None):
    if model_name == 'heavyvehicle':
        category_map = dict(HeavyVehicle.MAIN_TYPE_CHOICES)
    else:
        return value.replace('_', ' ').title()
    
    return category_map.get(value, value)

@register.filter
def format_category(value, model_name=None):
    if model_name == 'business':
        category_map = dict(BusinessIndustrialListing.CATEGORY_CHOICES)
    elif model_name == 'autoservice':
        category_map = dict(PetListing.CATEGORY_CHOICES)
    elif model_name == 'collectible':
        category_map = dict(CollectibleListing.CATEGORY_CHOICES)
    elif model_name == 'sports':
        category_map = dict(SportsListing.CATEGORY_CHOICES)
    elif model_name == 'computer':
        category_map = dict(ComputerListing.CATEGORY_CHOICES)
    elif model_name == 'repair':
        category_map = dict(CarRepairMaintenance.CATEGORY_CHOICES)
    elif model_name == 'pets':
        category_map = dict(PetListing.CATEGORY_CHOICES)
    elif model_name == 'musical':
        category_map = dict(MusicalListing.CATEGORY_CHOICES)
    elif model_name == 'gaming':
        category_map = dict(GamingListing.CATEGORY_CHOICES)
    elif model_name == 'lostfound':
        category_map = dict(LostFoundListing.CATEGORY_CHOICES)
    elif model_name == 'babyitem':
        category_map = dict(BabyItemsListing.CATEGORY_CHOICES)
    elif model_name == 'dvd':
        category_map = dict(DVDsMoviesListing.CATEGORY_CHOICES)
    elif model_name == 'toy':
        category_map = dict(ToysListing.CATEGORY_CHOICES)
    else:
        return value.replace('_', ' ').title()
    
    return category_map.get(value, value)


@register.filter
def format_listing_type(value, model_name=None):
    if model_name == 'business':
        listing_type_map = dict(BusinessIndustrialListing.LISTING_TYPE_CHOICES)
    elif model_name == 'electronics':
        listing_type_map = dict(ElectronicsListing.LISTING_TYPE_CHOICES)
    elif model_name == 'homeappliance':
        listing_type_map = dict(HomeApplianceListing.LISTING_TYPE_CHOICES)
    elif model_name == 'clothing':
        listing_type_map = dict(ClothingAccessoriesListing.LISTING_TYPE_CHOICES)
    elif model_name == 'camera':
        listing_type_map = dict(CameraListing.LISTING_TYPE_CHOICES)
    elif model_name == 'jewelry':
        listing_type_map = dict(JewelryListing.LISTING_TYPE_CHOICES)
    else:
        return value.replace('_', ' ').title()
    
    return listing_type_map.get(value, value)


@register.filter
def format_tv_mount_type(value):
        return value.replace('_', ' ').title()
    
@register.filter
def format_warranty(value, model_name=None):
    if model_name == 'electronics':
        category_map = dict(ElectronicsListing.WARRANTY_CHOICES)
    elif model_name == 'homeappliance':
        category_map = dict(HomeApplianceListing.WARRANTY_CHOICES)
    elif model_name == 'camera':
        category_map = dict(CameraListing.WARRANTY_CHOICES)
    elif model_name == 'jewelry':
        category_map = dict(JewelryListing.WARRANTY_CHOICES)
    else:
        return value.replace('_', ' ').title()
    
    return category_map.get(value, value)


@register.filter
def format_service_type(value, model_name=None):
    if model_name == 'autoservice':
        service_type_map = dict(AutoServiceListing.SERVICE_TYPE_CHOICES)
    elif model_name == 'business':
        service_type_map = dict(BusinessIndustrialListing.SERVICE_TYPE_CHOICES)
    elif model_name == 'consultancy':
        service_type_map = dict(ConsultancyServiceListing.SERVICE_TYPE_CHOICES)
    elif model_name == 'domestic':
        service_type_map = dict(DomesticServiceListing.SERVICE_TYPE_CHOICES)
    elif model_name == 'events':
        service_type_map = dict(EventEntertainmentServiceListing.SERVICE_TYPE_CHOICES)
    elif model_name == 'freelancer':
        service_type_map = dict(FreelancersServiceListing.SERVICE_TYPE_CHOICES)
    elif model_name == 'health':
        service_type_map = dict(HealthWellbeingServiceListing.SERVICE_TYPE_CHOICES)
    elif model_name == 'homemaintenance':
        service_type_map = dict(HomeMaintenanceServiceListing.SERVICE_TYPE_CHOICES)
    elif model_name == 'movers':
        service_type_map = dict(MoversServiceListing.SERVICE_TYPE_CHOICES)
    elif model_name == 'otherservices':
        service_type_map = dict(OtherServiceListing.SERVICE_TYPE_CHOICES)
    elif model_name == 'restoration':
        service_type_map = dict(RestorationServiceListing.SERVICE_TYPE_CHOICES)
    elif model_name == 'tutor':
        service_type_map = dict(TutorsServiceListing.SERVICE_TYPE_CHOICES)
    elif model_name == 'webservice':
        service_type_map = dict(WebComputerServiceListing.SERVICE_TYPE_CHOICES)
    else:
        return value.replace('_', ' ').title()
    
    return service_type_map.get(value, value)

@register.filter
def format_condition(value, model_name=None):
    if model_name == 'smartwatch':
        condition_map = dict(SmartWatch.CONDITION_CHOICES)
    elif model_name == 'headset':
        condition_map = dict(Headset.CONDITION_CHOICES)
    elif model_name == 'mobile':
        condition_map = dict(Mobile.CONDITION_CHOICES)
    elif model_name == 'accessory':
        condition_map = dict(Accessory.CONDITION_CHOICES)
    elif model_name == 'cover':
        condition_map = dict(Cover.CONDITION_CHOICES)
    elif model_name == 'tablet':
        condition_map = dict(Tablet.CONDITION_CHOICES)
    elif model_name == 'computer':
        condition_map = dict(ComputerListing.CONDITION_CHOICES)
    else:
        return value.replace('_', ' ').title()
    
    return condition_map.get(value, value)

@register.filter
def format_sub_category(value, model_name=None):
    """
    Format sub-category values based on the model name.
    """
    if model_name == 'autoaccessorypart':
        sub_category_map = dict(AutoAccessoryPart.SUB_CATEGORY_CHOICES)

    else:
        # fallback for unknown models
        return value.replace('_', ' ').title()
    
    # get the mapped value or fallback to formatted string
    return sub_category_map.get(value, value.replace('_', ' ').title())
@register.filter
def format_subcategory(value, arg=None):
    """
    Format subcategory value with optional model_name and category
    Usage: {{ value|format_subcategory:"model_name:category" }}
    or: {{ value|format_subcategory:"model_name" }}
    """
    if not arg:
        return value.replace('_', ' ').title()
    
    # Parse arguments
    args = arg.split(':')
    model_name = args[0]
    category = args[1] if len(args) > 1 else None
    
    if model_name == 'ticket':
        subcategory_map = dict(TicketVoucherListing.SUBCATEGORY_CHOICES)
    elif model_name == 'dvd':
        subcategory_map = dict(DVDsMoviesListing.SUBCATEGORY_CHOICES)
    elif model_name == 'collectible':
        subcategory_map = dict(CollectibleListing.SUBCATEGORY_CHOICES)
    elif model_name == 'gaming':
        if category == 'gaming_systems':
            subcategory_map = dict(GamingListing.GAMING_SYSTEM_SUBCATEGORY_CHOICES)
        elif category == 'video_games':
            subcategory_map = dict(GamingListing.VIDEO_GAME_SUBCATEGORY_CHOICES)
        else:
            subcategory_map = dict(GamingListing.ACCESSORY_SUBCATEGORY_CHOICES)
    else:
        return value.replace('_', ' ').title()
    
    return subcategory_map.get(value, value.replace('_', ' ').title())

@register.filter
def format_number_of_ticket(value, model_name=None):
    if model_name == 'ticket':
        ticket_map = dict(TicketVoucherListing.TICKET_NUMBER_CHOICES)
    else:
        return value.replace('_', ' ').title()
    
    return ticket_map.get(value, value)

@register.filter
def format_plate_type(value):
    """
    Custom display for PlateType values.
    - car → "Car Plate Numbers"
    - motorcycle → "Motorcycles Plate Numbers"
    """
    mapping = {
        "car": "Car Plate Numbers",
        "motorcycle": "Motorcycles Plate Numbers",
    }
    return mapping.get(value.lower(), value.title())



@register.filter
def time_ago(value):
    """Returns human-readable time difference like '2 hours ago', '3 days ago', '2 months ago'"""
    if not value:
        return ""
    
    now = timezone.now()
    diff = now - value
    
    if diff.days == 0:
        # Less than 24 hours - show hours only
        hours = diff.seconds // 3600
        if hours == 0:
            return "today"
        elif hours == 1:
            return "1 hour ago"
        else:
            return f"{hours} hours ago"
    elif diff.days < 30:
        # 1-29 days - show days
        if diff.days == 1:
            return "1 day ago"
        else:
            return f"{diff.days} days ago"
    else:
        # 30+ days - show months
        months = diff.days // 30
        if months == 1:
            return "1 month ago"
        else:
            return f"{months} months ago"
        
@register.filter
def remove_value(values, value_to_remove):
    """Remove a value from a comma-separated list."""
    if not values:
        return ""
    value_list = values.split(",")
    filtered = [v for v in value_list if v != value_to_remove]
    return ",".join(filtered) if filtered else None

@register.filter
def exclude_value(values, value):
    """
    Remove a single value from a comma-separated list (like 'a,b,c').
    """
    if not values:
        return ""
    value_list = values.split(",")
    filtered = [v for v in value_list if v != value]
    return ",".join(filtered) if filtered else None
@register.filter
def format_age(value, model_name=None):
    value = str(value).strip()
    
    if model_name == 'business':
        age_map = dict(BooksListing.AGE_CHOICES)
    elif model_name == 'electronics':
        age_map = dict(ElectronicsListing.AGE_CHOICES)
    elif model_name == 'music':
        age_map = dict(MusicListing.AGE_CHOICES)
    elif model_name == 'toy':
        age_map = dict(ToysListing.AGE_CHOICES)
    elif model_name == 'pets':
        age_map = dict(PetListing.AGE_CHOICES)
    elif model_name == 'furniture':
        age_map = dict(FurnitureHomeGardenListing.AGE_CHOICES)
    elif model_name == 'musical':
        age_map = dict(MusicalListing.AGE_CHOICES)
    elif model_name == 'jewelry':
        age_map = dict(JewelryListing.AGE_CHOICES)
    elif model_name == 'book':
        age_map = dict(BooksListing.AGE_CHOICES)
    elif model_name == 'camera':
        age_map = dict(CameraListing.AGE_CHOICES)
    elif model_name == 'dvd':
        age_map = dict(DVDsMoviesListing.AGE_CHOICES)
    elif model_name == 'clothing':
        age_map = dict(ClothingAccessoriesListing.AGE_CHOICES)
    elif model_name == 'collectible':
        age_map = dict(CollectibleListing.AGE_CHOICES)
    elif model_name == 'homeappliance':
        age_map = dict(HomeApplianceListing.AGE_CHOICES)
    elif model_name == 'gaming':
        age_map = dict(GamingListing.AGE_CHOICES)
    elif model_name == 'sports':
        age_map = dict(SportsListing.AGE_CHOICES)
    elif model_name == 'babyitem':
        age_map = dict(BabyItemsListing.AGE_CHOICES)
    else:
        return value.replace('_', ' ').title()
    
    try:
        return age_map.get(int(value), value)
    except ValueError:
        return age_map.get(value, value)

@register.filter
def format_usage(value, model_name=None):
    if model_name == 'business':
        usage_map = dict(BooksListing.USAGE_CHOICES)
    elif model_name == 'book':
        usage_map = dict(BooksListing.USAGE_CHOICES)
    elif model_name == 'electronics':
        usage_map = dict(ElectronicsListing.USAGE_CHOICES)
    elif model_name == 'music':
        usage_map = dict(MusicListing.USAGE_CHOICES)
    elif model_name == 'furniture':
        usage_map = dict(FurnitureHomeGardenListing.USAGE_CHOICES)
    elif model_name == 'clothing':
        usage_map = dict(ClothingAccessoriesListing.USAGE_CHOICES)
    elif model_name == 'homeappliance':
        usage_map = dict(ElectronicsListing.USAGE_CHOICES)
    elif model_name == 'camera':
        usage_map = dict(CameraListing.USAGE_CHOICES)
    elif model_name == 'dvd':
        usage_map = dict(DVDsMoviesListing.USAGE_CHOICES)
    elif model_name == 'gaming':
        usage_map = dict(GamingListing.USAGE_CHOICES)
    elif model_name == 'babyitem':
        usage_map = dict(BabyItemsListing.USAGE_CHOICES)
    elif model_name == 'toy':
        usage_map = dict(ToysListing.USAGE_CHOICES)
    elif model_name == 'collectible':
        usage_map = dict(CollectibleListing.USAGE_CHOICES)
    else:
        # Fallback: prettify the value if no mapping found
        return value.replace('_', ' ').title()
    
    return usage_map.get(value, value)

@register.filter
def format_package(value, model_name=None):
    if model_name == 'gaming':
        package_map = dict(GamingListing.PACKAGE_CHOICES)

    else:
        return value.replace('_', ' ').title()
    
    return package_map.get(value, value)

@register.filter
def format_operating_system(value):
    return value.replace('_', ' ').title()
    


@register.filter
def format_regional_specs(value, model_name=None):
    if model_name == 'car':
        usage_map = dict(Automobile.REGIONAL_SPEC_CHOICES)
    else:
        # Fallback: prettify the value if no mapping found
        return value.replace('_', ' ').title()
    
    return usage_map.get(value, value)
@register.filter
def format_types(value):
    types_map = dict(Quadbikes.PRODUCT_CHOICES)
    return types_map.get(value, value)

@register.filter
def format_types(value):
    types_map = dict(Quadbikes.PRODUCT_CHOICES)
    return types_map.get(value, value)

@register.filter
def format_accompaniments(value):
    accompaniments_map = dict(Mobile.ACCOMPANIMENT_CHOICES)
    return accompaniments_map.get(value, value)

@register.filter
def format_storage_capacity(value):
 
    if not value:
        return value
    return re.sub(r'(\d+)([A-Za-z]+)', r'\1 \2', value)

@register.filter
def format_kilometers(value):
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value

    if value < 1000:
        return f"{value} km"
    elif value < 1000000:
        # Show in 'k' format for 1000 and above (e.g., 1k km, 1.2k km, 15.5k km)
        if value % 1000 == 0:
            # If it's an exact thousand (1000, 2000, etc.)
            return f"{value//1000}k km"
        else:
            # For values like 1200, 15500, etc.
            return f"{value/1000:.1f}k km".rstrip('0').rstrip('.')
    else:
        # For values 1,000,000 and above, show in 'Lakh' format
        return f"{value/100000:.1f} Lakh km".rstrip('0').rstrip('.')



SUBCATEGORY_MAP = {
    'cycling': [
        ["bicycles", "Bicycles"],
        ["helmets", "Helmets & Safety Gear"],
        ["tires_tubes", "Tires & Tubes"],
        ["lights", "Lights & Reflectors"],
        ["accessories", "Cycling Accessories"],
        ["clothing", "Cycling Clothing"],
        ["repair_tools", "Repair & Maintenance Tools"],
        ["other", "Other"]
    ],
    'exercise_equipment': [
        ["treadmills", "Treadmills"],
        ["exercise_bikes", "Exercise Bikes"],
        ["ellipticals", "Ellipticals"],
        ["dumbbells", "Dumbbells & Weights"],
        ["benches", "Workout Benches"],
        ["yoga", "Yoga & Mats"],
        ["resistance_bands", "Resistance Bands"],
        ["fitness_accessories", "Fitness Accessories"],
        ["other", "Other"]
    ],
    'water_sports': [
        ["swimming", "Swimming Gear"],
        ["diving", "Diving & Snorkeling"],
        ["kayak", "Kayaks & Canoes"],
        ["surfing", "Surfboards & Accessories"],
        ["lifejackets", "Life Jackets & Safety"],
        ["paddleboards", "Paddle Boards"],
        ["other", "Other"]
    ],
    'camping_hiking': [
        ["camping_tools", "Camping Tools"],
        ["optics", "Monoculars & Binoculars"],
        ["lanterns", "Lanterns & Lamps"],
        ["tents_furniture", "Tents & Furniture"],
        ["coal_wood", "Coal & Wood"],
        ["clothes", "Camping Clothes"],
        ["barbecue", "Barbecue"],
        ["other", "Other"]
    ],
    'golf': [
        ["clubs", "Golf Clubs"],
        ["balls", "Golf Balls"],
        ["bags", "Golf Bags"],
        ["apparel", "Golf Clothing & Shoes"],
        ["training", "Training Equipment"],
        ["carts", "Golf Carts & Trolleys"],
        ["other", "Other"]
    ],
    'indoor_sports': [
        ["table_tennis", "Table Tennis"],
        ["badminton", "Badminton"],
        ["squash", "Squash"],
        ["chess", "Chess & Board Games"],
        ["carrom", "Carrom"],
        ["dart", "Darts"],
        ["other", "Other"]
    ],
    'team_sports': [
        ["football", "Football / Soccer"],
        ["basketball", "Basketball"],
        ["volleyball", "Volleyball"],
        ["cricket", "Cricket"],
        ["rugby", "Rugby"],
        ["hockey", "Hockey"],
        ["other", "Other"]
    ],
    'tennis_racquet': [
        ["tennis", "Tennis"],
        ["badminton", "Badminton"],
        ["squash", "Squash"],
        ["racquetball", "Racquetball"],
        ["paddle_tennis", "Paddle Tennis"],
        ["gear", "Racquets & Strings"],
        ["clothing", "Clothing & Shoes"],
        ["other", "Other"]
    ],
    'winter_sports': [
        ["skiing", "Skiing"],
        ["snowboarding", "Snowboarding"],
        ["ice_skating", "Ice Skating"],
        ["hockey", "Ice Hockey"],
        ["sledding", "Sledding"],
        ["winter_clothing", "Winter Sports Clothing"],
        ["safety", "Helmets & Safety Gear"],
        ["other", "Other"]
    ]
}

@register.filter
def get_subcategory_label(subcategory_key):
    """Convert subcategory key to display label"""
    for category, subcategories in SUBCATEGORY_MAP.items():
        for key, label in subcategories:
            if key == subcategory_key:
                return label
    return subcategory_key  # fallback to key if not found

@register.filter
def format_subcategory_display(subcategory_key):
    """Alternative name for the same filter"""
    return get_subcategory_label(subcategory_key)

SUBCATEGORY_MAP_BABY = {
    'strollers_car_seats': [
        ["car_seat_accessories", "Car Seat Accessories"],
        ["infant_car_seats", "Infant Car Seats"],
        ["jogging_strollers", "Jogging Strollers"],
        ["pram_strollers", "Pram Strollers"],
        ["standard_strollers", "Standard Strollers"],
        ["stroller_accessories", "Stroller Accessories"],
        ["toddler_car_seats", "Toddler Car Seats"],
        ["travel_system_strollers", "Travel System Strollers"],
        ["other", "Other"]
    ],
    'nursery_furniture': [
        ["baby_dressers", "Baby Dressers"],
        ["bassinets_cradles_rockers", "Bassinets, Cradles & Rockers"],
        ["changing_tables", "Changing Tables"],
        ["cribs", "Cribs"],
        ["nursery_bedding", "Nursery Bedding"],
        ["nursery_decor_accessories", "Nursery Decor & Accessories"],
        ["nursery_furniture_sets", "Nursery Furniture Sets"],
        ["other", "Other"]
    ],
    'baby_gear': [
        ["backpacks_carriers", "Backpacks & Carriers"],
        ["chairs", "Chairs"],
        ["jumping_exercisers", "Jumping Exercisers"],
        ["swings", "Swings"],
        ["walkers", "Walkers"],
        ["other", "Other"]
    ],
    'feeding': [
        ["baby_food_processor", "Baby Food Processor"],
        ["bibs", "Bibs"],
        ["booster_high_chairs", "Booster/High Chairs"],
        ["bottles", "Bottles"],
        ["dishes_utensils", "Dishes & Utensils"],
        ["nursing_pillows", "Nursing Pillows"],
        ["pacifiers", "Pacifiers"],
        ["other", "Other"]
    ],
    'safety_health': [
        ["baby_house_car_proofing", "Baby House & Car Proofing"],
        ["baby_monitors", "Baby Monitors"],
        ["baby_thermometers", "Baby Thermometers"],
        ["locks_latches", "Locks & Latches"],
        ["other", "Other"]
    ],
    'bath_diapers': [
        ["bath_tubs", "Bath Tubs"],
        ["diaper_bins", "Diaper Bins"],
        ["diapers_wipes", "Diapers & Wipes"],
        ["lotions_powders_shampoos", "Lotions, Powders & Shampoos"],
        ["potties", "Potties"]
    ],
    'baby_toys': [
        ["educational_toys", "Educational Toys"],
        ["soft_toys", "Soft Toys"],
        ["activity_centers", "Activity Centers"],
        ["other", "Other"]
    ]
}

@register.filter
def get_baby_subcategory_label(subcategory_key):
    """Convert baby items subcategory key to display label"""
    for category, subcategories in SUBCATEGORY_MAP_BABY.items():
        for key, label in subcategories:
            if key == subcategory_key:
                return label
    return subcategory_key  # fallback to key if not found

@register.filter
def format_baby_subcategory_display(subcategory_key):
    """Alternative name for the same filter for baby items"""
    return get_baby_subcategory_label(subcategory_key)

# You can also create a universal filter that works for both
@register.filter
def get_subcategory_label(subcategory_key, category_type='general'):
    """Universal subcategory label filter that works for both sports and baby items"""
    if category_type == 'baby':
        return get_baby_subcategory_label(subcategory_key)
    else:
        # Default to sports categories or your original implementation
        for category, subcategories in SUBCATEGORY_MAP.items():
            for key, label in subcategories:
                if key == subcategory_key:
                    return label
        return subcategory_key
    
SUBCATEGORY_MAP_HOME_APPLIANCES = {
    'large_white_goods': [
        ["air_conditioners", "Air Conditioners"],
        ["dishwashers", "Dishwashers"],
        ["gas_cylinders", "Gas Cylinders"],
        ["humidifiers_purifiers", "Humidifiers & Air Purifiers"],
        ["ovens_microwaves", "Ovens & Microwaves"],
        ["ranges_cooking", "Ranges & Cooking Appliances"],
        ["refrigerators_freezers", "Refrigerators & Freezers"],
        ["washers_dryers", "Washers & Dryers"],
        ["water_coolers", "Water Coolers"],
        ["other", "Other"]
    ],
    'small_kitchen': [
        ["blenders_juicers", "Blenders & Juicers"],
        ["bread_machines", "Bread Machines"],
        ["coffee_espresso", "Coffee & Espresso Appliances"],
        ["fryers", "Fryers"],
        ["hot_plates_grills", "Hot Plates & Grills"],
        ["kettles", "Kettles"],
        ["processors_mixers_grinders", "Processors, Mixers & Grinders"],
        ["slow_cookers_steamers", "Slow Cookers & Steamers"],
        ["toasters", "Toasters"],
        ["other", "Other"]
    ],
    'outdoor_appliances': [
        ["blowers", "Blowers"],
        ["charcoal_grills", "Charcoal Grills"],
        ["gas_grills", "Gas Grills"],
        ["ice_chests", "Ice Chests"],
        ["lawnmowers", "Lawnmowers"],
        ["power_tools", "Power Tools"],
        ["pressure_washers", "Pressure Washers"],
        ["other", "Other"]
    ],
    'small_bathroom': [
        ["hair_dryers", "Hair Dryers, Curlers & Straighteners"],
        ["massagers", "Massagers & Foot Spa"],
        ["scales", "Scales"],
        ["shavers_trimmers", "Shavers & Trimmers"],
        ["other", "Other"]
    ],
    'beauty_spa': [
        ["facial_steamers", "Facial Steamers"],
        ["hair_stylers", "Hair Stylers"],
        ["sauna_equipment", "Sauna Equipment"],
        ["spa_equipment", "Spa Equipment"],
        ["other", "Other"]
    ],
    'irons_sewing': [
        ["irons", "Irons"],
        ["sewing_machines", "Sewing Machines"],
        ["steam_stations", "Steam Stations"],
        ["other", "Other"]
    ],
    'vacuums_floor': [
        ["vacuum_cleaners", "Vacuum Cleaners"],
        ["floor_polishers", "Floor Polishers"],
        ["carpet_cleaners", "Carpet Cleaners"],
        ["other", "Other"]
    ],
    'other': [
        ["other", "Other Appliances"]
    ]
}

def _get_home_appliance_subcategory_label(subcategory_key):
    """Internal function to return the label for a subcategory key"""
    for category, subcategories in SUBCATEGORY_MAP_HOME_APPLIANCES.items():
        for key, label in subcategories:
            if key == subcategory_key:
                return label
    return subcategory_key  

@register.filter
def get_subcategory_label(subcategory_key, model_name=None):
    """
    Template filter to get the display label for a subcategory.
    Example: {{ v|get_subcategory_label:"home_appliance" }}
    """
    if model_name == "home_appliance":
        return _get_home_appliance_subcategory_label(subcategory_key)
    # Future extension for other categories
    return subcategory_key

# Fashion/Clothing subcategory mapping
SUBCATEGORY_MAP_CLOTHING = {
    "shoes_footwear": [
        ["children_shoes", "Children's Shoes and Footwear"],
        ["mens_shoes", "Men's Shoes and Footwear"],
        ["unisex_shoes", "Unisex Shoes and Footwear"],
        ["womens_shoes", "Women's Shoes and Footwear"]
    ],
    "clothing": [
        ["children_clothing", "Children's Clothing"],
        ["mens_clothing", "Men's Clothing"],
        ["unisex_clothing", "Unisex Clothing"],
        ["womens_clothing", "Women's Clothing"]
    ],
    "handbags_bags_wallets": [
        ["athletic_bags", "Athletic Bags"],
        ["bags", "Bags"],
        ["briefcases", "Briefcases"],
        ["mens_wallets", "Men's Wallets"],
        ["womens_handbags", "Women's Handbags"],
        ["womens_wallets", "Women's Wallets"]
    ],
    "mens_accessories": [
        ["belts", "Belts"],
        ["gloves", "Gloves"],
        ["hats", "Hats"],
        ["sunglasses", "Sunglasses"],
        ["ties", "Ties"],
        ["other", "Other"]
    ],
    "womens_accessories": [
        ["belts", "Belts"],
        ["gloves", "Gloves"],
        ["hair_accessories", "Hair Accessories"],
        ["hats", "Hats"],
        ["sunglasses", "Sunglasses"],
        ["other", "Other"]
    ],
    "luggage": [
        ["backpacks", "Backpacks"],
        ["cases", "Cases"],
        ["duffel_bags", "Duffel Bags"],
        ["roller_luggage", "Roller Luggage"]
    ],
    "fragrances": [
        ["mens_fragrances", "Men's Fragrances"],
        ["unisex_fragrances", "Unisex Fragrances"],
        ["womens_fragrances", "Women's Fragrances"]
    ],
    "wedding_apparel": [
        ["children_wedding", "Children's Wedding Apparel"],
        ["mens_wedding", "Men's Wedding Apparel"],
        ["womens_wedding", "Women's Wedding Apparel"]
    ],
    "costumes_uniforms": [
        ["children_costumes", "Children's Costumes & Uniforms"],
        ["mens_costumes", "Men's Costumes & Uniforms"],
        ["unisex_costumes", "Unisex Costumes & Uniforms"],
        ["womens_costumes", "Women's Costumes & Uniforms"]
    ],
    "vintage_highend": [
        ["children_vintage", "Children's Vintage & Highend Clothing"],
        ["mens_vintage", "Men's Vintage & Highend Clothing"],
        ["unisex_vintage", "Unisex Vintage & Highend Clothing"],
        ["womens_vintage", "Women's Vintage & Highend Clothing"]
    ],
    "gifts_bouquet": [],
    "makeup_skincare": [],
    "other": []
}

@register.filter
def get_clothing_subcategory_label(subcategory_key):
    """Convert clothing subcategory key to display label"""
    for category, subcategories in SUBCATEGORY_MAP_CLOTHING.items():
        for key, label in subcategories:
            if key == subcategory_key:
                return label
    return subcategory_key.replace('_', ' ').title()

@register.filter
def format_clothing_subcategory_display(subcategory_key):
    """Alternative name for the same filter for clothing items"""
    return get_clothing_subcategory_label(subcategory_key)

@register.filter
def get_fashion_subcategory_label(subcategory_key):
    """Alias for clothing subcategory filter"""
    return get_clothing_subcategory_label(subcategory_key)

# Universal filter that works for all categories
@register.filter
def get_subcategory_label(subcategory_key, category_type='general'):
    """Universal subcategory label filter that works for all item types"""
    if category_type == 'clothing' or category_type == 'fashion':
        return get_clothing_subcategory_label(subcategory_key)
    else:
        # Default fallback
        return subcategory_key.replace('_', ' ').title()

# Camera subcategory mapping
SUBCATEGORY_MAP_CAMERA = {
    "digital_cameras": [
        ["mirrorless", "Mirrorless Digital Cameras"],
        ["point_shoot", "Point & Shoot"],
        ["slr", "SLR / Professional"],
        ["underwater", "Underwater"],
        ["other", "Other"]
    ],
    "lenses_filters_lighting": [
        ["filter_accessories", "Filter Accessories"],
        ["filters", "Filters"],
        ["flash_accessories", "Flash Accessories"],
        ["flash_units", "Flash Units"],
        ["lens_accessories", "Lens Accessories"],
        ["lenses", "Lenses"]
    ],
    "professional_equipment": [
        ["audio", "Audio"],
        ["cables", "Cables"],
        ["editing", "Editing"],
        ["lighting", "Lighting"],
        ["monitors", "Monitors"],
        ["printing", "Printing"],
        ["projection", "Projection / Screens"],
        ["video_cameras", "Video Cameras"],
        ["other", "Other"]
    ],
    "camera_accessories": [
        ["bags_straps", "Bags & Straps"],
        ["digital_accessories", "Digital Camera Accessories"],
        ["film_accessories", "Film Camera Accessories"],
        ["other", "Other"]
    ],
    "tripods_stands": [
        ["monopods", "Monopods"],
        ["stand_accessories", "Stand Accessories"],
        ["tripods", "Tripods"],
        ["other", "Other"]
    ],
    "camcorders": [
        ["analog", "Analog"],
        ["digital", "Digital"],
        ["other", "Other"]
    ],
    "film_cameras": [
        ["35mm_point", "35mm Point & Shoot"],
        ["35mm_slr", "35mm SLR"],
        ["instant_polaroid", "Instant / Polaroid"],
        ["underwater", "Underwater"],
        ["other", "Other"]
    ],
    "binoculars_telescopes": [
        ["accessories", "Accessories"],
        ["binoculars", "Binoculars / Monoculars"],
        ["telescopes", "Telescopes"],
        ["other", "Other"]
    ],
    "camcorder_accessories": [],
    "camera_drones": []
}

@register.filter
def get_camera_subcategory_label(subcategory_key):
    """Convert camera subcategory key to display label"""
    for category, subcategories in SUBCATEGORY_MAP_CAMERA.items():
        for key, label in subcategories:
            if key == subcategory_key:
                return label
    return subcategory_key.replace('_', ' ').title()

@register.filter
def format_camera_subcategory_display(subcategory_key):
    """Alternative name for the same filter for camera items"""
    return get_camera_subcategory_label(subcategory_key)

@register.filter
def get_photography_subcategory_label(subcategory_key):
    """Alias for camera subcategory filter"""
    return get_camera_subcategory_label(subcategory_key)

# Universal filter that works for all categories
@register.filter
def get_subcategory_label(subcategory_key, category_type='general'):
    """Universal subcategory label filter that works for all item types"""
    if category_type == 'camera' or category_type == 'photography':
        return get_camera_subcategory_label(subcategory_key)
    else:
        # Default fallback
        return subcategory_key.replace('_', ' ').title()

@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter"""
    return value.split(delimiter)


SUBCATEGORY_MAP_JEWELRY = {
    "watches": [
        ["childrens_watches", "Children's Watches"],
        ["mens_sport_watches", "Men's Sport Watches"],
        ["mens_watches", "Men's Watches"],
        ["pocket_stop_watches", "Pocket Watches & Stop Watches"],
        ["womens_sport_watches", "Women's Sport Watches"],
        ["womens_watches", "Women's Watches"]
    ],
    "womens_jewelry": [
        ["body_jewelry", "Body Jewelry"],
        ["bracelets", "Bracelets"],
        ["earrings", "Earrings"],
        ["ethnic_artisan", "Ethnic & Artisan Jewelry"],
        ["hair_jewelry", "Hair Jewelry"],
        ["pins_brooches", "Pins & Brooches"],
        ["rings", "Rings"],
        ["other", "Other"]
    ],
    "mens_jewelry": [
        ["belt_buckles", "Belt Buckles"],
        ["bracelets", "Bracelets"],
        ["chains_necklaces", "Chains & Necklaces"],
        ["cufflinks", "Cufflinks"],
        ["pins_tie_clips", "Pins & Tie Clips"],
        ["rings", "Rings"],
        ["studs", "Studs"],
        ["other", "Other"]
    ],
    "loose_diamonds_gems": [
        ["cz", "CZ"],
        ["diamonds", "Diamonds"],
        ["gemstones", "Gemstones"],
        ["other", "Other"]
    ]
}

@register.filter
def get_jewelry_subcategory_label(subcategory_key):
    """Convert jewelry subcategory key to display label"""
    for category, subcategories in SUBCATEGORY_MAP_JEWELRY.items():
        for key, label in subcategories:
            if key == subcategory_key:
                return label
    return subcategory_key.replace('_', ' ').title()

@register.filter
def format_jewelry_subcategory_display(subcategory_key):
    """Alternative name for the same filter for jewelry items"""
    return get_jewelry_subcategory_label(subcategory_key)

@register.filter
def get_jewellery_subcategory_label(subcategory_key):
    """Alias for jewelry subcategory filter (alternative spelling)"""
    return get_jewelry_subcategory_label(subcategory_key)

# Universal filter that works for all categories
@register.filter
def get_subcategory_label(subcategory_key, category_type='general'):
    """Universal subcategory label filter that works for all item types"""
    if category_type == 'jewelry' or category_type == 'jewellery':
        return get_jewelry_subcategory_label(subcategory_key)
    else:
        # Default fallback
        return subcategory_key.replace('_', ' ').title()
    
SUBCATEGORY_MAP_SPORTS = {
    "cycling": [
        ["bicycles", "Bicycles"],
        ["helmets", "Helmets & Safety Gear"],
        ["tires_tubes", "Tires & Tubes"],
        ["lights", "Lights & Reflectors"],
        ["accessories", "Cycling Accessories"],
        ["clothing", "Cycling Clothing"],
        ["repair_tools", "Repair & Maintenance Tools"],
        ["other", "Other"]
    ],
    "exercise_equipment": [
        ["treadmills", "Treadmills"],
        ["exercise_bikes", "Exercise Bikes"],
        ["ellipticals", "Ellipticals"],
        ["dumbbells", "Dumbbells & Weights"],
        ["benches", "Workout Benches"],
        ["yoga", "Yoga & Mats"],
        ["resistance_bands", "Resistance Bands"],
        ["fitness_accessories", "Fitness Accessories"],
        ["other", "Other"]
    ],
    "water_sports": [
        ["swimming", "Swimming Gear"],
        ["diving", "Diving & Snorkeling"],
        ["kayak", "Kayaks & Canoes"],
        ["surfing", "Surfboards & Accessories"],
        ["lifejackets", "Life Jackets & Safety"],
        ["paddleboards", "Paddle Boards"],
        ["other", "Other"]
    ],
    "camping_hiking": [
        ["camping_tools", "Camping Tools"],
        ["optics", "Monoculars & Binoculars"],
        ["lanterns", "Lanterns & Lamps"],
        ["tents_furniture", "Tents & Furniture"],
        ["coal_wood", "Coal & Wood"],
        ["clothes", "Camping Clothes"],
        ["barbecue", "Barbecue"],
        ["other", "Other"]
    ],
    "golf": [
        ["clubs", "Golf Clubs"],
        ["balls", "Golf Balls"],
        ["bags", "Golf Bags"],
        ["apparel", "Golf Clothing & Shoes"],
        ["training", "Training Equipment"],
        ["carts", "Golf Carts & Trolleys"],
        ["other", "Other"]
    ],
    "indoor_sports": [
        ["table_tennis", "Table Tennis"],
        ["badminton", "Badminton"],
        ["squash", "Squash"],
        ["chess", "Chess & Board Games"],
        ["carrom", "Carrom"],
        ["dart", "Darts"],
        ["other", "Other"]
    ],
    "team_sports": [
        ["football", "Football / Soccer"],
        ["basketball", "Basketball"],
        ["volleyball", "Volleyball"],
        ["cricket", "Cricket"],
        ["rugby", "Rugby"],
        ["hockey", "Hockey"],
        ["other", "Other"]
    ],
    "tennis_racquet": [
        ["tennis", "Tennis"],
        ["badminton", "Badminton"],
        ["squash", "Squash"],
        ["racquetball", "Racquetball"],
        ["paddle_tennis", "Paddle Tennis"],
        ["gear", "Racquets & Strings"],
        ["clothing", "Clothing & Shoes"],
        ["other", "Other"]
    ],
    "winter_sports": [
        ["skiing", "Skiing"],
        ["snowboarding", "Snowboarding"],
        ["ice_skating", "Ice Skating"],
        ["hockey", "Ice Hockey"],
        ["sledding", "Sledding"],
        ["winter_clothing", "Winter Sports Clothing"],
        ["safety", "Helmets & Safety Gear"],
        ["other", "Other"]
    ],
}

# ✅ Main filter: Convert subcategory key → readable label
@register.filter
def get_sports_subcategory_label(subcategory_key):
    """Convert sports subcategory key to display label"""
    for category, subcategories in SUBCATEGORY_MAP_SPORTS.items():
        for key, label in subcategories:
            if key == subcategory_key:
                return label
    return subcategory_key.replace('_', ' ').title()

# ✅ Alternative alias (optional)
@register.filter
def format_sports_subcategory_display(subcategory_key):
    """Alternative name for same filter"""
    return get_sports_subcategory_label(subcategory_key)

# ✅ Universal fallback filter (recommended for template use)
@register.filter
def get_subcategory_label(subcategory_key, category_type='general'):
    """Universal subcategory label filter usable for all sections"""
    if category_type in ['sports', 'sport']:
        return get_sports_subcategory_label(subcategory_key)
    return subcategory_key.replace('_', ' ').title()

# ✅ Utility splitter for handling multiple comma-separated values
@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter (used in templates)"""
    return value.split(delimiter)

SUBCATEGORY_MAP_BOOKS = {
    "textbooks": [
        ["a_levels", "A Levels / High School"],
        ["primary_school", "Primary School"],
        ["secondary_school", "Secondary School"],
        ["university", "University"]
    ],
    "nonfiction": [
        ["business_science_tech", "Business / Science / Technology"],
        ["cook_books", "Cook Books"],
        ["history_biography", "History / Biography"],
        ["how_to_books", "How-To Books"],
        ["picture_books", "Picture Books"],
        ["religious_books", "Religious Books"],
        ["self_help", "Self Help / Motivational Books"],
        ["sports_health", "Sports / Health Books"],
        ["travel_books", "Travel Books"],
        ["other_nonfiction", "Other"]
    ],
    "fiction": [
        ["action_adventure", "Action / Adventure"],
        ["classics", "Classics"],
        ["fantasy_scifi", "Fantasy / Sci-Fi"],
        ["humor", "Humor"],
        ["mystery_thriller", "Mystery / Thriller"],
        ["romance", "Romance"],
        ["other_fiction", "Other"]
    ],
    "children_books": [
        ["coloring_activity", "Coloring / Activity Books"],
        ["educational_books", "Educational Books"],
        ["fiction_cb", "Fiction"],
        ["nonfiction_cb", "Nonfiction"],
        ["picture_popup_books", "Picture / Pop-Up Books"],
        ["other_cb", "Other"]
    ],
    "book_accessories": [
        ["book_lights", "Book Lights"],
        ["daily_planners", "Daily Planners"],
        ["diaries_notebooks", "Diaries / Notebooks"],
        ["other_accessories", "Other"]
    ],
    "digital_ebooks": [
        ["digital_ebooks", "Digital / E-books"]
    ],
    "audiobooks": [
        ["audiobooks", "Audiobooks"]
    ],
    "stationery": [
        ["stationery", "Stationery"]
    ]
}

# ✅ Main filter: Convert subcategory key → readable label
@register.filter
def get_books_subcategory_label(subcategory_key):
    """Convert books subcategory key to display label"""
    for category, subcategories in SUBCATEGORY_MAP_BOOKS.items():
        for key, label in subcategories:
            if key == subcategory_key:
                return label
    return subcategory_key.replace('_', ' ').title()

# ✅ Alternative alias (optional)
@register.filter
def format_books_subcategory_display(subcategory_key):
    """Alternative name for same filter"""
    return get_books_subcategory_label(subcategory_key)

# ✅ Universal fallback filter (recommended for template use)
@register.filter
def get_subcategory_label(subcategory_key, category_type='general'):
    """Universal subcategory label filter usable for all sections"""
    if category_type in ['books', 'book']:
        return get_books_subcategory_label(subcategory_key)
    return subcategory_key.replace('_', ' ').title()

# ✅ Utility splitter for handling multiple comma-separated values
@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter (used in templates)"""
    return value.split(delimiter)
# ✅ Music Subcategory Mapping
SUBCATEGORY_MAP_MUSIC = {
    "cds": [
        ["cds_classical", "Classical"],
        ["cds_country", "Country"],
        ["cds_jazz", "Jazz"],
        ["cds_latin", "Latin"],
        ["cds_metal", "Metal"],
        ["cds_rnb_soul_funk", "R&B / Soul / Funk"],
        ["cds_arabic", "Arabic"],
        ["cds_rock_indie", "Rock & Indie Rock"],
    ],
    "cassettes": [
        ["cass_classical", "Classical"],
        ["cass_country", "Country"],
        ["cass_jazz", "Jazz"],
        ["cass_latin", "Latin"],
        ["cass_metal", "Metal"],
        ["cass_rnb_soul_funk", "R&B / Soul / Funk"],
        ["cass_arabic", "Arabic"],
        ["cass_rock_indie", "Rock & Indie Rock"],
    ],
    "digital": [
        ["digital_classical", "Classical"],
        ["digital_country", "Country"],
        ["digital_jazz", "Jazz"],
        ["digital_latin", "Latin"],
        ["digital_metal", "Metal"],
        ["digital_rnb_soul_funk", "R&B / Soul / Funk"],
        ["digital_arabic", "Arabic"],
        ["digital_rock_indie", "Rock & Indie Rock"],
    ],
    "vinyl": [
        ["vinyl_classical", "Classical"],
        ["vinyl_country", "Country"],
        ["vinyl_jazz", "Jazz"],
        ["vinyl_latin", "Latin"],
        ["vinyl_metal", "Metal"],
        ["vinyl_rnb_soul_funk", "R&B / Soul / Funk"],
        ["vinyl_arabic", "Arabic"],
        ["vinyl_rock_indie", "Rock & Indie Rock"],
    ],
    "duration": [
        ["album", "Album"],
        ["ep", "EP"],
        ["box_set", "Box Set"],
        ["single", "Single"],
        ["other", "Other"],
    ],
}


# ✅ Filter: convert subcategory key → readable label
@register.filter
def get_music_subcategory_label(subcategory_key):
    """Convert music subcategory key to readable label"""
    for category, subcategories in SUBCATEGORY_MAP_MUSIC.items():
        for key, label in subcategories:
            if key == subcategory_key:
                return label
    return subcategory_key.replace('_', ' ').title()


# ✅ Universal fallback (supports multiple section types)
@register.filter
def get_subcategory_label(subcategory_key, category_type='general'):
    """Universal subcategory label filter usable for all sections"""
    if category_type in ['music', 'musics']:
        return get_music_subcategory_label(subcategory_key)
    return subcategory_key.replace('_', ' ').title()


# ✅ Utility splitter for handling multiple comma-separated values
@register.filter
def split(value, delimiter=','):
    """Split a string by delimiter (used in templates)"""
    return value.split(delimiter)

@register.filter
def format_bedrooms(value, model_name=None):
   
    # Always use the BEDROOM_CHOICES
    if model_name == 'apartment':
        bedroom_map = dict(Apartment.BEDROOM_CHOICES)
    elif model_name == 'villa':
        bedroom_map = dict(Villa.BEDROOM_CHOICES)
    elif model_name == 'townhouse':
        bedroom_map = dict(Townhouse.BEDROOM_CHOICES)
    elif model_name == 'farm':
        bedroom_map = dict(Farm.BEDROOM_CHOICES)
    elif model_name == 'staff':
        bedroom_map = dict(Staff.BEDROOM_CHOICES)
    elif model_name == 'hostel':
        bedroom_map = dict(Hostel.BEDROOM_CHOICES)
  

    # Fallback → convert to normal readable text
    else:
        return value.replace('_', ' ').title()

    # Return mapped label or fallback to raw
    return bedroom_map.get(value, value)


@register.filter
def format_floors(value, model_name=None):
    if model_name == 'apartment':
        floors_map = dict(Apartment.FLOOR_CHOICES)
    elif model_name == 'villa':
        floors_map = dict(Villa.FLOOR_CHOICES)
    elif model_name == 'townhouse':
        floors_map = dict(Townhouse.FLOOR_CHOICES)
    elif model_name == 'wholebuilding':
        floors_map = dict(Wholebuilding.FLOOR_CHOICES)
    elif model_name == 'office':
        floors_map = dict(Office.FLOOR_CHOICES)
    elif model_name == 'complex':
        floors_map = dict(Complex.FLOOR_CHOICES)
    elif model_name == 'clinic':
        floors_map = dict(Clinic.FLOOR_CHOICES)
    elif model_name == 'fullfloors':
        floors_map = dict(Fullfloors.FLOOR_CHOICES)
    elif model_name == 'hostel':
        floors_map = dict(Hostel.FLOOR_CHOICES)
    elif model_name == 'staff':
        floors_map = dict(Staff.FLOOR_CHOICES)
    elif model_name == 'commercial':
        floors_map = dict(Commercial.FLOOR_CHOICES)
    else:
        return value.replace('_', ' ').title()
    return floors_map.get(value, value)

@register.filter
def format_building(value, model_name=None):
    if model_name == 'apartment':
        building_map = dict(Apartment.BUILDING_AGE_CHOICES)
    elif model_name == 'villa':
        building_map = dict(Villa.BUILDING_AGE_CHOICES)
    elif model_name == 'townhouse':
        building_map = dict(Townhouse.BUILDING_AGE_CHOICES)
    elif model_name == 'farm':
        building_map = dict(Farm.BUILDING_AGE_CHOICES)
    else:
        return value.replace('_', ' ').title()
    return building_map.get(value, value)

@register.filter
def format_kilometer(value, model_name=None):
    if model_name == 'scooter':
        building_map = dict(Scooter.KILOMETER_CHOICES)
    elif model_name == 'motorcycle':
        building_map = dict(Motorcycle.KILOMETER_CHOICES)
    else:
        return value.replace('_', ' ').title()
    return building_map.get(value, value)

@register.filter
def format_property(value, model_name=None):
    if model_name == 'cafe':
       property_map = dict(Cafe.PROPERTY_CHOICES)
    elif model_name == 'fullfloors':
       property_map = dict(Fullfloors.PROPERTY_CHOICES)
    elif model_name == 'showrooms':
       property_map = dict(Showrooms.PROPERTY_CHOICES)
    elif model_name == 'supermarket':
       property_map = dict(Supermarket.PROPERTY_CHOICES)
    elif model_name == 'warehouse':
       property_map = dict(Warehouse.PROPERTY_CHOICES)
    else:
        return value.replace('_', ' ').title()
    return property_map.get(value, value)
@register.filter
def format_estate_type(value):
    estate_map = dict(Foreign.ESTATE_TYPE_CHOICES)
    return estate_map.get(value, value)

from django_countries import countries

@register.filter
def get_country_name(country_code):
    """Convert country code to country name"""
    try:
        return countries.name(country_code)
    except AttributeError:
        return country_code  # Fallback to code if name not found

@register.filter
def format_color(value, model_name=None):
    if model_name == 'mobile':
        color_map = dict(Mobile.COLOR_CHOICES)
    elif model_name == 'tablet':
        color_map = dict(Tablet.COLOR_CHOICES)
    else:
        return value.replace('_', ' ').title()
    return color_map.get(value, value)

@register.filter
def format_operator(value, model_name=None):
    if model_name == 'mobilesim':
        operator_map = dict(MobileSIM.MOBILE_OPERATOR_CHOICES)
    else:
        return value.replace('_', ' ').title()
    return operator_map.get(value, value)

@register.simple_tag
def get_category_name(category_id):
    if category_id:
        try:
            category = JobCategory.objects.get(id=category_id)
            return category.name
        except JobCategory.DoesNotExist:
            return "Everything"
    return "Everything"


