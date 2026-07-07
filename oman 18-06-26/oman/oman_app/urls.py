from django.urls import path, include  
from django.conf import settings
from django.conf.urls.static import static
from .import views
from .views import CustomPasswordResetConfirmView
from django.contrib.auth import views as auth_views

urlpatterns = [
# path('map/', views.map_view, name='map_view'),
path('map1/', views.upload_image, name='upload_image'),
path('clear-recently-viewed/', views.clear_recently_viewed, name='clear_recently_viewed'),
path('', views.index, name='index'),
path('indexarabic', views.indexarabic, name='indexarabic'),
path('car-reports/', views.car_reports_view, name='car_reports'),  # Fixed: was views.car_reports
    path('car-reports/preview/', views.car_report_preview_view, name='car_report_preview'),
path('recently-viewed/', views.recently_viewed_page, name='recently_viewed_page'),
   # Add this to your urlpatterns
path('product-inquiries/<int:product_id>/<str:product_type>/', views.product_inquiries_view, name='product_inquiries'),
    path('car-reports/download/', views.download_report_view, name='download_report'),
    
    path('chat/', views.user_chat_view, name='user_chat_view'),  # No receiver_id
path('chat/<int:receiver_id>/', views.user_chat_view, name='user_chat_view_with_receiver'),
path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),

path('my-cv/', views.my_cv, name='my_cv'),



path('ai-chat/', views.openai_chat_api, name='ai_chat_api'),


# In your urls.py
# Add this line to your urls.py
path('admin/reports/', views.product_reports_admin, name='product_reports_admin'),
path('admin/reports/<int:report_id>/', views.product_report_detail, name='product_report_detail'),  # Add this line
path('admin/reports/<int:report_id>/handle/', views.handle_product_report, name='handle_product_report'),
path('admin/reports/bulk-action/', views.bulk_report_action, name='bulk_report_action'),

 path('get-city-coordinates/', views.get_city_coordinates, name='get_city_coordinates'),
path('get-districts/', views.get_districts, name='get_districts'),
path('get-cities/', views.get_cities, name='get_cities'),
path('chat/<int:receiver_id>/', views.user_chat_view, name='user_chat_view'),
    path('chat/<int:receiver_id>/check-new/', views.check_new_messages, name='check_new_messages'),
    path('chat/<int:receiver_id>/check-chat-exists/', views.check_chat_exists, name='check_chat_exists'),
path('chat/<int:receiver_id>/get-messages/', views.get_chat_messages, name='get_chat_messages'),


path('login/', views.login1, name='login'),
path('loginphone/', views.loginphone, name='loginphone'),


path('sign/', views.sign, name='sign'),
path('cars/<str:make>/', views.car_make, name='car_make'),
path('motorcycles/<str:make>/', views.motorcycle_make, name='motorcycle_make'),
path('heavyvehicles/<str:manufacturer>/', views.heavy_vehicle_manufacturer, name='heavy_vehicle_manufacturer'),
path('boats/<str:manufacturer>/', views.boat_manufacturer, name='boat_manufacturer'),
path('search/', views.search_results, name='search_results'),
path('map-product/<str:product_type>/<int:product_id>/', views.map_product_redirect, name='map_product_redirect'),
path('search-product/<str:product_type>/<int:product_id>/',views.search_product_redirect,name='search_product_redirect'),
path('motors/', views.index2, name='index2'),
path('realestate/', views.index3, name='index3'),
path('job/', views.job, name='job'),
path('othercategories/', views.index5, name='index5'),
path('mobiles/', views.index6, name='index6'),
path('mobilelist/', views.mobilelist, name='mobilelist'),
path('services/', views.index4, name='index4'),
path('details/<str:category>/<int:id>/', views.mobiledetails, name='mobiledetails'),

#property
path('villas', views.villa, name='villa'),
path('land', views.land, name='land'),
path('commercial', views.commercial, name='commercial'),
path('farm', views.farm, name='farm'),
path('chalet', views.chalet, name='chalet'),
path('browseads2/<str:category>/<int:id>/', views.browseads2, name='browseads2'),

#property_details
path('farm/<int:id>/', views.farm_details, name='farm_details'),
path('villa/<int:id>/', views.villa_details, name='villa_details'),
path('land/<int:id>/', views.land_details, name='land_details'),
path('commercial/<int:id>/', views.commercial_details, name='commercial_details'),
path('chalet/<int:id>/', views.chalet_details, name='chalet_details'),

