from rest_framework import viewsets, generics, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from oman_app.models import *
from .serializers import *

import random
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView, RetrieveAPIView
from django.contrib.auth import authenticate, logout
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q, Count, Min, Max, Avg
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.contrib.contenttypes.models import ContentType

from oman_app.models import get_or_create_user_credits


# ============================================
# BASE VIEWSET WITH COMMON FUNCTIONALITY
# ============================================
class BaseListingViewSet(viewsets.ModelViewSet):
    """Base class with common listing functionality for all listing models"""
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Show approved to all, owners see their pending ones too"""
        user = self.request.user
        qs = self.queryset.model.objects.all()
        if user.is_authenticated:
            return qs.filter(Q(status='approved') | Q(user=user))
        return qs.filter(status='approved')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status='pending')


# ============================================
# DYNAMIC VIEWSET FACTORY FUNCTION
# ============================================
def create_viewset(model, serializer_class, model_name):
    """Factory function to create ViewSets dynamically"""
    
    class DynamicViewSet(BaseListingViewSet):
        queryset = model.objects.all()
        serializer_class = serializer_class
        
        def get_queryset(self):
            user = self.request.user
            qs = model.objects.all()
            if user.is_authenticated:
                return qs.filter(Q(status='approved') | Q(user=user))
            return qs.filter(status='approved')
        
        def perform_create(self, serializer):
            serializer.save(user=self.request.user, status='pending')
    
    # Set class name for better debugging
    DynamicViewSet.__name__ = f"{model_name}ViewSet"
    return DynamicViewSet


# ============================================
# REAL ESTATE VIEWSETS
# ============================================
class VillaViewSet(BaseListingViewSet):
    queryset = Villa.objects.all()
    serializer_class = VillaSerializer
    filterset_fields = ['city', 'listing_type', 'bedrooms', 'bathrooms', 'furnished']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'created_at', 'plot_area']


class LandViewSet(BaseListingViewSet):
    queryset = Land.objects.all()
    serializer_class = LandSerializer
    filterset_fields = ['city', 'listing_type', 'zoned_for']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class ApartmentViewSet(BaseListingViewSet):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    filterset_fields = ['city', 'listing_type', 'bedrooms', 'bathrooms', 'furnished']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class CommercialViewSet(BaseListingViewSet):
    queryset = Commercial.objects.all()
    serializer_class = CommercialSerializer
    filterset_fields = ['city', 'listing_type', 'furnished']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class FarmViewSet(BaseListingViewSet):
    queryset = Farm.objects.all()
    serializer_class = FarmSerializer
    filterset_fields = ['city', 'listing_type', 'furnished']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class ChaletViewSet(BaseListingViewSet):
    queryset = Chalet.objects.all()
    serializer_class = ChaletSerializer
    filterset_fields = ['listing_type']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'created_at']


class FactoryViewSet(BaseListingViewSet):
    queryset = Factory.objects.all()
    serializer_class = FactorySerializer
    filterset_fields = ['city', 'listing_type']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class ComplexViewSet(BaseListingViewSet):
    queryset = Complex.objects.all()
    serializer_class = ComplexSerializer
    filterset_fields = ['city', 'listing_type']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class ClinicViewSet(BaseListingViewSet):
    queryset = Clinic.objects.all()
    serializer_class = ClinicSerializer
    filterset_fields = ['city', 'listing_type']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class HostelViewSet(BaseListingViewSet):
    queryset = Hostel.objects.all()
    serializer_class = HostelSerializer
    filterset_fields = ['city', 'listing_type']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class OfficeViewSet(BaseListingViewSet):
    queryset = Office.objects.all()
    serializer_class = OfficeSerializer
    filterset_fields = ['city', 'listing_type', 'furnished']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class ShopViewSet(BaseListingViewSet):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer
    filterset_fields = ['city', 'listing_type']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class CafeViewSet(BaseListingViewSet):
    queryset = Cafe.objects.all()
    serializer_class = CafeSerializer
    filterset_fields = ['city', 'listing_type']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class StaffViewSet(BaseListingViewSet):
    queryset = Staff.objects.all()
    serializer_class = StaffSerializer
    filterset_fields = ['city', 'listing_type']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class WarehouseViewSet(BaseListingViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    filterset_fields = ['city', 'listing_type']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class TownhouseViewSet(BaseListingViewSet):
    queryset = Townhouse.objects.all()
    serializer_class = TownhouseSerializer
    filterset_fields = ['city', 'listing_type', 'bedrooms', 'bathrooms', 'furnished']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class FullfloorsViewSet(BaseListingViewSet):
    queryset = Fullfloors.objects.all()
    serializer_class = FullfloorsSerializer
    filterset_fields = ['city', 'listing_type']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class ShowroomsViewSet(BaseListingViewSet):
    queryset = Showrooms.objects.all()
    serializer_class = ShowroomsSerializer
    filterset_fields = ['city', 'listing_type']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class WholebuildingViewSet(BaseListingViewSet):
    queryset = Wholebuilding.objects.all()
    serializer_class = WholebuildingSerializer
    filterset_fields = ['city', 'listing_type']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class SupermarketViewSet(BaseListingViewSet):
    queryset = Supermarket.objects.all()
    serializer_class = SupermarketSerializer
    filterset_fields = ['city', 'listing_type']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'plot_area', 'created_at']


class ForeignViewSet(BaseListingViewSet):
    queryset = Foreign.objects.all()
    serializer_class = ForeignSerializer
    filterset_fields = ['city', 'listing_type', 'country']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'created_at']


class SharedViewSet(BaseListingViewSet):
    queryset = Shared.objects.all()
    serializer_class = SharedSerializer
    filterset_fields = ['city']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'created_at']


class SuitsViewSet(BaseListingViewSet):
    queryset = Suits.objects.all()
    serializer_class = SuitsSerializer
    filterset_fields = ['city']
    search_fields = ['property_title', 'description']
    ordering_fields = ['price', 'created_at']


# ============================================
# MOTORS VIEWSETS
# ============================================
class AutomobileViewSet(BaseListingViewSet):
    queryset = Automobile.objects.all()
    serializer_class = AutomobileSerializer
    filterset_fields = ['make', 'year', 'fuel_type', 'transmission', 'listing_type']
    search_fields = ['title', 'make', 'name', 'description']
    ordering_fields = ['price', 'year', 'created_at']


class MotorcycleViewSet(BaseListingViewSet):
    queryset = Motorcycle.objects.all()
    serializer_class = MotorcycleSerializer
    filterset_fields = ['make', 'year', 'body_type', 'listing_type']
    search_fields = ['make', 'model', 'description']
    ordering_fields = ['price', 'year', 'created_at']


class ScooterViewSet(BaseListingViewSet):
    queryset = Scooter.objects.all()
    serializer_class = ScooterSerializer
    filterset_fields = ['make', 'year', 'listing_type']
    search_fields = ['make', 'model', 'description']
    ordering_fields = ['price', 'year', 'created_at']


class QuadbikesViewSet(BaseListingViewSet):
    queryset = Quadbikes.objects.all()
    serializer_class = QuadbikesSerializer
    filterset_fields = ['condition', 'listing_type']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class HelmetClothesViewSet(BaseListingViewSet):
    queryset = HelmetClothes.objects.all()
    serializer_class = HelmetClothesSerializer
    filterset_fields = ['condition', 'listing_type', 'helmetcloth_type']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class HeavyVehicleViewSet(BaseListingViewSet):
    queryset = HeavyVehicle.objects.all()
    serializer_class = HeavyVehicleSerializer
    filterset_fields = ['main_type', 'condition', 'listing_type']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'year', 'created_at']


class BoatViewSet(BaseListingViewSet):
    queryset = Boat.objects.all()
    serializer_class = BoatSerializer
    filterset_fields = ['boat_type', 'condition', 'listing_type']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']


class AutoAccessoryPartViewSet(BaseListingViewSet):
    queryset = AutoAccessoryPart.objects.all()
    serializer_class = AutoAccessoryPartSerializer
    filterset_fields = ['main_category', 'condition', 'listing_type']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']


class NumberPlateViewSet(BaseListingViewSet):
    queryset = NumberPlate.objects.all()
    serializer_class = NumberPlateSerializer
    filterset_fields = ['plate_type', 'usage_type', 'listing_type']
    search_fields = ['number', 'letter_english', 'title']
    ordering_fields = ['price', 'created_at']


class JunkCarViewSet(BaseListingViewSet):
    queryset = JunkCar.objects.all()
    serializer_class = JunkCarSerializer
    filterset_fields = ['condition', 'listing_type']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']


class TiresAndCapsViewSet(BaseListingViewSet):
    queryset = TiresAndCaps.objects.all()
    serializer_class = TiresAndCapsSerializer
    filterset_fields = ['tire_type', 'condition']
    search_fields = ['title', 'brand', 'description']
    ordering_fields = ['price', 'created_at']


class CarRepairMaintenanceViewSet(BaseListingViewSet):
    queryset = CarRepairMaintenance.objects.all()
    serializer_class = CarRepairMaintenanceSerializer
    filterset_fields = ['category', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class DrivingTrainingViewSet(BaseListingViewSet):
    queryset = DrivingTraining.objects.all()
    serializer_class = DrivingTrainingSerializer
    filterset_fields = ['trainer_gender', 'transmission', 'body_type']
    search_fields = ['title', 'trainer_name', 'description']
    ordering_fields = ['price', 'created_at']


class SportsCarViewSet(BaseListingViewSet):
    queryset = SportsCar.objects.all()
    serializer_class = SportsCarSerializer
    filterset_fields = ['make', 'year']
    search_fields = ['make', 'description']
    ordering_fields = ['rental_price', 'created_at']


class PartViewSet(BaseListingViewSet):
    queryset = Part.objects.all()
    serializer_class = PartSerializer
    filterset_fields = ['types', 'condition']
    search_fields = ['name', 'description']
    ordering_fields = ['price', 'created_at']


# ============================================
# ELECTRONICS VIEWSETS
# ============================================
class MobileViewSet(BaseListingViewSet):
    queryset = Mobile.objects.all()
    serializer_class = MobileSerializer
    filterset_fields = ['brand', 'condition', 'listing_type', 'storage_capacity']
    search_fields = ['brand', 'model_number', 'description', 'title']
    ordering_fields = ['price', 'created_at']


class TabletViewSet(BaseListingViewSet):
    queryset = Tablet.objects.all()
    serializer_class = TabletSerializer
    filterset_fields = ['brand', 'condition', 'listing_type', 'storage_capacity']
    search_fields = ['brand', 'model_number', 'description', 'title']
    ordering_fields = ['price', 'created_at']


class SmartWatchViewSet(BaseListingViewSet):
    queryset = SmartWatch.objects.all()
    serializer_class = SmartWatchSerializer
    filterset_fields = ['brand', 'condition', 'listing_type']
    search_fields = ['brand', 'description', 'title']
    ordering_fields = ['price', 'created_at']


class HeadsetViewSet(BaseListingViewSet):
    queryset = Headset.objects.all()
    serializer_class = HeadsetSerializer
    filterset_fields = ['condition', 'listing_type']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class CoverViewSet(BaseListingViewSet):
    queryset = Cover.objects.all()
    serializer_class = CoverSerializer
    filterset_fields = ['condition', 'listing_type']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class AccessoryViewSet(BaseListingViewSet):
    queryset = Accessory.objects.all()
    serializer_class = AccessorySerializer
    filterset_fields = ['type', 'condition', 'listing_type']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class MobileSIMViewSet(BaseListingViewSet):
    queryset = MobileSIM.objects.all()
    serializer_class = MobileSIMSerializer
    filterset_fields = ['operator', 'listing_type']
    search_fields = ['title', 'description', 'oman_number']
    ordering_fields = ['price', 'created_at']


class ComputerViewSet(BaseListingViewSet):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer
    filterset_fields = ['brand', 'condition', 'operating_system']
    search_fields = ['brand', 'model_number', 'description', 'product_name']
    ordering_fields = ['price', 'created_at']


class SoundViewSet(BaseListingViewSet):
    queryset = Sound.objects.all()
    serializer_class = SoundSerializer
    filterset_fields = ['brand', 'condition']
    search_fields = ['brand', 'model_number', 'description', 'product_name']
    ordering_fields = ['price', 'created_at']


# ============================================
# OTHER CLASSIFIEDS VIEWSETS
# ============================================
class FashionViewSet(BaseListingViewSet):
    queryset = Fashion.objects.all()
    serializer_class = FashionSerializer
    filterset_fields = ['category', 'size', 'gender', 'condition']
    search_fields = ['name', 'brand', 'description', 'product_name']
    ordering_fields = ['price', 'created_at']


class ToysViewSet(BaseListingViewSet):
    queryset = Toys.objects.all()
    serializer_class = ToysSerializer
    filterset_fields = ['category', 'platform', 'age_group', 'condition']
    search_fields = ['product_name', 'brand', 'description']
    ordering_fields = ['price', 'created_at']


class FoodViewSet(BaseListingViewSet):
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    filterset_fields = ['product_type']
    search_fields = ['product_name', 'brand', 'description']
    ordering_fields = ['price', 'expiration_date', 'created_at']


class FitnessViewSet(BaseListingViewSet):
    queryset = Fitness.objects.all()
    serializer_class = FitnessSerializer
    filterset_fields = ['category', 'condition']
    search_fields = ['product_name', 'brand', 'description']
    ordering_fields = ['price', 'created_at']


class PetViewSet(BaseListingViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    filterset_fields = ['pet_type', 'vaccinated']
    search_fields = ['pet_name', 'breed', 'description']
    ordering_fields = ['price', 'age', 'created_at']


class BookViewSet(BaseListingViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filterset_fields = ['category', 'condition']
    search_fields = ['book_name', 'genre', 'description']
    ordering_fields = ['price', 'created_at']


class ApplianceViewSet(BaseListingViewSet):
    queryset = Appliance.objects.all()
    serializer_class = ApplianceSerializer
    filterset_fields = ['appliance_type', 'condition']
    search_fields = ['product_name', 'brand', 'model_number', 'description']
    ordering_fields = ['price', 'created_at']


class BusinessViewSet(BaseListingViewSet):
    queryset = Business.objects.all()
    serializer_class = BusinessSerializer
    filterset_fields = ['category', 'condition']
    search_fields = ['product_name', 'brand', 'description']
    ordering_fields = ['price', 'created_at']


class EducationViewSet(BaseListingViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer
    filterset_fields = ['course_type']
    search_fields = ['subject', 'description', 'instructor_name']
    ordering_fields = ['price', 'duration', 'created_at']


class ServiceViewSet(BaseListingViewSet):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filterset_fields = ['service_type']
    search_fields = ['provider_name', 'description']
    ordering_fields = ['price_range', 'created_at']


# ============================================
# LISTING MODELS VIEWSETS
# ============================================
class ComputerListingViewSet(BaseListingViewSet):
    queryset = ComputerListing.objects.all()
    serializer_class = ComputerListingSerializer
    filterset_fields = ['category', 'condition', 'listing_type']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class BusinessIndustrialListingViewSet(BaseListingViewSet):
    queryset = BusinessIndustrialListing.objects.all()
    serializer_class = BusinessIndustrialListingSerializer
    filterset_fields = ['category', 'condition', 'listing_type']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class PetListingViewSet(BaseListingViewSet):
    queryset = PetListing.objects.all()
    serializer_class = PetListingSerializer
    filterset_fields = ['category', 'listing_type']
    search_fields = ['title', 'description', 'name', 'breed']
    ordering_fields = ['price', 'created_at']


class SportsListingViewSet(BaseListingViewSet):
    queryset = SportsListing.objects.all()
    serializer_class = SportsListingSerializer
    filterset_fields = ['category', 'condition', 'listing_type']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class MusicalListingViewSet(BaseListingViewSet):
    queryset = MusicalListing.objects.all()
    serializer_class = MusicalListingSerializer
    filterset_fields = ['category', 'condition', 'listing_type']
    search_fields = ['title', 'description', 'type']
    ordering_fields = ['price', 'created_at']


class GamingListingViewSet(BaseListingViewSet):
    queryset = GamingListing.objects.all()
    serializer_class = GamingListingSerializer
    filterset_fields = ['category', 'condition', 'listing_type']
    search_fields = ['title', 'description', 'type']
    ordering_fields = ['price', 'created_at']


class TicketVoucherListingViewSet(BaseListingViewSet):
    queryset = TicketVoucherListing.objects.all()
    serializer_class = TicketVoucherListingSerializer
    filterset_fields = ['subcategory']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class CollectibleListingViewSet(BaseListingViewSet):
    queryset = CollectibleListing.objects.all()
    serializer_class = CollectibleListingSerializer
    filterset_fields = ['category', 'condition', 'listing_type']
    search_fields = ['title', 'description', 'type']
    ordering_fields = ['price', 'created_at']


class BooksListingViewSet(BaseListingViewSet):
    queryset = BooksListing.objects.all()
    serializer_class = BooksListingSerializer
    filterset_fields = ['category', 'condition', 'listing_type']
    search_fields = ['title', 'description', 'type']
    ordering_fields = ['price', 'created_at']


class MusicListingViewSet(BaseListingViewSet):
    queryset = MusicListing.objects.all()
    serializer_class = MusicListingSerializer
    filterset_fields = ['category', 'condition', 'listing_type']
    search_fields = ['title', 'description', 'type']
    ordering_fields = ['price', 'created_at']


class DVDsMoviesListingViewSet(BaseListingViewSet):
    queryset = DVDsMoviesListing.objects.all()
    serializer_class = DVDsMoviesListingSerializer
    filterset_fields = ['category', 'subcategory', 'condition', 'listing_type']
    search_fields = ['title', 'description', 'type']
    ordering_fields = ['price', 'created_at']


class FurnitureHomeGardenListingViewSet(BaseListingViewSet):
    queryset = FurnitureHomeGardenListing.objects.all()
    serializer_class = FurnitureHomeGardenListingSerializer
    filterset_fields = ['category', 'condition', 'listing_type']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class BabyItemsListingViewSet(BaseListingViewSet):
    queryset = BabyItemsListing.objects.all()
    serializer_class = BabyItemsListingSerializer
    filterset_fields = ['category', 'condition', 'listing_type']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class ToysListingViewSet(BaseListingViewSet):
    queryset = ToysListing.objects.all()
    serializer_class = ToysListingSerializer
    filterset_fields = ['category', 'condition', 'listing_type']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class LostFoundListingViewSet(BaseListingViewSet):
    queryset = LostFoundListing.objects.all()
    serializer_class = LostFoundListingSerializer
    filterset_fields = ['category', 'listing_type']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']


class CameraListingViewSet(BaseListingViewSet):
    queryset = CameraListing.objects.all()
    serializer_class = CameraListingSerializer
    filterset_fields = ['main_category', 'condition', 'listing_type']
    search_fields = ['title', 'description', 'brand']
    ordering_fields = ['price', 'created_at']


class JewelryListingViewSet(BaseListingViewSet):
    queryset = JewelryListing.objects.all()
    serializer_class = JewelryListingSerializer
    filterset_fields = ['main_category', 'condition', 'listing_type']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class HomeApplianceListingViewSet(BaseListingViewSet):
    queryset = HomeApplianceListing.objects.all()
    serializer_class = HomeApplianceListingSerializer
    filterset_fields = ['main_category', 'condition', 'listing_type']
    search_fields = ['title', 'description', 'brand']
    ordering_fields = ['price', 'created_at']


class ClothingAccessoriesListingViewSet(BaseListingViewSet):
    queryset = ClothingAccessoriesListing.objects.all()
    serializer_class = ClothingAccessoriesListingSerializer
    filterset_fields = ['main_category', 'condition', 'listing_type']
    search_fields = ['title', 'description', 'brand']
    ordering_fields = ['price', 'created_at']


class ElectronicsListingViewSet(BaseListingViewSet):
    queryset = ElectronicsListing.objects.all()
    serializer_class = ElectronicsListingSerializer
    filterset_fields = ['main_category', 'condition', 'listing_type']
    search_fields = ['title', 'description', 'brand']
    ordering_fields = ['price', 'created_at']


# ============================================
# SERVICES VIEWSETS
# ============================================
class AutoServiceListingViewSet(BaseListingViewSet):
    queryset = AutoServiceListing.objects.all()
    serializer_class = AutoServiceListingSerializer
    filterset_fields = ['service_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class ConsultancyServiceListingViewSet(BaseListingViewSet):
    queryset = ConsultancyServiceListing.objects.all()
    serializer_class = ConsultancyServiceListingSerializer
    filterset_fields = ['service_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class DomesticServiceListingViewSet(BaseListingViewSet):
    queryset = DomesticServiceListing.objects.all()
    serializer_class = DomesticServiceListingSerializer
    filterset_fields = ['service_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class EventEntertainmentServiceListingViewSet(BaseListingViewSet):
    queryset = EventEntertainmentServiceListing.objects.all()
    serializer_class = EventEntertainmentServiceListingSerializer
    filterset_fields = ['service_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class HealthWellbeingServiceListingViewSet(BaseListingViewSet):
    queryset = HealthWellbeingServiceListing.objects.all()
    serializer_class = HealthWellbeingServiceListingSerializer
    filterset_fields = ['service_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class HomeMaintenanceServiceListingViewSet(BaseListingViewSet):
    queryset = HomeMaintenanceServiceListing.objects.all()
    serializer_class = HomeMaintenanceServiceListingSerializer
    filterset_fields = ['service_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class MoversServiceListingViewSet(BaseListingViewSet):
    queryset = MoversServiceListing.objects.all()
    serializer_class = MoversServiceListingSerializer
    filterset_fields = ['service_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class RestorationServiceListingViewSet(BaseListingViewSet):
    queryset = RestorationServiceListing.objects.all()
    serializer_class = RestorationServiceListingSerializer
    filterset_fields = ['service_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class TutorsServiceListingViewSet(BaseListingViewSet):
    queryset = TutorsServiceListing.objects.all()
    serializer_class = TutorsServiceListingSerializer
    filterset_fields = ['service_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class WebComputerServiceListingViewSet(BaseListingViewSet):
    queryset = WebComputerServiceListing.objects.all()
    serializer_class = WebComputerServiceListingSerializer
    filterset_fields = ['service_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class FreelancersServiceListingViewSet(BaseListingViewSet):
    queryset = FreelancersServiceListing.objects.all()
    serializer_class = FreelancersServiceListingSerializer
    filterset_fields = ['service_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


class OtherServiceListingViewSet(BaseListingViewSet):
    queryset = OtherServiceListing.objects.all()
    serializer_class = OtherServiceListingSerializer
    filterset_fields = ['service_type', 'status']
    search_fields = ['title', 'description']
    ordering_fields = ['price', 'created_at']


# ============================================
# JOBS VIEWSETS
# ============================================
class JobCategoryViewSet(viewsets.ModelViewSet):
    queryset = JobCategory.objects.all()
    serializer_class = JobCategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['status']
    search_fields = ['company_name', 'email']


class JobPostViewSet(viewsets.ModelViewSet):
    queryset = JobPost.objects.all()
    serializer_class = JobPostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['job_type', 'experience_required', 'job_category', 'gender']
    search_fields = ['title', 'description', 'skills_required']
    ordering_fields = ['salary_range', 'application_deadline', 'posted_on']
    ordering = ['-posted_on']
    
    def get_queryset(self):
        return JobPost.objects.filter(application_deadline__gte=timezone.now())
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobApplicationViewSet(viewsets.ModelViewSet):
    queryset = JobApplication.objects.all()
    serializer_class = JobApplicationSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return JobApplication.objects.all()
        return JobApplication.objects.filter(user=user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class JobSeekerViewSet(viewsets.ModelViewSet):
    queryset = JobSeeker.objects.all()
    serializer_class = JobSeekerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['education_level', 'work_experience', 'expected_salary']
    search_fields = ['headline', 'nationality']
    
    def get_queryset(self):
        return JobSeeker.objects.filter(is_completed=True)
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Get the job seeker profile for the current user"""
        try:
            jobseeker = JobSeeker.objects.get(user=request.user)
            serializer = self.get_serializer(jobseeker)
            return Response(serializer.data)
        except JobSeeker.DoesNotExist:
            return Response({'detail': 'No job seeker profile found'}, status=404)


