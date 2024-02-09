import traceback
from django.db.models import Q
from django.core.exceptions import ValidationError
from rest_framework import viewsets, serializers
from rest_framework.decorators import list_route, detail_route
from rest_framework.response import Response
from datetime import datetime, timedelta
import pytz
from wildlifecompliance.helpers import is_customer, is_internal
from wildlifecompliance.components.licences.services import LicenceService
from wildlifecompliance.components.licences.models import (
    WildlifeLicence,
    LicenceCategory,
    LicencePurpose
)
from wildlifecompliance.components.applications.serializers import (
    ExternalApplicationSelectedActivitySerializer
)
from wildlifecompliance.components.licences.serializers import (
    LicenceCategorySerializer,
    DTInternalWildlifeLicenceSerializer,
    DTExternalWildlifeLicenceSerializer,
    ProposedPurposeSerializer,
    LicenceDocumentHistorySerializer,
)
from wildlifecompliance.components.applications.models import (
    Application,
    ApplicationSelectedActivity
)
from rest_framework_datatables.pagination import DatatablesPageNumberPagination
from rest_framework_datatables.filters import DatatablesFilterBackend
from rest_framework_datatables.renderers import DatatablesRenderer
from django.db.models import CharField, Value, Case, When
from django.db.models.functions import Concat


