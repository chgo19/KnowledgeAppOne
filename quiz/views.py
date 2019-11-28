from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User

from quiz.models import Category, Question, Choice, UserAnswer
from quiz.forms import CreateCategoryForm, CreateQuestionForm, NewUserForm
# Create your views here.


def index(request):
    """ Category list View as the Homepage. """
    num_categorys = Category.objects.count()
    num_questions = Question.objects.count()
    num_choices = Choice.objects.count()
    num_user_answers = UserAnswer.objects.count()
    num_users = User.objects.count()

    context = {
        'num_categorys': num_categorys,
        'num_questions': num_questions,
        'num_choices': num_choices,
        'num_user_answers': num_user_answers,
        'num_users': num_users,
    }

    return render(request, 'index.html', context=context)


class CategoryListView(generic.ListView):
    model = Category
    paginate_by = 10


class CategoryDetailView(generic.DetailView):
    model = Category


class QuestionListView(generic.ListView):
    model = Question
    paginate_by = 10


class QuestionDetailView(generic.DetailView):
    model = Question


def show_answer(request, pk):
    question = get_object_or_404(Question, pk=pk)
    if 'user_choice' in request.POST:
        user_choice = int(request.POST['user_choice'])
    else:
        return HttpResponse("<h1>Uh uh! Not so smart!</h1>")

    context = {
        'question': question,
        'user_choice': user_choice,
    }

    for choice in question.choice_set.all():
        if choice.is_correct:
            context['right_choice'] = choice.id
            break

    context['from_page'] = request.POST['page']

    user = request.user
    if user.is_authenticated:
        answered = UserAnswer.objects.filter(user=user)
        if pk not in [answer.question_id for answer in answered]:
            response = UserAnswer.objects.create(
                user=user, question_id=pk, answer_id=user_choice)
            response.save()

    return render(request, 'quiz/show_answer.html', context=context)


@login_required
def questions_doneby_user(request):
    records = UserAnswer.objects.filter(user=request.user)
    questions = [Question.objects.get(id=record.question_id)
                 for record in records]
    return render(request, 'quiz/questions_doneby_user.html', {'questions': questions})


@login_required
def create_new_category(request):
    if request.method == 'POST':
        form = CreateCategoryForm(request.POST)

        if form.is_valid():
            if not form.cleaned_data['category_title'] in [category.title for category in Category.objects.all()]:
                category = Category.objects.create(
                    title=form.cleaned_data['category_title'])
                category.save()

        return HttpResponseRedirect(reverse('categorys'))
    else:
        category_title = 'Undefined'
        form = CreateCategoryForm(initial={'category_title': category_title})

    context = {
        'form': form,
    }

    return render(request, 'quiz/new_category.html', context)


@login_required
def create_new_question(request):
    if request.method == 'POST':
        form = CreateQuestionForm(request.POST or None, request.FILES or None)

        if form.is_valid():
            category = form.cleaned_data['choose_category']
            question_text = form.cleaned_data['question_text']
            image = form.cleaned_data['image']
            option1 = form.cleaned_data['option_one']
            option2 = form.cleaned_data['option_two']
            option3 = form.cleaned_data['option_three']
            option4 = form.cleaned_data['option_four']
            right_answer = form.cleaned_data['answer']
            explanation = form.cleaned_data['explanation']

            question = Question.objects.create(
                category=category,
                question_text=question_text,
                image=image,
                explanation=explanation
            )
            question.save()
            for n, i in enumerate([option1, option2, option3, option4]):
                choice = Choice.objects.create(
                    question=question,
                    choice_text=i,
                    is_correct=(n+1) == int(right_answer)
                )
                choice.save()

            # messages.success(request, 'You uploaded it')

        return HttpResponseRedirect(reverse('all-questions'))
    else:
        form = CreateQuestionForm()

    context = {
        'form': form
    }

    return render(request, 'quiz/new_question.html', context=context)


def register(request):
    if request.method == 'POST':
        form = NewUserForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = User.objects.create_user(
                username=username, password=password)

        return HttpResponseRedirect(reverse('login'))
    else:
        form = NewUserForm()

    context = {
        'form': form
    }

    return render(request, 'quiz/new_user.html', context=context)
