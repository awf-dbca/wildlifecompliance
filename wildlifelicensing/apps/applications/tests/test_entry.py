import os

from django.core.urlresolvers import reverse
from django.core.files import File
from django.test import TestCase
from social.apps.django_app.default.models import UserSocialAuth

from ledger.accounts.models import EmailUser, Document, Address, Persona

from wildlifelicensing.apps.main.models import WildlifeLicenceType
from wildlifelicensing.apps.main.tests.helpers import SocialClient

TEST_ID_PATH = os.path.join('wildlifelicensing', 'apps', 'main', 'test_data', 'test_id.jpg')


class ApplicationEntryTestCase(TestCase):
    def setUp(self):
        self.customer = EmailUser.objects.create(email='customer@test.net')
        UserSocialAuth.create_social_auth(self.customer, self.customer.email, 'email')

        self.client = SocialClient()

        licence_type = WildlifeLicenceType.objects.get(code='regulation17')
        licence_type.identification_required = True
        licence_type.save()

    def test_select_licence_type(self):
        """Testing that a user can display the licence type selection list"""
        self.client.login(self.customer.email)

        # check that client can access the licence type selection list
        response = self.client.get(reverse('applications:select_licence_type'))
        self.assertEqual(200, response.status_code)

    def test_check_identification_required_no_current_id(self):
        """Testing that a user can display the identification required page in the case the user has no
        current identification, and upload an ID.
        """
        self.client.login(self.customer.email)

        # check that client can access the identification required page
        response = self.client.get(reverse('applications:check_identification', args=('regulation17',)))
        self.assertEqual(200, response.status_code)

        try:
            with open(TEST_ID_PATH) as fp:
                post_params = {
                    'identification_file': fp
                }
                response = self.client.post(reverse('applications:check_identification', args=('regulation17',)), post_params)

                self.assertRedirects(response, reverse('applications:create_select_persona', args=('regulation17',)),
                                     status_code=302, target_status_code=200, fetch_redirect_response=False)

                # update customer
                self.customer = EmailUser.objects.get(email=self.customer.email)

                # assert customer's ID is the uploaded file
                self.assertEqual(self.customer.identification.filename, 'test_id.jpg')
        finally:
            # remove uploaded file
            os.remove(self.customer.identification.path)

    def test_check_identification_required_current_id(self):
        """Testing that a user can display the identification required page in the case the user has a
        current identification.
        """
        self.client.login(self.customer.email)

        with open(TEST_ID_PATH) as fp:
            self.customer.identification =  Document.objects.create(name='test_id')
            self.customer.identification.file.save('test_id', File(fp), save=True)
            self.customer.save()

        # check that client is redirected to persona creation / selection page
        response = self.client.get(reverse('applications:check_identification', args=('regulation17',)))
        self.assertRedirects(response, reverse('applications:create_select_persona', args=('regulation17',)),
                             status_code=302, target_status_code=200, fetch_redirect_response=False)

        # clean up ID file
        os.remove(self.customer.identification.path)

    def test_create_select_persona_create(self):
        """Testing that a user can display the create / select persona page and create a persona
        in the case the user has no persona
        """
        self.client.login(self.customer.email)

        original_persona_count = self.customer.persona_set.count()

        # create the application dict in the session first
        # the session must be stored in a variable in order to be modifyable
        # https://docs.djangoproject.com/en/1.9/topics/testing/tools/#persistent-state
        session = self.client.session
        session['application'] = {}
        session.save()

        # check that client can access the persona create/select page
        response = self.client.get(reverse('applications:create_select_persona', args=('regulation17',)))
        self.assertEqual(200, response.status_code)

        # check there is not a persona selection form, meaning there is no persona
        self.assertFalse('persona_selection_form' in response.context)

        post_params = {
            'name': 'Test Persona',
            'email': 'test@testplace.net.au',
            'institution': 'Test Institution',
            'line1': '1 Test Street',
            'locality': 'Test Suburb',
            'state': 'WA',
            'postcode': '0001',
            'create': True
        }

        response = self.client.post(reverse('applications:create_select_persona', args=('regulation17',)), post_params)

        # check that client is redirected to enter details page
        self.assertRedirects(response, reverse('applications:enter_details', args=('regulation17',)),
                             status_code=302, target_status_code=200, fetch_redirect_response=False)

        # chech that a new persona was created
        self.assertEqual(self.customer.persona_set.count(), original_persona_count + 1)

        # check the created persona has been set in the session
        self.assertTrue('persona' in self.client.session['application'])

    def test_create_select_persona_select(self):
        """Testing that a user can display the create / select persona page and select a persona
        in the case the user has one or more existing personas
        """
        self.client.login(self.customer.email)

        # create personas
        address1 = Address.objects.create(line1='1 Test Street', locality='Test Suburb', state='WA', postcode='0001')
        persona1 = Persona.objects.create(user=self.customer, name='Test Persona', email='test@testplace.net.au',
                                          institution='Test Institution', postal_address=address1)

        address2 = Address.objects.create(line1='2 Test Street', locality='Test Suburb', state='WA', postcode='0001')
        persona2 = Persona.objects.create(user=self.customer, name='Test Persona 2', email='test@testplace.net.au',
                                          institution='Test Institution', postal_address=address2)

        # create the application dict in the session first
        # the session must be stored in a variable in order to be modifyable
        # https://docs.djangoproject.com/en/1.9/topics/testing/tools/#persistent-state
        session = self.client.session
        session['application'] = {}
        session.save()

        # check that client can access the persona create/select page
        response = self.client.get(reverse('applications:create_select_persona', args=('regulation17',)))
        self.assertEqual(200, response.status_code)

        # check there is a persona selection form, meaning there at least one existing persona
        self.assertTrue('persona_selection_form' in response.context)

        post_params = {
            'persona': persona2.pk,
            'select': True
        }

        response = self.client.post(reverse('applications:create_select_persona', args=('regulation17',)), post_params)

        # check that client is redirected to enter details page
        self.assertRedirects(response, reverse('applications:enter_details', args=('regulation17',)),
                             status_code=302, target_status_code=200, fetch_redirect_response=False)

        # check the persona has been set in the session
        self.assertTrue('persona' in self.client.session['application'])

        # check that the persona in the session is the selected persona
        self.assertEqual(self.client.session['application']['persona'], persona2.pk)

    def test_enter_details_draft(self):
        """Testing that a user can enter the details of an application form and save as a draft
        """
        self.client.login(self.customer.email)

        # create personas
        address = Address.objects.create(line1='1 Test Street', locality='Test Suburb', state='WA', postcode='0001')
        persona = Persona.objects.create(user=self.customer, name='Test Persona', email='test@testplace.net.au',
                                         institution='Test Institution', postal_address=address)

        # create the application dict in the session first
        # the session must be stored in a variable in order to be modifyable
        # https://docs.djangoproject.com/en/1.9/topics/testing/tools/#persistent-state
        session = self.client.session
        session['application'] = {'persona': persona.pk}
        session.save()

        original_applications_count = persona.application_set.count()

        # check that client can access the enter details page
        response = self.client.get(reverse('applications:enter_details', args=('regulation17',)))
        self.assertEqual(200, response.status_code)

        post_params = {
            'project_title': 'Test Title',
            'draft': True
        }

        response = self.client.post(reverse('applications:enter_details', args=('regulation17',)), post_params)

        # chech that a new applicaiton was created
        self.assertEqual(persona.application_set.count(), original_applications_count + 1)

        # check that the state of the application is draft
        self.assertEqual(persona.application_set.first().processing_status, 'draft')

    def test_enter_details_lodge(self):
        """Testing that a user can enter the details of an application form and that the data is
        saved in the session for previewing
        """
        self.client.login(self.customer.email)

        # create personas
        address = Address.objects.create(line1='1 Test Street', locality='Test Suburb', state='WA', postcode='0001')
        persona = Persona.objects.create(user=self.customer, name='Test Persona', email='test@testplace.net.au',
                                         institution='Test Institution', postal_address=address)

        # create the application dict in the session first
        # the session must be stored in a variable in order to be modifyable
        # https://docs.djangoproject.com/en/1.9/topics/testing/tools/#persistent-state
        session = self.client.session
        session['application'] = {'persona': persona.pk}
        session.save()

        # check that client can access the enter details page
        response = self.client.get(reverse('applications:enter_details', args=('regulation17',)))
        self.assertEqual(200, response.status_code)

        post_params = {
            'project_title': 'Test Title',
            'lodge': True
        }

        response = self.client.post(reverse('applications:enter_details', args=('regulation17',)), post_params)

        # check the data has been set in the session
        self.assertTrue('data' in self.client.session['application'])

        # check that the persona in the session is the selected persona
        self.assertEqual(self.client.session['application']['data'].get('project_title', ''), 'Test Title')

    def test_enter_details_preview(self):
        """Testing that a user can preview the details of an application form then lodge the application
        """
        self.client.login(self.customer.email)

        # create personas
        address = Address.objects.create(line1='1 Test Street', locality='Test Suburb', state='WA', postcode='0001')
        persona = Persona.objects.create(user=self.customer, name='Test Persona', email='test@testplace.net.au',
                                         institution='Test Institution', postal_address=address)

        # create the application dict in the session first
        # the session must be stored in a variable in order to be modifyable
        # https://docs.djangoproject.com/en/1.9/topics/testing/tools/#persistent-state
        session = self.client.session
        session['application'] = {'persona': persona.pk, 'data': {'project_title': 'Test Title'}}
        session.save()

        original_applications_count = persona.application_set.count()

        # check that client can access the enter details page
        response = self.client.get(reverse('applications:preview', args=('regulation17',)))
        self.assertEqual(200, response.status_code)

        post_params = {
            'lodge': True
        }

        response = self.client.post(reverse('applications:preview', args=('regulation17',)), post_params)

        # chech that a new applicaiton was created
        self.assertEqual(persona.application_set.count(), original_applications_count + 1)

        # check that the state of the application is draft
        self.assertEqual(persona.application_set.first().processing_status, 'new')