class LicenceFilterBackend(DatatablesFilterBackend):
    """
    Custom filters
    """
    def filter_queryset(self, request, queryset, view):

        # Get built-in DRF datatables queryset first to join with search text, then apply additional filters
        super_queryset = super(LicenceFilterBackend, self).filter_queryset(request, queryset, view).distinct()

        total_count = queryset.count()
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        category_name = request.GET.get('category_name')
        holder = request.GET.get('holder')
        search_text = request.GET.get('search[value]')

        if queryset.model is WildlifeLicence:
            # search_text filter, join all custom search columns
            # where ('searchable: false' in the datatable definition)
            if search_text:
                search_text = search_text.lower().strip()
                # join queries for the search_text search
                search_text_licence_ids = []
                search_text_licence_ids = WildlifeLicence.objects.annotate(
                    applicant_name=Case(
                        When(
                            current_application__proxy_applicant__isnull=False,
                            then=Concat(
                                'current_application__proxy_applicant__first_name',
                                Value(' '),
                                'current_application__proxy_applicant__last_name',
                                Value(''),
                            )
                        ),
                        default=Concat(
                            'current_application__submitter__first_name',
                            Value(' '),
                            'current_application__submitter__last_name',
                            Value(''),
                        ),
                        output_field=CharField(),
                    )
                ).filter(
                Q(applicant_name__icontains=search_text) |
                Q(current_application__submitter__email__icontains=search_text) |
                Q(current_application__submitter__first_name__icontains=search_text) |
                Q(current_application__submitter__first_name__icontains=search_text) |
                Q(current_application__proxy_applicant__email__icontains=search_text) |
                Q(current_application__proxy_applicant__first_name__icontains=search_text) |
                Q(current_application__proxy_applicant__last_name__icontains=search_text) |
                Q(current_application__org_applicant__organisation__name__icontains=search_text)
                ).values('id')

                # # use pipe to join both custom and built-in DRF datatables querysets (returned by super call above)
                # # (otherwise they will filter on top of each other)
                queryset = queryset.filter(id__in=search_text_licence_ids).distinct() | super_queryset

            # apply user selected filters
            category_name = category_name.lower() if category_name else 'all'
            if category_name != 'all':
                #category_name_licence_ids = []
                #for wildlifelicence in queryset:
                #    if category_name in wildlifelicence.current_application.licence_category_name.lower():
                #        category_name_licence_ids.append(wildlifelicence.id)
                #queryset = queryset.filter(id__in=category_name_licence_ids)
                queryset = queryset.filter(licence_category__name__iexact=category_name)

            #TODO this filter does not work
            if date_from:
                date_from_licence_ids = []
                for wildlifelicence in queryset:
                    # Order the queryset 'from' by issue date licence purpose.
                    # if (pytz.timezone('utc').localize(datetime.strptime(date_from, '%Y-%m-%d'))
                    #         <= wildlifelicence.current_activities.order_by('-issue_date').first().issue_date):
                    #             date_from_licence_ids.append(wildlifelicence.id)
                    _date_from = pytz.timezone('utc').localize(
                        datetime.strptime(date_from, '%Y-%m-%d'))

                    _issue_date = wildlifelicence.current_activities.first(
                        ).get_issue_date()

                    if _date_from <= _issue_date:
                        date_from_licence_ids.append(wildlifelicence.id)

                queryset = queryset.filter(id__in=date_from_licence_ids)
                
            #TODO this filter does not work
            if date_to:
                date_to_licence_ids = []
                for wildlifelicence in queryset:
                    # Order the queryset 'to' by issue date on licence purpose.
                    # if (pytz.timezone('utc').localize(datetime.strptime(date_to, '%Y-%m-%d')) + timedelta(days=1)
                    #         >= wildlifelicence.current_activities.order_by('-issue_date').first().issue_date):
                    #             date_to_licence_ids.append(wildlifelicence.id)
                    _date_to = pytz.timezone('utc').localize(
                        datetime.strptime(date_to, '%Y-%m-%d')
                        ) + timedelta(days=1)

                    _issue_date = wildlifelicence.current_activities.first(
                         ).get_issue_date()

                    if _date_to >= _issue_date:
                        date_to_licence_ids.append(wildlifelicence.id)

                queryset = queryset.filter(id__in=date_to_licence_ids)
            holder = holder.lower() if holder else 'all'
            if holder != 'all':
                #holder_licence_ids = []
                #for wildlifelicence in queryset:
                #    if holder in wildlifelicence.current_application.applicant.lower():
                #        holder_licence_ids.append(wildlifelicence.id)
                #queryset = queryset.filter(id__in=holder_licence_ids)
                queryset = queryset.annotate(
                    applicant_name=Case(
                        When(
                            current_application__proxy_applicant__isnull=False,
                            then=Concat(
                                'current_application__proxy_applicant__first_name',
                                Value(' '),
                                'current_application__proxy_applicant__last_name',
                                Value(''),
                            )
                        ),
                        default=Concat(
                            'current_application__submitter__first_name',
                            Value(' '),
                            'current_application__submitter__last_name',
                            Value(''),
                        ),
                        output_field=CharField(),
                    )
                ).filter(Q(applicant_name__iexact=holder)
                |Q(current_application__org_applicant__organisation__name__iexact=holder))

        # override queryset ordering, required because the ordering is usually handled
        # in the super call, but is then clobbered by the custom queryset joining above
        # also needed to disable ordering for all fields for which data is not an
        # WildlifeLicence model field, as property functions will not work with order_by
        getter = request.query_params.get
        fields = self.get_fields(getter)
        ordering = self.get_ordering(getter, fields)
        if len(ordering):
            queryset = queryset.order_by(*ordering)

        setattr(view, '_datatables_total_count', total_count)
        return queryset