class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']


# ============================================
# CHAT & MESSAGING VIEWSETS
# ============================================
class ChatMessageViewSet(viewsets.ModelViewSet):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        return ChatMessage.objects.filter(Q(sender=user) | Q(receiver=user)).order_by('-timestamp')
    
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)
    
    @action(detail=True, methods=['post'])
    def mark_read(self, request, pk=None):
        message = self.get_object()
        if message.receiver == request.user:
            message.is_read = True
            message.save()
            return Response({'status': 'marked as read'})
        return Response({'error': 'Not authorized'}, status=403)
    
    @action(detail=False, methods=['get'])
    def unread_count(self, request):
        count = ChatMessage.objects.filter(receiver=request.user, is_read=False).count()
        return Response({'unread_count': count})


class BlockedUserViewSet(viewsets.ModelViewSet):
    queryset = BlockedUser.objects.all()
    serializer_class = BlockedUserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return BlockedUser.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# ============================================
# LOCATION VIEWSETS
# ============================================
class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']


class GovernateViewSet(viewsets.ModelViewSet):
    queryset = Governate.objects.all()
    serializer_class = GovernateSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']


class DistrictViewSet(viewsets.ModelViewSet):
    queryset = District.objects.all()
    serializer_class = DistrictSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['governate']
    search_fields = ['name']


