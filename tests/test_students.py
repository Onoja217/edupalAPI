"""
Student CRUD endpoint tests
"""

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models import Student, StudentCreate


@pytest.fixture
def sample_student_data() -> dict:
    """Sample student data for testing"""
    return {
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+1234567890",
        "age": 18,
        "grade": "ss3",
        "course": "Mathematics",
    }


@pytest.fixture
def create_sample_student(session: Session, sample_student_data: dict) -> Student:
    """Create a sample student in database"""
    student = Student(**sample_student_data)
    session.add(student)
    session.commit()
    session.refresh(student)
    return student


class TestStudentCRUD:
    """Student CRUD tests"""

    def test_create_student(self, client: TestClient, sample_student_data: dict):
        """Test creating a new student"""
        response = client.post("/api/v1/students/", json=sample_student_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == sample_student_data["name"]
        assert data["email"] == sample_student_data["email"]
        assert data["grade"] == "SS3"  # Should be uppercase
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_student_duplicate_email(
        self, client: TestClient, sample_student_data: dict, create_sample_student
    ):
        """Test that duplicate emails are rejected"""
        response = client.post("/api/v1/students/", json=sample_student_data)
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_create_student_invalid_email(self, client: TestClient):
        """Test that invalid email is rejected"""
        invalid_data = {
            "name": "Jane Doe",
            "email": "invalid-email",
            "age": 20,
            "grade": "ss2",
        }
        response = client.post("/api/v1/students/", json=invalid_data)
        assert response.status_code == 422

    def test_create_student_invalid_age(self, client: TestClient):
        """Test that invalid age is rejected"""
        invalid_data = {
            "name": "Jane Doe",
            "email": "jane@example.com",
            "age": 200,  # Too old
            "grade": "ss2",
        }
        response = client.post("/api/v1/students/", json=invalid_data)
        assert response.status_code == 422

    def test_list_students_empty(self, client: TestClient):
        """Test listing students when database is empty"""
        response = client.get("/api/v1/students/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["page_size"] == 10
        assert data["data"] == []

    def test_list_students_with_data(
        self, client: TestClient, create_sample_student
    ):
        """Test listing students with data"""
        response = client.get("/api/v1/students/")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert len(data["data"]) == 1
        assert data["data"][0]["name"] == create_sample_student.name

    def test_list_students_pagination(self, client: TestClient, session: Session):
        """Test pagination"""
        # Create multiple students
        for i in range(15):
            student = Student(
                name=f"Student {i}",
                email=f"student{i}@example.com",
                age=15 + i,
                grade="SS1",
            )
            session.add(student)
        session.commit()

        # Test first page
        response = client.get("/api/v1/students/?page=1&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 15
        assert len(data["data"]) == 10

        # Test second page
        response = client.get("/api/v1/students/?page=2&page_size=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["data"]) == 5

    def test_list_students_filter_by_name(
        self, client: TestClient, session: Session
    ):
        """Test filtering by name"""
        # Create students
        session.add(Student(name="Alice", email="alice@example.com", age=18, grade="SS1"))
        session.add(Student(name="Bob", email="bob@example.com", age=19, grade="SS1"))
        session.commit()

        response = client.get("/api/v1/students/?name=Alice")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["data"][0]["name"] == "Alice"

    def test_list_students_filter_by_grade(
        self, client: TestClient, session: Session
    ):
        """Test filtering by grade"""
        session.add(Student(name="Alice", email="alice@example.com", age=18, grade="SS1"))
        session.add(Student(name="Bob", email="bob@example.com", age=19, grade="SS2"))
        session.commit()

        response = client.get("/api/v1/students/?grade=SS2")
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 1
        assert data["data"][0]["grade"] == "SS2"

    def test_get_student(self, client: TestClient, create_sample_student):
        """Test getting a specific student"""
        response = client.get(f"/api/v1/students/{create_sample_student.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == create_sample_student.id
        assert data["name"] == create_sample_student.name
        assert data["email"] == create_sample_student.email

    def test_get_student_not_found(self, client: TestClient):
        """Test getting non-existent student"""
        response = client.get("/api/v1/students/999")
        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_update_student(self, client: TestClient, create_sample_student):
        """Test updating a student"""
        update_data = {
            "name": "Jane Doe",
            "grade": "ss2",
        }
        response = client.patch(
            f"/api/v1/students/{create_sample_student.id}",
            json=update_data,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Jane Doe"
        assert data["grade"] == "SS2"
        assert data["email"] == create_sample_student.email

    def test_update_student_email_duplicate(
        self, client: TestClient, session: Session
    ):
        """Test that updating to duplicate email is rejected"""
        student1 = Student(name="Alice", email="alice@example.com", age=18, grade="SS1")
        student2 = Student(name="Bob", email="bob@example.com", age=19, grade="SS1")
        session.add(student1)
        session.add(student2)
        session.commit()

        response = client.patch(
            f"/api/v1/students/{student1.id}",
            json={"email": "bob@example.com"},
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_update_student_not_found(self, client: TestClient):
        """Test updating non-existent student"""
        response = client.patch(
            "/api/v1/students/999",
            json={"name": "Jane"},
        )
        assert response.status_code == 404

    def test_delete_student(self, client: TestClient, create_sample_student):
        """Test deleting a student (soft delete)"""
        response = client.delete(f"/api/v1/students/{create_sample_student.id}")
        assert response.status_code == 204

        # Verify student is soft-deleted
        response = client.get(f"/api/v1/students/{create_sample_student.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["is_active"] is False

    def test_delete_student_not_found(self, client: TestClient):
        """Test deleting non-existent student"""
        response = client.delete("/api/v1/students/999")
        assert response.status_code == 404

    def test_student_name_validation(self, client: TestClient):
        """Test that student names are trimmed"""
        data = {
            "name": "  John Doe  ",
            "email": "john@example.com",
            "age": 18,
            "grade": "ss1",
        }
        response = client.post("/api/v1/students/", json=data)
        assert response.status_code == 201
        assert response.json()["name"] == "John Doe"

    def test_student_grade_uppercase(self, client: TestClient):
        """Test that grades are converted to uppercase"""
        data = {
            "name": "John Doe",
            "email": "john@example.com",
            "age": 18,
            "grade": "ss1",
        }
        response = client.post("/api/v1/students/", json=data)
        assert response.status_code == 201
        assert response.json()["grade"] == "SS1"