#classifieds
path('computer', views.computer, name='computer'),
path('computer/<int:id>/', views.computer_details, name='computer_details'),
path('electronics', views.electronics, name='electronics'),
path('electronics/<int:id>/', views.electronics_details, name='electronics_details'),
path('homeappliance', views.homeappliance, name='homeappliance'),
path('homeappliance/<int:id>/', views.homeappliance_details, name='homeappliance_details'),
path('business', views.business, name='business'),
path('business/<int:id>/', views.business_details, name='business_details'),
path('pet', views.pet, name='pet'),
path('pet/<int:id>/', views.pet_details, name='pet_details'),
path('lostfound/', views.lostfound, name='lostfound'),
path('lostfound/<int:id>/', views.lostfound_details, name='lostfound_details'),
path('jewelry/', views.jewelry, name='jewelry'),
path('jewelry/<int:id>/', views.jewelry_details, name='jewelry_details'),
path('camera/', views.camera, name='camera'),
path('camera/<int:id>/', views.camera_details, name='camera_details'),
path('clothing/', views.clothing, name='clothing'),
path('clothing/<int:id>/', views.clothing_details, name='clothing_details'),
path('sports', views.sports, name='sports'),
path('sports/<int:id>/', views.sports_details, name='sports_details'),
path('musical', views.musical, name='musical'),
path('musical/<int:id>/', views.musical_details, name='musical_details'),
path('babyitem', views.babyitem, name='babyitem'),
path('babyitem/<int:id>/', views.babyitem_details, name='babyitem_details'),
path('ticket', views.ticket, name='ticket'),
path('ticket/<int:id>/', views.ticket_details, name='ticket_details'),
path('collectible', views.collectible, name='collectible'),
path('collectible/<int:id>/', views.collectible_details, name='collectible_details'),
path('book', views.book, name='book'),
path('book/<int:id>/', views.book_details, name='book_details'),
path('dvd', views.dvd, name='dvd'),
path('dvd/<int:id>/', views.dvd_details, name='dvd_details'),
path('music', views.music, name='music'),
path('music/<int:id>/', views.music_details, name='music_details'),
path('toys', views.toys, name='toys'),
path('toys/<int:id>/', views.toys_details, name='toys_details'),
path('furniture', views.furniture, name='furniture'),
path('furniture/<int:id>/', views.furniture_details, name='furniture_details'),
path('gaming', views.gaming, name='gaming'),
path('gaming/<int:id>/', views.gaming_details, name='gaming_details'),

#electronics
path('mobiles', views.mobiles, name='mobiles'),
path('tablets', views.tablets, name='tablets'),
path('smartwatch', views.smartwatch, name='smartwatch'),
path('headset', views.headset,name='headset'),
path('cover', views.cover,name='cover'),
path('accessory', views.accessory,name='accessory'),
path('mobilesim', views.mobilesim,name='mobilesim'),
path('sounds', views.sounds, name='sounds'),



#electronics_details
path('mobiles/<int:id>/', views.mobiles_details, name='mobiles_details'),
path('tablets/<int:id>/', views.tablets_details, name='tablets_details'),
path('smartwatch/<int:id>/', views.smartwatch_details, name='smartwatch_details'),
path('headset/<int:id>/', views.headset_details, name='headset_details'),
path('cover/<int:id>/', views.cover_details, name='cover_details'),
path('accessory/<int:id>/', views.accessory_details, name='accessory_details'),
path('mobilesim/<int:id>/', views.mobilesim_details, name='mobilesim_details'),
path('sounds/<int:id>/', views.sounds_details, name='sounds_details'),

#community
path('autoservices/', views.autoservices, name='autoservices'),
path('consultancy/', views.consultancy, name='consultancy'),
path('domestic/', views.domestic, name='domestic'),
path('events/', views.events, name='events'),
path('health/', views.health, name='health'),
path('homemaintenance/', views.homemaintenance, name='homemaintenance'),
path('movers/', views.movers, name='movers'),
path('otherservices/',views.otherservices,name='otherservices'),
path('restoration/', views.restoration, name='restoration'),
path('tutor/', views.tutor, name='tutor'),
path('webservice/', views.webservice, name='webservice'),
path('freelancer/', views.freelancer, name='freelancer'),

#community_details
path('autoservices/<int:id>/', views.autoservices_details, name='autoservices_details'),
path('consultancy/<int:id>/', views.consultancy_details, name='consultancy_details'),
path('domestic/<int:id>/', views.domestic_details, name='domestic_details'),
path('events/<int:id>/', views.events_details, name='events_details'),
path('health/<int:id>/', views.health_details, name='health_details'),
path('homemaintenance/<int:id>/', views.homemaintenance_details, name='homemaintenance_details'),
path('freelancer/<int:id>/', views.freelancer_details, name='freelancer_details'),
path('movers/<int:id>/', views.movers_details, name='movers_details'),
path('otherservices/<int:id>/', views.otherservices_details, name='otherservices_details'),
path('restoration/<int:id>/', views.restoration_details, name='restoration_details'),
path('tutor/<int:id>/', views.tutor_details, name='tutor_details'),
path('webservice/<int:id>/', views.webservice_details, name='webservice_details'),

#motors
path('car', views.car, name='car'),
path('car-repair/', views.car_repair, name='car_repair'),
path('motorcycle', views.motorcycle, name='motorcycle'),
path('motorcyclemain', views.motorcyclemain, name='motorcyclemain'),
path('vehiclerent', views.vehiclerent, name='vehiclerent'),
path('scooter', views.scooter, name='scooter'),
path('quadbikes', views.quadbikes, name='quadbikes'),
path('tiresandcaps', views.tiresandcaps, name='tiresandcaps'),
path('helmetclothes', views.helmetclothes, name='helmetclothes'),
path('heavyvehicle', views.heavyvehicle, name='heavyvehicle'),
path('accessoriesparts', views.accessoriesparts, name='accessoriesparts'),
path('boat', views.boat, name='boat'),
path('numberplate', views.numberplate, name='numberplate'),
path('junkcars', views.junkcars, name='junkcars'),

#motors_details
path('car/<int:id>/', views.car_details, name='car_details'),
path('car-repair/<int:id>/', views.car_repair_details, name='car_repair_details'),
path('calculator', views.calculator, name='calculator'),
path('motorcycle/<int:id>/', views.motorcycle_details, name='motorcycle_details'),
path("motorcyclemain/<str:model_type>/<int:id>/", views.motorcyclemain_details, name="motorcyclemain_details"),
path("vehiclerent/<str:model_type>/<int:id>/", views.vehiclerent_details, name="vehiclerent_details"),
path('scooter/<int:id>/', views.scooter_details, name='scooter_details'),
path('quadbikes/<int:id>/', views.quadbikes_details, name='quadbikes_details'),
path('helmetclothes/<int:id>/', views.helmetclothes_details, name='helmetclothes_details'),
path('heavyvehicle/<int:id>/', views.heavyvehicle_details, name='heavyvehicle_details'),
path('accessoriesparts/<int:id>/', views.accessoriesparts_details, name='accessoriesparts_details'),
path('boat/<int:id>/', views.boat_details, name='boat_details'),
path('tiresandcaps/<int:id>/', views.tiresandcaps_details, name='tiresandcaps_details'),
path('numberplate/<int:id>/', views.numberplate_details, name='numberplate_details'),
path('junkcars/<int:id>/', views.junkcars_details, name='junkcars_details'),


