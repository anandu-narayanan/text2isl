from django.test import TestCase
from .nlp_utils import process_text_to_isl

class NLPUtilsTest(TestCase):
    def test_svo_to_sov(self):
        text = "I am driving a car"
        glosses = process_text_to_isl(text)
        # Expect I, car, drive. "am" and "a" should be removed. Note: lemma of driving is drive.
        # "car" should be before "drive"
        self.assertIn("car", glosses)
        self.assertIn("drive", glosses)
        
        car_idx = glosses.index("car")
        drive_idx = glosses.index("drive")
        self.assertTrue(car_idx < drive_idx, "Object should come before verb in SOV")

    def test_stop_words_removal(self):
        text = "The doctor is visiting the hospital"
        glosses = process_text_to_isl(text)
        
        self.assertNotIn("the", glosses)
        self.assertNotIn("is", glosses)
