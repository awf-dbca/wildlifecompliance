import traceback

from rest_framework.fields import CharField
from rest_framework_gis.serializers import GeoFeatureModelSerializer, GeometryField

from ledger.accounts.models import EmailUser, Address
from wildlifecompliance.components.call_email.models import (
    CallEmail,
    Classification,
    Referrer,
    ReportType,
    ComplianceFormDataRecord,
    ComplianceLogEntry,
    Location,
    ComplianceUserAction,
    MapLayer,
    ComplianceWorkflowLogEntry,
    CasePriority,
    InspectionType,
    )
from wildlifecompliance.components.main.models import get_related_items
from wildlifecompliance.components.main.serializers import CommunicationLogEntrySerializer
from wildlifecompliance.components.users.serializers import (
    ComplianceUserDetailsOptimisedSerializer,
    CompliancePermissionGroupMembersSerializer
)
from rest_framework import serializers
from django.core.exceptions import ValidationError
from wildlifecompliance.components.main.fields import CustomChoiceField

from wildlifecompliance.components.users.serializers import UserAddressSerializer


class SaveEmailUserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(allow_blank=True)  # We need allow_blank=True otherwise blank is not allowed by blank=False setting in the model
    last_name = serializers.CharField(allow_blank=True)  # We need allow_blank=True otherwise blank is not allowed by blank=False setting in the model
    residential_address = UserAddressSerializer(read_only=True)
    residential_address_id = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    # residential_address = UserAddressSerializer()

    # def create(self, validated_data):
    #     return super(SaveEmailUserSerializer, self).create(validated_data)

    # def update(self, instance, validated_data):
    #     return super(SaveEmailUserSerializer, self).update(instance, validated_data)
    def validate_first_name(self, value):
        # if not value:
        #     raise serializers.ValidationError('First name must not be null.')
        return value

    def validate_last_name(self, value):
        # if not value:
        #     raise serializers.ValidationError('Last name must not be null.')
        return value

    def validate(self, data):
        # return data
        if not data['first_name'] and not data['last_name']:
            raise serializers.ValidationError('Please fill in at least Given Name(s) field or Last Name field.')
        else:
            return data

    class Meta:
        model = EmailUser
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'residential_address',
            'residential_address_id',
            'phone_number',
            'mobile_number',
            'organisation',
            'dob',
        )
        read_only_fields = (
            # 'id',
            # 'residential_address',
        )


class SaveUserAddressSerializer(serializers.ModelSerializer):
    line1 = serializers.CharField(allow_blank=True)  # We need allow_blank=True otherwise blank is not allowed by blank=False setting in the model
    postcode = serializers.CharField(allow_blank=True)  # We need allow_blank=True otherwise blank is not allowed by blank=False setting in the model
    locality = serializers.CharField(allow_blank=True)  # We need allow_blank=True otherwise blank is not allowed by blank=False setting in the model
    country = serializers.CharField(allow_blank=True)  # We need allow_blank=True otherwise blank is not allowed by blank=False setting in the model
    user_id = serializers.IntegerField(required=False, write_only=True, allow_null=True)

    class Meta:
        model = Address
        fields = (
            'id',
            'line1',
            'line2',
            'line3',
            'locality',
            'state',
            'country',
            'postcode',
            'user_id',
        )


class EmailUserSerializer(serializers.ModelSerializer):
    residential_address = UserAddressSerializer()

    class Meta:
        model = EmailUser
        fields = (
            'id',
            'email',
            'first_name',
            'last_name',
            'residential_address',
            'phone_number',
            'mobile_number',
            'organisation',
            'dob',
        )


class ComplianceFormDataRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = ComplianceFormDataRecord
        fields = (
            'field_name',
            'schema_name',
            'component_type',
            'instance_name',
            'comment',
            'deficiency',
            'value',
        )
        read_only_fields = (
            'field_name',
            'schema_name',
            'component_type',
            'instance_name',
            'comment',
            'deficiency',
            'value',
        )


class ClassificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Classification
        fields = (
            'id',
            'name',
        )
        read_only_fields = ('id', 'name', )


class ReferrerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Referrer
        fields = (
            'id',
            'name',
        )
        read_only_fields = ('id', 'name', )


class LocationSerializerOptimized(GeoFeatureModelSerializer):
    class Meta:
        model = Location
        geo_field = 'wkb_geometry'

        fields = (
            'id',
            'wkb_geometry',
            'call_email_id',
        )


class LocationSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = Location
        geo_field = 'wkb_geometry'
        
        fields = (
            'id',
            'street',
            'town_suburb',
            'state',
            'postcode',
            'country',
            'wkb_geometry',
            'details',
            #'call_email_id',
        )
        

class ReportTypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = ReportType
        fields = (
            'id', 
            'report_type',
            'version',
        )
        read_only_fields = (
            'id', 
            'report_type',
            'version',
             )


class CasePrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = CasePriority
        fields = '__all__'


class InspectionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionType
        fields = '__all__'


class SaveCallEmailSerializer(serializers.ModelSerializer):
    status = CustomChoiceField(read_only=True)
    classification = ClassificationSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    report_type = ReportTypeSerializer(read_only=True)
    referrer = ReferrerSerializer(read_only=True)
    email_user = EmailUserSerializer(read_only=True)
    classification_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    report_type_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    location_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    #referrer_id = serializers.IntegerField(
     #   required=False, write_only=True, allow_null=True)
    #referrers_selected = serializer.ListField(
     #   required=False, write_only=True, blank=True)
    email_user_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    region_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    district_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    assigned_to_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    allocated_group_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    case_priority_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    inspection_type_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)

    class Meta:
        model = CallEmail
        fields = (
            'id',
            'number',
            'status',
            'assigned_to_id',
            # 'allocated_to',
            'allocated_group_id',
            # 'status_display',
            'schema',
            'location',
            'classification',
            'report_type',
            'location_id',
            'classification_id',
            'report_type_id',
            'caller',
            
            #'referrer_selected',
            'referrer',
            'caller_phone_number',
            'anonymous_call',
            'caller_wishes_to_remain_anonymous',
            'occurrence_from_to',
            'occurrence_date_from',
            'occurrence_time_start',
            'occurrence_date_to',
            'occurrence_time_end',
            'advice_given',
            'advice_details',
            'email_user',
            'email_user_id',
            'region_id',
            'district_id',
            'case_priority_id',
            'inspection_type_id',
        )
        read_only_fields = (
            'id', 
            # 'status_display',
            'number', 
            'location',
            'classification',
            'report_type',
            'referrer',
            'email_user',
            )


class ReportTypeSchemaSerializer(serializers.ModelSerializer):
    report_type_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)        

    class Meta:
        model = CallEmail
        fields = (
            'id',
            'schema',
            'report_type_id',
        )
        read_only_fields = (
            'id', 
            )


class CallEmailOptimisedSerializer(serializers.ModelSerializer):
    classification = ClassificationSerializer(read_only=True)
    location = LocationSerializerOptimized()
    report_type = ReportTypeSerializer(read_only=True)

    class Meta:
        model = CallEmail
        fields = (
            'id',
            'location',
            'classification',
            'number',
            'report_type',
        )
        read_only_fields = ('id', )


class CallEmailAllocatedGroupSerializer(serializers.ModelSerializer):
    allocated_group = CompliancePermissionGroupMembersSerializer()

    class Meta:
        model = CallEmail
        fields = (
            'allocated_group',
        )


