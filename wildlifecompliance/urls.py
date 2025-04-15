import logging
from django.conf import settings
from django.contrib import admin
from django.urls import re_path, include
from django.views.generic.base import TemplateView, RedirectView
from django.conf.urls.static import static
from rest_framework import routers

from wildlifecompliance import views
from wildlifecompliance.components.returns.views import (
    ReturnSuccessView,
    ReturnSheetSuccessView,
)
from wildlifecompliance.components.applications.views import (
    ApplicationSuccessView,
    ApplicationSuccessViewPreload,
    LicenceFeeSuccessView,
)

from wildlifecompliance.components.main.views import (
        SearchKeywordsView,
        SearchReferenceView,
        SearchWeakLinksView,
        CreateWeakLinkView,
        RemoveWeakLinkView,
        GeocodingAddressSearchTokenView,
        SystemPreferenceView,
        )
from wildlifecompliance.components.applications import views as application_views
from wildlifecompliance.components.users import api as users_api
from wildlifecompliance.components.organisations import api as org_api
from wildlifecompliance.components.applications import api as application_api
from wildlifecompliance.components.licences import api as licence_api
from wildlifecompliance.components.returns import api as return_api
from wildlifecompliance.components.wc_payments.views import DeferredInvoicingView, DeferredInvoicingPreviewView
from wildlifecompliance.management.permissions_manager import CollectorManager
from wildlifecompliance.components.call_email import api as call_email_api
from wildlifecompliance.components.offence import api as offence_api
from wildlifecompliance.components.inspection import api as inspection_api
from wildlifecompliance.components.sanction_outcome import api as sanction_outcome_api
from wildlifecompliance.components.main import api as main_api
from wildlifecompliance.components.wc_payments import views as payment_views
from wildlifecompliance.components.legal_case import api as legal_case_api
from wildlifecompliance.components.artifact import api as artifact_api

from wildlifecompliance.management.default_data_manager import DefaultDataManager
from wildlifecompliance.utils import are_migrations_running

from ledger_api_client.urls import urlpatterns as ledger_patterns
from django_media_serv.urls import urlpatterns as media_serv_patterns

logger = logging.getLogger(__name__)