class LicenceRenderer(DatatablesRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        if 'view' in renderer_context and hasattr(renderer_context['view'], '_datatables_total_count'):
            data['recordsTotal'] = renderer_context['view']._datatables_total_count
        return super(LicenceRenderer, self).render(data, accepted_media_type, renderer_context)


class LicencePaginatedViewSet(viewsets.ModelViewSet):
    filter_backends = (LicenceFilterBackend,)
    pagination_class = DatatablesPageNumberPagination
    renderer_classes = (LicenceRenderer,)
    queryset = WildlifeLicence.objects.none()
    serializer_class = DTExternalWildlifeLicenceSerializer
    page_size = 10

    def get_queryset(self):
        user = self.request.user
        # Filter for WildlifeLicence objects that have a current application
        # linked with an ApplicationSelectedActivity that has been ACCEPTED.
        asa_accepted = ApplicationSelectedActivity.objects.filter(
            processing_status__in=[
                ApplicationSelectedActivity.PROCESSING_STATUS_ACCEPTED,
                ApplicationSelectedActivity.PROCESSING_STATUS_OFFICER_FINALISATION])
        if is_internal(self.request):
            return WildlifeLicence.objects.filter(
                current_application__in=asa_accepted.values_list(
                    'application_id', flat=True))
        elif is_customer(self.request):
            user_orgs = [
                org.id for org in user.wildlifecompliance_organisations.all()]
            return WildlifeLicence.objects.filter(
                Q(current_application__org_applicant_id__in=user_orgs) |
                Q(current_application__proxy_applicant=user) |
                Q(current_application__submitter=user)
            ).filter(current_application__in=asa_accepted.values_list('application_id', flat=True))
        return WildlifeLicence.objects.none()

    @list_route(methods=['GET', ])
    def internal_datatable_list(self, request, *args, **kwargs):
        self.serializer_class = DTInternalWildlifeLicenceSerializer
        queryset = self.get_queryset()
        # Filter by org
        org_id = request.GET.get('org_id', None)
        if org_id:
            queryset = queryset.filter(current_application__org_applicant_id=org_id)
        # Filter by proxy_applicant
        proxy_applicant_id = request.GET.get('proxy_applicant_id', None)
        if proxy_applicant_id:
            queryset = queryset.filter(current_application__proxy_applicant_id=proxy_applicant_id)
        # Filter by submitter
        submitter_id = request.GET.get('submitter_id', None)
        if submitter_id:
            queryset = queryset.filter(current_application__submitter_id=submitter_id)
        # Filter by user (submitter or proxy_applicant)
        user_id = request.GET.get('user_id', None)
        if user_id:
            queryset = WildlifeLicence.objects.filter(
                Q(current_application__proxy_applicant=user_id) |
                Q(current_application__submitter=user_id)
            )
        queryset = self.filter_queryset(queryset)
        self.paginator.page_size = queryset.count()
        result_page = self.paginator.paginate_queryset(queryset, request)
        serializer = DTInternalWildlifeLicenceSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)

    @list_route(methods=['GET', ])
    def external_datatable_list(self, request, *args, **kwargs):
        self.serializer_class = DTExternalWildlifeLicenceSerializer
        # Filter for WildlifeLicence objects that have a current application linked with an
        # ApplicationSelectedActivity that has been ACCEPTED
        user_orgs = [
            org.id for org in request.user.wildlifecompliance_organisations.all()]
        asa_accepted = ApplicationSelectedActivity.objects.filter(
            Q(application__org_applicant_id__in=user_orgs) |
            Q(application__proxy_applicant=request.user) |
            Q(application__submitter=request.user)
        ).filter(
            processing_status=ApplicationSelectedActivity.PROCESSING_STATUS_ACCEPTED
        )
        queryset = WildlifeLicence.objects.filter(
            current_application__in=asa_accepted.values_list('application_id', flat=True)
        )
        # Filter by org
        org_id = request.GET.get('org_id', None)
        if org_id:
            queryset = queryset.filter(current_application__org_applicant_id=org_id)
        # Filter by proxy_applicant
        proxy_applicant_id = request.GET.get('proxy_applicant_id', None)
        if proxy_applicant_id:
            queryset = queryset.filter(current_application__proxy_applicant_id=proxy_applicant_id)
        # Filter by submitter
        submitter_id = request.GET.get('submitter_id', None)
        if submitter_id:
            queryset = queryset.filter(current_application__submitter_id=submitter_id)
        queryset = self.filter_queryset(queryset)
        self.paginator.page_size = queryset.count()
        result_page = self.paginator.paginate_queryset(queryset, request)
        serializer = DTExternalWildlifeLicenceSerializer(result_page, context={'request': request}, many=True)
        return self.paginator.get_paginated_response(serializer.data)