path('browse-ads-2/', views.browseads2, name='browse-ads-2'),
path('browse-ads-3/', views.browseads3, name='browse-ads-3'),
path('joblist/', views.joblist, name='joblist'),
path('classifiedlist/', views.classifiedlist, name='classifiedlist'),
path('communitylist', views.communitylist, name='communitylist'),


path('browse-ads-details/', views.browseadsdetails, name='browse-ads-details'),
path('browseads/<str:category>/<int:id>/', views.browseads1, name='browseads1'),
path('jobdetails/', views.jobdetails, name='jobdetails'),
 path('classified/<str:ad_type>/<int:ad_id>/', views.classified_details, name='classified_details'),
 path('classified/<str:ad_type>/<int:ad_id>/', views.classified_details, name='classified_details'),
path('servicedetails/<str:category>/<int:id>/', views.servicedetails, name='servicedetails'),
path('categories/<str:category>/<int:id>/', views.categorydetails, name='categorydetails'),

path('chat/delete-message/<int:message_id>/', views.delete_message, name='delete_message'),
    path('chat/block-user/<int:user_id>/', views.block_user, name='block_user'),
    path('chat/unblock-user/<int:user_id>/', views.unblock_user, name='unblock_user'),
    path('chat/check-block-status/<int:user_id>/', views.check_block_status, name='check_block_status'),
    path('chat/delete-chat/<int:user_id>/', views.delete_chat, name='delete_chat'),  # Add this line
    # In your chat/urls.py
path('check-all-new/', views.check_all_new_messages, name='check_all_new_messages'),
path('chat/<int:user_id>/mark-read/', views.mark_messages_read, name='mark_messages_read'),

 path('chat/product/<str:product_type>/<int:product_id>/', views.chat_product_redirect, name='chat_product_redirect'),
#user
path('profile/<int:user_id>/', views.userprofile, name='userprofile'),
path('job-application/<int:user_id>/', views.jobapplication, name='jobapplication'),
path('listingads/', views.listingads, name='listingads'),
path('account/settings/<int:user_id>/', views.account_settings, name='account_settings'),
path('ads/<int:user_id>/', views.listingadss, name='listingadss'),
path('user/<int:user_id>/listing/', views.adss, name='adss1'),
path('listingclassified/', views.listingclassified, name='listingclassified'),
path('listingsub/', views.listingsub, name='listingsub'),
path('listingsub1/', views.listingsub1, name='listingsub1'),
path('listingcommunity/', views.listingcommunity, name='listingcommunity'),



path('favorites/<int:user_id>/', views.favorites, name='favorites'),
path('listingmobile/', views.listingmobile, name='listingmobile'),

#job
path('jobcategories/', views.jobcategories, name='jobcategories'),
path('jobcategory/<int:category_id>/', views.jobcategorylist, name='jobcategorylist'),
path('company/<int:company_id>/posts/ajax/', views.view_company_posts_ajax, name='view_company_posts_ajax'),
path('jobdetails/<int:user_id>/<int:job_id>/', views.jobdetails, name='jobdetails'),
# ADMIN 

path('admin/',views.admin,name='admin'),
path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
path('adminlogout/',views. logoutadmin,name='adminlogout'),


path('category/', views.category, name='category'),
path('subcategory/', views.subcategory, name='subcategory'),

path('add-to-favorites/<str:product_type>/<int:product_id>/<str:action>/', views.add_to_favorites, name='add_to_favorites'),

path('search-redirect/<str:product_type>/<int:product_id>/', views.search_product_redirect, name='search_redirect'),

# authenticated user reg,login,logout

path('signup/', views.signup_view1, name='signup'),
path('login1/', views.custom_login_view1, name='login1'),
path('logout/', views.custom_logout_view, name='logout'),

# forgot passwrd

path('password_reset/', views.password_reset_view, name='password_reset'),
path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'), 
path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),


path('forgot-username/', views.forgot_username_view, name='forgot_username'),
path('change-username/<uidb64>/<token>/', views.change_username_confirm_view, name='change_username_confirm'),
# user product details
path('product/<str:product_type>/<int:product_id>/', views.product_detail, name='product_detail'),
path('product/<str:product_type>/<int:product_id>/delete/', views.delete_product, name='delete_product'),

# dashboard
path('property/<str:property_type>/<int:pk>/', views.property_detail_view, name='property_detail_view'),
path('automobile/<int:pk>/', views.automobile_detail_view, name='automobile_detail_view'),
path('product-dashboard/', views.product_dashboard, name='product_dashboard'),
path('get_product_details/<str:product_type>/<int:product_id>/', views.get_product_details, name='get_product_details'),

# admin category
path('category/', views.category, name='category'),
path('admin/category/add/', views.add_category, name='add_category'),
path('admin/category/<int:cat_id>/edit/', views.edit_category, name='edit_category'),
path('admin/category/<int:cat_id>/', views.view_category, name='view_category'),
path('admin/category/<int:cat_id>/delete/', views.delete_category, name='delete_category'),