# API patterns
router = routers.DefaultRouter()
router.include_root_view = settings.SHOW_ROOT_API
router.register(r'application', application_api.ApplicationViewSet,'application')
router.register(r'application_selected_activity', application_api.ApplicationSelectedActivityViewSet,'application_selected_activity')
router.register(r'application_paginated', application_api.ApplicationPaginatedViewSet,'application_paginated')
router.register(r'application_conditions', application_api.ApplicationConditionViewSet,'application_conditions')
router.register(r'application_standard_conditions', application_api.ApplicationStandardConditionViewSet,'application_standard_conditions')
router.register(r'assessment', application_api.AssessmentViewSet,'assessment')
router.register(r'assessment_paginated', application_api.AssessmentPaginatedViewSet,'assessment_paginated')
router.register(r'amendment', application_api.AmendmentRequestViewSet,'amendment')
router.register(r'assessor_group', application_api.AssessorGroupViewSet,'assessor_group')
router.register(r'licences', licence_api.LicenceViewSet,'licences')
router.register(r'licences_paginated', licence_api.LicencePaginatedViewSet,'licences_paginated')
router.register(r'licences_class', licence_api.LicenceCategoryViewSet,'licences_class')
router.register(r'licence_available_purposes', licence_api.UserAvailableWildlifeLicencePurposesViewSet,'licence_available_purposes')
router.register(r'returns', return_api.ReturnViewSet,'returns')
router.register(r'returns_paginated', return_api.ReturnPaginatedViewSet,'returns_paginated')
router.register(r'returns_amendment', return_api.ReturnAmendmentRequestViewSet,'returns_amendment')
router.register(r'return_types', return_api.ReturnTypeViewSet,'return_types')
router.register(r'organisations', org_api.OrganisationViewSet,'organisations')
router.register(r'organisations_compliancemanagement', org_api.OrganisationComplianceManagementViewSet,'organisations_compliancemanagement')
router.register(r'organisations_paginated', org_api.OrganisationPaginatedViewSet,'organisations_paginated')
router.register(r'organisation_requests', org_api.OrganisationRequestsViewSet,'organisation_requests')
router.register(r'organisation_requests_paginated', org_api.OrganisationRequestsPaginatedViewSet,'organisation_requests_paginated')
router.register(r'organisation_contacts', org_api.OrganisationContactViewSet,'organisation_contacts')
router.register(r'my_organisations', org_api.MyOrganisationsViewSet,'my_organisations')
router.register(r'users', users_api.UserViewSet,'users')
router.register(r'compliance_management_users', users_api.ComplianceManagementUserViewSet,'compliance_management_users')
router.register(r'users_paginated', users_api.UserPaginatedViewSet,'users_paginated')
#router.register(r'profiles', users_api.ProfileViewSet,'profiles')
#router.register(r'my_profiles', users_api.MyProfilesViewSet,'my_profiles')
router.register(r'emailidentities', users_api.EmailIdentityViewSet,'emailidentities')
router.register(r'call_email', call_email_api.CallEmailViewSet,'call_email')
router.register(r'call_email_location', call_email_api.LocationViewSet,'call_email_location')
router.register(r'classification', call_email_api.ClassificationViewSet,'classification')
router.register(r'lov_collection', call_email_api.LOVCollectionViewSet,'lov_collection')
router.register(r'report_types', call_email_api.ReportTypeViewSet,'report_types')
router.register(r'location', call_email_api.LocationViewSet,'location')
router.register(r'referrers', call_email_api.ReferrerViewSet,'referrers')
router.register(r'search_user', call_email_api.EmailUserViewSet,'search_user')
router.register(r'search_alleged_offences', offence_api.SearchSectionRegulation,'search_alleged_offences')
router.register(r'search_organisation', offence_api.SearchOrganisation,'search_organisation')
router.register(r'map_layers', call_email_api.MapLayerViewSet,'map_layers')
#router.register(r'compliancepermissiongroup', users_api.CompliancePermissionGroupViewSet,'compliancepermissiongroup')
#router.register(r'region_district', users_api.RegionDistrictViewSet,'region_district')
router.register(r'regions', main_api.RegionViewSet,'regions')
router.register(r'districts', main_api.DistrictViewSet,'districts')
router.register(r'legal_case_priorities', legal_case_api.LegalCasePriorityViewSet,'legal_case_priorities')
router.register(r'inspection_types', inspection_api.InspectionTypeViewSet,'inspection_types')
router.register(r'call_email_paginated', call_email_api.CallEmailPaginatedViewSet,'call_email_paginated')
router.register(r'inspection', inspection_api.InspectionViewSet,'inspection')
router.register(r'inspection_paginated', inspection_api.InspectionPaginatedViewSet,'inspection_paginated')
router.register(r'sanction_outcome', sanction_outcome_api.SanctionOutcomeViewSet,'sanction_outcome')
router.register(r'sanction_outcome_paginated', sanction_outcome_api.SanctionOutcomePaginatedViewSet,'sanction_outcome_paginated')
router.register(r'remediation_action', sanction_outcome_api.RemediationActionViewSet,'remediation_action')
router.register(r'offence', offence_api.OffenceViewSet,'offence')
router.register(r'offence_paginated', offence_api.OffencePaginatedViewSet,'offence_paginated')
router.register(r'temporary_document', main_api.TemporaryDocumentCollectionViewSet,'temporary_document')
router.register(r'legal_case', legal_case_api.LegalCaseViewSet,'legal_case')
router.register(r'legal_case_paginated', legal_case_api.LegalCasePaginatedViewSet,'legal_case_paginated')
router.register(r'document_artifact', artifact_api.DocumentArtifactViewSet,'document_artifact')
router.register(r'artifact', artifact_api.ArtifactViewSet,'artifact')
router.register(r'artifact_paginated', artifact_api.ArtifactPaginatedViewSet,'artifact_paginated')
router.register(r'physical_artifact', artifact_api.PhysicalArtifactViewSet,'physical_artifact')
router.register(r'physical_artifact_types', artifact_api.PhysicalArtifactTypeViewSet,'physical_artifact_types')
router.register(r'disposal_methods', artifact_api.PhysicalArtifactDisposalMethodViewSet,'disposal_methods')