class CitiesViewSet(viewsets.ModelViewSet):
    queryset = Cities.objects.all()
    serializer_class = CitiesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['district', 'district__governate']
    search_fields = ['name']


# ============================================
# AMENITIES VIEWSETS
# ============================================
class NearbyLocationViewSet(viewsets.ModelViewSet):
    queryset = NearbyLocation.objects.all()
    serializer_class = NearbyLocationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']


class MainAmenitiesViewSet(viewsets.ModelViewSet):
    queryset = MainAmenities.objects.all()
    serializer_class = MainAmenitiesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']


class AdditionalAmenitiesViewSet(viewsets.ModelViewSet):
    queryset = AdditionalAmenities.objects.all()
    serializer_class = AdditionalAmenitiesSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']


class InteriorOptionsViewSet(viewsets.ModelViewSet):
    queryset = InteriorOptions.objects.all()
    serializer_class = InteriorOptionsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']


class ExteriorOptionsViewSet(viewsets.ModelViewSet):
    queryset = ExteriorOptions.objects.all()
    serializer_class = ExteriorOptionsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']


class TechnologyOptionsViewSet(viewsets.ModelViewSet):
    queryset = TechnologyOptions.objects.all()
    serializer_class = TechnologyOptionsSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    search_fields = ['name']


# ============================================
# CONTENT MANAGEMENT VIEWSETS
# ============================================
class AdvertisementViewSet(viewsets.ModelViewSet):
    queryset = Advertisement.objects.all()
    serializer_class = AdvertisementSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['category', 'is_active']