# user admin dashboard
path('user/', views.user, name='user'),
path('admin/user/add/', views.add_user, name='add_user'),
path('admin/user/<int:pk>/edit/', views.edit_user, name='edit_user'),
path('admin/user/<int:user_id>/', views.view_user, name='view_user'),
path('admin/user/<int:user_id>/delete/', views.delete_user, name='delete_user'),

#jobcategory
path('jobcategory/', views.jobcategory, name='jobcategory'),
path('jobpost/', views.jobpost, name='jobpost'),
path('admin/jobcategory/add/', views.add_jobcategory, name='add_jobcategory'),
path('admin/jobcategory/<int:jobcat_id>/edit/', views.edit_jobcategory, name='edit_jobcategory'),
path('admin/jobcategory/<int:jobcat_id>/', views.view_jobcategory, name='view_jobcategory'),
path('admin/jobcategory/<int:jobcat_id>/delete/', views.delete_jobcategory, name='delete_jobcategory'),

#region
path('region/', views.region, name='region'),
path('admin/region/add/', views.add_region, name='add_region'),
path('admin/region/<int:region_id>/edit/', views.edit_region, name='edit_region'),
path('admin/region/<int:region_id>/', views.view_region, name='view_region'),
path('admin/region/<int:region_id>/delete/', views.delete_region, name='delete_region'),

#governate
path('governate/', views.governate, name='governate'),
path('admin/governate/add/', views.add_governate, name='add_governate'),
path('admin/governate/<int:governate_id>/edit/', views.edit_governate, name='edit_governate'),
path('admin/governate/<int:governate_id>/', views.view_governate, name='view_governate'),
path('admin/governate/<int:governate_id>/delete/', views.delete_governate, name='delete_governate'),

path('districts/', views.districts, name='districts'),
path('districts/add/', views.add_district, name='add_district'),
path('districts/<int:district_id>/edit/', views.edit_district, name='edit_district'),
path('districts/<int:district_id>/delete/', views.delete_district, name='delete_district'),

path('cities/', views.cities, name='cities'),
path('cities/add/', views.add_city, name='add_city'),
path('cities/<int:city_id>/edit/', views.edit_city, name='edit_city'),
path('cities/<int:city_id>/delete/', views.delete_city, name='delete_city'),

#nearby_location
path('nearbylocation/', views.nearbylocation, name='nearbylocation'),
path('admin/nearbylocation/add/', views.add_nearbylocation, name='add_nearbylocation'),
path('admin/nearbylocation/<int:nearbylocation_id>/edit/', views.edit_nearbylocation, name='edit_nearbylocation'),
path('admin/nearbylocation/<int:nearbylocation_id>/', views.view_nearbylocation, name='view_nearbylocation'),
path('admin/nearbylocation/<int:nearbylocation_id>/delete/', views.delete_nearbylocation, name='delete_nearbylocation'),

#main_amenities
path('mainamenities/', views.mainamenities, name='mainamenities'),
path('admin/mainamenities/add/', views.add_mainamenities, name='add_mainamenities'),
path('admin/mainamenities/<int:mainamenities_id>/edit/', views.edit_mainamenities, name='edit_mainamenities'),
path('admin/mainamenities/<int:mainamenities_id>/', views.view_mainamenities, name='view_mainamenities'),
path('admin/mainamenities/<int:mainamenities_id>/delete/', views.delete_mainamenities, name='delete_mainamenities'),

#additional_amenities
path('additionalamenities/', views.additionalamenities, name='additionalamenities'),
path('admin/additionalamenities/add/', views.add_additionalamenities, name='add_additionalamenities'),
path('admin/additionalamenities/<int:additionalamenities_id>/edit/', views.edit_additionalamenities, name='edit_additionalamenities'),
path('admin/additionalamenities/<int:additionalamenities_id>/', views.view_additionalamenities, name='view_additionalamenities'),
path('admin/additionalamenities/<int:additionalamenities_id>/delete/', views.delete_additionalamenities, name='delete_additionalamenities'),

#advertisements
path('advertisement/', views.advertisement, name='advertisement'),
path('admin/advertisements/add/', views.add_advertisements, name='add_advertisements'),
path('admin/advertisements/<int:advertisement_id>/edit/', views.edit_advertisements, name='edit_advertisements'),
path('admin/advertisements/<int:advertisement_id>/', views.view_advertisements, name='view_advertisements'),
path('admin/advertisements/<int:advertisement_id>/delete/', views.delete_advertisements, name='delete_advertisements'),



# job we are hiring
path('we_are_hiring/', views.we_are_hiring, name='we_are_hiring'),
path('personal-registration/', views.personal_registration, name='personal_registration'),
path('company-registration/<int:user_id>/', views.register_company, name='company_registration'),
path('dashboard/<int:user_id>/<int:company_id>/', views.company_dashboard, name='company_dashboard'),



# product soldout
path('<str:product_type>/<int:product_id>/soldout/',views.mark_sold_out, name='mark_sold_out'),


  path('chat/', views.user_chat_view, name='user_chat'),                  # main chat page
    path('chat/<int:receiver_id>/', views.user_chat_view, name='user_chat_user'),  # chat with a specific user

    # User-to-admin chat
    path('chat/admin/', views.user_admin_chat_view, name='user_admin_chat'),  # unique path for admin chat

    # Admin-to-user chat
    path('admin/chats/', views.admin_chat_list_view, name='admin_chat_list'),        # list all users/admin chats
    path('admin/chats/<int:user_id>/', views.admin_chat_view, name='admin_chat_view'),  # admin chats with a specific user