router.register(
    r'schema_masterlist',
    main_api.SchemaMasterlistViewSet
)
router.register(
    r'schema_masterlist_paginated', main_api.SchemaMasterlistPaginatedViewSet, 'schema_masterlist_paginated')
router.register(
    r'schema_purpose', main_api.SchemaPurposeViewSet, 'schema_purpose')
router.register(
    r'schema_purpose_paginated', main_api.SchemaPurposePaginatedViewSet, 'schema_purpose_paginated')
router.register(
    r'schema_group', main_api.SchemaGroupViewSet, 'schema_group')
router.register(
    r'schema_group_paginated', main_api.SchemaGroupPaginatedViewSet, 'schema_group_paginated')
router.register(
    r'schema_question', main_api.SchemaQuestionViewSet, 'schema_question')
router.register(
    r'schema_question_paginated', main_api.SchemaQuestionPaginatedViewSet, 'schema_question_paginated')

api_patterns = [re_path(r'^api/my_user_details/$',
                    users_api.GetMyUserDetails.as_view(),
                    name='get-my-user-details'),
                re_path(r'^api/is_compliance_management_callemail_readonly_user$', 
                    users_api.IsComplianceManagementCallEmailReadonlyUser.as_view(), 
                    name='is-compliance-management-callemail-readonly-user'),
                re_path(r'^api/allocated_group_members$', 
                    main_api.AllocatedGroupMembers.as_view(), 
                    name='allocated-group-members'),
                re_path(r'^api/countries$', 
                    users_api.GetCountries.as_view(), 
                    name='get-countries'),
                re_path(r'^api/staff_member_lookup$', 
                    users_api.StaffMemberLookup.as_view(), 
                    name='staff-member-lookup'),
                #re_path(r'^api/department_users$',
                 #   users_api.DepartmentUserList.as_view(),
                  #  name='department-users-list'),
                re_path(r'^api/my_compliance_user_details/$',
                    users_api.GetComplianceUserDetails.as_view(),
                    name='get-my-compliance-user-details'),
                re_path(r'^api/is_new_user/$',
                    users_api.IsNewUser.as_view(),
                    name='is-new-user'),
                re_path(r'^api/user_profile_completed/$',
                    users_api.UserProfileCompleted.as_view(),
                    name='get-user-profile-completed'),
                re_path(r'^api/amendment_request_reason_choices',
                    application_api.AmendmentRequestReasonChoicesView.as_view(),
                    name='amendment_request_reason_choices'),
                re_path(r'^api/return_amendment_request_reason_choices',
                    return_api.ReturnAmendmentRequestReasonChoicesView.as_view(),
                    name='return_amendment_request_reason_choices'),
                re_path(r'^api/empty_list/$',
                    application_api.GetEmptyList.as_view(),
                    name='get-empty-list'),
                re_path(r'^api/organisation_access_group_members',
                    org_api.OrganisationAccessGroupMembers.as_view(),
                    name='organisation-access-group-members'),
                re_path(r'^api/get_organisation_id/$',
                    org_api.GetOrganisationId.as_view(),
                    name='get-organisation-id'),
                re_path(r'^api/search_keywords',
                    SearchKeywordsView.as_view(),
                    name='search_keywords'),
                re_path(r'^api/search_reference',
                    SearchReferenceView.as_view(),
                    name='search_reference'),
                re_path(r'^api/search_weak_links',
                    SearchWeakLinksView.as_view(),
                    name='search_weak_links'),
                re_path(r'^api/create_weak_link',
                    CreateWeakLinkView.as_view(),
                    name='create_weak_link'),
                re_path(r'^api/remove_weak_link',
                    RemoveWeakLinkView.as_view(),
                    name='remove_weak_link'),
                re_path(r'^api/geocoding_address_search_token',
                    GeocodingAddressSearchTokenView.as_view(),
                    name='geocoding_address_search_token'),
                re_path(r'^api/system_preference',
                    SystemPreferenceView.as_view(),
                    name='system_preference'),
                re_path(r'^api/',
                    include(router.urls))]

