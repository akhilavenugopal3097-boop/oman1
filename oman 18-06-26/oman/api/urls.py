# api_urls.py - COMPLETE VERSION
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from . import views


# Create router for ViewSets
router = DefaultRouter()

# ============================================
# REAL ESTATE
# ============================================
router.register(r'villas', views.VillaViewSet, basename='villa')
router.register(r'lands', views.LandViewSet, basename='land')
router.register(r'apartments', views.ApartmentViewSet, basename='apartment')
router.register(r'commercials', views.CommercialViewSet, basename='commercial')
router.register(r'farms', views.FarmViewSet, basename='farm')
router.register(r'chalets', views.ChaletViewSet, basename='chalet')
router.register(r'factories', views.FactoryViewSet, basename='factory')
router.register(r'complexes', views.ComplexViewSet, basename='complex')
router.register(r'clinics', views.ClinicViewSet, basename='clinic')
router.register(r'hostels', views.HostelViewSet, basename='hostel')
router.register(r'offices', views.OfficeViewSet, basename='office')
router.register(r'shops', views.ShopViewSet, basename='shop')
router.register(r'cafes', views.CafeViewSet, basename='cafe')
router.register(r'staffs', views.StaffViewSet, basename='staff')
router.register(r'warehouses', views.WarehouseViewSet, basename='warehouse')
router.register(r'townhouses', views.TownhouseViewSet, basename='townhouse')
router.register(r'fullfloors', views.FullfloorsViewSet, basename='fullfloors')
router.register(r'showrooms', views.ShowroomsViewSet, basename='showrooms')
router.register(r'wholebuildings', views.WholebuildingViewSet, basename='wholebuilding')
router.register(r'supermarkets', views.SupermarketViewSet, basename='supermarket')
router.register(r'foreigns', views.ForeignViewSet, basename='foreign')
router.register(r'shareds', views.SharedViewSet, basename='shared')
router.register(r'suits', views.SuitsViewSet, basename='suits')

# ============================================
# MOTORS
# ============================================
router.register(r'cars', views.AutomobileViewSet, basename='car')
router.register(r'motorcycles', views.MotorcycleViewSet, basename='motorcycle')
router.register(r'scooters', views.ScooterViewSet, basename='scooter')
router.register(r'quadbikes', views.QuadbikesViewSet, basename='quadbike')
router.register(r'helmet-clothes', views.HelmetClothesViewSet, basename='helmetclothes')
router.register(r'heavy-vehicles', views.HeavyVehicleViewSet, basename='heavyvehicle')
router.register(r'boats', views.BoatViewSet, basename='boat')
router.register(r'auto-parts', views.AutoAccessoryPartViewSet, basename='autopart')
router.register(r'number-plates', views.NumberPlateViewSet, basename='numberplate')
router.register(r'junk-cars', views.JunkCarViewSet, basename='junkcar')
router.register(r'tires-caps', views.TiresAndCapsViewSet, basename='tirescaps')
router.register(r'car-repairs', views.CarRepairMaintenanceViewSet, basename='carrepair')
router.register(r'driving-trainings', views.DrivingTrainingViewSet, basename='drivingtraining')
router.register(r'sports-cars', views.SportsCarViewSet, basename='sportscar')
router.register(r'parts', views.PartViewSet, basename='part')

# ============================================
# ELECTRONICS
# ============================================
router.register(r'mobiles', views.MobileViewSet, basename='mobile')
router.register(r'tablets', views.TabletViewSet, basename='tablet')
router.register(r'smartwatches', views.SmartWatchViewSet, basename='smartwatch')
router.register(r'headsets', views.HeadsetViewSet, basename='headset')
router.register(r'covers', views.CoverViewSet, basename='cover')
router.register(r'accessories', views.AccessoryViewSet, basename='accessory')
router.register(r'mobile-sims', views.MobileSIMViewSet, basename='mobilesim')
router.register(r'computers', views.ComputerViewSet, basename='computer')
router.register(r'sounds', views.SoundViewSet, basename='sound')

# ============================================
# OTHER CLASSIFIEDS
# ============================================
router.register(r'fashion', views.FashionViewSet, basename='fashion')
router.register(r'toys', views.ToysViewSet, basename='toys')
router.register(r'foods', views.FoodViewSet, basename='food')
router.register(r'fitness', views.FitnessViewSet, basename='fitness')
router.register(r'pets', views.PetViewSet, basename='pet')
router.register(r'books', views.BookViewSet, basename='book')
router.register(r'appliances', views.ApplianceViewSet, basename='appliance')
router.register(r'businesses', views.BusinessViewSet, basename='business')
router.register(r'educations', views.EducationViewSet, basename='education')
router.register(r'services', views.ServiceViewSet, basename='service')

