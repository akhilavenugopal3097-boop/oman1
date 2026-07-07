from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.apps import apps
from oman_app.models import *

User = get_user_model()


# ============================================
# HELPER BASE SERIALIZER
# ============================================
class BaseListingSerializer(serializers.ModelSerializer):
    """Base serializer with common fields for all listing types"""
    owner = serializers.SerializerMethodField()
    images_list = serializers.SerializerMethodField()
    videos_list = serializers.SerializerMethodField()
    city_name = serializers.SerializerMethodField()
    
    def get_owner(self, obj):
        if hasattr(obj, 'user') and obj.user:
            return {
                'id': obj.user.id,
                'username': obj.user.username,
                'email': obj.user.email,
                'phone': obj.user.phone,
            }
        return None
    
    def get_images_list(self, obj):
        if hasattr(obj, 'images'):
            return [{'id': img.id, 'url': img.image.url} for img in obj.images.all()]
        return []
    
    def get_videos_list(self, obj):
        if hasattr(obj, 'videos'):
            return [{'id': vid.id, 'url': vid.video.url} for vid in obj.videos.all()]
        return []
    
    def get_city_name(self, obj):
        if hasattr(obj, 'city') and obj.city:
            city = obj.city
            district = city.district if hasattr(city, 'district') else None
            governate = district.governate if district else None
            return {
                'id': city.id,
                'name': city.name,
                'district': district.name if district else None,
                'governate': governate.name if governate else None,
            }
        return None


# ============================================
# USER SERIALIZERS
# ============================================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'user_type', 'image', 
                  'date_joined', 'is_approved', 'is_active']
        read_only_fields = ['id', 'date_joined']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'phone', 'password', 'password2', 'user_type']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords do not match"})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.is_active = True
        user.save()
        return user


