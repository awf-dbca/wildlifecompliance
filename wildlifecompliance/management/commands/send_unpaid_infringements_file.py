import datetime

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils import timezone
from django.core.mail import EmailMessage
from six.moves import StringIO
import csv

import logging

from wildlifecompliance import settings
from wildlifecompliance.components.sanction_outcome.models import SanctionOutcome
from wildlifecompliance.components.users.models import CompliancePermissionGroup

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Send unpaid infringements file emails for infringements which have past payment due dates'

    def handle(self, *args, **options):
        try:
            logger.info('Running command {}'.format(__name__))
            today = timezone.localtime(timezone.now()).date()

            unpaid_infringements = SanctionOutcome.objects.filter(Q(type=SanctionOutcome.TYPE_INFRINGEMENT_NOTICE) &
                                                                  Q(due_date_extended_max__lt=today) &
                                                                  Q(status=SanctionOutcome.STATUS_AWAITING_PAYMENT) &
                                                                  Q(payment_status=SanctionOutcome.PAYMENT_STATUS_UNPAID))
            unpaid_infringements = SanctionOutcome.objects.filter(id=273)

            strIO = StringIO()
            fieldnames = ['Infringement Number', 'Offence Date/Time', ]
            writer = csv.writer(strIO)
            writer.writerow(fieldnames)
            for infringement in unpaid_infringements.all():
                # fullname = '{} {}'.format(o.details.get('first_name'),o.details.get('last_name'))
                # writer.writerow([o.confirmation_number,fullname,o.campground.name,o.arrival.strftime('%d/%m/%Y'),o.departure.strftime('%d/%m/%Y'),o.outstanding])
                writer.writerow([infringement.lodgement_number, infringement.offence_occurrence_datetime])
            strIO.flush()
            strIO.seek(0)
            _file = strIO

            dt = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')

            recipients = []
            compliance_content_type = ContentType.objects.get(model="compliancepermissiongroup")
            permissions = Permission.objects.filter(codename='infringement_notice_coordinator', content_type_id=compliance_content_type.id)
            allowed_groups = CompliancePermissionGroup.objects.filter(permissions__in=permissions)
            groups = [group for group in allowed_groups.all()]
            members = [member for member in group.members for group in groups]

            # recipients = OutstandingBookingRecipient.objects.all()
            email = EmailMessage(
                'Unpaid Infringements File at {}'.format(dt),
                'Unpaid Bookings File',
                settings.EMAIL_FROM,
                # to=[r.email for r in recipients]if recipients else [settings.NOTIFICATION_EMAIL]
                to=['katsufumi.shibata@dbca.wa.gov.au']
            )
            email.attach('UnpaidInfringementsFile_{}.csv'.format(dt), _file.getvalue(), 'text/csv')
            email.send()

        # for c in Compliance.objects.filter(processing_status = 'due'):
        #     try:
        #         c.send_reminder(user)
        #         c.save()
        #     except Exception as e:
        #         logger.info('Error sending Reminder Compliance {}\n{}'.format(c.lodgement_number, e))

            logger.info('Command {} completed'.format(__name__))

        except Exception as e:
            logger.error('Error command {}'.format(__name__))
