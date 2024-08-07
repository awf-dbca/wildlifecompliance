from django.conf import settings
from ledger.accounts.models import EmailUser, OrganisationAddress
from wildlifecompliance.components.organisations.models import (
    Organisation,
    OrganisationContact,
    OrganisationRequest,
    OrganisationRequestUserAction,
    OrganisationAction,
    OrganisationRequestLogEntry,
    OrganisationLogEntry,
    ledger_organisation,
)
from wildlifecompliance.components.organisations.utils import (
    can_manage_org,
    can_admin_org,
    is_consultant,
    can_relink,
    can_approve,
    is_last_admin,
)
from wildlifecompliance.components.main.fields import CustomChoiceField
from rest_framework import serializers, status
import rest_framework_gis.serializers as gis_serializers

from wildlifecompliance.components.main.utils import (
    get_full_name
)

class LedgerOrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ledger_organisation
        fields = '__all__'


class OrganisationCheckSerializer(serializers.Serializer):
    # Validation serializer for new Organisations
    abn = serializers.CharField()
    name = serializers.CharField()

    def validate(self, data):
        # Check no admin request pending approval.
        requests = OrganisationRequest.objects.\
            filter(
                abn=data['abn'],
                role=OrganisationRequest.ORG_REQUEST_ROLE_EMPLOYEE)\
            .exclude(
                status__in=(
                    OrganisationRequest.ORG_REQUEST_STATUS_DECLINED,
                    OrganisationRequest.ORG_REQUEST_STATUS_APPROVED)
        )
        if requests.exists():
            raise serializers.ValidationError(
                'A request has been submitted and is Pending Approval.')
        return data


class OrganisationPinCheckSerializer(serializers.Serializer):
    pin1 = serializers.CharField()
    pin2 = serializers.CharField()


class OrganisationAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationAddress
        fields = (
            'id',
            'line1',
            'locality',
            'state',
            'country',
            'postcode'
        )


class ComplianceManagementSaveOrganisationAddressSerializer(serializers.ModelSerializer):
    organisation_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    class Meta:
        model = OrganisationAddress
        fields = (
            'id',
            'line1',
            'locality',
            'state',
            'country',
            'postcode',
            'organisation_id',
            )
        read_only_fields = ('id',)


class DelegateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='get_full_name')

    class Meta:
        model = EmailUser
        fields = (
            'id',
            'name',
        )


class DTOrganisationSerializer(serializers.ModelSerializer):
    address_string = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Organisation
        fields = (
            'id',
            'name',
            'abn',
            'address_string',
        )
        # the serverSide functionality of datatables is such that only columns that have field 'data'
        # defined are requested from the serializer. Use datatables_always_serialize to force render
        # of fields that are not listed as 'data' in the datatable columns
        datatables_always_serialize = fields

    def get_address_string(self, obj):
        return obj.address_string


class ComplianceManagementCreateLedgerOrganisationSerializer(serializers.ModelSerializer):
    postal_address_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    class Meta:
        model = ledger_organisation
        fields = (
            'id',
            'name',
            'abn',
            'postal_address_id',
            )
        read_only_fields = ('id', )


class ComplianceManagementUpdateLedgerOrganisationSerializer(serializers.ModelSerializer):
    class Meta:
        model = ledger_organisation
        fields = (
            'id',
            'name',
            'abn',
            #'address',
            )
        read_only_fields = ('id', 'abn')


class ComplianceManagementSaveOrganisationSerializer(serializers.ModelSerializer):
    organisation_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    # address = OrganisationAddressSerializer(read_only=True)
    #organisation = LedgerOrganisationSerializer()

    class Meta:
        model = Organisation
        fields = (
            'id',
            'name',
            'abn',
            # 'address',
            #'email',
            'organisation_id',
        )
        read_only_fields = ('id', 'name', 'abn')


class ComplianceManagementOrganisationSerializer(serializers.ModelSerializer):
    #organisation_id = serializers.IntegerField(
     #   required=False, write_only=True, allow_null=True)
    address = OrganisationAddressSerializer(read_only=True)
    organisation = LedgerOrganisationSerializer()

    class Meta:
        model = Organisation
        fields = (
            'id',
            'name',
            'abn',
            'address',
            'email',
            'organisation',
        )

