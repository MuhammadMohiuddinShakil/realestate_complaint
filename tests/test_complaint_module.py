from odoo.tests import TransactionCase
from odoo.exceptions import ValidationError
from unittest.mock import patch
from contextlib import contextmanager


class TestComplaint(TransactionCase):

    def setUp(self):
        super(TestComplaint, self).setUp()
        self.Complaint = self.env['realestate.complaint']
        self.group_customer_service_representative = self.env.ref(
            'realestate_complaint.group_customer_service_representative')

    def test_complaint_creation(self):
        # Test creation of a new complaint
        complaint_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'flat_address': '123 Main St, Berlin',
            'complaint_type': 'electrical_issue',
            'description': 'There is a problem with the electrical wiring.'
        }
        complaint = self.Complaint.create(complaint_data)
        self.assertEqual(complaint.name, 'John Doe')
        self.assertEqual(complaint.email, 'john@example.com')
        self.assertEqual(complaint.flat_address, '123 Main St, Berlin')
        self.assertEqual(complaint.complaint_type, 'electrical_issue')
        self.assertEqual(complaint.description, 'There is a problem with the electrical wiring.')
        self.assertEqual(complaint.state, 'new')  # Should be in 'new' state initially
        self.assertTrue(complaint.complaint_reference.startswith('NEW'), "Complaint reference should start with 'NEW'")

    def test_auto_assign_customer_service_representative(self):
        # Test automatic assignment of customer service representative
        complaint_data = {
            'name': 'Alice Smith',
            'email': 'alice@example.com',
            'flat_address': '456 Oak St, Munich',
            'complaint_type': 'heating_issue',
            'description': 'The heating is not working properly.'
        }
        complaint = self.Complaint.create(complaint_data)
        self.assertTrue(complaint.customer_service_representative, "Customer service representative not assigned")

    def test_complaint_classification(self):
        # Test complaint classification
        complaint_data = {
            'name': 'Bob Brown',
            'email': 'bob@example.com',
            'flat_address': '321 Pine St, Frankfurt',
            'complaint_type': 'question',
            'description': 'I have a question about my lease agreement.'
        }
        complaint = self.Complaint.create(complaint_data)
        complaint.action_classify()
        self.assertEqual(complaint.state, 'in_review')

    def test_action_plan_generation(self):
        # Test action plan generation
        complaint_data = {
            'name': 'Eva Green',
            'email': 'eva@example.com',
            'flat_address': '987 Maple St, Cologne',
            'complaint_type': 'heating_issue',
            'description': 'The radiator is leaking.'
        }
        complaint = self.Complaint.create(complaint_data)
        complaint.action_classify()
        complaint.action_plan = 'Schedule repair for the radiator.'
        self.assertEqual(complaint.state, 'in_progress')
        self.assertEqual(complaint.action_plan, 'Schedule repair for the radiator')

    def test_invalid_complaint_drop(self):
        # Test dropping an invalid complaint
        complaint_data = {
            'name': 'Invalid Complaint',
            'email': 'invalid@example.com',
            'flat_address': '123 Elm St, Hamburg',
            'complaint_type': 'question',
            'description': 'Invalid complaint description'
        }
        with self.assertRaises(ValidationError):
            self.Complaint.create(complaint_data)

    def test_complaint_closure(self):
        # Test closure of a complaint
        complaint_data = {
            'name': 'Michael White',
            'email': 'michael@example.com',
            'flat_address': '654 Birch St, Stuttgart',
            'complaint_type': 'question',
            'description': 'I need information about the parking policy.'
        }
        complaint = self.Complaint.create(complaint_data)
        complaint.action_close()
        self.assertEqual(complaint.state, 'solved')

    def test_email_notification_on_submission(self):
        # Test email notification on complaint submission
        complaint_data = {
            'name': 'John Doe',
            'email': 'john@example.com',
            'flat_address': '123 Main St, Berlin',
            'complaint_type': 'electrical_issue',
            'description': 'There is a problem with the electrical wiring.'
        }
        complaint = self.Complaint.create(complaint_data)
        with self.mock_send_mail() as mocked_send_mail:
            complaint.action_classify()
            self.assertTrue(mocked_send_mail.called)

    def test_email_notification_on_closure(self):
        # Test email notification on complaint closure
        complaint_data = {
            'name': 'Michael White',
            'email': 'michael@example.com',
            'flat_address': '654 Birch St, Stuttgart',
            'complaint_type': 'question',
            'description': 'I need information about the parking policy.'
        }
        complaint = self.Complaint.create(complaint_data)
        with self.mock_send_mail() as mocked_send_mail:
            complaint.action_close()
            self.assertTrue(mocked_send_mail.called)

    @contextmanager
    def mock_send_mail(self):
        """Context manager to mock the send_mail method"""
        with patch.object(self.env['mail.template'], 'send_mail') as mocked_send_mail:
            yield mocked_send_mail
