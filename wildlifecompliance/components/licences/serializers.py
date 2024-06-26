from django.urls import reverse
from django.utils import timezone

from wildlifecompliance.components.licences.models import (
    WildlifeLicence,
    LicenceCategory,
    LicenceActivity,
    LicencePurpose,
    LicenceDocument,
)
from wildlifecompliance.components.licences.utils import LicencePurposeUtil
from wildlifecompliance import settings
from wildlifecompliance.components.applications.models import (
    ApplicationSelectedActivity,
    ApplicationSelectedActivityPurpose,
    ActivityInvoice,
)
from wildlifecompliance.components.applications.serializers import (
    WildlifeLicenceApplicationSerializer,
)
from ledger.payments.invoice.models import Invoice
from rest_framework import serializers


class WildlifeLicenceSerializer(serializers.ModelSerializer):
    licence_document = serializers.CharField(
        source='licence_document._file.url')
    current_application = WildlifeLicenceApplicationSerializer(read_only=True)
    last_issue_date = serializers.SerializerMethodField(read_only=True)
    latest_activities_merged = serializers.SerializerMethodField(
        read_only=True)
    can_add_purpose = serializers.SerializerMethodField(read_only=True)
    status = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WildlifeLicence
        fields = (
            'id',
            'licence_number',
            'licence_document',
            'replaced_by',
            'current_application',
            'extracted_fields',
            'last_issue_date',
            'latest_activities_merged',
            'can_add_purpose',
            'status',
        )

    def get_last_issue_date(self, obj):
        issue_date = ''
        if obj.latest_activities:
            issue_date = obj.latest_activities.first().get_issue_date()

        return issue_date

    def get_latest_activities_merged(self, obj):
        from wildlifecompliance.components.licences.services import (
            LicenceService,
        )
        return LicenceService.get_activities_list_for(obj)

    def get_can_add_purpose(self, obj):
        '''
        Check if there are purposes left in the category to add on licence.
        '''
        is_latest = obj.is_latest_in_category
        has_available_purposes = obj.purposes_available_to_add.count() > 0 
        has_current_purposes = obj.has_proposed_purposes_in_current()
        # can_add = obj.is_latest_in_category and\
        #     obj.purposes_available_to_add.count() > 0 and\
        #         obj.has_proposed_purposes_in_current()

        return is_latest and has_available_purposes and has_current_purposes

    def get_status(self, obj):

        default_status = [
            obj.LICENCE_STATUS_CURRENT
        ]

        status = [
            s[1] for s in obj.LICENCE_STATUS_CHOICES
            if s[0] == obj.get_property_cache_status() or
            (s[0] in default_status and not obj.get_property_cache_status())
        ][0]

        return status


class DTInternalWildlifeLicenceSerializer(WildlifeLicenceSerializer):
    licence_document = serializers.CharField(
        source='licence_document._file.url')
    current_application = WildlifeLicenceApplicationSerializer(read_only=True)
    can_action = serializers.SerializerMethodField(read_only=True)
    invoice_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WildlifeLicence
        fields = (
            'id',
            'licence_number',
            'licence_document',
            'current_application',
            'last_issue_date',
            'latest_activities_merged',
            'is_latest_in_category',
            'can_action',
            'can_add_purpose',
            'invoice_url',
            'has_inspection_open',
            'status',
        )
        # the serverSide functionality of datatables is such that only columns
        # that have field 'data' defined are requested from the serializer. Use
        # datatables_always_serialize to force render of fields that are not
        # listed as 'data' in the datatable columns.
        datatables_always_serialize = fields

    def get_can_action(self, obj):
        # set default but use to_representation to calculate based on
        # latest_activities_merged.can_action.
        can_action = {
            'can_amend': False,
            'can_renew': False,
            'can_reactivate_renew': False,
            'can_surrender': False,
            'can_cancel': False,
            'can_suspend': False,
            'can_reissue': False,
            'can_reinstate': False,
        }
        return can_action

    def to_representation(self, obj):
        data = super(
            DTInternalWildlifeLicenceSerializer, self).to_representation(obj)

        latest_activities_merged = data['latest_activities_merged']

        # only check if licence is the latest in its category for the applicant
        if data['is_latest_in_category']:
            # set True if any activities can be actioned
            for activity in latest_activities_merged:
                activity_can_action = activity.get('can_action')
                if activity_can_action.get('can_amend'):
                    data.get('can_action')['can_amend'] = True
                if activity_can_action.get('can_renew'):
                    data.get('can_action')['can_renew'] = True
                if activity_can_action.get('can_reactivate_renew'):
                    data.get('can_action')['can_reactivate_renew'] = True
                if activity_can_action.get('can_surrender'):
                    data.get('can_action')['can_surrender'] = True
                if activity_can_action.get('can_cancel'):
                    data.get('can_action')['can_cancel'] = True
                if activity_can_action.get('can_suspend'):
                    data.get('can_action')['can_suspend'] = True
                if activity_can_action.get('can_reissue'):
                    data.get('can_action')['can_reissue'] = True
                if activity_can_action.get('can_reinstate'):
                    data.get('can_action')['can_reinstate'] = True

        return data

    def get_invoice_url(self, obj):
        url = None
        if obj.current_application.get_property_cache_key('latest_invoice_ref')['latest_invoice_ref']:
            url = '{0}{1}'.format(
            settings.WC_PAYMENT_SYSTEM_URL_PDF,
            obj.current_application.get_property_cache_key(
                    'latest_invoice_ref'
            )['latest_invoice_ref']
            )

        return url

