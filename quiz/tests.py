from django.test import TestCase
from .models import Stud_Ans

class Stud_Ans_testcase(TestCase):
    savedId = int()
    def setUp(self):
        jsondata = {"result":"ok"}
        stud_ansTestCase = Stud_Ans(qna=jsondata)
        stud_ansTestCase.save()
        
    
    def test_student_ans_saved(self):
        studAns = Stud_Ans.objects.get(id = 1)
        self.assertEqual(studAns.qna, {"result":"ok"})