# ============================================
# LISTINGS
# ============================================
router.register(r'computer-listings', views.ComputerListingViewSet, basename='computerlisting')
router.register(r'business-listings', views.BusinessIndustrialListingViewSet, basename='businesslisting')
router.register(r'pet-listings', views.PetListingViewSet, basename='petlisting')
router.register(r'sports-listings', views.SportsListingViewSet, basename='sportslisting')
router.register(r'musical-listings', views.MusicalListingViewSet, basename='musicallisting')
router.register(r'gaming-listings', views.GamingListingViewSet, basename='gaminglisting')
router.register(r'ticket-listings', views.TicketVoucherListingViewSet, basename='ticketlisting')
router.register(r'collectible-listings', views.CollectibleListingViewSet, basename='collectiblelisting')
router.register(r'books-listings', views.BooksListingViewSet, basename='bookslisting')
router.register(r'music-listings', views.MusicListingViewSet, basename='musiclisting')
router.register(r'dvds-listings', views.DVDsMoviesListingViewSet, basename='dvdslisting')
router.register(r'furniture-listings', views.FurnitureHomeGardenListingViewSet, basename='furniturelisting')
router.register(r'baby-listings', views.BabyItemsListingViewSet, basename='babylisting')
router.register(r'toys-listings', views.ToysListingViewSet, basename='toyslisting')
router.register(r'lost-found-listings', views.LostFoundListingViewSet, basename='lostfoundlisting')
router.register(r'camera-listings', views.CameraListingViewSet, basename='cameralisting')
router.register(r'jewelry-listings', views.JewelryListingViewSet, basename='jewelrylisting')
router.register(r'home-appliance-listings', views.HomeApplianceListingViewSet, basename='homeappliancelisting')
router.register(r'clothing-listings', views.ClothingAccessoriesListingViewSet, basename='clothinglisting')
router.register(r'electronics-listings', views.ElectronicsListingViewSet, basename='electronicslisting')

# ============================================
# SERVICES
# ============================================
router.register(r'auto-services', views.AutoServiceListingViewSet, basename='autoservice')
router.register(r'consultancy-services', views.ConsultancyServiceListingViewSet, basename='consultancyservice')
router.register(r'domestic-services', views.DomesticServiceListingViewSet, basename='domesticservice')
router.register(r'event-services', views.EventEntertainmentServiceListingViewSet, basename='eventservice')
router.register(r'health-services', views.HealthWellbeingServiceListingViewSet, basename='healthservice')
router.register(r'home-services', views.HomeMaintenanceServiceListingViewSet, basename='homeservice')
router.register(r'movers-services', views.MoversServiceListingViewSet, basename='moversservice')
router.register(r'restoration-services', views.RestorationServiceListingViewSet, basename='restorationservice')
router.register(r'tutors-services', views.TutorsServiceListingViewSet, basename='tutorsservice')
router.register(r'web-services', views.WebComputerServiceListingViewSet, basename='webservice')
router.register(r'freelancers-services', views.FreelancersServiceListingViewSet, basename='freelancersservice')
router.register(r'other-services', views.OtherServiceListingViewSet, basename='otherservice')

# ============================================
# JOBS
# ============================================
router.register(r'job-categories', views.JobCategoryViewSet, basename='jobcategory')
router.register(r'companies', views.CompanyViewSet, basename='company')
router.register(r'job-posts', views.JobPostViewSet, basename='jobpost')
router.register(r'job-applications', views.JobApplicationViewSet, basename='jobapplication')
router.register(r'job-seekers', views.JobSeekerViewSet, basename='jobseeker')
router.register(r'skills', views.SkillViewSet, basename='skill')

# ============================================
# CHAT
# ============================================
router.register(r'chat-messages', views.ChatMessageViewSet, basename='chatmessage')
router.register(r'blocked-users', views.BlockedUserViewSet, basename='blockeduser')

# ============================================
# LOCATION
# ============================================
router.register(r'regions', views.RegionViewSet, basename='region')
router.register(r'governates', views.GovernateViewSet, basename='governate')
router.register(r'districts', views.DistrictViewSet, basename='district')
router.register(r'cities', views.CitiesViewSet, basename='city')

# ============================================
# AMENITIES
# ============================================
router.register(r'nearby-locations', views.NearbyLocationViewSet, basename='nearbylocation')
router.register(r'main-amenities', views.MainAmenitiesViewSet, basename='mainamenity')
router.register(r'additional-amenities', views.AdditionalAmenitiesViewSet, basename='additionalamenity')
router.register(r'interior-options', views.InteriorOptionsViewSet, basename='interioroption')
router.register(r'exterior-options', views.ExteriorOptionsViewSet, basename='exterioroption')
router.register(r'technology-options', views.TechnologyOptionsViewSet, basename='technologyoption')

# ============================================
# CONTENT MANAGEMENT
# ============================================
router.register(r'advertisements', views.AdvertisementViewSet, basename='advertisement')
router.register(r'banners', views.BannerViewSet, basename='banner')
router.register(r'blogs', views.BlogViewSet, basename='blog')
router.register(r'faqs', views.FAQViewSet, basename='faq')
router.register(r'offers', views.OffersViewSet, basename='offer')
router.register(r'privacy-policies', views.PrivacyPolicyViewSet, basename='privacypolicy')
router.register(r'terms-conditions', views.TermsConditionsViewSet, basename='termsconditions')
router.register(r'about-us', views.AboutUsViewSet, basename='aboutus')
router.register(r'refund-policies', views.RefundPolicyViewSet, basename='refundpolicy')
router.register(r'contact-us', views.ContactUsViewSet, basename='contactus')