class BannerViewSet(viewsets.ModelViewSet):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['category', 'is_active']


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['category', 'is_active']
    search_fields = ['title', 'content']


class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = ['is_active']
    search_fields = ['question', 'answer']


class OffersViewSet(viewsets.ModelViewSet):
    queryset = Offers.objects.all()
    serializer_class = OffersSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class PrivacyPolicyViewSet(viewsets.ModelViewSet):
    queryset = PrivacyPolicy.objects.filter(is_active=True)
    serializer_class = PrivacyPolicySerializer
    permission_classes = [AllowAny]


class TermsConditionsViewSet(viewsets.ModelViewSet):
    queryset = TermsConditions.objects.filter(is_active=True)
    serializer_class = TermsConditionsSerializer
    permission_classes = [AllowAny]


class AboutUsViewSet(viewsets.ModelViewSet):
    queryset = AboutUs.objects.filter(is_active=True)
    serializer_class = AboutUsSerializer
    permission_classes = [AllowAny]


class RefundPolicyViewSet(viewsets.ModelViewSet):
    queryset = RefundPolicy.objects.filter(is_active=True)
    serializer_class = RefundPolicySerializer
    permission_classes = [AllowAny]


class ContactUsViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.filter(is_active=True)
    serializer_class = ContactUsSerializer
    permission_classes = [AllowAny]


# ============================================
# FAVORITE & REPORT VIEWSETS
# ============================================
class FavoriteViewSet(viewsets.ModelViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['post'])
    def toggle(self, request):
        """Toggle favorite for any product"""
        content_type_id = request.data.get('content_type')
        object_id = request.data.get('object_id')
        
        if not content_type_id or not object_id:
            return Response({'error': 'content_type and object_id required'}, status=400)
        
        try:
            favorite = Favorite.objects.get(
                user=request.user,
                content_type_id=content_type_id,
                object_id=object_id
            )
            favorite.delete()
            return Response({'status': 'removed'})
        except Favorite.DoesNotExist:
            Favorite.objects.create(
                user=request.user,
                content_type_id=content_type_id,
                object_id=object_id
            )
            return Response({'status': 'added'})


class ProductReportViewSet(viewsets.ModelViewSet):
    queryset = ProductReport.objects.all()
    serializer_class = ProductReportSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return ProductReport.objects.all()
        return ProductReport.objects.filter(reporter=user)
    
    def perform_create(self, serializer):
        serializer.save(reporter=self.request.user)


# ============================================
# USER PROFILE & AUTHENTICATION
# ============================================
class CurrentUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class UserRegistrationView(generics.CreateAPIView):
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return User.objects.all()
        return User.objects.filter(id=user.id)


# ============================================
# USER LISTINGS - GET ALL USER'S LISTINGS
# ============================================
class UserListingsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SearchResultSerializer
    
    def get_queryset(self):
        user = self.request.user
        results = []
        
        # All models that have 'user' field and 'status' field
        model_names = [
            # Real Estate
            'Villa', 'Land', 'Apartment', 'Commercial', 'Farm', 'Chalet',
            'Factory', 'Complex', 'Clinic', 'Hostel', 'Office', 'Shop',
            'Cafe', 'Staff', 'Warehouse', 'Townhouse', 'Fullfloors',
            'Showrooms', 'Wholebuilding', 'Supermarket', 'Foreign',
            'Shared', 'Suits',
            # Motors
            'Automobile', 'Motorcycle', 'Scooter', 'Quadbikes', 'HelmetClothes',
            'HeavyVehicle', 'AutoAccessoryPart', 'Boat', 'NumberPlate',
            'TiresAndCaps', 'JunkCar', 'DrivingTraining', 'CarRepairMaintenance',
            'SportsCar', 'Part',
            # Electronics
            'Mobile', 'Tablet', 'SmartWatch', 'Headset', 'Cover',
            'Accessory', 'MobileSIM', 'Computer', 'Sound',
            # Other Classifieds
            'Fashion', 'Toys', 'Food', 'Fitness', 'Pet', 'Book', 'Appliance',
            'Business', 'Education', 'Service', 'ComputerListing',
            'BusinessIndustrialListing', 'PetListing', 'SportsListing',
            'MusicalListing', 'GamingListing', 'TicketVoucherListing',
            'CollectibleListing', 'BooksListing', 'MusicListing',
            'DVDsMoviesListing', 'FurnitureHomeGardenListing',
            'BabyItemsListing', 'ToysListing', 'LostFoundListing',
            'CameraListing', 'JewelryListing', 'HomeApplianceListing',
            'ClothingAccessoriesListing', 'ElectronicsListing',
            # Services
            'AutoServiceListing', 'ConsultancyServiceListing',
            'DomesticServiceListing', 'EventEntertainmentServiceListing',
            'HealthWellbeingServiceListing', 'HomeMaintenanceServiceListing',
            'MoversServiceListing', 'RestorationServiceListing',
            'TutorsServiceListing', 'WebComputerServiceListing',
            'FreelancersServiceListing', 'OtherServiceListing',
            # Jobs
            'JobPost',
        ]
        
        for model_name in model_names:
            try:
                model = apps.get_model('oman_app', model_name)
                if hasattr(model, 'user') and hasattr(model, 'status'):
                    items = model.objects.filter(user=user)
                    
                    for item in items:
                        # Get title
                        title = str(item)
                        if hasattr(item, 'title') and item.title:
                            title = item.title
                        elif hasattr(item, 'property_title') and item.property_title:
                            title = item.property_title
                        elif hasattr(item, 'name') and item.name:
                            title = item.name
                        elif hasattr(item, 'product_name') and item.product_name:
                            title = item.product_name
                        
                        # Get image
                        image_url = ''
                        if hasattr(item, 'images') and item.images.exists():
                            try:
                                image_url = item.images.first().image.url
                            except:
                                pass
                        elif hasattr(item, 'image') and item.image:
                            try:
                                image_url = item.image.url
                            except:
                                pass
                        
                        # Get city
                        city_name = ''
                        if hasattr(item, 'city') and item.city:
                            city_name = item.city.name
                        
                        # Get price
                        price = 0
                        if hasattr(item, 'price') and item.price:
                            price = item.price
                        elif hasattr(item, 'rental_price') and item.rental_price:
                            price = item.rental_price
                        
                        # Get created_at
                        created_at = getattr(item, 'created_at', timezone.now())
                        if hasattr(item, 'posted_on'):
                            created_at = item.posted_on
                        
                        results.append({
                            'id': item.id,
                            'type': model_name.lower(),
                            'type_display': model_name,
                            'title': str(title),
                            'price': price,
                            'image': image_url,
                            'city': city_name,
                            'created_at': created_at,
                            'status': getattr(item, 'status', 'pending'),
                            'user_id': item.user.id if hasattr(item, 'user') and item.user else None,
                            'username': item.user.username if hasattr(item, 'user') and item.user else None,
                        })
            except LookupError:
                continue
        
        # Sort by created_at descending
        results.sort(key=lambda x: x['created_at'], reverse=True)
        return results


