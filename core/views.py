from django.shortcuts import render, redirect, get_object_or_404
from .models import Question, Answer
from .forms import QuestionForm, AnswerForm, RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


def custom_logout_view(request):
    logout(request)
    return redirect('login')

def register_view(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('question_list')
    return render(request, 'register.html', {'form': form})


@login_required
def post_question(request):
    form = QuestionForm(request.POST or None)
    if form.is_valid():
        question = form.save(commit=False)
        question.user = request.user
        question.save()
        return redirect('question_list')
    return render(request, 'post_question.html', {'form': form})


def question_list(request):
    questions = Question.objects.all().order_by('-created_at')
    return render(request, 'question_list.html', {'questions': questions})


def question_detail(request, pk):
    question = get_object_or_404(Question, pk=pk)
    answers = Answer.objects.filter(question=question).order_by('-created_at')
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.user = request.user
            answer.question = question
            answer.save()
            return redirect('question_detail', pk=pk)
    else:
        form = AnswerForm()
    return render(request, 'question_detail.html', {'question': question, 'answers': answers, 'form': form})


@login_required
def like_answer(request, pk):
    answer = get_object_or_404(Answer, pk=pk)
    if request.user in answer.likes.all():
        answer.likes.remove(request.user)
    else:
        answer.likes.add(request.user)
    return redirect('question_detail', pk=answer.question.pk)