# jpb 30-12-24
path('jobdetailsindex/<int:job_id>/', views.job_details_index, name='jobdetailsindex'),
path('job/<int:job_id>/', views.job_details_non_authenticated, name='jobdetailsnon'),
path('jobs/full-time/', views.full_time_jobs, name='full_time_jobs'),
path('jobs/part-time/', views.part_time_jobs, name='part_time_jobs'),
path('job_post/<int:pk>/', views.job_post_detail, name='job_post_detail'),

path('browse-ads-11/<str:category>/<int:id>/', views.browseads11, name='browseads11'),
 

       #  mobiles by brand
path('mobiles/<str:brand>/', views.mobiles_by_brand, name='mobiles_by_brand'),
path('computer/<str:brand>/', views.computer_by_brand, name='computer_by_brand'),
 path('sound/<str:brand>/', views.sound_by_brand, name='sound_by_brand'),

 
 path('cars/<str:make>/', views.car_make, name='car_make'),
path('motorcycle/<str:make>/', views.motorcycle_make, name='motorcycle_make'),
 path('heavy-vehicles/<str:manufacturer>/', views.heavy_vehicle_manufacturer, name='heavy_vehicle'),  
  path('boat/<str:manufacturer>/', views.boat_manufacturer, name='boat'), 

path('company/<int:user_id>/<int:company_id>/edit/', views.edit_company, name='edit_company'),
  path('application/approve/<int:application_id>/', views.approve_application, name='approve_application'),
    path('application/reject/<int:application_id>/', views.reject_application, name='reject_application'),
      path('companies/',views.company_list_view, name='company_list'),
path('delete_company/<int:company_id>/', views.delete_company, name='delete_company'),

path('companies/<int:company_id>/approve/', views.approve_company, name='approve_company'),
    path('companies/<int:company_id>/reject/', views.reject_company, name='reject_company'),
 path('temporary-jobs/', views.temporary_jobs, name='temporary_jobs'),




 path('register/', views.register_driving_training, name='register_driving_training'),

path('driving-training/', views.driving_training, name='driving_training'),
 path('driving/<int:id>/', views.driving_details, name='driving_details'),


path('demo',views.demo,name='demo'),




path('interioroptions/', views.interioroptions, name='interioroptions'),
path('admin/interioroptions/add/', views.add_interioroptions, name='add_interioroptions'),
path('admin/interioroptions/<int:interioroptions_id>/edit/', views.edit_interioroptions, name='edit_interioroptions'),
# path('admin/interioroptions/<int:interioroptions_id>/', views.view_interioroptions, name='view_interioroptions'),
path('admin/interioroptions/<int:interioroptions_id>/delete/', views.delete_interioroptions, name='delete_interioroptions'),


path('exterioroptions/', views.exterioroptions, name='exterioroptions'),
path('admin/exterioroptions/add/', views.add_exterioroptions, name='add_exterioroptions'),
path('admin/exterioroptions/<int:exterioroptions_id>/edit/', views.edit_exterioroptions, name='edit_exterioroptions'),
# path('admin/interioroptions/<int:interioroptions_id>/', views.view_interioroptions, name='view_interioroptions'),
path('admin/exterioroptions/<int:exterioroptions_id>/delete/', views.delete_exterioroptions, name='delete_exterioroptions'),



path('technologyoptions/', views.technologyoptions, name='technologyoptions'),
path('admin/technologyoptions/add/', views.add_technologyoptions, name='add_technologyoptions'),
path('admin/technologyoptions/<int:technologyoptions_id>/edit/', views.edit_technologyoptions, name='edit_technologyoptions'),
# path('admin/interioroptions/<int:interioroptions_id>/', views.view_interioroptions, name='view_interioroptions'),
path('admin/technologyoptions/<int:technologyoptions_id>/delete/', views.delete_technologyoptions, name='delete_technologyoptions'),




# ---------------------------------------------new--------------------------------------------

path('ForSale/', views.index_sale, name='index_sale'),
path('ForRent/', views.index_rent, name='index_rent'),


path('apartment', views.apartment, name='apartment'),
path('apartment/<int:id>/', views.apartment_details, name='apartment_details'),

path('shared', views.shared, name='shared'),
path('shared/<int:id>/', views.shared_details, name='shared_details'),

path('suits', views.suits, name='suits'),
path('suits/<int:id>/', views.suits_details, name='suits_details'),


path('complex', views.complex, name='complex'),
path('complex/<int:id>/', views.complex_details, name='complex_details'),


path('clinic', views.clinic, name='clinic'),
path('clinic/<int:id>/', views.clinic_details, name='clinic_details'),

path('hotel', views.hostel, name='hostel'),
path('hotel/<int:id>/', views.hostel_details, name='hostel_details'),

path('office', views.office, name='office'),
path('office/<int:id>/', views.office_details, name='office_details'),

path('shop', views.shop, name='shop'),
path('shop/<int:id>/', views.shop_details, name='shop_details'),

path('cafe', views.cafe, name='cafe'),
path('cafe/<int:id>/', views.cafe_details, name='cafe_details'),

path('staff', views.staff, name='staff'),
path('staff/<int:id>/', views.staff_details, name='staff_details'),

path('warehouse', views.warehouse, name='warehouse'),
path('warehouse/<int:id>/', views.warehouse_details, name='warehouse_details'),

path('townhouse', views.townhouse, name='townhouse'),
path('townhouse/<int:id>/', views.townhouse_details, name='townhouse_details'),

path('fullfloors', views.fullfloors, name='fullfloors'),
path('fullfloors/<int:id>/', views.fullfloors_details, name='fullfloors_details'),