# ============================================
# GLOBAL SEARCH API
# ============================================
class GlobalSearchView(generics.ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SearchResultSerializer
    
    def get_queryset(self):
        query = self.request.query_params.get('q', '')
        category = self.request.query_params.get('category', 'all')
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        listing_type = self.request.query_params.get('listing_type', '')
        
        results = []
        
        # All searchable models
        searchable_models = [
            # Real Estate
            ('Villa', ['property_title', 'description']),
            ('Land', ['property_title', 'description']),
            ('Apartment', ['property_title', 'description']),
            ('Commercial', ['property_title', 'description']),
            ('Farm', ['property_title', 'description']),
            ('Office', ['property_title', 'description']),
            ('Shop', ['property_title', 'description']),
            # Motors
            ('Automobile', ['title', 'make', 'name', 'description']),
            ('Motorcycle', ['make', 'model', 'description']),
            ('Boat', ['name', 'description']),
            # Electronics
            ('Mobile', ['brand', 'model_number', 'description', 'title']),
            ('Tablet', ['brand', 'model_number', 'description', 'title']),
            # Jobs
            ('JobPost', ['title', 'description', 'skills_required']),
        ]
        
        for model_name, search_fields in searchable_models:
            try:
                model = apps.get_model('oman_app', model_name)
                if hasattr(model, 'status'):
                    qs = model.objects.filter(status='approved')
                    
                    if query:
                        q_filter = Q()
                        for field in search_fields:
                            q_filter |= Q(**{f"{field}__icontains": query})
                        qs = qs.filter(q_filter)
                    
                    if min_price and hasattr(model, 'price'):
                        qs = qs.filter(price__gte=min_price)
                    if max_price and hasattr(model, 'price'):
                        qs = qs.filter(price__lte=max_price)
                    if listing_type and hasattr(model, 'listing_type'):
                        qs = qs.filter(listing_type=listing_type)
                    
                    for item in qs[:50]:
                        # Get title
                        title = str(item)
                        if hasattr(item, 'title') and item.title:
                            title = item.title
                        elif hasattr(item, 'property_title') and item.property_title:
                            title = item.property_title
                        elif hasattr(item, 'name') and item.name:
                            title = item.name
                        
                        # Get image
                        image_url = ''
                        if hasattr(item, 'images') and item.images.exists():
                            try:
                                image_url = item.images.first().image.url
                            except:
                                pass
                        
                        # Get city
                        city_name = ''
                        if hasattr(item, 'city') and item.city:
                            city_name = item.city.name
                        
                        # Get price
                        price = getattr(item, 'price', 0)
                        
                        # Get created_at
                        created_at = getattr(item, 'created_at', timezone.now())
                        if hasattr(item, 'posted_on'):
                            created_at = item.posted_on
                        
                        results.append({
                            'id': item.id,
                            'type': model_name.lower(),
                            'type_display': model_name,
                            'title': str(title),
                            'price': price,
                            'image': image_url,
                            'city': city_name,
                            'created_at': created_at,
                            'status': getattr(item, 'status', 'unknown'),
                            'user_id': item.user.id if hasattr(item, 'user') and item.user else None,
                            'username': item.user.username if hasattr(item, 'user') and item.user else None,
                        })
            except LookupError:
                continue
        
        results.sort(key=lambda x: x['created_at'], reverse=True)
        return results[:100]


# ============================================
# DASHBOARD STATS API
# ============================================
class DashboardStatsView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        stats = {
            'total_listings': 0,
            'by_category': {},
            'by_listing_type': {'sale': 0, 'rent': 0},
        }
        
        # Count all approved listings across all models
        model_names = [
            # Real Estate
            'Villa', 'Land', 'Apartment', 'Commercial', 'Farm', 'Chalet',
            'Factory', 'Complex', 'Clinic', 'Hostel', 'Office', 'Shop',
            'Cafe', 'Staff', 'Warehouse', 'Townhouse', 'Fullfloors',
            'Showrooms', 'Wholebuilding', 'Supermarket', 'Foreign',
            'Shared', 'Suits',
            # Motors
            'Automobile', 'Motorcycle', 'Scooter', 'Quadbikes', 'HelmetClothes',
            'HeavyVehicle', 'AutoAccessoryPart', 'Boat', 'NumberPlate',
            'TiresAndCaps', 'JunkCar', 'DrivingTraining', 'CarRepairMaintenance',
            # Electronics
            'Mobile', 'Tablet', 'SmartWatch', 'Headset', 'Cover',
            'Accessory', 'MobileSIM', 'Computer', 'Sound',
            # Other Classifieds
            'Fashion', 'Toys', 'Food', 'Fitness', 'Pet', 'Book', 'Appliance',
            'Business', 'Education', 'Service', 'ComputerListing',
            'BusinessIndustrialListing', 'PetListing', 'SportsListing',
            'MusicalListing', 'GamingListing', 'TicketVoucherListing',
            'CollectibleListing', 'BooksListing', 'MusicListing',
            'DVDsMoviesListing', 'FurnitureHomeGardenListing',
            'BabyItemsListing', 'ToysListing', 'LostFoundListing',
            'CameraListing', 'JewelryListing', 'HomeApplianceListing',
            'ClothingAccessoriesListing', 'ElectronicsListing',
            # Services
            'AutoServiceListing', 'ConsultancyServiceListing',
            'DomesticServiceListing', 'EventEntertainmentServiceListing',
            'HealthWellbeingServiceListing', 'HomeMaintenanceServiceListing',
            'MoversServiceListing', 'RestorationServiceListing',
            'TutorsServiceListing', 'WebComputerServiceListing',
            'FreelancersServiceListing', 'OtherServiceListing',
            # Jobs
            'JobPost',
        ]
        
        for model_name in model_names:
            try:
                model = apps.get_model('oman_app', model_name)
                if hasattr(model, 'status'):
                    count = model.objects.filter(status='approved').count()
                    stats['total_listings'] += count
                    
                    if hasattr(model, 'listing_type'):
                        stats['by_listing_type']['sale'] += model.objects.filter(status='approved', listing_type='sell').count()
                        stats['by_listing_type']['rent'] += model.objects.filter(status='approved', listing_type='rent').count()
            except LookupError:
                continue
        
        return Response(stats)


# ============================================
# LOCATION DATA API (Hierarchical)
# ============================================
class LocationHierarchyView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        governates = Governate.objects.all().values('id', 'name', 'latitude', 'longitude')
        
        data = []
        for gov in governates:
            districts = District.objects.filter(governate_id=gov['id']).values('id', 'name', 'latitude', 'longitude')
            district_list = []
            for dist in districts:
                cities = Cities.objects.filter(district_id=dist['id']).values('id', 'name', 'latitude', 'longitude')
                district_list.append({
                    'id': dist['id'],
                    'name': dist['name'],
                    'latitude': dist['latitude'],
                    'longitude': dist['longitude'],
                    'cities': list(cities)
                })
            data.append({
                'id': gov['id'],
                'name': gov['name'],
                'latitude': gov['latitude'],
                'longitude': gov['longitude'],
                'districts': district_list
            })
        
        return Response(data)


# ============================================
# CONTACT OWNER API
# ============================================
class ContactOwnerView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        model_name = request.data.get('model')
        object_id = request.data.get('object_id')
        message = request.data.get('message', '')
        
        if not model_name or not object_id:
            return Response({'error': 'model and object_id required'}, status=400)
        
        try:
            model = apps.get_model('oman_app', model_name.capitalize())
            item = get_object_or_404(model, id=object_id)
            
            if not hasattr(item, 'user'):
                return Response({'error': 'This item has no owner'}, status=400)
            
            if item.user == request.user:
                return Response({'error': 'You cannot message yourself'}, status=400)
            
            chat = ChatMessage.objects.create(
                sender=request.user,
                receiver=item.user,
                message=message,
                product_id=item.id,
                product_type=model_name.lower()
            )
            
            return Response({
                'success': True,
                'message': 'Message sent to owner',
                'chat_id': chat.id
            })
        except LookupError:
            return Response({'error': 'Invalid model name'}, status=400)
        
# ============================================
# ADD THESE TO YOUR EXISTING api_views.py
# ============================================

# Import these at the top
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, CreateAPIView
from django.contrib.auth import authenticate, logout
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q, Count
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from oman_app.models import *
from .serializers import *
from .utils import *


# ============================================
# 1. EMAIL OTP ENDPOINTS
# ============================================

class EmailOTPSendView(GenericAPIView):
    """Send OTP to email for verification"""
    permission_classes = [AllowAny]
    serializer_class = EmailOTPSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            # Check if email already registered
            if User.objects.filter(email=email).exists():
                return Response(
                    {'error': 'Email already registered'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            
            # Store in session
            request.session['otp'] = otp
            request.session['otp_email'] = email
            request.session['otp_created_at'] = timezone.now().timestamp()
            
            # Send email
            subject = f"Your Zoqo Verification Code"
            message = f"""
            Hello,
            
            Your verification code is: {otp}
            
            This code will expire in 5 minutes.
            
            If you didn't request this, please ignore this email.
            
            Best regards,
            Zoqo Team
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return Response({'success': True, 'message': 'OTP sent to your email'})
            except Exception as e:
                return Response(
                    {'error': f'Failed to send OTP: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EmailOTPVerifyView(GenericAPIView):
    """Verify OTP and complete registration"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')
        username = request.data.get('username')
        password = request.data.get('password')
        phone = request.data.get('phone')
        user_type = request.data.get('user_type', 'regular')
        
        # Validate required fields
        if not all([email, otp, username, password]):
            return Response(
                {'error': 'Email, OTP, username, and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check OTP
        session_otp = request.session.get('otp')
        session_email = request.session.get('otp_email')
        otp_created_at = request.session.get('otp_created_at')
        
        if not session_otp or not session_email or not otp_created_at:
            return Response(
                {'error': 'OTP session expired. Please request a new OTP.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if OTP expired (5 minutes)
        if timezone.now().timestamp() - otp_created_at > 300:
            return Response(
                {'error': 'OTP expired. Please request a new OTP.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if session_email != email or session_otp != otp:
            return Response(
                {'error': 'Invalid OTP'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if user already exists
        if User.objects.filter(username=username).exists():
            return Response(
                {'error': 'Username already taken'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'Email already registered'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create user
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                phone=phone,
                user_type=user_type,
                is_active=True
            )
            
            # Clear OTP session
            del request.session['otp']
            del request.session['otp_email']
            del request.session['otp_created_at']
            
            # Return user data
            serializer = UserSerializer(user)
            return Response({
                'success': True,
                'message': 'Registration successful',
                'user': serializer.data
            })
            
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# ============================================
# 2. PASSWORD RESET ENDPOINTS
# ============================================

class PasswordResetRequestView(GenericAPIView):
    """Request password reset OTP"""
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response(
                    {'error': 'No user found with this email'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Generate OTP
            otp = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            
            # Store in session
            request.session['reset_otp'] = otp
            request.session['reset_email'] = email
            request.session['reset_otp_created_at'] = timezone.now().timestamp()
            
            # Send email
            subject = "Password Reset Request - Zoqo"
            message = f"""
            Hello {user.username},
            
            You requested to reset your password.
            
            Your verification code is: {otp}
            
            This code will expire in 10 minutes.
            
            If you didn't request this, please ignore this email.
            
            Best regards,
            Zoqo Team
            """
            
            try:
                send_mail(
                    subject,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                    fail_silently=False,
                )
                return Response({'success': True, 'message': 'OTP sent to your email'})
            except Exception as e:
                return Response(
                    {'error': f'Failed to send OTP: {str(e)}'},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(GenericAPIView):
    """Confirm OTP and reset password"""
    permission_classes = [AllowAny]
    serializer_class = PasswordResetConfirmSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            new_password = serializer.validated_data['new_password']
            
            # Check OTP
            session_otp = request.session.get('reset_otp')
            session_email = request.session.get('reset_email')
            otp_created_at = request.session.get('reset_otp_created_at')
            
            if not session_otp or not session_email or not otp_created_at:
                return Response(
                    {'error': 'OTP session expired. Please request a new OTP.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Check if OTP expired (10 minutes)
            if timezone.now().timestamp() - otp_created_at > 600:
                return Response(
                    {'error': 'OTP expired. Please request a new OTP.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            if session_email != email or session_otp != otp:
                return Response(
                    {'error': 'Invalid OTP'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                
                # Clear session
                del request.session['reset_otp']
                del request.session['reset_email']
                del request.session['reset_otp_created_at']
                
                return Response({
                    'success': True,
                    'message': 'Password reset successfully'
                })
                
            except User.DoesNotExist:
                return Response(
                    {'error': 'User not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================
# 3. USERNAME CHANGE
# ============================================

class ChangeUsernameView(GenericAPIView):
    """Change username"""
    permission_classes = [IsAuthenticated]
    serializer_class = UsernameChangeSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            new_username = serializer.validated_data['new_username']
            
            # Check if username taken
            if User.objects.filter(username=new_username).exclude(id=request.user.id).exists():
                return Response(
                    {'error': 'Username already taken'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            request.user.username = new_username
            request.user.save()
            
            return Response({
                'success': True,
                'message': 'Username updated successfully',
                'username': new_username
            })
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================
# 4. LOGOUT
# ============================================

class LogoutView(APIView):
    """Logout user"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        # If using token authentication
        if hasattr(request.user, 'auth_token'):
            request.user.auth_token.delete()
        
        logout(request)
        return Response({'success': True, 'message': 'Logged out successfully'})


# ============================================
# 5. FAVORITES WITH PRODUCT DETAILS
# ============================================

class MyFavoritesView(ListAPIView):
    """Get all favorites with product details"""
    permission_classes = [IsAuthenticated]
    serializer_class = FavoriteProductSerializer
    
    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).order_by('-created_at')
    
    @action(detail=False, methods=['get'])
    def check(self, request):
        """Check if a specific listing is favorited"""
        category = request.query_params.get('category')
        listing_id = request.query_params.get('listing_id')
        
        if not category or not listing_id:
            return Response(
                {'error': 'category and listing_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        model = get_model_for_category(category)
        if not model:
            return Response(
                {'error': 'Invalid category'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product = model.objects.get(id=listing_id)
            content_type = ContentType.objects.get_for_model(product)
            is_favorited = Favorite.objects.filter(
                user=request.user,
                content_type=content_type,
                object_id=product.id
            ).exists()
            
            return Response({'is_favorited': is_favorited})
        except model.DoesNotExist:
            return Response(
                {'error': 'Listing not found'},
                status=status.HTTP_404_NOT_FOUND
            )


# ============================================
# 6. CHAT ENHANCEMENTS
# ============================================

class ChatListView(ListAPIView):
    """Get all chats with preview for current user"""
    permission_classes = [IsAuthenticated]
    serializer_class = ChatListSerializer
    
    def get_queryset(self):
        user = self.request.user
        
        # Get all users the current user has chatted with
        chat_users = User.objects.filter(
            Q(sent_messages__receiver=user) |
            Q(received_messages__sender=user)
        ).distinct()
        
        results = []
        
        for other_user in chat_users:
            if other_user == user:
                continue
            
            # Get last message
            last_message = ChatMessage.objects.filter(
                Q(sender=user, receiver=other_user) |
                Q(sender=other_user, receiver=user)
            ).order_by('-timestamp').first()
            
            if not last_message:
                continue
            
            # Count unread messages
            unread_count = ChatMessage.objects.filter(
                sender=other_user,
                receiver=user,
                is_read=False
            ).count()
            
            # Check if it's a product chat
            product_id = last_message.product_id
            product_type = last_message.product_type
            product_title = None
            product_image = None
            
            if product_id and product_type:
                model = get_model_for_category(product_type)
                if model:
                    try:
                        product = model.objects.get(id=product_id)
                        product_title = get_listing_title(product)
                        product_image = get_listing_image(product)
                    except:
                        pass
            
            # Generate chat session ID
            user_ids = sorted([str(user.id), str(other_user.id)])
            if product_id and product_type:
                chat_session_id = f"{user_ids[0]}_{user_ids[1]}_{product_type}_{product_id}"
            else:
                chat_session_id = f"{user_ids[0]}_{user_ids[1]}_general"
            
            results.append({
                'user_id': other_user.id,
                'username': other_user.username,
                'user_image': other_user.image.url if other_user.image else None,
                'last_message': last_message.message,
                'last_message_time': last_message.timestamp,
                'unread_count': unread_count,
                'chat_session_id': chat_session_id,
                'product_id': product_id,
                'product_type': product_type,
                'product_title': product_title,
                'product_image': product_image,
            })
        
        # Sort by last message time
        results.sort(key=lambda x: x['last_message_time'], reverse=True)
        return results


class ChatMessagesView(ListAPIView):
    """Get messages for a specific chat session"""
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer
    
    def get_queryset(self):
        user = self.request.user
        other_user_id = self.kwargs.get('user_id')
        product_type = self.request.query_params.get('product_type')
        product_id = self.request.query_params.get('product_id')
        
        other_user = get_object_or_404(User, id=other_user_id)
        
        # Build query
        query = Q(sender=user, receiver=other_user) | Q(sender=other_user, receiver=user)
        
        # Filter by product if specified
        if product_type and product_id:
            query &= Q(product_type=product_type, product_id=product_id)
        else:
            query &= Q(product_id__isnull=True, product_type__isnull=True)
        
        return ChatMessage.objects.filter(query).order_by('timestamp')
    
    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        
        # Mark messages as read
        other_user_id = self.kwargs.get('user_id')
        other_user = get_object_or_404(User, id=other_user_id)
        product_type = self.request.query_params.get('product_type')
        product_id = self.request.query_params.get('product_id')
        
        # Build query for marking read
        query = Q(sender=other_user, receiver=request.user, is_read=False)
        if product_type and product_id:
            query &= Q(product_type=product_type, product_id=product_id)
        else:
            query &= Q(product_id__isnull=True, product_type__isnull=True)
        
        ChatMessage.objects.filter(query).update(is_read=True)
        
        return response


class SendMessageView(CreateAPIView):
    """Send a message"""
    permission_classes = [IsAuthenticated]
    serializer_class = ChatMessageSerializer
    
    def perform_create(self, serializer):
        receiver_id = self.request.data.get('receiver_id')
        product_type = self.request.data.get('product_type')
        product_id = self.request.data.get('product_id')
        
        receiver = get_object_or_404(User, id=receiver_id)
        
        serializer.save(
            sender=self.request.user,
            receiver=receiver,
            product_type=product_type,
            product_id=product_id
        )


class MarkChatReadView(APIView):
    """Mark all messages in a chat as read"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        other_user = get_object_or_404(User, id=user_id)
        product_type = request.data.get('product_type')
        product_id = request.data.get('product_id')
        
        # Build query
        query = Q(sender=other_user, receiver=request.user, is_read=False)
        if product_type and product_id:
            query &= Q(product_type=product_type, product_id=product_id)
        else:
            query &= Q(product_id__isnull=True, product_type__isnull=True)
        
        updated = ChatMessage.objects.filter(query).update(is_read=True)
        
        return Response({
            'success': True,
            'marked_read_count': updated
        })


class DeleteChatView(APIView):
    """Delete an entire chat (soft delete for user)"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, user_id):
        other_user = get_object_or_404(User, id=user_id)
        product_type = request.data.get('product_type')
        product_id = request.data.get('product_id')
        
        # Build query
        query = Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request_user)
        if product_type and product_id:
            query &= Q(product_type=product_type, product_id=product_id)
        else:
            query &= Q(product_id__isnull=True, product_type__isnull=True)
        
        messages = ChatMessage.objects.filter(query)
        
        for message in messages:
            message.delete_for_user(request.user)
        
        return Response({
            'success': True,
            'message': 'Chat deleted successfully'
        })


# ============================================
# 7. USER CREDITS & BOOST
# ============================================

class UserCreditsView(RetrieveAPIView):
    """Get user's credit balance"""
    permission_classes = [IsAuthenticated]
    serializer_class = UserCreditsSerializer
    
    def get_object(self):
        return get_or_create_user_credits(self.request.user)


class CreditPackagesView(ListAPIView):
    """Get available credit packages"""
    permission_classes = [AllowAny]
    serializer_class = CreditPackageSerializer
    queryset = CreditPackage.objects.filter(is_active=True).order_by('display_order', 'price_omr')


class BoostListingView(APIView):
    """Boost an existing listing"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = BoostListingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        category = serializer.validated_data['category']
        listing_id = serializer.validated_data['listing_id']
        days = serializer.validated_data.get('days', 7)
        
        # Validate days
        if days not in [7, 14, 30]:
            return Response(
                {'error': 'Invalid boost duration. Choose 7, 14, or 30 days.'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get the listing
        model = get_model_for_category(category)
        if not model:
            return Response(
                {'error': 'Invalid category'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            listing = model.objects.get(id=listing_id, user=request.user)
        except model.DoesNotExist:
            return Response(
                {'error': 'Listing not found or you don\'t own it'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Check if listing is approved
        if hasattr(listing, 'status') and listing.status != 'approved':
            return Response(
                {'error': 'Only approved listings can be boosted'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if already boosted
        existing_boost = BoostUsage.objects.filter(
            user=request.user,
            listing_type=category,
            listing_id=listing_id,
            is_active=True
        ).first()
        
        if existing_boost and existing_boost.is_boost_active():
            return Response(
                {'error': f'Listing is already boosted! Expires in {existing_boost.days_remaining} days'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get user credits
        credits = get_or_create_user_credits(request.user)
        
        # Check if user has enough boost days
        if credits.boost_days_available < days:
            return Response(
                {'error': f'Insufficient boost days. Need {days} days, have {credits.boost_days_available}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Deduct boost days
        success, msg = credits.use_boost_credit(days)
        if not success:
            return Response(
                {'error': msg},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Create or extend boost
        if existing_boost:
            existing_boost.expires_at = timezone.now() + timedelta(days=days)
            existing_boost.is_active = True
            existing_boost.boost_days = days
            existing_boost.save(update_fields=['expires_at', 'is_active', 'boost_days'])
            
            # Update posting_method if exists
            if hasattr(listing, 'posting_method'):
                listing.posting_method = 'boosted'
                listing.save(update_fields=['posting_method'])
            
            message = f'Boost extended by {days} days!'
        else:
            BoostUsage.objects.create(
                user=request.user,
                listing_type=category,
                listing_id=listing_id,
                boost_days=days,
                expires_at=timezone.now() + timedelta(days=days),
                is_active=True
            )
            
            if hasattr(listing, 'posting_method'):
                listing.posting_method = 'boosted'
                listing.save(update_fields=['posting_method'])
            
            message = f'Listing boosted for {days} days!'
        
        # Get updated credit balance
        credits.refresh_from_db()
        
        return Response({
            'success': True,
            'message': message,
            'boost_days_left': credits.boost_days_available,
            'expires_at': (timezone.now() + timedelta(days=days)).isoformat()
        })


# ============================================
# 8. UNIFIED CATEGORY LISTINGS
# ============================================

class UnifiedCategoryListingsView(ListAPIView):
    """Get listings from multiple categories with filters"""
    permission_classes = [AllowAny]
    serializer_class = SearchResultSerializer
    
    def get_queryset(self):
        categories = self.request.query_params.get('categories', '').split(',')
        if not categories or not categories[0]:
            categories = list(CATEGORY_MODEL_MAP.keys())
        
        limit = int(self.request.query_params.get('limit', 20))
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        listing_type = self.request.query_params.get('listing_type')
        city_id = self.request.query_params.get('city')
        sort = self.request.query_params.get('sort', 'newest')
        
        results = []
        
        for category_key in categories:
            category_key = category_key.strip()
            model = get_model_for_category(category_key)
            if not model:
                continue
            
            # Build queryset
            qs = model.objects.filter(status='approved')
            
            # Price filter
            if min_price and hasattr(model, 'price'):
                qs = qs.filter(price__gte=float(min_price))
            if max_price and hasattr(model, 'price'):
                qs = qs.filter(price__lte=float(max_price))
            
            # Listing type filter
            if listing_type and hasattr(model, 'listing_type'):
                qs = qs.filter(listing_type=listing_type)
            
            # City filter
            if city_id and hasattr(model, 'city'):
                qs = qs.filter(city_id=city_id)
            
            # Get items
            for item in qs[:limit]:
                results.append({
                    'id': item.id,
                    'type': category_key,
                    'type_display': get_category_display(category_key),
                    'title': get_listing_title(item),
                    'price': get_listing_price(item),
                    'image': get_listing_image(item),
                    'city': get_listing_city(item),
                    'created_at': getattr(item, 'created_at', timezone.now()),
                    'status': getattr(item, 'status', 'approved'),
                    'user_id': item.user.id if hasattr(item, 'user') and item.user else None,
                    'username': item.user.username if hasattr(item, 'user') and item.user else None,
                })
        
        # Sort results
        if sort == 'price_asc':
            results.sort(key=lambda x: x['price'])
        elif sort == 'price_desc':
            results.sort(key=lambda x: x['price'], reverse=True)
        elif sort == 'oldest':
            results.sort(key=lambda x: x['created_at'])
        else:  # newest
            results.sort(key=lambda x: x['created_at'], reverse=True)
        
        return results[:limit]


class BoostedListingsView(ListAPIView):
    """Get boosted listings across all categories"""
    permission_classes = [AllowAny]
    serializer_class = SearchResultSerializer
    
    def get_queryset(self):
        limit = int(self.request.query_params.get('limit', 20))
        results = []
        
        boosted = get_boosted_listings_all(limit)
        
        for item_data in boosted:
            item = item_data['item']
            category_key = item_data['category']
            
            results.append({
                'id': item.id,
                'type': category_key,
                'type_display': get_category_display(category_key),
                'title': get_listing_title(item),
                'price': get_listing_price(item),
                'image': get_listing_image(item),
                'city': get_listing_city(item),
                'created_at': getattr(item, 'created_at', timezone.now()),
                'status': getattr(item, 'status', 'approved'),
                'user_id': item.user.id if hasattr(item, 'user') and item.user else None,
                'username': item.user.username if hasattr(item, 'user') and item.user else None,
            })
        
        return results[:limit]


# ============================================
# 9. CATEGORY FILTERS DATA
# ============================================

class CategoryFiltersView(APIView):
    """Get available filters for a category"""
    permission_classes = [AllowAny]
    
    def get(self, request, category):
        model = get_model_for_category(category)
        if not model:
            return Response(
                {'error': 'Invalid category'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        filters_data = {
            'category': category,
            'category_display': get_category_display(category),
            'filters': {}
        }
        
        # Get distinct values for filterable fields
        filterable_fields = {
            'make': 'makes',
            'brand': 'brands',
            'model': 'models',
            'year': 'years',
            'condition': 'conditions',
            'fuel_type': 'fuel_types',
            'transmission': 'transmissions',
            'body_type': 'body_types',
            'listing_type': 'listing_types',
            'bedrooms': 'bedrooms',
            'bathrooms': 'bathrooms',
            'furnished': 'furnished_options',
            'category': 'categories',
            'main_category': 'main_categories',
        }
        
        for field, key in filterable_fields.items():
            if hasattr(model, field):
                values = model.objects.filter(status='approved').values_list(field, flat=True).distinct()
                filters_data['filters'][key] = list(values)
        
        # Special handling for price ranges
        if hasattr(model, 'price'):
            price_stats = model.objects.filter(status='approved').aggregate(
                min_price=Min('price'),
                max_price=Max('price'),
                avg_price=Avg('price')
            )
            filters_data['filters']['price_range'] = {
                'min': float(price_stats['min_price']) if price_stats['min_price'] else 0,
                'max': float(price_stats['max_price']) if price_stats['max_price'] else 0,
                'avg': float(price_stats['avg_price']) if price_stats['avg_price'] else 0,
            }
        
        return Response(filters_data)


# ============================================
# 10. PRODUCT REPORTS
# ============================================

class CreateReportView(CreateAPIView):
    """Report a listing"""
    permission_classes = [IsAuthenticated]
    serializer_class = CreateReportSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            category = serializer.validated_data['category']
            listing_id = serializer.validated_data['listing_id']
            reason = serializer.validated_data['reason']
            description = serializer.validated_data.get('description', '')
            
            model = get_model_for_category(category)
            if not model:
                return Response(
                    {'error': 'Invalid category'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                product = model.objects.get(id=listing_id)
            except model.DoesNotExist:
                return Response(
                    {'error': 'Listing not found'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            content_type = ContentType.objects.get_for_model(product)
            
            # Check if user already reported this listing
            existing_report = ProductReport.objects.filter(
                reporter=request.user,
                content_type=content_type,
                object_id=product.id,
                status__in=['pending', 'under_review']
            ).exists()
            
            if existing_report:
                return Response(
                    {'error': 'You have already reported this listing'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Create report
            report = ProductReport.objects.create(
                reporter=request.user,
                content_type=content_type,
                object_id=product.id,
                reason=reason,
                description=description,
                status='pending'
            )
            
            return Response({
                'success': True,
                'message': 'Report submitted successfully',
                'report_id': report.id
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ============================================
# 11. LISTING COMMENTS
# ============================================

class ListingCommentsView(ListAPIView):
    """Get comments for a listing"""
    permission_classes = [IsAuthenticated]
    serializer_class = ListingCommentSerializer
    
    def get_queryset(self):
        category = self.kwargs.get('category')
        listing_id = self.kwargs.get('listing_id')
        
        return ListingComment.objects.filter(
            listing_type=category,
            listing_id=listing_id
        ).order_by('-created_at')
    
    def post(self, request, category, listing_id):
        """Add a comment to a listing (admin only)"""
        if not request.user.is_staff:
            return Response(
                {'error': 'Only admins can add comments'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        model = get_model_for_category(category)
        if not model:
            return Response(
                {'error': 'Invalid category'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            product = model.objects.get(id=listing_id)
        except model.DoesNotExist:
            return Response(
                {'error': 'Listing not found'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        comment_text = request.data.get('comment')
        if not comment_text:
            return Response(
                {'error': 'Comment is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        comment = ListingComment.objects.create(
            listing_type=category,
            listing_id=listing_id,
            user=product.user,
            admin=request.user,
            comment=comment_text,
            is_read=False
        )
        
        serializer = ListingCommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# ============================================
# 12. IMAGE UPLOAD
# ============================================

class UploadImageView(CreateAPIView):
    """Upload an image with watermarking"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        image_file = request.FILES.get('image')
        if not image_file:
            return Response(
                {'error': 'Image file is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Determine which image model to use based on category
        category = request.data.get('category')
        listing_id = request.data.get('listing_id')
        
        if category and listing_id:
            model = get_model_for_category(category)
            if not model:
                return Response(
                    {'error': 'Invalid category'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            try:
                listing = model.objects.get(id=listing_id, user=request.user)
            except model.DoesNotExist:
                return Response(
                    {'error': 'Listing not found or you don\'t own it'},
                    status=status.HTTP_404_NOT_FOUND
                )
            
            # Get the image model for this listing
            image_model = None
            if hasattr(listing, 'images'):
                image_model = listing.images.model
            elif hasattr(listing, 'image_set'):
                image_model = listing.image_set.model
            
            if image_model:
                image_obj = image_model.objects.create(image=image_file)
                listing.images.add(image_obj)
                return Response({
                    'success': True,
                    'image_id': image_obj.id,
                    'url': image_obj.image.url
                })
        
        # Fallback: Upload to generic UploadedImage
        uploaded = UploadedImage.objects.create(image=image_file)
        return Response({
            'success': True,
            'image_id': uploaded.id,
            'url': uploaded.image.url
        })


# ============================================
# 13. RECENTLY VIEWED
# ============================================

class RecentlyViewedView(APIView):
    """Get user's recently viewed listings"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        limit = int(request.query_params.get('limit', 20))
        
        # Get from session
        recently_viewed = request.session.get('recently_viewed', [])
        results = []
        
        for item in recently_viewed[:limit]:
            category = item.get('category')
            listing_id = item.get('id')
            
            if not category or not listing_id:
                continue
            
            model = get_model_for_category(category)
            if not model:
                continue
            
            try:
                listing = model.objects.get(id=listing_id)
                results.append({
                    'id': listing.id,
                    'category': category,
                    'category_display': get_category_display(category),
                    'title': get_listing_title(listing),
                    'price': get_listing_price(listing),
                    'image': get_listing_image(listing),
                    'city': get_listing_city(listing),
                    'status': getattr(listing, 'status', 'unknown'),
                    'viewed_at': item.get('viewed_at'),
                })
            except model.DoesNotExist:
                continue
        
        return Response(results)


# ============================================
# 14. MARK LISTING AS SOLD OUT
# ============================================

class MarkSoldOutView(APIView):
    """Mark a listing as sold out"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        category = request.data.get('category')
        listing_id = request.data.get('listing_id')
        
        if not category or not listing_id:
            return Response(
                {'error': 'category and listing_id are required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        model = get_model_for_category(category)
        if not model:
            return Response(
                {'error': 'Invalid category'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            listing = model.objects.get(id=listing_id, user=request.user)
        except model.DoesNotExist:
            return Response(
                {'error': 'Listing not found or you don\'t own it'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if not hasattr(listing, 'status'):
            return Response(
                {'error': 'This listing type does not support status updates'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if listing.status == 'soldout':
            return Response(
                {'error': 'Listing is already marked as sold out'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        listing.status = 'soldout'
        listing.save()
        
        return Response({
            'success': True,
            'message': 'Listing marked as sold out'
        })