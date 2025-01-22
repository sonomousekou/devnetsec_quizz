from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()
from django.utils.text import slugify
import random

class MyCustomManager(models.Manager):
    def all(self, is_active=True):
        queryset = super().get_queryset()
        if is_active:
            queryset = queryset.filter(active=True)
        return queryset
    
class Categorie(models.Model):
    libelle = models.CharField(max_length=255)
    image = models.ImageField(upload_to='categories/%Y/%m/%d/', null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, null=True, blank=True)
   
    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyCustomManager()

    def save(self, *args, **kwargs):
        # Vérifiez si le slug est vide ou différent du slug généré à partir du nom de la catégorie
        if not self.slug or self.slug != slugify(self.libelle):
            self.slug = slugify(self.libelle)

        # Vérifiez si un slug identique existe déjà et ajoutez un suffixe numérique si nécessaire
        i = 1
        original_slug = self.slug
        while Categorie.objects.filter(slug=self.slug).exclude(id=self.id).exists():
            self.slug = f"{original_slug}-{i}"
            i += 1

        super().save(*args, **kwargs)

    def __str__(self):
        return self.libelle

class Question(models.Model):
    categorie = models.ForeignKey(Categorie, on_delete=models.CASCADE)
    question = models.TextField(max_length=5000)
    description = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyCustomManager()

    def get_answer(self):
        answer_objs = list(Answer.objects.filter(question=self))
        random.shuffle(answer_objs)
        data = []
        for answer_obj in answer_objs:
            data.append({
                'answer': answer_obj.answer,
                'is_correct': answer_obj.is_correct
            })
        return data

    def __str__(self):
        return self.question


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, blank=True, null=True,
                                 related_name="fk_question")
    answer = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    description = models.TextField(null=True, blank=True)

    active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyCustomManager()

    def __str__(self):
        return self.answer


