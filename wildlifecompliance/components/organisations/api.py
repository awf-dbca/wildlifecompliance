import traceback
import base64
import geojson
from six.moves.urllib.parse import urlparse
from wsgiref.util import FileWrapper
from django.db.models import Q, Min
from django.db import transaction
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Value
from django.db.models.functions import Concat
from rest_framework import viewsets, serializers, status, generics, views
from rest_framework.decorators import detail_route, list_route, renderer_classes
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser, BasePermission
from rest_framework.pagination import PageNumberPagination
from datetime import datetime, timedelta
from collections import OrderedDict
from django.core.cache import cache
from ledger.accounts.models import EmailUser, OrganisationAddress, Organisation as ledger_organisation
from ledger.address.models import Country
from datetime import datetime, timedelta, date
from wildlifecompliance.helpers import is_customer, is_internal
from wildlifecompliance.components.organisations.models import (
    Organisation,
    OrganisationContact,
    OrganisationRequest,
    OrganisationRequestUserAction,
    OrganisationContact,
    OrganisationRequestLogEntry,
    OrganisationAction,
)

from wildlifecompliance.components.organisations.serializers import (
    OrganisationSerializer,
    DTOrganisationSerializer,
    OrganisationAddressSerializer,
    DetailsSerializer,
    OrganisationRequestSerializer,
    OrganisationRequestDTSerializer,
    OrganisationContactSerializer,
    OrganisationContactCheckSerializer,
    OrganisationCheckSerializer,
    OrganisationPinCheckSerializer,
    OrganisationRequestActionSerializer,
    OrganisationActionSerializer,
    OrganisationRequestCommsSerializer,
    OrganisationCommsSerializer,
    OrgUserCheckSerializer,
    OrgUserAcceptSerializer,
    MyOrganisationsSerializer,
    OrganisationCheckExistSerializer,
    ComplianceManagementSaveOrganisationSerializer,
    ComplianceManagementOrganisationSerializer,
    ComplianceManagementCreateLedgerOrganisationSerializer,
    ComplianceManagementUpdateLedgerOrganisationSerializer,
    ComplianceManagementSaveOrganisationAddressSerializer,
)
from wildlifecompliance.components.applications.serializers import (
    BaseApplicationSerializer,
)

from wildlifecompliance.components.organisations.emails import (
    send_organisation_address_updated_email_notification,
)


from wildlifecompliance.components.applications.models import (
    Application,
    Assessment,
    ApplicationRequest,
    ActivityPermissionGroup
)
from wildlifecompliance.components.main.process_document import process_generic_document

from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer


