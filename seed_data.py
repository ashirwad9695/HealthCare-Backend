import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'healthcare_backend.settings')
django.setup()

from authentication.models import User
from patients.models import Patient
from doctors.models import Doctor
from mappings.models import PatientDoctorMapping

def seed():
    print("Seeding initial healthcare backend data...")

    # Create admin / test user
    test_user, created = User.objects.get_or_create(
        email='doctor.admin@healthcare.com',
        defaults={
            'name': 'Dr. Sarah Connor',
            'is_staff': True,
            'is_superuser': True,
        }
    )
    if created:
        test_user.set_password('Admin@12345')
        test_user.save()
        print("Created Superuser: doctor.admin@healthcare.com (Password: Admin@12345)")
    else:
        print("Superuser already exists.")

    # Create another test user
    regular_user, created = User.objects.get_or_create(
        email='john.doe@example.com',
        defaults={
            'name': 'John Doe',
        }
    )
    if created:
        regular_user.set_password('Password@123')
        regular_user.save()
        print("Created Regular User: john.doe@example.com (Password: Password@123)")

    # Create Doctors
    doc1, _ = Doctor.objects.get_or_create(
        email='gregory.house@princeton.edu',
        defaults={
            'name': 'Gregory House',
            'specialization': 'Diagnostic Medicine & Nephrology',
            'phone_number': '+15550192834',
            'years_of_experience': 22,
            'hospital_affiliation': 'Princeton-Plainsboro Teaching Hospital',
            'bio': 'Specializes in infectious disease and rare diagnostic puzzles.'
        }
    )
    doc2, _ = Doctor.objects.get_or_create(
        email='meredith.grey@seattlegrace.org',
        defaults={
            'name': 'Meredith Grey',
            'specialization': 'General Surgery',
            'phone_number': '+15550183746',
            'years_of_experience': 15,
            'hospital_affiliation': 'Grey Sloan Memorial Hospital',
            'bio': 'Chief of General Surgery, expert in minimally invasive procedures.'
        }
    )
    doc3, _ = Doctor.objects.get_or_create(
        email='stephen.strange@metrogeneral.org',
        defaults={
            'name': 'Stephen Strange',
            'specialization': 'Neurosurgery',
            'phone_number': '+15550172635',
            'years_of_experience': 18,
            'hospital_affiliation': 'Metro-General Hospital',
            'bio': 'Acclaimed neurosurgeon with expertise in complex cranial procedures.'
        }
    )
    print(f"Created/Verified 3 Doctors: Dr. {doc1.name}, Dr. {doc2.name}, Dr. {doc3.name}")

    # Create Patients
    p1, _ = Patient.objects.get_or_create(
        name='Alice Walker',
        created_by=regular_user,
        defaults={
            'age': 34,
            'gender': 'Female',
            'contact_number': '+15550111222',
            'email': 'alice.walker@patient.com',
            'address': '742 Evergreen Terrace, Springfield',
            'medical_history': 'Asthma, seasonal allergies.'
        }
    )
    p2, _ = Patient.objects.get_or_create(
        name='Robert Vance',
        created_by=regular_user,
        defaults={
            'age': 58,
            'gender': 'Male',
            'contact_number': '+15550133444',
            'email': 'robert.vance@patient.com',
            'address': '124 Conch Street, Bikini',
            'medical_history': 'Hypertension, Type 2 Diabetes.'
        }
    )
    print(f"Created/Verified 2 Patients for user {regular_user.name}: {p1.name}, {p2.name}")

    # Create Mapping
    m1, _ = PatientDoctorMapping.objects.get_or_create(
        patient=p1,
        doctor=doc1,
        defaults={'notes': 'Patient referred for unexplained respiratory flare-ups.'}
    )
    m2, _ = PatientDoctorMapping.objects.get_or_create(
        patient=p2,
        doctor=doc2,
        defaults={'notes': 'Scheduled pre-op surgical consultation.'}
    )
    print(f"Created/Verified 2 Mappings: {p1.name} -> Dr. {doc1.name}, {p2.name} -> Dr. {doc2.name}")
    print("Database seeding completed successfully!")

if __name__ == '__main__':
    seed()
