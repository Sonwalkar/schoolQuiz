from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect, JsonResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
import json
from .models import User, CreateQuiz, Stud_Ans
from django.contrib.auth.decorators import login_required
import requests


# index page shows all quiz's list
def index(request):
    return render(request, "quiz/index.html",{
        "quiz" : CreateQuiz.objects.all().order_by('-id')
    })


# To login user
def login_view(request):
    if request.is_ajax and request.method=="POST":

        # Attempt to sign user in
        username = request.POST.get("username", None)
        password = request.POST.get("password",None)
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return JsonResponse({'result':'ok'})
        else:
            return JsonResponse({'result':'ontok'})
    else:
        return render(request, "quiz/login.html")
    

# To logout user
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


# To register or create account user
def register(request):
    if request.is_ajax and request.method == "POST":
        username = request.POST.get("username", None)
        email = request.POST.get("email", None)

        # Ensure password matches confirmation
        password = request.POST.get("password", None)
        confirmation = request.POST.get("confirmation", None)
        accountType = request.POST.get("accountType", None)
        
        if password != confirmation:
            return JsonResponse({"result": "notokpass"})

        # Attempt to create new user
        try:
            if accountType == "student":
                is_teacher = False
            else:
                is_teacher = True
            user = User.objects.create_user(username, email, password, is_teacher=is_teacher)
            user.save()
        except IntegrityError:
            return JsonResponse({"result": "notok"})
                
        login(request, user)
        return JsonResponse({"result": "ok"})
    else:
        return render(request, "quiz/register.html")


#only Teacher account can create quiz
@login_required(login_url="login")
def create_quiz(request):
    # authenticate user account is teacher
    if request.user.is_teacher:
        if request.method == "POST":
            number_of_questions = request.POST.get("numberOfQuestion")
            category = request.POST.get("category")
            difficulty = request.POST.get("difficulty")
            type_of_question = request.POST.get("type")

            createQ = CreateQuiz(user=request.user, number_of_questions=number_of_questions, category=category, difficulty=difficulty, type_of_question=type_of_question)
            createQ.save()

            return HttpResponseRedirect(reverse("index"))
        return render(request, "quiz/create_quiz.html")
    else:
        return HttpResponseBadRequest(reverse("index"))


#  To show's quiz page
def quiz_page(request, id):
    #shows all the questions randomly on loads
    url = "https://opentdb.com/api.php?amount="
    
    quiz_details = CreateQuiz.objects.get(id=id)
    url += str(quiz_details.number_of_questions)

    if quiz_details.category != 'any':
        url += "&category=" + quiz_details.category

    if quiz_details.difficulty != "any":
        url += "&difficulty=" + quiz_details.difficulty
    
    if quiz_details.type_of_question != "any":
        url += "&type=" + quiz_details.type_of_question

    qnas = requests.get(url).json()
    
    
    if request.is_ajax and request.method == "POST":
        return JsonResponse(qnas)
    
    return render(request, "quiz/quiz_page.html",{
        "questions" : qnas
    })


# To store or show all the user's record
@login_required(login_url="login")
def record(request):
    if request.is_ajax and request.method == "POST":
        # if user wants to records answers and submit
        if request.POST.get("isForRecord") == "True":
            saveQuizdata = json.loads(request.POST.get("saveQuiz", None))
            rec = Stud_Ans(qna=saveQuizdata)
            rec.save()

            addToUserData = User.objects.get(id= request.user.id)
            addToUserData.recorded_Ans.add(rec)

            return JsonResponse({"result":"ok"})

        #if user wants to only submit
        elif request.POST.get("isForRecord") == "False":
            return JsonResponse({"result":"ok"})
    
    #if user want's to see his records
    return render(request, "quiz/record.html")