class OrganisationFilterBackend(DatatablesFilterBackend):
    """
    Custom filters
    """
    def filter_queryset(self, request, queryset, view):

        # Get built-in DRF datatables queryset first to join with search text, then apply additional filters
        super_queryset = super(OrganisationFilterBackend, self).filter_queryset(request, queryset, view).distinct()

        total_count = queryset.count()
        search_text = request.GET.get('search[value]')
        organisation_name = request.GET.get('organisation')
        applicant = request.GET.get('applicant')
        role = request.GET.get('role')
        status = request.GET.get('status')

        if queryset.model is Organisation:
            # search_text filter, join all custom search columns
            # where ('searchable: false' in the datatable definition)
            if search_text:
                search_text = search_text.lower()
                # join queries for the search_text search
                search_text_org_ids = []
                for organisation in queryset:
                    if search_text in organisation.address_string.lower():
                        search_text_org_ids.append(organisation.id)
                # use pipe to join both custom and built-in DRF datatables querysets (returned by super call above)
                # (otherwise they will filter on top of each other)
                queryset = queryset.filter(id__in=search_text_org_ids).distinct() | super_queryset

        if queryset.model is OrganisationRequest:
            # search_text filter, join all custom search columns
            # where ('searchable: false' in the datatable definition)
            if search_text:
                search_text = search_text.lower()
                # join queries for the search_text search
                search_text_org_request_ids = []
                search_text_org_request_ids = OrganisationRequest.objects.filter(
                Q(requester__first_name__icontains=search_text) |
                Q(requester__last_name__icontains=search_text) |
                Q(assigned_officer__first_name__icontains=search_text) |
                Q(assigned_officer__last_name__icontains=search_text)
                ).values('id')
                # for organisation_request in queryset:
                #     if search_text in organisation_request.address_string.lower():
                #         search_text_org_request_ids.append(organisation_request.id)
                # use pipe to join both custom and built-in DRF datatables querysets (returned by super call above)
                # (otherwise they will filter on top of each other)
                queryset = queryset.filter(id__in=search_text_org_request_ids).distinct() | super_queryset

            # apply user selected filters
            organisation_name = organisation_name.lower() if organisation_name else 'all'
            if organisation_name != 'all':
                queryset = queryset.filter(name__iexact=organisation_name)
            applicant = applicant.lower() if applicant else 'all'
            if applicant != 'all':
                queryset = queryset.annotate(applicant_name=Concat('requester__first_name',
                    Value(' '),'requester__last_name')).filter(applicant_name__iexact=applicant)
            role = role.lower() if role else 'all'
            if role != 'all':
                queryset = queryset.filter(role__iexact=role)
            
            status = status.lower().replace(" ","_") if status else 'all'
            if status != 'all':
                queryset = queryset.filter(status__iexact=status)

        # override queryset ordering, required because the ordering is usually handled
        # in the super call, but is then clobbered by the custom queryset joining above
        # also needed to disable ordering for all fields for which data is not an
        # Organisation model field, as property functions will not work with order_by
        getter = request.query_params.get
        fields = self.get_fields(getter)
        ordering = self.get_ordering(getter, fields)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        setattr(view, '_datatables_total_count', total_count)
        return queryset