# URL Patterns
urlpatterns = [
    re_path(r'contact-us/$',
        TemplateView.as_view(
            template_name="wildlifecompliance/contact_us.html"),
        name='wc_contact'),
    re_path(
        r'further-info/$',
        RedirectView.as_view(
            url='https://www.dpaw.wa.gov.au/plants-and-animals/licences-and-permits'),
        name='wc_further_info'),
    re_path(r'^admin/', admin.site.urls, name="admin"),
    #re_path(r'^ledger/admin/', admin.site.urls, name='ledger_admin'),
    re_path(r'^chaining/', include('smart_selects.urls')),
    re_path(r'', include(api_patterns)),
    re_path(r'^$', views.WildlifeComplianceRoutingView.as_view(), name='home'),
    re_path(r'^internal/', views.InternalView.as_view(), name='internal'),
    re_path(r'^external/', views.ExternalView.as_view(), name='external'),
    re_path(r'^external/application/(?P<application_pk>\d+)/$', views.ExternalApplicationView.as_view(), name='external-application-detail'),
    re_path(r'^external/return/(?P<return_pk>\d+)/$', views.ExternalReturnView.as_view(), name='external-return-detail'),
    re_path(r'^firsttime/$', views.first_time, name='first_time'),
    re_path(r'^account/$', views.ExternalView.as_view(), name='manage-account'),
    re_path(r'^organisation/$', views.ExternalView.as_view(), name='organisation'),
    re_path(r'^profiles/', views.ExternalView.as_view(), name='manage-profiles'),
    # re_path(r'^external/organisations/manage/$', views.ExternalView.as_view(), name='manage-org'),
    re_path(r'^application/$',
        application_views.ApplicationView.as_view(),
        name='application'),
    # re_path(r'^organisations/(?P<pk>\d+)/confirm-delegate-access/(?P<uid>[0-9A-Za-z]+)-(?P<token>.+)/$',
    #     views.ConfirmDelegateAccess.as_view(), name='organisation_confirm_delegate_access'),
    re_path('^healthcheck/', views.HealthCheckView.as_view(), name='health_check'),

    # following url is defined so that to include url path when sending
    # call_email emails to users
    re_path(r'^internal/call_email/(?P<call_email_id>\d+)/$', views.ApplicationView.as_view(),
        name='internal-call-email-detail'),
    # following url is defined so that to include url path when sending
    # artifact emails to users
    re_path(r'^internal/object/(?P<artifact_id>\d+)/$', views.ApplicationView.as_view(),
        name='internal-artifact-detail'),

    # following url is defined so that to include url path when sending
    # inspection emails to users
    re_path(r'^internal/inspection/(?P<inspection_id>\d+)/$', views.ApplicationView.as_view(),
        name='internal-inspection-detail'),

    # following url is defined so that to include url path when sending
    # sanction outcome emails to users
    re_path(r'^internal/sanction_outcome/(?P<sanction_outcome_id>\d+)/$', views.ApplicationView.as_view(), name='internal-sanction-outcome-detail'),

    re_path(r'^internal/offence/(?P<offence_id>\d+)/$', views.ApplicationView.as_view(), name='internal-offence-detail'),

    # following url is defined so that to include url path when sending
    # inspection emails to users
    re_path(r'^internal/legal_case/(?P<legal_case_id>\d+)/$', views.ApplicationView.as_view(),
        name='internal-legal-case-detail'),
    re_path(r'^internal/application/(?P<application_pk>\d+)/$', views.ApplicationView.as_view(),
        name='internal-application-detail'),
    re_path(r'^internal/application/assessment/(?P<application_pk>\d+)/$', views.ApplicationView.as_view(),
        name='internal-assessment-detail'),
    re_path(r'^application_submit/submit_with_invoice_preload/(?P<lodgement_number>.+)/',
        ApplicationSuccessViewPreload.as_view(),
        name='external-application-success-invoice-preload'),
    re_path(r'^application_submit/submit_with_invoice/',
        ApplicationSuccessView.as_view(),
        name='external-application-success-invoice'),
    re_path(r'^application/finish_licence_fee_payment/',
        LicenceFeeSuccessView.as_view(),
        name='external-licence-fee-success-invoice'),
    re_path(r'^returns_submit/submit_with_invoice/',
        ReturnSuccessView.as_view(),
        name='external-returns-success-invoice'),
    re_path(r'^returns/finish_sheet_fee_payment/',
        ReturnSheetSuccessView.as_view(),
        name='external-sheet-success-invoice'),

    # re_path(r'^export/xls/$', application_views.export_applications, name='export_applications'),
    re_path(r'^export/pdf/$', application_views.pdflatex, name='pdf_latex'),
    re_path(r'^mgt-commands/$',
        views.ManagementCommandsView.as_view(),
        name='mgt-commands'),

    # payment related urls
    re_path(r'^infringement_penalty/(?P<sanction_outcome_id>\d+)/$', payment_views.InfringementPenaltyView.as_view(), name='infringement_penalty'),
    re_path(r'^success/fee_preload/(?P<lodgement_number>.+)/$', payment_views.InfringementPenaltySuccessViewPreload.as_view(), name='penalty_success_preload'),
    re_path(r'^success/fee/$', payment_views.InfringementPenaltySuccessView.as_view(), name='penalty_success'),

    # For 'Record Payment'
    re_path(r'^payment_deferred/(?P<sanction_outcome_pk>\d+)/$', DeferredInvoicingView.as_view(), name='deferred_invoicing'),
    re_path(r'^preview_deferred/(?P<sanction_outcome_pk>\d+)/$', DeferredInvoicingPreviewView.as_view(), name='preview_deferred_invoicing'),

    # Reports
    re_path(r'^api/oracle_job$',main_api.OracleJob.as_view(), name='get-oracle'),
    #re_path(r'^api/oracle_job$',main_api.OracleJob.as_view(), name='get-oracle'),
    #re_path(r'^api/reports/booking_settlements$', main_api.BookingSettlementReportView.as_view(),name='booking-settlements-report'),

    # history comparison.
    re_path(r'^history/application/(?P<pk>\d+)/$',
        application_views.ApplicationHistoryCompareView.as_view(),
        name='application-history'),

    re_path(r'^preview/licence-pdf/(?P<application_pk>\d+)',application_views.PreviewLicencePDFView.as_view(), name='preview_licence_pdf'),

    re_path(r'^securebase-view/',views.SecureBaseView.as_view(), name='securebase-view'),
    re_path(r'^api/person_org_lookup$', users_api.GetPersonOrg.as_view(), name='get-person-org'),
    #re_path(r'^ledger-private/identification/(?P<emailuser_id>\d+)', views.getLedgerIdentificationFile, name='view_ledger_identification_file'),
    #re_path(r'^ledger-private/senior-card/(?P<emailuser_id>\d+)', views.getLedgerSeniorCardFile, name='view_ledger_senior_card_file'),

    re_path(r'^private-media/', views.getPrivateFile, name='view_private_file'),
    re_path(r'infringement/', views.InfringementView.as_view(), name='wc_infringement'),

] + ledger_patterns #+ media_serv_patterns

if not are_migrations_running():
    DefaultDataManager()
    CollectorManager()

# whitenoise
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.SHOW_DEBUG_TOOLBAR:
    import debug_toolbar
    urlpatterns = [
        re_path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