class OrganisationSerializer(serializers.ModelSerializer):
    address = OrganisationAddressSerializer(read_only=True)
    pins = serializers.SerializerMethodField(read_only=True)
    delegates = DelegateSerializer(many=True, read_only=True)
    organisation = LedgerOrganisationSerializer()

    class Meta:
        model = Organisation
        fields = (
            'id',
            'name',
            'abn',
            'address',
            'email',
            'organisation',
            'pins',
            'delegates'
        )

    def get_pins(self, obj):
        try:
            user = self.context['request'].user
            # Check if the request user is among the first five delegates in
            # the organisation
            if can_manage_org(obj, user):
                return {
                    'one': obj.admin_pin_one,
                    'two': obj.admin_pin_two,
                    'three': obj.user_pin_one,
                    'four': obj.user_pin_two}
            else:
                return None
        except KeyError:
            return None


class ExternalOrganisationSerializer(serializers.ModelSerializer):
    address = OrganisationAddressSerializer(read_only=True)
    delegates = DelegateSerializer(many=True, read_only=True)
    organisation = LedgerOrganisationSerializer()

    class Meta:
        model = Organisation
        fields = (
            'id',
            'name',
            'abn',
            'address',
            'email',
            'organisation',
            'delegates'
        )


class OrganisationCheckExistSerializer(serializers.Serializer):
    # Validation Serializer for existing Organisations
    exists = serializers.BooleanField(default=False)
    id = serializers.IntegerField(default=0)
    first_five = serializers.CharField(allow_blank=True, required=False)
    user = serializers.IntegerField()
    abn = serializers.CharField()

    def validate(self, data):
        user = EmailUser.objects.get(id=data['user'])
        if data['exists']:
            org = Organisation.objects.get(id=data['id'])
            if can_relink(org, user):
                raise serializers.ValidationError(
                    'Please contact {} to re-link to Organisation.' .format(data['first_five']))
            if can_approve(org, user):
                raise serializers.ValidationError(
                    'Please contact {} to Approve your request.' .format(
                        data['first_five']))
        # Check no consultant request is pending approval for an ABN
        if OrganisationRequest.objects.\
            filter(
                abn=data['abn'],
                requester=user,
                role=OrganisationRequest.ORG_REQUEST_ROLE_CONSULTANT)\
            .exclude(
                status__in=(
                    OrganisationRequest.ORG_REQUEST_STATUS_DECLINED,
                    OrganisationRequest.ORG_REQUEST_STATUS_APPROVED))\
            .exists():
                raise serializers.ValidationError(
                    'A request has been submitted and is Pending Approval.')
        return data


class MyOrganisationsSerializer(serializers.ModelSerializer):
    is_admin = serializers.SerializerMethodField(read_only=True)
    is_consultant = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Organisation
        fields = (
            'id',
            'name',
            'abn',
            'is_admin',
            'is_consultant'
        )

    def get_is_consultant(self, obj):
        user = self.context['request'].user
        # Check if the request user is among the first five delegates in the
        # organisation
        return is_consultant(obj, user)

    def get_is_admin(self, obj):
        user = self.context['request'].user
        # Check if the request user is among the first five delegates in the
        # organisation
        return can_admin_org(obj, user)


class DetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ledger_organisation
        fields = ('id', 'name')


class OrganisationContactCheckSerializer(serializers.Serializer):
    '''
    Validation Serializer for Organisation Contact.
    '''
    last_name = serializers.CharField()
    first_name = serializers.CharField()
    organisation = serializers.CharField()
    email = serializers.CharField()

    def validate(self, data):
        is_invalid = False
        invalid_attr = ''

        if data['organisation'] == '':
            is_invalid = True

        # validate formatting.
        # if data['phone_number'] == '':
        #     is_invalid = True

        if data['email'] == '':
            is_invalid = True

        if is_invalid:
            raise serializers.ValidationError('Contact details are invalid.')

        return data


class OrganisationContactSerializer(serializers.ModelSerializer):
    user_status = CustomChoiceField(read_only=True)
    user_role = CustomChoiceField(read_only=True)

    class Meta:
        model = OrganisationContact
        fields = '__all__'


class OrgRequestRequesterSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = EmailUser
        fields = (
            'email',
            'mobile_number',
            'phone_number',
            'full_name'
        )

    def get_full_name(self, obj):
        return get_full_name(obj)