# ============================================
# REAL ESTATE SERIALIZERS
# ============================================
class VillaSerializer(BaseListingSerializer):
    class Meta:
        model = Villa
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class LandSerializer(BaseListingSerializer):
    class Meta:
        model = Land
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ApartmentSerializer(BaseListingSerializer):
    class Meta:
        model = Apartment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class CommercialSerializer(BaseListingSerializer):
    class Meta:
        model = Commercial
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class FarmSerializer(BaseListingSerializer):
    class Meta:
        model = Farm
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ChaletSerializer(BaseListingSerializer):
    class Meta:
        model = Chalet
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class FactorySerializer(BaseListingSerializer):
    class Meta:
        model = Factory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ComplexSerializer(BaseListingSerializer):
    class Meta:
        model = Complex
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ClinicSerializer(BaseListingSerializer):
    class Meta:
        model = Clinic
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class HostelSerializer(BaseListingSerializer):
    class Meta:
        model = Hostel
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class OfficeSerializer(BaseListingSerializer):
    class Meta:
        model = Office
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ShopSerializer(BaseListingSerializer):
    class Meta:
        model = Shop
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class CafeSerializer(BaseListingSerializer):
    class Meta:
        model = Cafe
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class StaffSerializer(BaseListingSerializer):
    class Meta:
        model = Staff
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class WarehouseSerializer(BaseListingSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class TownhouseSerializer(BaseListingSerializer):
    class Meta:
        model = Townhouse
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class FullfloorsSerializer(BaseListingSerializer):
    class Meta:
        model = Fullfloors
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ShowroomsSerializer(BaseListingSerializer):
    class Meta:
        model = Showrooms
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class WholebuildingSerializer(BaseListingSerializer):
    class Meta:
        model = Wholebuilding
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class SupermarketSerializer(BaseListingSerializer):
    class Meta:
        model = Supermarket
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ForeignSerializer(BaseListingSerializer):
    class Meta:
        model = Foreign
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class SharedSerializer(BaseListingSerializer):
    class Meta:
        model = Shared
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class SuitsSerializer(BaseListingSerializer):
    class Meta:
        model = Suits
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


# ============================================
# MOTORS SERIALIZERS
# ============================================
class AutomobileSerializer(BaseListingSerializer):
    class Meta:
        model = Automobile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class MotorcycleSerializer(BaseListingSerializer):
    class Meta:
        model = Motorcycle
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ScooterSerializer(BaseListingSerializer):
    class Meta:
        model = Scooter
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class QuadbikesSerializer(BaseListingSerializer):
    class Meta:
        model = Quadbikes
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class HelmetClothesSerializer(BaseListingSerializer):
    class Meta:
        model = HelmetClothes
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class HeavyVehicleSerializer(BaseListingSerializer):
    class Meta:
        model = HeavyVehicle
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class BoatSerializer(BaseListingSerializer):
    class Meta:
        model = Boat
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class AutoAccessoryPartSerializer(BaseListingSerializer):
    class Meta:
        model = AutoAccessoryPart
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class NumberPlateSerializer(BaseListingSerializer):
    class Meta:
        model = NumberPlate
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class JunkCarSerializer(BaseListingSerializer):
    class Meta:
        model = JunkCar
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class TiresAndCapsSerializer(BaseListingSerializer):
    class Meta:
        model = TiresAndCaps
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class CarRepairMaintenanceSerializer(BaseListingSerializer):
    class Meta:
        model = CarRepairMaintenance
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class DrivingTrainingSerializer(BaseListingSerializer):
    class Meta:
        model = DrivingTraining
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class SportsCarSerializer(BaseListingSerializer):
    class Meta:
        model = SportsCar
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class PartSerializer(BaseListingSerializer):
    class Meta:
        model = Part
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


# ============================================
# ELECTRONICS SERIALIZERS
# ============================================
class MobileSerializer(BaseListingSerializer):
    class Meta:
        model = Mobile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class TabletSerializer(BaseListingSerializer):
    class Meta:
        model = Tablet
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class SmartWatchSerializer(BaseListingSerializer):
    class Meta:
        model = SmartWatch
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class HeadsetSerializer(BaseListingSerializer):
    class Meta:
        model = Headset
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class CoverSerializer(BaseListingSerializer):
    class Meta:
        model = Cover
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class AccessorySerializer(BaseListingSerializer):
    class Meta:
        model = Accessory
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class MobileSIMSerializer(BaseListingSerializer):
    class Meta:
        model = MobileSIM
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ComputerSerializer(BaseListingSerializer):
    class Meta:
        model = Computer
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class SoundSerializer(BaseListingSerializer):
    class Meta:
        model = Sound
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


# ============================================
# OTHER CLASSIFIEDS SERIALIZERS
# ============================================
class FashionSerializer(BaseListingSerializer):
    class Meta:
        model = Fashion
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ToysSerializer(BaseListingSerializer):
    class Meta:
        model = Toys
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class FoodSerializer(BaseListingSerializer):
    class Meta:
        model = Food
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class FitnessSerializer(BaseListingSerializer):
    class Meta:
        model = Fitness
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class PetSerializer(BaseListingSerializer):
    class Meta:
        model = Pet
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class BookSerializer(BaseListingSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ApplianceSerializer(BaseListingSerializer):
    class Meta:
        model = Appliance
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class BusinessSerializer(BaseListingSerializer):
    class Meta:
        model = Business
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class EducationSerializer(BaseListingSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ServiceSerializer(BaseListingSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


# ============================================
# LISTING MODELS SERIALIZERS
# ============================================
class ComputerListingSerializer(BaseListingSerializer):
    class Meta:
        model = ComputerListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class BusinessIndustrialListingSerializer(BaseListingSerializer):
    class Meta:
        model = BusinessIndustrialListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class PetListingSerializer(BaseListingSerializer):
    class Meta:
        model = PetListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class SportsListingSerializer(BaseListingSerializer):
    class Meta:
        model = SportsListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class MusicalListingSerializer(BaseListingSerializer):
    class Meta:
        model = MusicalListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class GamingListingSerializer(BaseListingSerializer):
    class Meta:
        model = GamingListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class TicketVoucherListingSerializer(BaseListingSerializer):
    class Meta:
        model = TicketVoucherListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class CollectibleListingSerializer(BaseListingSerializer):
    class Meta:
        model = CollectibleListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class BooksListingSerializer(BaseListingSerializer):
    class Meta:
        model = BooksListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class MusicListingSerializer(BaseListingSerializer):
    class Meta:
        model = MusicListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class DVDsMoviesListingSerializer(BaseListingSerializer):
    class Meta:
        model = DVDsMoviesListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class FurnitureHomeGardenListingSerializer(BaseListingSerializer):
    class Meta:
        model = FurnitureHomeGardenListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class BabyItemsListingSerializer(BaseListingSerializer):
    class Meta:
        model = BabyItemsListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ToysListingSerializer(BaseListingSerializer):
    class Meta:
        model = ToysListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class LostFoundListingSerializer(BaseListingSerializer):
    class Meta:
        model = LostFoundListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class CameraListingSerializer(BaseListingSerializer):
    class Meta:
        model = CameraListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class JewelryListingSerializer(BaseListingSerializer):
    class Meta:
        model = JewelryListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class HomeApplianceListingSerializer(BaseListingSerializer):
    class Meta:
        model = HomeApplianceListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ClothingAccessoriesListingSerializer(BaseListingSerializer):
    class Meta:
        model = ClothingAccessoriesListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ElectronicsListingSerializer(BaseListingSerializer):
    class Meta:
        model = ElectronicsListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


# ============================================
# SERVICES SERIALIZERS
# ============================================
class AutoServiceListingSerializer(BaseListingSerializer):
    class Meta:
        model = AutoServiceListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class ConsultancyServiceListingSerializer(BaseListingSerializer):
    class Meta:
        model = ConsultancyServiceListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class DomesticServiceListingSerializer(BaseListingSerializer):
    class Meta:
        model = DomesticServiceListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class EventEntertainmentServiceListingSerializer(BaseListingSerializer):
    class Meta:
        model = EventEntertainmentServiceListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class HealthWellbeingServiceListingSerializer(BaseListingSerializer):
    class Meta:
        model = HealthWellbeingServiceListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class HomeMaintenanceServiceListingSerializer(BaseListingSerializer):
    class Meta:
        model = HomeMaintenanceServiceListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class MoversServiceListingSerializer(BaseListingSerializer):
    class Meta:
        model = MoversServiceListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class RestorationServiceListingSerializer(BaseListingSerializer):
    class Meta:
        model = RestorationServiceListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class TutorsServiceListingSerializer(BaseListingSerializer):
    class Meta:
        model = TutorsServiceListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class WebComputerServiceListingSerializer(BaseListingSerializer):
    class Meta:
        model = WebComputerServiceListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class FreelancersServiceListingSerializer(BaseListingSerializer):
    class Meta:
        model = FreelancersServiceListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


class OtherServiceListingSerializer(BaseListingSerializer):
    class Meta:
        model = OtherServiceListing
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'status']


# ============================================
# JOBS SERIALIZERS
# ============================================
class JobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = JobCategory
        fields = '__all__'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['id']


class JobPostSerializer(serializers.ModelSerializer):
    company_name = serializers.CharField(source='company.company_name', read_only=True)
    owner = UserSerializer(source='user', read_only=True)
    
    class Meta:
        model = JobPost
        fields = '__all__'
        read_only_fields = ['id', 'posted_on']


class JobApplicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobApplication
        fields = '__all__'
        read_only_fields = ['id', 'applied_on']


class JobSeekerSerializer(serializers.ModelSerializer):
    user_details = UserSerializer(source='user', read_only=True)
    city_name = serializers.CharField(source='city.name', read_only=True)
    
    class Meta:
        model = JobSeeker
        fields = '__all__'
        read_only_fields = ['id']


class JobSeekerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobSeekerProfile
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'


# ============================================
# CHAT & MESSAGING SERIALIZERS
# ============================================
class ChatMessageSerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source='sender.username', read_only=True)
    receiver_name = serializers.CharField(source='receiver.username', read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = '__all__'
        read_only_fields = ['id', 'timestamp']


class BlockedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlockedUser
        fields = '__all__'


# ============================================
# LOCATION SERIALIZERS
# ============================================
class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'


class GovernateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Governate
        fields = '__all__'


class DistrictSerializer(serializers.ModelSerializer):
    governate_name = serializers.CharField(source='governate.name', read_only=True)
    
    class Meta:
        model = District
        fields = '__all__'


class CitiesSerializer(serializers.ModelSerializer):
    district_name = serializers.CharField(source='district.name', read_only=True)
    governate_name = serializers.CharField(source='district.governate.name', read_only=True)
    
    class Meta:
        model = Cities
        fields = '__all__'


# ============================================
# AMENITIES SERIALIZERS
# ============================================
class NearbyLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = NearbyLocation
        fields = '__all__'


class MainAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = MainAmenities
        fields = '__all__'


class AdditionalAmenitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = AdditionalAmenities
        fields = '__all__'


class InteriorOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InteriorOptions
        fields = '__all__'


class ExteriorOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExteriorOptions
        fields = '__all__'


class TechnologyOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TechnologyOptions
        fields = '__all__'


# ============================================
# CONTENT MANAGEMENT SERIALIZERS
# ============================================
class AdvertisementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Advertisement
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'


class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = '__all__'


class OffersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offers
        fields = '__all__'


class PrivacyPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrivacyPolicy
        fields = '__all__'


class TermsConditionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermsConditions
        fields = '__all__'


class AboutUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutUs
        fields = '__all__'


class RefundPolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = RefundPolicy
        fields = '__all__'


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactUs
        fields = '__all__'


# ============================================
# FAVORITE & REPORT SERIALIZERS
# ============================================
class FavoriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favorite
        fields = '__all__'


class ProductReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductReport
        fields = '__all__'
        read_only_fields = ['id', 'created_at']


# ============================================
# UNIFIED SEARCH RESULT SERIALIZER
# ============================================
class SearchResultSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    type = serializers.CharField()
    type_display = serializers.CharField()
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    image = serializers.URLField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    created_at = serializers.DateTimeField()
    status = serializers.CharField()
    user_id = serializers.IntegerField(required=False)
    username = serializers.CharField(required=False, allow_blank=True)

# ============================================
# ADD THESE TO YOUR EXISTING api_serializers.py
# ============================================

# Chat List Serializer
class ChatListSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField()
    user_image = serializers.CharField(required=False, allow_blank=True)
    last_message = serializers.CharField()
    last_message_time = serializers.DateTimeField()
    unread_count = serializers.IntegerField()
    chat_session_id = serializers.CharField(required=False, allow_blank=True)
    product_id = serializers.IntegerField(required=False, allow_null=True)
    product_type = serializers.CharField(required=False, allow_blank=True)
    product_title = serializers.CharField(required=False, allow_blank=True)
    product_image = serializers.CharField(required=False, allow_blank=True)


# Credit Balance Serializer
class UserCreditsSerializer(serializers.ModelSerializer):
    available_free_listings = serializers.IntegerField(read_only=True)
    available_listing_credits = serializers.IntegerField(read_only=True)
    free_tier_days_left = serializers.IntegerField(read_only=True)
    
    class Meta:
        model = UserCredits
        fields = [
            'id', 'user', 'free_listings_total', 'free_listings_used',
            'available_free_listings', 'purchased_listing_credits',
            'available_listing_credits', 'boost_days_available',
            'is_business_user', 'business_expires_at',
            'free_listings_expires_at', 'free_tier_days_left',
            'total_listings_created', 'total_boosts_used',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']


# Credit Package Serializer
class CreditPackageSerializer(serializers.ModelSerializer):
    price_with_vat = serializers.DecimalField(max_digits=10, decimal_places=3, read_only=True)
    vat_amount = serializers.DecimalField(max_digits=10, decimal_places=3, read_only=True)
    
    class Meta:
        model = CreditPackage
        fields = '__all__'


# Boost Listing Request/Response
class BoostListingSerializer(serializers.Serializer):
    listing_id = serializers.IntegerField(required=True)
    category = serializers.CharField(required=True)
    days = serializers.IntegerField(required=False, default=7)


# Favorites with Product Details
class FavoriteProductSerializer(serializers.ModelSerializer):
    product = serializers.SerializerMethodField()
    
    class Meta:
        model = Favorite
        fields = ['id', 'product', 'created_at']
    
    def get_product(self, obj):
        from .api_utils import get_favorite_product_data
        return get_favorite_product_data(obj)


# Report Listing Serializer
class CreateReportSerializer(serializers.Serializer):
    category = serializers.CharField(required=True)
    listing_id = serializers.IntegerField(required=True)
    reason = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)


# Listing Comment Serializer
class ListingCommentSerializer(serializers.ModelSerializer):
    admin_name = serializers.CharField(source='admin.username', read_only=True)
    user_name = serializers.CharField(source='user.username', read_only=True)
    
    class Meta:
        model = ListingComment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'admin']


# Recently Viewed Serializer
class RecentlyViewedSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    category = serializers.CharField()
    category_display = serializers.CharField()
    title = serializers.CharField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2, required=False)
    image = serializers.URLField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    viewed_at = serializers.DateTimeField()


# Email OTP Serializer
class EmailOTPSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class EmailOTPVerifySerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)


# Password Reset Serializer
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)


class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    otp = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=8)


# Username Change Serializer
class UsernameChangeSerializer(serializers.Serializer):
    new_username = serializers.CharField(required=True, max_length=150)


# Mark Sold Out Serializer
class MarkSoldOutSerializer(serializers.Serializer):
    category = serializers.CharField(required=True)
    listing_id = serializers.IntegerField(required=True)