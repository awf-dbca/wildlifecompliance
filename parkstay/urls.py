from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from rest_framework import routers
from parkstay import views, api
from parkstay.admin import admin

from ledger.urls import urlpatterns as ledger_patterns

# API patterns
router = routers.DefaultRouter()
router.register(r'campground_map', api.CampgroundMapViewSet)
router.register(r'campground_map_filter', api.CampgroundMapFilterViewSet)
router.register(r'availability', api.AvailabilityViewSet, 'availability')
router.register(r'availability_ratis', api.AvailabilityRatisViewSet, 'availability_ratis')
router.register(r'campgrounds', api.CampgroundViewSet)
router.register(r'campsites', api.CampsiteViewSet)
router.register(r'campsite_bookings', api.CampsiteBookingViewSet)
router.register(r'promo_areas',api.PromoAreaViewSet)
router.register(r'parks',api.ParkViewSet)
router.register(r'parkentryrate',api.ParkEntryRateViewSet)
router.register(r'features',api.FeatureViewSet)
router.register(r'regions',api.RegionViewSet)
router.register(r'districts',api.DistrictViewSet)
router.register(r'campsite_classes',api.CampsiteClassViewSet)
router.register(r'booking',api.BookingViewSet)
router.register(r'campground_booking_ranges',api.CampgroundBookingRangeViewset)
router.register(r'campsite_booking_ranges',api.CampsiteBookingRangeViewset)
router.register(r'campsite_rate',api.CampsiteRateViewSet)
router.register(r'campsites_stay_history',api.CampsiteStayHistoryViewSet)
router.register(r'campground_stay_history',api.CampgroundStayHistoryViewSet)
router.register(r'rates',api.RateViewset)
router.register(r'closureReasons',api.ClosureReasonViewSet)
router.register(r'openReasons',api.OpenReasonViewSet)
router.register(r'priceReasons',api.PriceReasonViewSet)
router.register(r'maxStayReasons',api.MaximumStayReasonViewSet)
router.register(r'users',api.UsersViewSet)
router.register(r'contacts',api.ContactViewSet)

api_patterns = [
    url(r'^api/profile$',api.GetProfile.as_view(), name='get-profile'),
    url(r'^api/oracle_job$',api.OracleJob.as_view(), name='get-oracle'),
    url(r'^api/bulkPricing', api.BulkPricingView.as_view(),name='bulkpricing-api'),
    url(r'^api/search_suggest', api.search_suggest, name='search_suggest'),
    url(r'^api/create_booking', api.create_booking, name='create_booking'),
    url(r'api/get_confirmation/(?P<booking_id>[0-9]+)/$', api.get_confirmation, name='get_confirmation'),
    url(r'^api/reports/booking_refunds$', api.BookingRefundsReportView.as_view(),name='booking-refunds-report'),
    url(r'^api/',include(router.urls))
]

# URL Patterns
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'', include(api_patterns)),
    url(r'^account/', views.AccountView.as_view(), name='account'),
    url(r'^$', views.ParkstayRoutingView.as_view(), name='ps_home'),
    url(r'^campsites/(?P<ground_id>[0-9]+)/$', views.CampsiteBookingSelector.as_view(), name='campsite_booking_selector'),
    url(r'^availability/$', views.CampsiteAvailabilitySelector.as_view(), name='campsite_availaiblity_selector'),
    #url(r'^ical/campground/(?P<ground_id>[0-9]+)/$', views.CampgroundFeed(), name='campground_calendar'),
    url(r'^dashboard/campgrounds$', views.DashboardView.as_view(), name='dash-campgrounds'),
    url(r'^dashboard/campsite-types$', views.DashboardView.as_view(), name='dash-campsite-types'),
    url(r'^dashboard/bookings/edit/', views.DashboardView.as_view(), name='dash-bookings'),
    url(r'^dashboard/bookings$', views.DashboardView.as_view(), name='dash-bookings'),
    url(r'^dashboard/bulkpricing$', views.DashboardView.as_view(), name='dash-bulkpricing'),
    url(r'^dashboard/', views.DashboardView.as_view(), name='dash'),
    url(r'^booking/abort$', views.abort_booking_view, name='public_abort_booking'),
    url(r'^booking/', views.MakeBookingsView.as_view(), name='public_make_booking'),
    url(r'^mybookings/', views.MyBookingsView.as_view(), name='public_my_bookings'),
    url(r'^success/', views.BookingSuccessView.as_view(), name='public_booking_success'),
    url(r'^map/', views.MapView.as_view(), name='map'),
] + ledger_patterns

if settings.DEBUG:  # Serve media locally in development.
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
