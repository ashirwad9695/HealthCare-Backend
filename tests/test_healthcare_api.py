from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from authentication.models import User
from patients.models import Patient
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping


class HealthcareAPITests(APITestCase):
    def setUp(self):
        # Create users
        self.user1 = User.objects.create_user(
            email='user1@healthcare.com',
            name='User One',
            password='TestPassword@123'
        )
        self.user2 = User.objects.create_user(
            email='user2@healthcare.com',
            name='User Two',
            password='TestPassword@123'
        )

        # Create doctor
        self.doctor1 = Doctor.objects.create(
            name='Dr. Allison Cameron',
            specialization='Immunology',
            email='allison.cameron@hospital.org',
            phone_number='+15551234567',
            years_of_experience=8
        )

        # Create patient for user1
        self.patient1 = Patient.objects.create(
            created_by=self.user1,
            name='Charlie Brown',
            gender='Male',
            age=30,
            contact_number='+15559876543',
            email='charlie@peanuts.com'
        )

        # Create patient for user2
        self.patient2 = Patient.objects.create(
            created_by=self.user2,
            name='Lucy van Pelt',
            gender='Female',
            age=28,
            contact_number='+15559876544'
        )

    # 1. Authentication APIs
    def test_user_registration_success(self):
        url = reverse('auth_register')
        data = {
            'name': 'New Doctor',
            'email': 'new.doc@healthcare.com',
            'password': 'SecurePassword@123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(response.data['success'])
        self.assertIn('tokens', response.data['data'])
        self.assertIn('access', response.data['data']['tokens'])

    def test_user_registration_duplicate_email(self):
        url = reverse('auth_register')
        data = {
            'name': 'Duplicate User',
            'email': 'user1@healthcare.com',
            'password': 'Password@123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    def test_user_login_success(self):
        url = reverse('auth_login')
        data = {
            'email': 'user1@healthcare.com',
            'password': 'TestPassword@123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['success'])
        self.assertIn('access', response.data['data']['tokens'])

    def test_user_login_invalid_password(self):
        url = reverse('auth_login')
        data = {
            'email': 'user1@healthcare.com',
            'password': 'WrongPassword'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(response.data['success'])

    # 2. Patient Management APIs
    def test_patient_list_only_authenticated_user_records(self):
        # Authenticate as user1
        self.client.force_authenticate(user=self.user1)
        url = reverse('patient_list_create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['data'][0]['name'], 'Charlie Brown')

    def test_patient_create_authenticated(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('patient_list_create')
        data = {
            'name': 'Linus van Pelt',
            'gender': 'Male',
            'age': 25,
            'contact_number': '+15552345678',
            'medical_history': 'None'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['data']['created_by_name'], 'User One')

    def test_patient_detail_and_update(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('patient_detail', kwargs={'pk': self.patient1.id})
        
        # GET
        get_res = self.client.get(url)
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertEqual(get_res.data['data']['name'], 'Charlie Brown')

        # PUT update
        put_data = {
            'name': 'Charlie Brown Jr.',
            'gender': 'Male',
            'age': 31,
            'contact_number': '+15559876543'
        }
        put_res = self.client.put(url, put_data, format='json')
        self.assertEqual(put_res.status_code, status.HTTP_200_OK)
        self.patient1.refresh_from_db()
        self.assertEqual(self.patient1.name, 'Charlie Brown Jr.')

    def test_patient_delete(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('patient_detail', kwargs={'pk': self.patient1.id})
        del_res = self.client.delete(url)
        self.assertEqual(del_res.status_code, status.HTTP_200_OK)
        self.assertFalse(Patient.objects.filter(pk=self.patient1.id).exists())

    # 3. Doctor Management APIs
    def test_doctor_crud_endpoints(self):
        self.client.force_authenticate(user=self.user1)
        url = reverse('doctor_list_create')
        
        # POST
        doc_data = {
            'name': 'Robert Chase',
            'specialization': 'Intensive Care Medicine',
            'email': 'robert.chase@hospital.org',
            'phone_number': '+15557654321',
            'years_of_experience': 10
        }
        post_res = self.client.post(url, doc_data, format='json')
        self.assertEqual(post_res.status_code, status.HTTP_201_CREATED)
        new_doc_id = post_res.data['data']['id']

        # GET all
        get_all_res = self.client.get(url)
        self.assertEqual(get_all_res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(get_all_res.data['count'], 2)

        # GET specific
        detail_url = reverse('doctor_detail', kwargs={'pk': new_doc_id})
        detail_res = self.client.get(detail_url)
        self.assertEqual(detail_res.status_code, status.HTTP_200_OK)
        self.assertEqual(detail_res.data['data']['name'], 'Robert Chase')

        # DELETE
        del_res = self.client.delete(detail_url)
        self.assertEqual(del_res.status_code, status.HTTP_200_OK)
        self.assertFalse(Doctor.objects.filter(pk=new_doc_id).exists())

    # 4. Patient-Doctor Mapping APIs
    def test_mapping_lifecycle(self):
        self.client.force_authenticate(user=self.user1)
        list_url = reverse('mapping_list_create')

        # POST /api/mappings/ - Assign doctor to patient
        mapping_data = {
            'patient': self.patient1.id,
            'doctor': self.doctor1.id,
            'notes': 'Consultation regarding recurrent symptoms.'
        }
        assign_res = self.client.post(list_url, mapping_data, format='json')
        self.assertEqual(assign_res.status_code, status.HTTP_201_CREATED)
        mapping_id = assign_res.data['data']['id']

        # Prevent duplicate assignment
        dup_res = self.client.post(list_url, mapping_data, format='json')
        self.assertEqual(dup_res.status_code, status.HTTP_400_BAD_REQUEST)

        # GET /api/mappings/ - Retrieve all mappings
        all_res = self.client.get(list_url)
        self.assertEqual(all_res.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(all_res.data['count'], 1)

        # GET /api/mappings/<patient_id>/ - Get all doctors assigned to a specific patient
        patient_mappings_url = reverse('mapping_detail_or_patient', kwargs={'id': self.patient1.id})
        patient_res = self.client.get(patient_mappings_url)
        self.assertEqual(patient_res.status_code, status.HTTP_200_OK)
        self.assertEqual(patient_res.data['patient_id'], self.patient1.id)
        self.assertEqual(len(patient_res.data['data']), 1)
        self.assertEqual(patient_res.data['data'][0]['doctor']['name'], 'Dr. Allison Cameron')

        # DELETE /api/mappings/<id>/ - Remove doctor from patient
        delete_url = reverse('mapping_detail_or_patient', kwargs={'id': mapping_id})
        del_res = self.client.delete(delete_url)
        self.assertEqual(del_res.status_code, status.HTTP_200_OK)
        self.assertFalse(PatientDoctorMapping.objects.filter(pk=mapping_id).exists())
