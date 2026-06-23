"""
Pytest configuration and shared fixtures for the QLSV project.
This file is automatically loaded by pytest and makes fixtures available across all tests.
"""

import pytest
import os
from django.conf import settings
from rest_framework.test import APIClient
from accounts.models import User
from model_bakery import baker


@pytest.fixture
def api_client():
    """Provides an unauthenticated API client for testing."""
    return APIClient()


@pytest.fixture
def admin_user():
    """Creates a test admin user."""
    return baker.make(
        User,
        username="admin_test",
        email="admin@test.com",
        role=User.Role.ADMIN,
        is_staff=True,
        is_superuser=False,
    )


@pytest.fixture
def student_user():
    """Creates a test student user."""
    return baker.make(
        User,
        username="student_test",
        email="student@test.com",
        role=User.Role.STUDENT,
    )


@pytest.fixture
def teacher_user():
    """Creates a test teacher user."""
    return baker.make(
        User,
        username="teacher_test",
        email="teacher@test.com",
        role=User.Role.TEACHER,
    )


@pytest.fixture
def admin_client(api_client, admin_user):
    """Provides an API client authenticated as an admin."""
    api_client.force_authenticate(user=admin_user)
    return api_client


@pytest.fixture
def student_client(api_client, student_user):
    """Provides an API client authenticated as a student."""
    api_client.force_authenticate(user=student_user)
    return api_client


@pytest.fixture
def teacher_client(api_client, teacher_user):
    """Provides an API client authenticated as a teacher."""
    api_client.force_authenticate(user=teacher_user)
    return api_client


@pytest.fixture
def sample_student(student_user):
    """Creates a sample student profile for testing."""
    from datetime import date
    from students.models import StudentProfile
    
    profile = baker.make(
        StudentProfile,
        user=student_user,
        mssv="SV20230001",
        dob=date(2003, 1, 1),
    )
    return profile