class LicenceViewSet(viewsets.ModelViewSet):
    queryset = WildlifeLicence.objects.all()
    serializer_class = DTExternalWildlifeLicenceSerializer

    def get_queryset(self):
        user = self.request.user
        # Filter for WildlifeLicence objects that have a current application linked with an
        # ApplicationSelectedActivity that has been ACCEPTED
        asa_accepted = ApplicationSelectedActivity.objects.filter(
            processing_status=ApplicationSelectedActivity.PROCESSING_STATUS_ACCEPTED)
        if is_internal(self.request):
            return WildlifeLicence.objects.filter(
                current_application__in=asa_accepted.values_list('application_id', flat=True))
        elif is_customer(self.request):
            user_orgs = [
                org.id for org in user.wildlifecompliance_organisations.all()]
            return WildlifeLicence.objects.filter(
                Q(current_application__org_applicant_id__in=user_orgs) |
                Q(current_application__proxy_applicant=user) |
                Q(current_application__submitter=user)
            ).filter(current_application__in=asa_accepted.values_list('application_id', flat=True))
        return WildlifeLicence.objects.none()

    def list(self, request, pk=None, *args, **kwargs):
        queryset = self.get_queryset()
        # Filter by org
        org_id = request.GET.get('org_id', None)
        if org_id:
            queryset = queryset.filter(current_application__org_applicant_id=org_id)
        # Filter by proxy_applicant
        proxy_applicant_id = request.GET.get('proxy_applicant_id', None)
        if proxy_applicant_id:
            queryset = queryset.filter(current_application__proxy_applicant_id=proxy_applicant_id)
        # Filter by submitter
        submitter_id = request.GET.get('submitter_id', None)
        if submitter_id:
            queryset = queryset.filter(current_application__submitter_id=submitter_id)
        serializer = self.get_serializer(queryset, many=True)
        # Display only the relevant Activity if activity_id param set
        activity_id = request.GET.get('activity_id', None)
        if activity_id and pk:
            queryset = queryset.get(id=pk).current_activities.get(id=activity_id)
            serializer = ExternalApplicationSelectedActivitySerializer(queryset)
        return Response(serializer.data)

    @list_route(methods=['GET', ])
    def user_list(self, request, *args, **kwargs):
        user_orgs = [
            org.id for org in request.user.wildlifecompliance_organisations.all()]
        qs = []
        qs.extend(list(self.get_queryset().filter(current_application__submitter=request.user)))
        qs.extend(
            list(
                self.get_queryset().filter(
                    current_application__proxy_applicant=request.user)))
        qs.extend(
            list(
                self.get_queryset().filter(
                    current_application__org_applicant_id__in=user_orgs)))
        queryset = list(set(qs))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @detail_route(methods=['POST', ])
    def add_licence_inspection(self, request, pk=None, *args, **kwargs):
        try:
            if pk:
                instance = self.get_object()
                instance.create_inspection(request)

                serializer = DTExternalWildlifeLicenceSerializer(
                    instance,
                    context={'request': request}
                    )
                   
                return Response(serializer.data)

            raise serializers.ValidationError('Licence ID must be specified')

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
    def reactivate_renew_purposes(self, request, pk=None, *args, **kwargs):
        try:
            purpose_ids_list = request.data.get('purpose_ids_list', None)
            if not type(purpose_ids_list) == list:
                raise serializers.ValidationError(
                    'Purpose IDs must be a list')
            if not request.user.has_perm('wildlifecompliance.issuing_officer'):
                raise serializers.ValidationError(
                    'You are not authorised to reactivate renew for licenced activities')
            if LicencePurpose.objects.filter(id__in=purpose_ids_list).\
                    values_list('licence_activity_id',flat=True).\
                    distinct().count() != 1:
                raise serializers.ValidationError(
                    'Selected purposes must all be of the same licence activity')
            if purpose_ids_list and pk:
                licence_activity_id = LicencePurpose.objects.filter(id__in=purpose_ids_list).\
                                        first().licence_activity_id
                instance = self.get_object()
                can_reactivate_renew_purposes = instance.get_latest_purposes_for_licence_activity_and_action(
                    licence_activity_id, WildlifeLicence.ACTIVITY_PURPOSE_ACTION_REACTIVATE_RENEW)
                can_reactivate_renew_purposes_ids_list = [purpose.id for purpose in can_reactivate_renew_purposes.order_by('id')]
                if not set(purpose_ids_list).issubset(can_reactivate_renew_purposes_ids_list):
                    raise serializers.ValidationError(
                        'Renew for selected purposes cannot be reactivated')
                instance.apply_action_to_purposes(request, WildlifeLicence.ACTIVITY_PURPOSE_ACTION_REACTIVATE_RENEW)
                serializer = DTExternalWildlifeLicenceSerializer(instance, context={'request': request})
                return Response(serializer.data)
            else:
                raise serializers.ValidationError(
                    'Licence ID and Purpose IDs list must be specified')
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
    def surrender_licence(self, request, pk=None, *args, **kwargs):
        try:
            if pk:
                instance = self.get_object()
                LicenceService.request_surrender_licence(instance, request)
                serializer = DTExternalWildlifeLicenceSerializer(
                    instance, context={'request': request}
                )

                return Response(serializer.data)
            else:
                raise serializers.ValidationError(
                    'Licence ID must be specified')
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
    def surrender_purposes(self, request, pk=None, *args, **kwargs):
        try:
            purpose_ids_list = request.data.get('purpose_ids_list', None)

            if not request.user.has_perm('wildlifecompliance.issuing_officer'):
                raise serializers.ValidationError(
                    'You are not authorised to surrender licenced activities')

            if not purpose_ids_list and pk:
                raise serializers.ValidationError(
                    'Licence ID and Purpose IDs list must be specified')

            instance = self.get_object()
            LicenceService.request_surrender_licence(instance, request)
            serializer = DTExternalWildlifeLicenceSerializer(
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
    def cancel_licence(self, request, pk=None, *args, **kwargs):
        try:
            if not request.user.has_perm('wildlifecompliance.issuing_officer'):
                raise serializers.ValidationError(
                    'You are not authorised to cancel licences')
            if pk:
                instance = self.get_object()
                LicenceService.request_cancel_licence(instance, request)
                serializer = DTExternalWildlifeLicenceSerializer(
                    instance, context={'request': request}
                )

                return Response(serializer.data)
            else:
                raise serializers.ValidationError(
                    'Licence ID must be specified')
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
    def cancel_purposes(self, request, pk=None, *args, **kwargs):
        try:
            purpose_ids_list = request.data.get('purpose_ids_list', None)

            if not request.user.has_perm('wildlifecompliance.issuing_officer'):
                raise serializers.ValidationError(
                    'You are not authorised to cancel licenced activities')

            if not purpose_ids_list and pk:
                raise serializers.ValidationError(
                    'Licence ID and Purpose IDs list must be specified')

            instance = self.get_object()
            LicenceService.request_cancel_licence(instance, request)
            serializer = DTExternalWildlifeLicenceSerializer(
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
    def suspend_licence(self, request, pk=None, *args, **kwargs):
        try:
            if not request.user.has_perm('wildlifecompliance.issuing_officer'):
                raise serializers.ValidationError(
                    'You are not authorised to suspend licences')
            if pk:
                instance = self.get_object()
                LicenceService.request_suspend_licence(instance, request)
                serializer = DTExternalWildlifeLicenceSerializer(
                    instance, context={'request': request}
                )

                return Response(serializer.data)
            else:
                raise serializers.ValidationError(
                    'Licence ID must be specified')
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
    def suspend_purposes(self, request, pk=None, *args, **kwargs):
        '''
        Request to suspend purposes.
        '''
        MSG_NOAUTH = 'You are not authorised to suspend licenced activities'
        # MSG_NOSAME = 'Purposes must all be of the same licence activity'
        try:
            purpose_ids_list = request.data.get('purpose_ids_list', None)

            if not request.user.has_perm('wildlifecompliance.issuing_officer'):
                raise serializers.ValidationError(MSG_NOAUTH)

            if not purpose_ids_list and pk:
                raise serializers.ValidationError(
                    'Licence ID and Purpose IDs list must be specified')

            instance = self.get_object()
            LicenceService.request_suspend_licence(instance, request)
            serializer = DTExternalWildlifeLicenceSerializer(
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
    def reinstate_licence(self, request, pk=None, *args, **kwargs):
        try:
            if not request.user.has_perm('wildlifecompliance.issuing_officer'):
                raise serializers.ValidationError(
                    'You are not authorised to reinstate licences')
            if pk:
                instance = self.get_object()
                LicenceService.request_reinstate_licence(instance, request)
                serializer = DTExternalWildlifeLicenceSerializer(
                    instance, context={'request': request}
                )

                return Response(serializer.data)
            else:
                raise serializers.ValidationError(
                    'Licence ID must be specified')
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
    def reinstate_purposes(self, request, pk=None, *args, **kwargs):
        MSG_NOAUTH = 'You are not authorised to reinstate licenced activities'
        # MSG_NOSAME = 'Purposes must all be of the same licence activity'
        try:
            purpose_ids_list = request.data.get('purpose_ids_list', None)

            if not request.user.has_perm('wildlifecompliance.issuing_officer'):
                raise serializers.ValidationError(MSG_NOAUTH)

            if not purpose_ids_list and pk:
                raise serializers.ValidationError(
                    'Licence ID and Purpose IDs list must be specified')

            instance = self.get_object()
            LicenceService.request_reinstate_licence(instance, request)
            serializer = DTExternalWildlifeLicenceSerializer(
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
    def reissue_purposes(self, request, pk=None, *args, **kwargs):
        try:
            purpose_ids_list = request.data.get('purpose_ids_list', None)

            # if not type(purpose_ids_list) == list:
            #     raise serializers.ValidationError(
            #         'Purpose IDs must be a list')
            if not request.user.has_perm('wildlifecompliance.issuing_officer'):
                raise serializers.ValidationError(
                    'You are not authorised to reissue licenced activities')
            # if LicencePurpose.objects.filter(id__in=purpose_ids_list).\
            #         values_list('licence_activity_id',flat=True).\
            #         distinct().count() != 1:
            #     raise serializers.ValidationError(
            #       'Selected purposes must all be of the same licence activity')

            if not purpose_ids_list and pk:
                raise serializers.ValidationError(
                    'Licence ID and Purpose IDs list must be specified')

            instance = self.get_object()
            licence = LicenceService.request_reissue_licence(instance, request)
            serializer = DTExternalWildlifeLicenceSerializer(
                licence, context={'request': request})

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
    def regenerate_licence_pdf(self, request, pk=None, *args, **kwargs):
        try:
            if not request.user.has_perm('wildlifecompliance.issuing_officer'):
                raise serializers.ValidationError(
                    'You are not authorised to reinstate licences')
            if pk:
                instance = self.get_object()
                instance.generate_doc()
                serializer = DTExternalWildlifeLicenceSerializer(instance, context={'request': request})
                return Response(serializer.data)
            else:
                raise serializers.ValidationError(
                    'Licence ID must be specified')
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
    def get_latest_purposes_for_licence_activity_and_action(
            self, request, *args, **kwargs
    ):
        try:
            instance = self.get_object()
            activity_id = request.GET.get('licence_activity_id', None)
            action = request.GET.get('action', None)
            if not activity_id or not action:
                raise serializers.ValidationError(
                    'A licence activity ID and action must be specified')
            queryset = LicenceService.request_licence_purpose_list(
                instance, request
            )
            serializer = ProposedPurposeSerializer(queryset, many=True)

            return Response(serializer.data)

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

    @list_route(methods=['GET', ])
    def licence_history(self, request, *args, **kwargs):
        try:
            qs = None
            licence_history_id = request.query_params['licence_history_id']

            if licence_history_id != '0':
                instance = WildlifeLicence.objects.get(id=licence_history_id)
                qs = instance.get_document_history()

            serializer = LicenceDocumentHistorySerializer(qs, many=True)

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

class LicenceCategoryViewSet(viewsets.ModelViewSet):
    queryset = LicenceCategory.objects.all()
    serializer_class = LicenceCategorySerializer


class UserAvailableWildlifeLicencePurposesViewSet(viewsets.ModelViewSet):
    # Filters to only return purposes that are
    # available for selection when applying for
    # a new application
    queryset = LicenceCategory.objects.all()
    serializer_class = LicenceCategorySerializer

    def list(self, request, *args, **kwargs):
        """
        Returns a queryset of LicenceCategory objects and a queryset of LicencePurpose objects allowed for
        licence activity/purpose selection.
        Filters based on the following request parameters:
        - application_type
        - licence_category (LicenceCategory, id)
        - licence_activity (LicenceActivity, id)
        - organisation_id (Organisation, id), used in Application.get_active_licence_applications
        - proxy_id (EmailUser, id), used in Application.get_active_licence_applications
        - licence_no (WildlifeLicence, id)
        """
        from wildlifecompliance.components.licences.models import LicencePurpose

        queryset = self.get_queryset()
        available_purpose_records = LicencePurpose.objects.filter(
            replaced_by=None    # current versions only.
        )
        application_type = request.GET.get('application_type')
        licence_category_id = request.GET.get('licence_category')
        licence_activity_id = request.GET.get('licence_activity')
        licence_no = request.GET.get('licence_no')
        select_activity_id = request.GET.get('select_activity')
        select_purpose_id = request.GET.get('select_purpose')
        # active_applications are applications linked with licences that have CURRENT or SUSPENDED activities
        active_applications = Application.get_active_licence_applications(request, application_type)
        active_current_applications = active_applications.exclude(
            selected_activities__activity_status=ApplicationSelectedActivity.ACTIVITY_STATUS_SUSPENDED
        )
        open_applications = Application.get_open_applications(request)

        # Exclude purposes in currently OPEN applications which cannot exist in
        # multiple applications.
        if open_applications:
            for app in open_applications:
                available_purpose_records = available_purpose_records.exclude(
                    id__in=app.licence_purposes.exclude(
                        apply_multiple=True
                    ).values_list('id', flat=True)
                )

        if request.user.is_staff:
            # filter out purposes not related to selected licence.
            active_purpose_ids = []
            if licence_no:
                licence = WildlifeLicence.objects.get(id=licence_no)
                for selected_activity in licence.current_activities:
                    active_purpose_ids.extend(
                        [purpose.id for purpose in selected_activity.purposes])

            if application_type in [
                Application.APPLICATION_TYPE_ACTIVITY,
                Application.APPLICATION_TYPE_NEW_LICENCE,
            ]:
                # filter out currently active purposes from available records.
                available_purpose_records = available_purpose_records.exclude(
                    id__in=active_purpose_ids,
                    apply_multiple=False,
                )

            if application_type in [
                Application.APPLICATION_TYPE_AMENDMENT,
                Application.APPLICATION_TYPE_RENEWAL,
                Application.APPLICATION_TYPE_REISSUE,
            ]:
                # rebuild available records with active purposes for Activity 
                # Amendments.
                active_purpose_ids = []
                current = licence.current_activities.filter(
                    licence_activity__id=licence_activity_id
                )
                for selected_activity in current:
                    active_purpose_ids.extend(
                        [purpose.id for purpose in selected_activity.purposes])

                available_purpose_records = LicencePurpose.objects.filter(
                    id__in=active_purpose_ids
                )

        if not active_applications.count() and application_type == Application.APPLICATION_TYPE_RENEWAL:
            # Do not present with renewal options if no activities are within the renewal period
            queryset = LicenceCategory.objects.none()
            available_purpose_records = LicencePurpose.objects.none()

        # Filter based on currently ACTIVE applications (elif block below)
        # - Exclude active licence categories for New Licence application type
        # - Only display active licence categories for New Activity/purpose application type
        # - Only include current (active but not suspended) purposes for
        #     Amendment, Renewal or Reissue application types
        elif active_applications.count():
            # Activities relevant to the current application type
            current_activities = Application.get_active_licence_activities(request, application_type)

            if licence_activity_id:
                current_activities = current_activities.filter(licence_activity__id=licence_activity_id)

            active_licence_activity_ids = current_activities.values_list(
                'licence_activity__licence_category_id',
                flat=True
            )

            active_purpose_ids = []
            for selected_activity in current_activities:
                active_purpose_ids += [
                    p.purpose_id for p in selected_activity.proposed_purposes.all() 
                    if p.is_issued
                ]

            # Exclude active purposes for New Activity/Purpose or New Licence application types
            if application_type in [
                Application.APPLICATION_TYPE_ACTIVITY,
                Application.APPLICATION_TYPE_NEW_LICENCE,
            ]:
                available_purpose_records = available_purpose_records.exclude(
                    id__in=active_purpose_ids,
                    apply_multiple=False,
                )

            # Exclude active licence categories for New Licence application type
            if application_type == Application.APPLICATION_TYPE_NEW_LICENCE:
                queryset = queryset.exclude(id__in=current_activities.values_list(
                    'licence_activity__licence_category_id', flat=True).distinct())

            # Only display active licence categories for New Activity/purpose application type
            if application_type == Application.APPLICATION_TYPE_ACTIVITY:
                queryset = queryset.filter(id__in=current_activities.values_list(
                    'licence_activity__licence_category_id', flat=True).distinct())

            # Only include current (active but not suspended) purposes for
            # Amendment, Renewal or Reissue application types
            elif application_type in [
                Application.APPLICATION_TYPE_AMENDMENT,
                Application.APPLICATION_TYPE_RENEWAL,
                Application.APPLICATION_TYPE_REISSUE,
            ]:
                '''
                NOTE: No filtering required as purposes are not selected by
                applicant for amendment/renewals. Not applicable for REISSUE.
                '''
                # amendable_purpose_ids = active_current_applications.values_list(
                #     'licence_purposes__id',
                #     flat=True
                # )

                # select_activity_id = int(select_activity_id)
                # activitys = [
                #     a for a in current_activities if a.id == select_activity_id
                # ]
                # p_ids = [
                #     p.purpose_id for p in activitys[0].proposed_purposes.all()
                #     if p.id == int(select_purpose_id)
                # ]
                # amendable_purpose_ids = p_ids

                # available_purpose_records = available_purpose_records.filter(
                #     id__in=amendable_purpose_ids,
                #     licence_activity_id__in=current_activities.values_list(
                #         'licence_activity_id', flat=True)
                # )
                queryset = queryset.filter(id__in=active_licence_activity_ids)

        # Filter by Licence Category ID if specified or return empty queryset 
        # if available_purpose_records is empty for the Licence Category ID.
        if licence_category_id:
            if available_purpose_records:
                available_purpose_records = available_purpose_records.filter(
                    licence_category_id=licence_category_id
                )
                queryset = queryset.filter(id=licence_category_id)
            else:
                queryset = LicenceCategory.objects.none()

        # Set any changes to base fees.
        # if application_type == Application.APPLICATION_TYPE_AMENDMENT:
        #     policy = ApplicationFeePolicyForAmendment
        #     for purpose in available_purpose_records:
        #         policy.set_zero_licence_fee_for(purpose)
        #         policy.set_base_application_fee_for(purpose)

        # if application_type == Application.APPLICATION_TYPE_RENEWAL:
        #     policy = ApplicationFeePolicyForRenew
        #     for purpose in available_purpose_records:
        #         policy.set_base_application_fee_for(purpose)

        serializer = LicenceCategorySerializer(queryset, many=True, context={
            'request': request,
            'purpose_records': available_purpose_records
        })
        return Response(serializer.data)