path('showrooms', views.showrooms, name='showrooms'),
path('showrooms/<int:id>/', views.showrooms_details, name='showrooms_details'),

path('wholebuilding', views.wholebuilding, name='wholebuilding'),
path('wholebuilding/<int:id>/', views.wholebuilding_details, name='wholebuilding_details'),

path('supermarket', views.supermarket, name='supermarket'),
path('supermarket/<int:id>/', views.supermarket_details, name='supermarket_details'),

path('factory', views.factory, name='factory'),
path('factory/<int:id>/', views.factory_details, name='factory_details'),

path('foreign', views.foreign, name='foreign'),
path('foreign/<int:id>/', views.foreign_details, name='foreign_details'),


path('edit-jobseeker/', views.edit_jobseeker, name='edit_jobseeker'),

path('jobseekers/', views.jobseeker_list, name='jobseeker_list'),
# urls.py
path('jobseeker/<int:pk>/<int:profile_pk>/', views.jobseeker_detail, name='jobseeker_detail'),
    
path('profile/delete/<int:profile_id>/', views.delete_profile, name='delete_profile'),
 path('add-custom-skill/', views.add_custom_skill, name='add_custom_skill'),
 path('delete-jobseeker-profile/', views.delete_jobseeker_profile, name='delete_jobseeker_profile'),


path('user/<int:user_id>/listings/', views.user_listings, name='user_listings'),
path('jobhome/', views.job_home, name='job_home'),
path('jobseekers1/', views.jobseekers_home, name='jobseekers_home'),
path('jobseekers1/', views.jobseekers_home, name='jobseekers_home'),

path('user/<int:user_id>/follow/', views.follow_user, name='follow_user'),
    path('user/<int:user_id>/unfollow/', views.unfollow_user, name='unfollow_user'),
    path('user/<int:user_id>/listings/', views.user_listings, name='user_listings'),

# ------------------------------------------------------------------ADMIN-----------------------------------------------------------------
path('admin/chat-monitor/', views.admin_chat_monitor, name='admin_chat_monitor'),
path('admin/chat-monitor/user/<int:user_id>/', views.admin_user_chats, name='admin_user_chats'),
path('admin/chat-monitor/message/<int:message_id>/delete/', views.admin_delete_message, name='admin_delete_message'),
path('admin/chat-monitor/stats/', views.admin_chat_stats, name='admin_chat_stats'),


path('admin/block-user/<int:user_id>/', views.admin_block_user, name='admin_block_user'),
path('admin/unblock-user/<int:user_id>/', views.admin_unblock_user, name='admin_unblock_user'),
path('admin/check-block-status/<int:user_id>/', views.admin_check_block_status, name='admin_check_block_status'),

# Blocked Users List
path('admin/blocked-users/', views.admin_blocked_users, name='admin_blocked_users'),
path('admin/chat-analytics/', views.admin_chat_analytics, name='admin_chat_analytics'),

# ---------------------------------FAQ----------------------------------------------------


path('faq/', views.faq_list, name='faq_list'),
    path('faq/add/', views.add_faq, name='add_faq'),
    path('faq/edit/<int:id>/', views.edit_faq, name='edit_faq'),
    path('faq/delete/<int:id>/', views.delete_faq, name='delete_faq'),
    path('faq/toggle/<int:id>/', views.toggle_faq_status, name='toggle_faq_status'),

    # Public FAQ Page
    path('faqs/', views.public_faq, name='public_faq'),


# ----------------------------------Blog-----------------------------------------------------


 path('blog/', views.blog_list, name='blog_list'),
    path('blog/add/', views.add_blog, name='add_blog'),
    path('blog/edit/<int:id>/', views.edit_blog, name='edit_blog'),
    path('blog/delete/<int:id>/', views.delete_blog, name='delete_blog'),
    path('blog/toggle/<int:id>/', views.toggle_blog_status, name='toggle_blog_status'),

    # Public Blog
    path('blogs/', views.public_blog, name='public_blog'),
    path('blog/<int:id>/', views.public_blog_detail, name='public_blog_detail'),

# -------------------------------------------------------Banner Slider -------------------------------------------------------

path('admin/banner/', views.banner_list, name='banner_list'),
    path('admin/banner/add/', views.add_banner, name='add_banner'),
    path('admin/banner/edit/<int:id>/', views.edit_banner, name='edit_banner'),
    path('admin/banner/delete/<int:id>/', views.delete_banner, name='delete_banner'),
    path('admin/banner/toggle/<int:id>/', views.toggle_banner_status, name='toggle_banner_status'),

path('property/<str:property_type>/<int:pk>/', views.property_detail_view, name='property_detail'),
    
    # Edit page URL
    path('property/<str:property_type>/<int:pk>/edit/', views.property_edit_view, name='property_edit'),
    
    # Delete URL
    path('property/<str:property_type>/<int:pk>/delete/', views.property_delete_view, name='property_delete'),



    path('admin/analytics/', views.ad_analytics, name='ad_analytics'),
    
    # User Analytics (Admin can view any user)
    path('admin/analytics/user/<int:user_id>/', views.user_ad_analytics, name='admin_user_analytics'),
    
    # User's own analytics
    path('my-analytics/', views.user_ad_analytics, name='my_analytics'),