class DTExternalWildlifeLicenceSerializer(WildlifeLicenceSerializer):
    licence_document = serializers.SerializerMethodField(read_only=True)
    current_application = WildlifeLicenceApplicationSerializer(read_only=True)
    last_issue_date = serializers.SerializerMethodField(read_only=True)
    can_action = serializers.SerializerMethodField(read_only=True)
    invoice_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = WildlifeLicence
        fields = (
            'id',
            'licence_number',
            'licence_document',
            'current_application',
            'last_issue_date',
            'latest_activities_merged',
            'is_latest_in_category',
            'can_action',
            'can_add_purpose',
            'invoice_url',
            'status',
        )
        # the serverSide functionality of datatables is such that only columns
        # that have field 'data' defined are requested from the serializer. Use
        # datatables_always_serialize to force render of fields that are not
        # listed as 'data' in the datatable columns.
        datatables_always_serialize = fields

    def get_licence_document(self, obj):
        return None

    def get_can_action(self, obj):
        # set default but use to_representation to calculate based on
        # latest_activities_merged.can_action.
        can_action = {
            'can_amend': False,
            'can_renew': False,
            'can_reactivate_renew': False,
            'can_surrender': False,
            'can_cancel': False,
            'can_suspend': False,
            'can_reissue': False,
            'can_reinstate': False,
        }
        return can_action

    def to_representation(self, obj):
        data = super(
            DTExternalWildlifeLicenceSerializer, self).to_representation(obj)

        latest_activities_merged = data['latest_activities_merged']

        # only check if licence is the latest in its category for the applicant
        if data['is_latest_in_category']:
            # set can_action True for any activities that can be actioned
            for activity in latest_activities_merged:
                activity_can_action = activity.get('can_action')
                if activity_can_action.get('can_amend'):
                    data.get('can_action')['can_amend'] = True
                if activity_can_action.get('can_renew'):
                    data.get('can_action')['can_renew'] = True
                if activity_can_action.get('can_reactivate_renew'):
                    data.get('can_action')['can_reactivate_renew'] = True
                if activity_can_action.get('can_surrender'):
                    data.get('can_action')['can_surrender'] = True
                if activity_can_action.get('can_cancel'):
                    data.get('can_action')['can_cancel'] = True
                if activity_can_action.get('can_suspend'):
                    data.get('can_action')['can_suspend'] = True
                if activity_can_action.get('can_reissue'):
                    data.get('can_action')['can_reissue'] = True
                if activity_can_action.get('can_reinstate'):
                    data.get('can_action')['can_reinstate'] = True

        return data

    def get_invoice_url(self, obj):
        url = None
        try:
            licence_activity = ApplicationSelectedActivity.objects.filter(
                application_id=obj.current_application_id)
            activity_inv = ActivityInvoice.objects.filter(
                activity_id=licence_activity[0].id).first()
            latest_invoice = Invoice.objects.get(
                reference=activity_inv.invoice_reference)

            url = reverse(
                'payments:invoice-pdf',
                kwargs={'reference': latest_invoice.reference})

            return url

        except Exception:
            return None


class BasePurposeSerializer(serializers.ModelSerializer):
    name = serializers.CharField()

    class Meta:
        model = LicencePurpose
        fields = (
            'id',
            'name',
            'short_name',
        )


class DefaultPurposeSerializer(BasePurposeSerializer):
    name = serializers.CharField()
    amendment_application_fee = serializers.DecimalField(
        max_digits=8, decimal_places=2, coerce_to_string=False, read_only=True)

    class Meta:
        model = LicencePurpose
        fields = (
            'id',
            'name',
            'base_application_fee',
            'base_licence_fee',
            'short_name',
            'renewal_application_fee',
            'amendment_application_fee',
        )


