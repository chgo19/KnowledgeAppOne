from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from quiz.models import Category


class CreateCategoryForm(forms.Form):
    category_title = forms.CharField(
        help_text="Enter the name of a new category.")

    def clean_category_title(self):
        c = self.cleaned_data['category_title']
        c = ' '.join([i.capitalize() for i in c.split()])
        return c


class CreateQuestionForm(forms.Form):
    choose_category = forms.ModelChoiceField(queryset=Category.objects.all())
    question_text = forms.CharField(
        help_text="Type your question statement here.")
    image = forms.ImageField(
        help_text="Upload an Image if the question requires it.", required=False)
    option_one = forms.CharField(help_text="Type First Option.")
    option_two = forms.CharField(help_text="Type Second Option.")
    option_three = forms.CharField(help_text="Type Third Option.")
    option_four = forms.CharField(help_text="Type Fourth Option.")
    answer = forms.ChoiceField(choices=(
        ('1', 'Option 1'),
        ('2', 'Option 2'),
        ('3', 'Option 3'),
        ('4', 'Option 4'),

    ), help_text="Choose the correct option.")
    explanation = forms.CharField(
        help_text="Write an explanation for the answer here")


class NewUserForm(forms.Form):
    username = forms.CharField(help_text="Type a username for your account.")
    password = forms.CharField(widget=forms.PasswordInput)