path('advertisements/toggle/<int:advertisement_id>/', views.toggle_advertisement_status, name='toggle_advertisement'),
path('advertisements/delete/<int:advertisement_id>/', views.delete_advertisements, name='delete_advertisements'),
path('advertisements/bulk-action/', views.bulk_advertisement_action, name='bulk_advertisement_action'),


    path('payments/', views.payments_dashboard, name='payments_dashboard'),
    
    # Individual Views
    path('payments/transactions/', views.view_transactions, name='view_transactions'),
    path('payments/refunds/', views.refund_management, name='refund_management'),
    path('payments/subscriptions/', views.subscription_plans, name='subscription_plans'),
    path('payments/boosted-pricing/', views.boosted_ads_pricing, name='boosted_ads_pricing'),
    path('payments/coupons/', views.coupon_codes, name='coupon_codes'),
    path('payments/commissions/', views.commission_management, name='commission_management'),
    path('payments/invoices/', views.invoice_generation, name='invoice_generation'),
    path('payments/gateway-logs/', views.payment_gateway_logs, name='payment_gateway_logs'),


    path('admin/dashboard/', views.admin_dashboard_overview, name='admin_dashboard_overview'),


   path('admin/activity-log/', views.user_activity_log, name='user_activity_log'),
path('admin/activity-log/user/<int:user_id>/', views.user_activity_detail, name='user_activity_detail'),
path('admin/activity-log/model/<str:model_name>/<int:object_id>/', views.model_activity_detail, name='model_activity_detail'),

path("suspend-user/", views.suspend_user, name="suspend_user"),
path("unsuspend-user/<int:id>/", views.unsuspend_user, name="unsuspend_user"),



    path('notifications_dashboard/', views.notifications_dashboard, name='dashboard'),
    path('notifications_dashboard/push/', views.push_notifications, name='push_notifications'),
    path('notifications_dashboard/email-templates/', views.email_templates, name='email_templates'),
    path('notifications_dashboard/sms-templates/', views.sms_templates, name='sms_templates'),
    path('notifications_dashboard/broadcast/', views.announcement_broadcast, name='announcement_broadcast'),
    path('notifications_dashboard/alerts/', views.automated_alerts, name='automated_alerts'),



    # ------------------------------------------------------------------Report----------------------------------------------


# Add the following URL patterns to your main `urls.py`:

# Analytics & Reports
path('admin/analytics/export/', views.export_data_view, name='export_data'),
path('admin/analytics/revenue/', views.revenue_report_view, name='revenue_report'),
path('admin/analytics/user-activity/', views.user_activity_report_view, name='user_activity_report'),
path('admin/analytics/category-performance/', views.category_performance_view, name='category_performance'),
path('admin/analytics/marketing-performance/', views.marketing_performance_view, name='marketing_performance'),
path('admin/analytics/conversion-tracking/', views.conversion_tracking_view, name='conversion_tracking'),




# -------------------------Sub Admin---------------------------------------------------------
 path('admin/subadmins/', views.subadmin_list, name='subadmin_list'),
    path('admin/subadmins/create/', views.subadmin_create, name='subadmin_create'),
    path('admin/subadmins/<int:subadmin_id>/edit/', views.subadmin_edit, name='subadmin_edit'),
    path('admin/subadmins/<int:subadmin_id>/delete/', views.subadmin_delete, name='subadmin_delete'),
    
    # Permission management
    path('admin/subadmins/permissions/', views.subadmin_permissions_list, name='subadmin_permissions_list'),
    path('admin/subadmins/permissions/create/', views.subadmin_permission_create, name='subadmin_permission_create'),
    path('admin/subadmins/permissions/<int:perm_id>/edit/', views.subadmin_permission_edit, name='subadmin_permission_edit'),
     path('admin/subadmins/permissions/<int:perm_id>/delete/', views.subadmin_permission_delete, name='subadmin_permission_delete'),  # Add this line
    # Sub-admin dashboard
    path('subadmin/dashboard/', views.subadmin_dashboard, name='subadmin_dashboard'),

    
 path('subadmin/login/', views.subadmin_login_view, name='subadmin_login'),
    
    # Sub-admin dashboard (protected)
    path('subadmin/dashboard/', views.subadmin_dashboard, name='subadmin_dashboard'),



    path('offers/', views.offers_list, name='offers_list'),
    path('offers/add/', views.add_offer, name='add_offer'),
    path('offers/edit/<int:id>/', views.edit_offer, name='edit_offer'),
    path('offers/delete/<int:id>/', views.delete_offer, name='delete_offer'),


    # -----------------------------------------------------Staff Reset --------------------------------------------------

    path('admin/users/reset-password/<int:user_id>/', views.admin_reset_user_password, name='admin_reset_user_password'),
    
    # Legacy success URL (redirects to user list)
    path('admin/users/reset-password-success/', views.admin_reset_password_success, name='admin_reset_password_success'),



    path('admin/edit/<str:property_type>/<int:pk>/', views.universal_edit_view, name='universal_edit'),
    
    # Universal update view
    path('admin/update/<str:property_type>/<int:pk>/', views.universal_update_view, name='universal_update'),
    
    
path('admin/exclusive-listings/', views.exclusive_listings, name='exclusive_listings'),

path('offers/gallery/', views.offers_gallery, name='offers_gallery'),
path('resend-otp/', views.resend_otp, name='resend_otp'),



 path('admin/privacy-policy/', views.privacy_policy_list, name='privacy_policy_list'),
    path('admin/privacy-policy/add/', views.add_privacy_policy, name='add_privacy_policy'),
    path('admin/privacy-policy/edit/<int:id>/', views.edit_privacy_policy, name='edit_privacy_policy'),
    path('admin/privacy-policy/delete/<int:id>/', views.delete_privacy_policy, name='delete_privacy_policy'),
    path('admin/privacy-policy/toggle/<int:id>/', views.toggle_privacy_policy_status, name='toggle_privacy_policy_status'),
    
    # Public URL
    path('privacy-policy/', views.public_privacy_policy, name='public_privacy_policy'),


    path('admin/terms/', views.terms_list, name='terms_list'),
    path('admin/terms/add/', views.add_terms, name='add_terms'),
    path('admin/terms/edit/<int:id>/', views.edit_terms, name='edit_terms'),
    path('admin/terms/delete/<int:id>/', views.delete_terms, name='delete_terms'),
    path('admin/terms/toggle/<int:id>/', views.toggle_terms_status, name='toggle_terms_status'),
    
    # Public URLs
    
    path('terms-and-conditions/', views.public_terms, name='public_terms'),
    path('submit-collaboration', views.submit_collaboration, name='submit_collaboration'),
    path('clear-popup-flag/', views.clear_popup_flag, name='clear_popup_flag'),  # for popup closing
    path('complete-profile/', views.complete_profile, name='complete_profile'),


    # About Us URLs