class ProposedPurposeSerializer(serializers.ModelSerializer):
    purpose = DefaultPurposeSerializer(read_only=True)
    name = serializers.SerializerMethodField()
    application = serializers.SerializerMethodField()

    class Meta:
        model = ApplicationSelectedActivityPurpose
        fields = (
            'id',
            'selected_activity',
            'purpose',
            'name',
            'application',
        )

    def get_name(self, obj):
        return obj.purpose.name if obj.purpose else ''

    def get_application(self, obj):
        return obj.selected_activity.application_id


class DefaultActivitySerializer(serializers.ModelSerializer):

    name = serializers.CharField()
    activity = DefaultPurposeSerializer(many=True, read_only=True)

    class Meta:
        model = LicenceActivity
        fields = (
            'id',
            'name',
            'activity',
            'short_name',
            'not_for_organisation'
        )


class PurposeSerializer(BasePurposeSerializer):
    name = serializers.CharField()
    amendment_application_fee = serializers.DecimalField(
        max_digits=8, decimal_places=2, coerce_to_string=False, read_only=True)
    renewal_application_fee = serializers.DecimalField(
        max_digits=8, decimal_places=2, coerce_to_string=False, read_only=True)
    is_valid_age = serializers.SerializerMethodField()

    class Meta:
        model = LicencePurpose
        fields = (
            'id',
            'name',
            'base_application_fee',
            'base_licence_fee',
            'short_name',
            'renewal_application_fee',
            'amendment_application_fee',
            'minimum_age',
            'is_valid_age',
        )

    def get_is_valid_age(self, obj):
        '''
        Check user dob is valid for Licence Purpose.
        '''
        is_valid = False
        user = self.context.get('user')
        licence = LicencePurposeUtil(obj)
        is_valid = licence.is_valid_age_for(user) if user else False

        return is_valid


class ActivitySerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    purpose = serializers.SerializerMethodField()

    class Meta:
        model = LicenceActivity
        fields = (
            'id',
            'name',
            'purpose',
            'short_name',
            'not_for_organisation'
        )
        order_by = ['-id']

    def get_purpose(self, obj):
        purposes = self.context.get('purpose_records')
        user = self.context.get('user')
        records = purposes if purposes else obj.purpose.all()
        serializer = PurposeSerializer(
            records.filter(
                licence_activity_id=obj.id
            ),
            many=True,
            context={
                'user': user,
            }
        )
        try:
            if purposes.target_field_name == 'licencepurpose':
                # when field_name exists the purposes have not been built.
                return serializer.data

        except AttributeError:
            pass

        # update changes to the base fees.
        for data in serializer.data:
            licence_fee = [
                p.base_licence_fee for p in records if p.id == data['id']]
            application_fee = [
                p.base_application_fee for p in records if p.id == data['id']]

            data['base_licence_fee'] = licence_fee[0]
            data['base_application_fee'] = application_fee[0]

        return serializer.data


class LicenceCategorySerializer(serializers.ModelSerializer):
    activity = serializers.SerializerMethodField()

    class Meta:
        model = LicenceCategory
        fields = (
            'id',
            'name',
            'short_name',
            'activity'
        )

    def get_activity(self, obj):
        purposes = self.context.get('purpose_records')
        activity_ids = list(purposes.values_list(
            'licence_activity_id', flat=True
        )) if purposes else []

        # If purpose_records context is set but is empty, force display of zero
        # activities otherwise, assume we want to retrieve all activities for
        # the Licence Category.
        if purposes:
            activities = [
                a for a in obj.get_activities() if a.id in activity_ids
            ]
        else:
            if activity_ids:
                activities = [
                    a for a in obj.get_activities() if a.id in activity_ids
                ]
            else:
                activities = [
                    a for a in obj.get_activities()
                ]

        activities = sorted(activities, key=lambda x: x.id, reverse=False)
        request = self.context.get('request')
        user = request.user if request and request.user else None
        serializer = ActivitySerializer(
            activities,
            many=True,
            context={
                'user': user,
                'purpose_records': purposes
            }
        )
        return serializer.data


class LicenceDocumentHistorySerializer(serializers.ModelSerializer):
    history_date = serializers.SerializerMethodField()
    history_document_url = serializers.SerializerMethodField()

    class Meta:
        model = LicenceDocument
        fields = (
            'history_date',
            'history_document_url',
        )

    def get_history_date(self, obj):
        date_format_loc = timezone.localtime(
            obj['uploaded_date']
        )
        history_date = date_format_loc.strftime('%d/%m/%Y %H:%M:%S.%f')

        return history_date

    def get_history_document_url(self, obj):
        doc_id = obj['id']
        pdf = obj['name']
        url = '/private-media/wildlifecompliance/licences/{0}/documents/{1}'.format(
            doc_id, pdf
        )
        return url