class CallEmailSerializer(serializers.ModelSerializer):
    status = CustomChoiceField(read_only=True)
    classification = ClassificationSerializer(read_only=True)
    lodgement_date = serializers.CharField(source='lodged_on')
    report_type = ReportTypeSerializer(read_only=True)
    location = LocationSerializer(read_only=True)
    referrer = ReferrerSerializer(many=True)
    data = ComplianceFormDataRecordSerializer(many=True)
    email_user = EmailUserSerializer(read_only=True)
    # allocated_group = CallEmailAllocatedGroupSerializer(many=True)
    # allocated_group = CompliancePermissionGroupMembersSerializer()
    allocated_group = serializers.SerializerMethodField()
    user_in_group = serializers.SerializerMethodField()
    readonly_user = serializers.SerializerMethodField()
    readonly_status = serializers.SerializerMethodField()
    related_items = serializers.SerializerMethodField()
    selected_referrers = serializers.SerializerMethodField()
    user_is_assignee = serializers.SerializerMethodField()

    class Meta:
        model = CallEmail
        fields = (
            'id',
            'status',
            # 'status_display',
            'assigned_to_id',
            'allocated_group',
            'allocated_group_id',
            'location',
            'location_id',
            'classification',
            'classification_id',
            'schema',
            'lodgement_date',
            'number',
            'caller',
            
            'report_type',
            'report_type_id',
            'data',
            'caller_phone_number',
            'anonymous_call',
            'caller_wishes_to_remain_anonymous',
            'occurrence_from_to',
            'occurrence_date_from',
            'occurrence_time_start',
            'occurrence_date_to',
            'occurrence_time_end',
            'referrer',
            # 'referrer_id',
            'advice_given',
            'advice_details',
            'email_user',
            'region_id',
            'district_id',
            'case_priority_id',
            'inspection_type_id',
            'user_in_group',
            'readonly_user',
            'readonly_status',
            'related_items',
            'selected_referrers',
            'user_is_assignee',
        )
        read_only_fields = (
            'id', 
            )

    def get_user_in_group(self, obj):
        user_id = self.context.get('request', {}).user.id

        if obj.allocated_group:
           for member in obj.allocated_group.members:
               if user_id == member.id:
                  return True
        else:
            return False

    def get_readonly_user(self, obj):
        user_id = self.context.get('request', {}).user.id

        if user_id == obj.assigned_to_id:
            return False
        elif obj.allocated_group and not obj.assigned_to_id:
           for member in obj.allocated_group.members:
               if user_id == member.id:
                  return False
        else:
            return True

    def get_readonly_status(self, obj):
        if obj.status != 'draft':
            return True
        else:
            return False

    def get_allocated_group(self, obj):
        allocated_group = [{
            'email': '',
            'first_name': '',
            'full_name': '',
            'id': None,
            'last_name': '',
            'title': '',
            }]
        returned_allocated_group = CompliancePermissionGroupMembersSerializer(instance=obj.allocated_group)
        for member in returned_allocated_group.data['members']:
            allocated_group.append(member)

        return allocated_group

    def get_related_items(self, obj):
        return get_related_items(obj)

    def get_selected_referrers(self, obj):
        referrers_selected  = []
        #returned_referrers = ReferrerSerializer(obj.referrer)
        #print(returned_referrers.data)
        for referrer in obj.referrer.all():
            print(referrer)
            referrers_selected.append(str(referrer.id))

        return referrers_selected
    
    def get_user_is_assignee(self, obj):
        user_id = self.context.get('request', {}).user.id
        if user_id == obj.assigned_to_id:
            return True