path('admin/aboutus/', views.aboutus_list, name='aboutus_list'),
path('admin/aboutus/add/', views.add_aboutus, name='add_aboutus'),
path('admin/aboutus/edit/<int:id>/', views.edit_aboutus, name='edit_aboutus'),
path('admin/aboutus/delete/<int:id>/', views.delete_aboutus, name='delete_aboutus'),
path('admin/aboutus/toggle/<int:id>/', views.toggle_aboutus_status, name='toggle_aboutus_status'),

# Refund Policy URLs  
path('admin/refundpolicy/', views.refundpolicy_list, name='refundpolicy_list'),
path('admin/refundpolicy/add/', views.add_refundpolicy, name='add_refundpolicy'),
path('admin/refundpolicy/edit/<int:id>/', views.edit_refundpolicy, name='edit_refundpolicy'),
path('admin/refundpolicy/delete/<int:id>/', views.delete_refundpolicy, name='delete_refundpolicy'),
path('admin/refundpolicy/toggle/<int:id>/', views.toggle_refundpolicy_status, name='toggle_refundpolicy_status'),

# Contact Us URLs
path('admin/contactus/', views.contactus_list, name='contactus_list'),
path('admin/contactus/add/', views.add_contactus, name='add_contactus'),
path('admin/contactus/edit/<int:id>/', views.edit_contactus, name='edit_contactus'),
path('admin/contactus/delete/<int:id>/', views.delete_contactus, name='delete_contactus'),
path('admin/contactus/toggle/<int:id>/', views.toggle_contactus_status, name='toggle_contactus_status'),

path('about-us/', views.public_aboutus, name='public_aboutus'),
path('refund-policy/', views.public_refundpolicy, name='public_refundpolicy'),
path('contact-us/', views.public_contactus, name='public_contactus'),


path('credits/packages/', views.credit_packages, name='credit_packages'),
path('credits/my-credits/', views.my_credits, name='my_credits'),
path('credits/buy/<int:package_id>/', views.buy_credits, name='buy_credits'),
path('paymob/webhook/', views.paymob_webhook, name='paymob_webhook'),
path('paymob/success/', views.paymob_success, name='paymob_success'),
path('paymob/cancel/', views.paymob_cancel, name='paymob_cancel'),
path('boost-listing/<str:listing_type>/<int:listing_id>/', views.boost_existing_listing, name='boost_existing_listing'),
path('boost/<str:listing_type>/<int:listing_id>/<int:duration>/', views.boost_existing_listing, name='boost_listing_with_duration'),
path('pay-for-listing/<int:listing_id>/', views.initiate_paymob_payment, name='initiate_paymob_payment'),
path('boost-listing/<str:listing_type>/<int:listing_id>/<int:days>/', views.boost_existing_listing, name='boost_listing_with_days'),

path('repost/<str:product_type>/<int:product_id>/', views.repost_listing, name='repost_listing'),

path('continue-normal-posting/', views.continue_normal_posting, name='continue_normal_posting'),
path('continue-boost-posting/', views.continue_boost_posting, name='continue_boost_posting'),
path('continue-normal-mobile-posting/', views.continue_normal_mobile_posting, name='continue_normal_mobile_posting'),
path('continue-boost-mobile-posting/', views.continue_boost_mobile_posting, name='continue_boost_mobile_posting'),
path('continue-normal-classified-posting/', views.continue_normal_classified_posting, name='continue_normal_classified_posting'),
path('continue-boost-classified-posting/', views.continue_boost_classified_posting, name='continue_boost_classified_posting'),
path('continue-normal-motors-posting/', views.continue_normal_motors_posting, name='continue_normal_motors_posting'),
path('continue-boost-motors-posting/', views.continue_boost_motors_posting, name='continue_boost_motors_posting'),
path('continue-normal-property-posting/', views.continue_normal_property_posting, name='continue_normal_property_posting'),
path('continue-boost-property-posting/', views.continue_boost_property_posting, name='continue_boost_property_posting'),
path('continue-exclusive-property/', views.continue_exclusive_property_posting, name='continue_exclusive_property_posting'),

path('my-listings/edit/<str:model_name>/<int:pk>/', views.user_product_edit, name='user_product_edit'),
path('delete-application/<int:pk>/', views.delete_application, name='delete_application'),



 path('admin/all-comments/', views.admin_all_comments, name='admin_all_comments'),
    path('admin/delete-comment/<int:comment_id>/', views.admin_delete_comment, name='admin_delete_comment'),
    path('admin/toggle-action-required/<int:comment_id>/', views.admin_toggle_action_required, name='admin_toggle_action_required'),
    path('admin/clear-all-comments/', views.admin_clear_all_comments, name='admin_clear_all_comments'),
    path('get-user-comments/<str:listing_type>/<int:listing_id>/', views.get_user_comments, name='get_user_comments'),


 ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)