# ============================================
# FAVORITES & REPORTS
# ============================================
router.register(r'favorites', views.FavoriteViewSet, basename='favorite')
router.register(r'reports', views.ProductReportViewSet, basename='report')

urlpatterns = [
    # ============================================
    # API ROOT
    # ============================================
    path('', include(router.urls)),
    
    # ============================================
    # AUTHENTICATION
    # ============================================
    path('auth/register/', views.UserRegistrationView.as_view(), name='api-register'),
    path('auth/login/', obtain_auth_token, name='api-login'),
    path('auth/me/', views.CurrentUserView.as_view(), name='api-user-profile'),
    path('auth/users/', views.UserListView.as_view(), name='api-users'),
    path('auth/logout/', views.LogoutView.as_view(), name='api-logout'),
    path('auth/change-username/', views.ChangeUsernameView.as_view(), name='api-change-username'),
    
    # ============================================
    # EMAIL OTP (Email Verification)
    # ============================================
    path('auth/email-otp/send/', views.EmailOTPSendView.as_view(), name='api-email-otp-send'),
    path('auth/email-otp/verify/', views.EmailOTPVerifyView.as_view(), name='api-email-otp-verify'),
    
    # ============================================
    # PASSWORD RESET
    # ============================================
    path('auth/password-reset/request/', views.PasswordResetRequestView.as_view(), name='api-password-reset-request'),
    path('auth/password-reset/confirm/', views.PasswordResetConfirmView.as_view(), name='api-password-reset-confirm'),
    
    # ============================================
    # USER LISTINGS
    # ============================================
    path('user/listings/', views.UserListingsView.as_view(), name='api-user-listings'),
    path('listings/sold-out/', views.MarkSoldOutView.as_view(), name='api-mark-sold-out'),
    
    # ============================================
    # FAVORITES
    # ============================================
    path('favorites/my/', views.MyFavoritesView.as_view(), name='api-my-favorites'),
    path('favorites/check/', views.MyFavoritesView.as_view(), name='api-favorite-check'),
    
    # ============================================
    # CHAT
    # ============================================
    path('chats/', views.ChatListView.as_view(), name='api-chats'),
    path('chats/<int:user_id>/messages/', views.ChatMessagesView.as_view(), name='api-chat-messages'),
    path('chats/<int:user_id>/send/', views.SendMessageView.as_view(), name='api-send-message'),
    path('chats/<int:user_id>/read/', views.MarkChatReadView.as_view(), name='api-mark-chat-read'),
    path('chats/<int:user_id>/delete/', views.DeleteChatView.as_view(), name='api-delete-chat'),
    
    # ============================================
    # CREDITS & BOOST
    # ============================================
    path('credits/balance/', views.UserCreditsView.as_view(), name='api-credits-balance'),
    path('credits/packages/', views.CreditPackagesView.as_view(), name='api-credit-packages'),
    path('boost/', views.BoostListingView.as_view(), name='api-boost-listing'),
    
    # ============================================
    # UNIFIED LISTINGS
    # ============================================
    path('listings/all/', views.UnifiedCategoryListingsView.as_view(), name='api-all-listings'),
    path('listings/boosted/', views.BoostedListingsView.as_view(), name='api-boosted-listings'),
    
    # ============================================
    # SEARCH
    # ============================================
    path('search/', views.GlobalSearchView.as_view(), name='api-search'),
    
    # ============================================
    # FILTERS
    # ============================================
    path('filters/<str:category>/', views.CategoryFiltersView.as_view(), name='api-category-filters'),
    
    # ============================================
    # REPORTS
    # ============================================
    path('reports/create/', views.CreateReportView.as_view(), name='api-create-report'),
    
    # ============================================
    # COMMENTS
    # ============================================
    path('comments/<str:category>/<int:listing_id>/', views.ListingCommentsView.as_view(), name='api-listing-comments'),
    
    # ============================================
    # IMAGE UPLOAD
    # ============================================
    path('upload/image/', views.UploadImageView.as_view(), name='api-upload-image'),
    
    # ============================================
    # RECENTLY VIEWED
    # ============================================
    path('recently-viewed/', views.RecentlyViewedView.as_view(), name='api-recently-viewed'),
    
    # ============================================
    # CONTACT OWNER
    # ============================================
    path('contact/', views.ContactOwnerView.as_view(), name='api-contact'),
    
    # ============================================
    # DASHBOARD STATS
    # ============================================
    path('stats/', views.DashboardStatsView.as_view(), name='api-stats'),
    
    # ============================================
    # LOCATION HIERARCHY
    # ============================================
    path('locations/hierarchy/', views.LocationHierarchyView.as_view(), name='api-locations-hierarchy'),
]