class CallEmailDatatableSerializer(serializers.ModelSerializer):
    status = CustomChoiceField(read_only=True)
    classification = ClassificationSerializer(read_only=True)
    lodgement_date = serializers.CharField(source='lodged_on')
    user_is_assignee = serializers.SerializerMethodField()
    assigned_to = ComplianceUserDetailsOptimisedSerializer(read_only=True)
    user_action = serializers.SerializerMethodField()

    class Meta:
        model = CallEmail
        fields = (
            'id',
            'status',
            # 'status_display',
            'user_is_assignee',
            'classification',
            'classification_id',
            'lodgement_date',
            'number',
            'caller',
            'assigned_to',
            'assigned_to_id',
            'user_action'

        )
        read_only_fields = (
            'id', 
            )

    def get_user_is_assignee(self, obj):
        # user = EmailUser.objects.get(id=self.context.get('request', {}).user.id)
        user_id = self.context.get('request', {}).user.id
        # compliance_permissions = []
        # for group in user.groups.all():
          #  for permission in group.permissions.all():
           #     compliance_permissions.append(permission.codename)
        if user_id == obj.assigned_to_id:
            return True

    def get_user_action(self, obj):
        user_id = self.context.get('request', {}).user.id
        url = "/internal/call_email/" + str(obj.id)

        if obj.status == 'closed':
            return '<a href=' + url + '>View</a>';
        elif user_id == obj.assigned_to_id:
            return '<a href=' + url + '>Process</a>';
        elif obj.allocated_group and not obj.assigned_to_id:
           for member in obj.allocated_group.members:
               if user_id == member.id:
                  return '<a href=' + url + '>Process</a>';
        else:
            return '<a href=' + url + '>View</a>';


class UpdateAssignedToIdSerializer(serializers.ModelSerializer):
    assigned_to_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    
    class Meta:
        model = CallEmail
        fields = (
            'assigned_to_id',
        )


class CreateCallEmailSerializer(serializers.ModelSerializer):
    # status_display = serializers.CharField(source='get_status_display')
    status = CustomChoiceField(read_only=True)
    # customer_status = CustomChoiceField(read_only=True)

    lodgement_date = serializers.CharField(
        source='lodged_on')
    classification_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    report_type_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)        
    location_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)        
    #referrer_id = serializers.IntegerField(
     #   required=False, write_only=True, allow_null=True)   
    region_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    district_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    # allocated_to = serializers.ListField(
    #     required=False, write_only=True, allow_empty=True)
    assigned_to_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    allocated_group_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    case_priority_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)
    inspection_type_id = serializers.IntegerField(
        required=False, write_only=True, allow_null=True)

    class Meta:
        model = CallEmail
        fields = (
            'id',
            'status',
            'assigned_to_id',
            # 'allocated_to',
            'allocated_group_id',
            'location_id',
            'classification_id',
            'lodgement_date',
            'caller',
            
            'report_type_id',
            'caller_phone_number',
            'anonymous_call',
            'caller_wishes_to_remain_anonymous',
            'occurrence_from_to',
            'occurrence_date_from',
            'occurrence_time_start',
            'occurrence_date_to',
            'occurrence_time_end',
            'advice_given',
            'advice_details',
            #'referrer_id',
            'region_id',
            'district_id',
            'case_priority_id',
            'inspection_type_id',
        )
        read_only_fields = (
            'id', 
            )


class ComplianceUserActionSerializer(serializers.ModelSerializer):
    who = serializers.CharField(source='who.get_full_name')

    class Meta:
        model = ComplianceUserAction
        fields = '__all__'


class ComplianceLogEntrySerializer(CommunicationLogEntrySerializer):
    documents = serializers.SerializerMethodField()

    class Meta:
        model = ComplianceLogEntry
        fields = '__all__'
        read_only_fields = (
            'customer',
        )

    def get_documents(self, obj):
        return [[d.name, d._file.url] for d in obj.documents.all()]


class ComplianceWorkflowLogEntrySerializer(serializers.ModelSerializer):
    documents = serializers.SerializerMethodField()
    call_email_id = serializers.IntegerField(
        required=False, 
        write_only=True, 
        allow_null=True
    )
    region_id = serializers.IntegerField(
        required=False, 
        write_only=True, 
        allow_null=True
    )
    district_id = serializers.IntegerField(
        required=False, 
        write_only=True, 
        allow_null=True
    )

    class Meta:
        model = ComplianceWorkflowLogEntry
        fields = '__all__'

    def get_documents(self, obj):
        return [[d.name, d._file.url] for d in obj.documents.all()]


class MapLayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapLayer
        fields = (
            'display_name',
            'layer_name',
        )
