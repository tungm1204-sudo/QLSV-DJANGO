from django.test import TestCase
from decimal import Decimal
from apps.exams.services import convert_10_to_4

class ExamServicesTest(TestCase):
    def test_convert_10_to_4(self):
        """Test hàm quy đổi điểm"""
        # Test điểm A
        score_4, letter = convert_10_to_4(Decimal('8.5'))
        self.assertEqual(score_4, Decimal('4.00'))
        self.assertEqual(letter, 'A')
        
        # Test điểm B+
        score_4, letter = convert_10_to_4(Decimal('8.4'))
        self.assertEqual(score_4, Decimal('3.50'))
        self.assertEqual(letter, 'B+')
        
        # Test điểm F
        score_4, letter = convert_10_to_4(Decimal('3.9'))
        self.assertEqual(score_4, Decimal('0.00'))
        self.assertEqual(letter, 'F')
        
        # Test None
        score_4, letter = convert_10_to_4(None)
        self.assertEqual(score_4, Decimal('0.00'))
        self.assertEqual(letter, 'F')