class OrganisationRenderer(DatatablesRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
            data['recordsTotal'] = renderer_context['view']._datatables_total_count
        return super(OrganisationRenderer, self).render(data, accepted_media_type, renderer_context)


class OrganisationPaginatedViewSet(viewsets.ModelViewSet):
    filter_backends = (OrganisationFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (OrganisationRenderer,)
    queryset = Organisation.objects.none()
    serializer_class = DTOrganisationSerializer
    page_size = 10

    def get_queryset(self):
        if is_internal(self.request):
            return Organisation.objects.all()
        elif is_customer(self.request):
            return Organisation.objects.none()
        return Organisation.objects.none()

    @list_route(methods=['GET', ])
    def datatable_list(self, request, *args, **kwargs):
        self.serializer_class = DTOrganisationSerializer
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        self.paginator.page_size = queryset.count()
        result_page = self.paginator.paginate_queryset(queryset, request)
        serializer = DTOrganisationSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class OrganisationViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return Organisation.objects.all()
        elif is_customer(self.request):
            return user.wildlifecompliance_organisations.all()
        return Organisation.objects.none()

    @detail_route(methods=['GET'])
    @renderer_classes((JSONRenderer,))
    def get_intelligence_text(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            intelligence_text = instance.intelligence_information_text
            return Response({"intelligence_text": intelligence_text})

        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                # raise serializers.ValidationError(repr(e[0].encode('utf-8')))
                raise serializers.ValidationError(repr(e[0]))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST'])
    @renderer_classes((JSONRenderer,))
    def save_intelligence_text(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            intelligence_text = request.data.get('intelligence_text')
            instance.intelligence_information_text = intelligence_text
            instance.save()
            return Response()

        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                # raise serializers.ValidationError(repr(e[0].encode('utf-8')))
                raise serializers.ValidationError(repr(e[0]))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST'])
    @renderer_classes((JSONRenderer,))
    def process_intelligence_document(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            # process docs
            returned_data = process_generic_document(request, instance, 'intelligence_document')
            # delete Sanction Outcome if user cancels modal
            action = request.data.get('action')
            if action == 'cancel' and returned_data:
                instance.status = 'discarded'
                instance.save()

            # return response
            if returned_data:
                return Response(returned_data)
            else:
                return Response()

        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            if hasattr(e, 'error_dict'):
                raise serializers.ValidationError(repr(e.error_dict))
            else:
                # raise serializers.ValidationError(repr(e[0].encode('utf-8')))
                raise serializers.ValidationError(repr(e[0]))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def contacts(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = OrganisationContactSerializer(
                instance.contacts.all(), many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def contacts_linked(self, request, *args, **kwargs):
        try:
            qs = self.get_queryset()
            serializer = OrganisationContactSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def contacts_exclude(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.contacts.exclude(user_status=OrganisationContact.ORG_CONTACT_STATUS_DRAFT)
            serializer = OrganisationContactSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def add_nonuser_contact(self, request, *args, **kwargs):
        try:
            serializer = OrganisationContactCheckSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            instance = self.get_object()
            admin_flag = False
            role = OrganisationContact.ORG_CONTACT_ROLE_USER
            status = OrganisationContact.ORG_CONTACT_STATUS_DRAFT

            with transaction.atomic():

                OrganisationContact.objects.create(
                    organisation=instance,
                    first_name=request.data.get('first_name'),
                    last_name=request.data.get('last_name'),
                    mobile_number=request.data.get('mobile_number',''),
                    phone_number=request.data.get('phone_number'),
                    fax_number=request.data.get('fax_number',''),
                    email=request.data.get('email'),
                    user_role=role,
                    user_status=status,
                    is_admin=admin_flag
                )

                instance.log_user_action(
                    OrganisationAction.ACTION_CONTACT_ADDED.format(
                        '{} {}({})'.format(
                            request.data.get('first_name'),
                            request.data.get('last_name'),
                            request.data.get('email')
                        )
                    ), 
                    request
                )

            serializer = self.get_serializer(instance)

            return Response(serializer.data)

        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def validate_pins(self, request, *args, **kwargs):
        try:
            instance = Organisation.objects.get(id=request.data.get('id'))
            serializer = OrganisationPinCheckSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            with transaction.atomic():
                data = {
                    'valid': instance.validate_pins(
                        serializer.validated_data['pin1'],
                        serializer.validated_data['pin2'],
                        request)}

            if data['valid']:
                # Notify each Admin member of request.
                instance.send_organisation_request_link_notification(request)
            return Response(data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def accept_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data['email']
            )
            instance.accept_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def accept_declined_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data['email']
            )
            instance.accept_declined_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def decline_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data['email']
            )
            instance.decline_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def unlink_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            request.data.update([('org_id', instance.id)])
            serializer = OrgUserCheckSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data['email']
            )
            instance.unlink_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def make_admin_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data['email']
            )
            instance.make_admin_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def make_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            request.data.update([('org_id', instance.id)])
            serializer = OrgUserCheckSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data['email']
            )
            instance.make_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def make_consultant(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            request.data.update([('org_id', instance.id)])
            serializer = OrgUserCheckSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data['email']
            )
            instance.make_consultant(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def suspend_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            request.data.update([('org_id', instance.id)])
            serializer = OrgUserCheckSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data['email']
            )
            instance.suspend_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def reinstate_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data['email']
            )
            instance.reinstate_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def relink_user(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            serializer = OrgUserAcceptSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user_obj = EmailUser.objects.get(
                email=serializer.validated_data['email']
            )
            instance.relink_user(user_obj, request)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = OrganisationActionSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def applications(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.org_applications.all()
            serializer = BaseApplicationSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def comms_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.comms_logs.all()
            serializer = OrganisationCommsSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @list_route(methods=['POST', ])
    def existance(self, request, *args, **kwargs):
        try:
            serializer = OrganisationCheckSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = Organisation.existance(serializer.validated_data['abn'])
            # Check request user cannot be relinked to org.
            data.update([('user', request.user.id)])
            data.update([('abn', request.data['abn'])])
            serializer = OrganisationCheckExistSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def update_details(self, request, *args, **kwargs):
        try:
            org = self.get_object()
            instance = org.organisation
            serializer = DetailsSerializer(instance, data=request.data)
            serializer.is_valid(raise_exception=True)
            instance = serializer.save()
            serializer = self.get_serializer(org)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def update_address(self, request, *args, **kwargs):
        try:
            org = self.get_object()
            instance = org.organisation
            serializer = OrganisationAddressSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            address, created = OrganisationAddress.objects.get_or_create(
                line1=serializer.validated_data['line1'],
                locality=serializer.validated_data['locality'],
                state=serializer.validated_data['state'],
                country=serializer.validated_data['country'],
                postcode=serializer.validated_data['postcode'],
                organisation=instance
            )
            instance.postal_address = address
            instance.save()
            send_organisation_address_updated_email_notification(
                request.user, instance, org, request)
            serializer = self.get_serializer(org)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def upload_id(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.organisation.upload_identification(request)
            with transaction.atomic():
                instance.save()
                instance.log_user_action(
                    OrganisationAction.ACTION_ID_UPDATE.format(
                        '{} ({})'.format(
                            instance.name, instance.abn)), request)
            # For any of the submitter's applications that have requested ID update,
            # email the assigned officer
            applications = instance.org_applications.filter(
                org_applicant=instance,
                id_check_status=Application.ID_CHECK_STATUS_AWAITING_UPDATE,
                proxy_applicant=None
            ).exclude(customer_status__in=(
                Application.CUSTOMER_STATUS_ACCEPTED,
                Application.CUSTOMER_STATUS_DECLINED)
            ).order_by('id')
            Organisation.send_organisation_id_upload_email_notification(
                instance, applications, request)
            serializer = OrganisationSerializer(instance, partial=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class OrganisationRequestsPaginatedViewSet(viewsets.ModelViewSet):
    filter_backends = (OrganisationFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (OrganisationRenderer,)
    queryset = OrganisationRequest.objects.none()
    serializer_class = OrganisationRequestDTSerializer
    page_size = 10

    def get_queryset(self):
        if is_internal(self.request):
            return OrganisationRequest.objects.all()
        elif is_customer(self.request):
            return OrganisationRequest.objects.none()
        return OrganisationRequest.objects.none()

    @list_route(methods=['GET', ])
    def datatable_list(self, request, *args, **kwargs):
        self.serializer_class = OrganisationRequestDTSerializer
        queryset = self.get_queryset()
        queryset = self.filter_queryset(queryset)
        self.paginator.page_size = queryset.count()
        result_page = self.paginator.paginate_queryset(queryset, request)
        serializer = OrganisationRequestDTSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class OrganisationRequestsViewSet(viewsets.ModelViewSet):
    queryset = OrganisationRequest.objects.all()
    serializer_class = OrganisationRequestSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return OrganisationRequest.objects.all()
        elif is_customer(self.request):
            return user.organisationrequest_set.all()
        return OrganisationRequest.objects.none()

    @list_route(methods=['GET', ])
    def datatable_list(self, request, *args, **kwargs):
        try:
            qs = self.get_queryset()
            serializer = OrganisationRequestDTSerializer(
                qs, many=True, context={'request': request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    # @list_route(methods=['GET',])
    # def user_organisation_request_list(self, request, *args, **kwargs):
    #     try:
    #         queryset = self.get_queryset()
    #         queryset = queryset.filter(requester = request.user)

    #         # instance = OrganisationRequest.objects.get(requester = request.user)
    #         serializer = self.get_serializer(queryset, many=True)
    #         return Response(serializer.data)
    #     except serializers.ValidationError:
    #         print(traceback.print_exc())
    #         raise
    #     except ValidationError as e:
    #         print(traceback.print_exc())
    #         raise serializers.ValidationError(repr(e.error_dict))
    #     except Exception as e:
    #         print(traceback.print_exc())
    #         raise serializers.ValidationError(str(e))

    @list_route(methods=['GET', ])
    def get_pending_requests(self, request, *args, **kwargs):
        try:
            qs = self.get_queryset().filter(requester=request.user,
                                            status=OrganisationRequest.ORG_REQUEST_STATUS_WITH_ASSESSOR)
            serializer = OrganisationRequestDTSerializer(qs, many=True, context={'request': request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @list_route(methods=['GET', ])
    def get_amendment_requested_requests(self, request, *args, **kwargs):
        try:
            qs = self.get_queryset().filter(
                requester=request.user, status=OrganisationRequest.ORG_REQUEST_STATUS_AMENDMENT_REQUESTED)
            serializer = OrganisationRequestDTSerializer(qs, many=True, context={'request': request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def assign_to_me(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user = request.user
            if not request.user.has_perm('wildlifecompliance.organisation_access_request'):
                raise serializers.ValidationError(
                    'You do not have permission to process organisation access requests')
            instance.assign_officer(request.user, request)
            serializer = OrganisationRequestSerializer(
                instance, context={'request': request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def assign_officer(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            user_id = request.data.get('officer_id', None)
            user = None
            if not user_id:
                raise serializers.ValiationError('An officer id is required')
            try:
                user = EmailUser.objects.get(id=user_id)
            except EmailUser.DoesNotExist:
                raise serializers.ValidationError(
                    'A user with the id passed in does not exist')
            if not request.user.has_perm('wildlifecompliance.organisation_access_request'):
                raise serializers.ValidationError(
                    'You do not have permission to process organisation access requests')
            instance.assign_officer(user, request)
            serializer = OrganisationRequestSerializer(
                instance, context={'request': request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def unassign_officer(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.unassign_officer(request)
            serializer = OrganisationRequestSerializer(
                instance, context={'request': request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def accept(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.accept(request)
            serializer = OrganisationRequestSerializer(
                instance, context={'request': request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def amendment_request(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.amendment_request(request)
            serializer = OrganisationRequestSerializer(
                instance, context={'request': request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['PUT', ])
    def reupload_identification_amendment_request(
            self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.reupload_identification_amendment_request(request)
            serializer = OrganisationRequestSerializer(
                instance, partial=True, context={'request': request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def decline(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.decline(request)
            serializer = OrganisationRequestSerializer(
                instance, context={'request': request})
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def action_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.action_logs.all()
            serializer = OrganisationRequestActionSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['GET', ])
    def comms_log(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            qs = instance.comms_logs.all()
            serializer = OrganisationRequestCommsSerializer(qs, many=True)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.validated_data['requester'] = request.user
            if request.data['role'] == OrganisationRequest.ORG_REQUEST_ROLE_CONSULTANT:
                # Check if consultant can be relinked to org.
                data = Organisation.existance(request.data['abn'])
                data.update([('user', request.user.id)])
                data.update([('abn', request.data['abn'])])
                existing_org = OrganisationCheckExistSerializer(data=data)
                existing_org.is_valid(raise_exception=True)
            with transaction.atomic():
                instance = serializer.save()
                instance.log_user_action(
                    OrganisationRequestUserAction.ACTION_LODGE_REQUEST.format(
                        instance.id), request)
                instance.send_organisation_request_email_notification(request)
            return Response(serializer.data)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))


class OrganisationAccessGroupMembers(views.APIView):

    renderer_classes = [JSONRenderer, ]

    def get(self, request, format=None):
        members = []
        if is_internal(request):
            groups = ActivityPermissionGroup.objects.filter(
                permissions__codename__in=[
                    'organisation_access_request',
                    'system_administrator'
                ]
            )
            for group in groups:
                for member in group.members:
                    members.append({'name': member.get_full_name(), 'id': member.id})
        return Response(members)


class OrganisationContactViewSet(viewsets.ModelViewSet):
    serializer_class = OrganisationContactSerializer
    queryset = OrganisationContact.objects.all()

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return OrganisationContact.objects.all()
        elif is_customer(self.request):
            user_orgs = [
                org.id for org in user.wildlifecompliance_organisations.all()]
            return OrganisationContact.objects.filter(
                Q(organisation_id__in=user_orgs))
        return OrganisationContact.objects.none()


class MyOrganisationsViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = MyOrganisationsSerializer

    def get_queryset(self):
        user = self.request.user
        if is_internal(self.request):
            return Organisation.objects.all()
        elif is_customer(self.request):
            return user.wildlifecompliance_organisations.all()
        return Organisation.objects.none()


class OrganisationComplianceManagementViewSet(viewsets.ModelViewSet):
    queryset = Organisation.objects.all()
    serializer_class = ComplianceManagementOrganisationSerializer
    
    def create(self, request, *args, **kwargs):
        print("create org")
        print(request.data)
        try:
            with transaction.atomic():
                abn = request.data.get('abn')
                address = request.data.get('address')
                ledger_org = None
                wc_org = None

                if not abn:
                    return Response({'message': 'ABN must be specified'}, status=status.HTTP_400_BAD_REQUEST)
                ledger_org_list = ledger_organisation.objects.filter(abn=abn)
                if ledger_org_list:
                    ledger_org = ledger_org_list[0]
                if ledger_org:
                    wc_org_list = Organisation.objects.filter(organisation=ledger_org)
                    if wc_org_list:
                        wc_org = wc_org_list[0]
                        return Response({'message': 'WC org already exists'}, status=status.HTTP_400_BAD_REQUEST)
                if address:
                    if ledger_org and ledger_org_address:
                        print("existing address")
                        ledger_org_address = ledger_org.adresses.first()
                        address_serializer = ComplianceManagementSaveOrganisationAddressSerializer(
                                instance=ledger_org_address, 
                                data=address)
                    else:
                        print("no existing address")
                        address_serializer = ComplianceManagementSaveOrganisationAddressSerializer(
                                data=address)
                    address_serializer.is_valid(raise_exception=True)
                    if address_serializer.is_valid:
                        saved_address = address_serializer.save()
                        print("address saved") 
                # WC only cares about the postal address
                saved_address = update_or_create_postal_address(address, ledger_org)
                ledger_org_data = {'name': request.data.get('name'),
                        'abn': request.data.get('abn'),
                        'postal_address_id': saved_address.id
                        }
                if ledger_org:
                    # update existing ledger_org
                    ledger_serializer = ComplianceManagementUpdateLedgerOrganisationSerializer(instance=ledger_org.id, data=ledger_org_data)
                else:
                    # create ledger_org if it doesn't exist
                    ledger_serializer = ComplianceManagementCreateLedgerOrganisationSerializer(data=ledger_org_data)
                ledger_serializer.is_valid(raise_exception=True)
                if ledger_serializer.is_valid:
                    ledger_org = ledger_serializer.save()
                    org_serializer = ComplianceManagementSaveOrganisationSerializer(data={'organisation_id': ledger_org.id})
                    org_serializer.is_valid(raise_exception=True)
                    if org_serializer.is_valid:
                        org_serializer.save()
                        # return serialized data for all objects
                        content = {'ledger_org': ledger_serializer.data, 
                                    'wc_org': org_serializer.data,
                                    'ledger_address': address_serializer.data
                                    }
                        return Response(content, status=status.HTTP_201_CREATED)

            return Response({'message': 'No org created'}, status=status.HTTP_400_BAD_REQUEST)
        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    @detail_route(methods=['POST', ])
    def update_postal_address(self, request, *args, **kwargs):
        print("create org")
        print(request.data)
        try:
            instance = self.get_object()
            postal_address = instance.organisation.postal_address
            address = request.data.get('address')
            if address:
                address_serializer = ComplianceManagementSaveOrganisationAddressSerializer(
                        instance=ledger_org_address, 
                        data=address)
                address_serializer.is_valid(raise_exception=True)
                if address_serializer.is_valid:
                    saved_address = address_serializer.save()
                    print("address saved") 
                    return Response(address_serializer.data, status=status.HTTP_201_CREATED)

        except serializers.ValidationError:
            print(traceback.print_exc())
            raise
        except ValidationError as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(repr(e.error_dict))
        except Exception as e:
            print(traceback.print_exc())
            raise serializers.ValidationError(str(e))

    #def update_or_create_postal_address(address, ledger_org=None):
    #    if ledger_org and ledger_org.postal_address:
    #        print("existing address")
    #        #ledger_org_address = ledger_org.adresses.first()
    #        address_serializer = ComplianceManagementSaveOrganisationAddressSerializer(
    #                instance=ledger_org.postal_address, 
    #                data=address)
    #    else:
    #        print("no existing address")
    #        address_serializer = ComplianceManagementSaveOrganisationAddressSerializer(
    #                data=address)

    #    address_serializer.is_valid(raise_exception=True)
    #    if address_serializer.is_valid:
    #        saved_address = address_serializer.save()
    #        print("address saved")
    #    return saved_address
