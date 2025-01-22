from django.core.management.base import BaseCommand
from core.models import Categorie, Question, Answer
import random

class Command(BaseCommand):
    help = "Ajoute 10 questions pour chaque catégorie prédéfinie."

    def handle(self, *args, **kwargs):
        categories = ["Culture générale", "Informatique", "Religion"]
        for category_name in categories:
            # Vérifiez si la catégorie existe ou créez-la
            category, created = Categorie.objects.get_or_create(
                libelle=category_name,
                defaults={"active": True}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Catégorie créée : {category_name}"))

            # Ajouter 10 questions pour cette catégorie
            for i in range(1, 11):
                question_text = f"Question {i} pour la catégorie {category_name}."
                question_description = f"Description de la question {i} dans {category_name}."
                question = Question.objects.create(
                    categorie=category,
                    question=question_text,
                    description=question_description,
                    active=True
                )
                self.stdout.write(self.style.SUCCESS(f"Question créée : {question_text}"))

                # Ajouter 4 réponses pour chaque question
                for j in range(1, 5):
                    is_correct = (j == 1)  # La première réponse est correcte
                    answer_text = f"Réponse {j} pour la question {i} dans {category_name}."
                    Answer.objects.create(
                        question=question,
                        answer=answer_text,
                        is_correct=is_correct,
                        active=True
                    )
                    self.stdout.write(self.style.SUCCESS(f"Réponse ajoutée : {answer_text}"))

        self.stdout.write(self.style.SUCCESS("Ajout des questions et réponses terminé !"))
