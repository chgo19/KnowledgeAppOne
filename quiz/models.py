from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"categoryID: {self.id} - {self.title}"

    def get_absolute_url(self):
        """Returns the url to access a questions for this category."""
        return reverse('category-detail', args=[self.id])


class Question(models.Model):
    def default_category():
        return Category.objects.get_or_create(title="Undefined")[0]

    category = models.ForeignKey(
        Category, on_delete=models.SET_DEFAULT, default=default_category)
    question_text = models.TextField(help_text="Type a question here.")
    image = models.ImageField(blank=True, null=True,
                              upload_to='question_images',
                              help_text='Upload image only if needed for Question.')
    explanation = models.TextField(
        help_text="Give an explanation for answer or other info related to question.")

    def __str__(self):
        return f"{self.category.title} - questionID: {self.id}"

    def get_absolute_url(self):
        """Returns the url to access a detail view of this question."""
        return reverse('question-detail', args=[self.id])

    def get_answer_url(self):
        return reverse('show-answer', args=[self.id])


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    is_correct = models.BooleanField(
        default=False, help_text="Mark right if this is the right choice")

    def __str__(self):
        return f"choiceID:{self.id} - {self.choice_text}"


class UserAnswer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question_id = models.IntegerField(help_text="Give Question ID.")
    answer_id = models.IntegerField(help_text="Give Answer ID.")

    def __str__(self):
        return f"ID: {self.user.id} - qID: {self.question_id} - aID: {self.answer_id}"