class OrganisationRequestSerializer(serializers.ModelSerializer):
    # assigned_officer = serializers.CharField(
    #     source='assigned_officer.get_full_name')
    identification = serializers.FileField()
    requester = OrgRequestRequesterSerializer(read_only=True)
    status = CustomChoiceField(read_only=True)
    can_be_processed = serializers.SerializerMethodField()
    user_can_process_org_access_requests = serializers.SerializerMethodField()

    class Meta:
        model = OrganisationRequest
        fields = (
            'id',
            'identification',
            'requester',
            'status',
            'name',
            'abn',
            'role',
            'lodgement_number',
            'lodgement_date',
            'assigned_officer',
            'can_be_processed',
            'user_can_process_org_access_requests'
        )
        read_only_fields = ('requester', 'lodgement_date')

    def get_can_be_processed(self, obj):
        return obj.status == OrganisationRequest.ORG_REQUEST_STATUS_WITH_ASSESSOR

    def get_user_can_process_org_access_requests(self, obj):
        if self.context['request'].user and self.context['request'].\
                user.has_perm('wildlifecompliance.organisation_access_request'):
            return True
        return False


class OrganisationRequestDTSerializer(OrganisationRequestSerializer):
    requester = serializers.SerializerMethodField()

    class Meta:
        model = OrganisationRequest
        fields = (
            'id',
            'identification',
            'requester',
            'status',
            'name',
            'abn',
            'role',
            'lodgement_number',
            'lodgement_date',
            'assigned_officer',
            'can_be_processed',
            'user_can_process_org_access_requests'
        )
        # the serverSide functionality of datatables is such that only columns that have field 'data'
        # defined are requested from the serializer. Use datatables_always_serialize to force render
        # of fields that are not listed as 'data' in the datatable columns
        datatables_always_serialize = fields

    def get_requester(self, obj):
        return get_full_name(obj.requester)


class UserOrganisationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='organisation.name')
    abn = serializers.CharField(source='organisation.abn')

    class Meta:
        model = Organisation
        fields = (
            'id',
            'name',
            'abn'
        )


class OrganisationRequestActionSerializer(serializers.ModelSerializer):
    who = serializers.CharField(source='who.get_full_name')

    class Meta:
        model = OrganisationRequestUserAction
        fields = '__all__'


class OrganisationActionSerializer(serializers.ModelSerializer):
    who = serializers.CharField(source='who.get_full_name')

    class Meta:
        model = OrganisationAction
        fields = '__all__'


class OrganisationRequestCommsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationRequestLogEntry
        fields = '__all__'


class OrganisationCommsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrganisationLogEntry
        fields = '__all__'


class OrganisationUnlinkUserSerializer(serializers.Serializer):
    user = serializers.IntegerField()

    def validate(self, obj):
        user = None
        try:
            user = EmailUser.objects.get(id=obj['user'])
            obj['user_obj'] = user
        except EmailUser.DoesNotExist:
            raise serializers.ValidationError(
                'The user you want to unlink does not exist.')
        return obj


class OrgUserAcceptSerializer(serializers.Serializer):
    """
    A validation class to check action for the addition of privileges for an Organisation user.
    """
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    mobile_number = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)
    phone_number = serializers.CharField(
        required=False, allow_null=True, allow_blank=True)

    def validate(self, data):
        # Check for either mobile number or phone number.
        if not (data['mobile_number'] or data['phone_number']):
            raise serializers.ValidationError(
                "User must have an associated phone number or mobile number.")
        return data


class OrgUserCheckSerializer(OrgUserAcceptSerializer):
    """
    A validation class to check action for the removal of privileges for an Organisation user.
    """
    org_id = serializers.IntegerField()

    def validate(self, data):
        # Check for either mobile number or phone number.
        if not (data['mobile_number'] or data['phone_number']):
            raise serializers.ValidationError(
                "User must have an associated phone number or mobile number.")
        # Check user is not the only Admin.
        user = EmailUser.objects.filter(email=data['email']).first()
        org = Organisation.objects.get(id=data['org_id'])
        if is_last_admin(org, user):
            raise serializers.ValidationError(
                "The Organisation will have no Administrator.")
        return data
