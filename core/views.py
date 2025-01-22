from .models import Categorie, Question, Answer
import random
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view

def home_quiz_view(request):
    categories = Categorie.objects.filter(active=True)
    return render(request, 'home_quiz.html', {'categories': categories})

def quiz_view(request, slug):
    try:
        categorie = Categorie.objects.filter(active=True, slug=slug)
    except Exception as e:
        pass

    try:
        question_objs = Question.objects.filter(active=True)

        # if categorie:
        #     question_objs = question_objs.filter(categorie=categorie)

        question_objs = list(question_objs)
        data = []
        random.shuffle(question_objs)

        for question_obj in question_objs:
            data.append({
                "categorie": question_obj.categorie.libelle,
                "question": question_obj.question,
                "answer": question_obj.get_answer()
            })
        print(data)
        return render(request, 'quiz.html', {'quiz_data': data, 'categorie': categorie})
    except Exception as e:
        return render(request, 'quiz.html', {'quiz_data': [], 'categorie': categorie})

def submit_quiz(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        user_answers = request.POST
        results = []
        score = 0
        total = 0

        for key, value in user_answers.items():
            # Exclure les champs CSRF ou autres non pertinents
            if key.startswith('q'):
                question_id = int(key[1:])  # Extraire l'ID de la question
                total += 1

                # Récupérer la question et vérifier la réponse
                try:
                    question = Question.objects.get(id=question_id)
                    answers = question.get_answer()
                    correct_answer_obj = Answer.objects.filter(question=question, is_correct=True).first()  # La bonne réponse
                    correct_answer = correct_answer_obj.answer if correct_answer_obj else None

                    # Vérifier si la réponse de l'utilisateur est correcte
                    is_correct = value == correct_answer
                    if is_correct:
                        score += 1

                    # Ajouter au résultat avec la classe CSS et la bonne réponse
                    results.append({
                        'question': question.question,
                        'selected_answer': value,
                        'correct_answer': correct_answer,
                        'answers': answers,
                        'is_correct': is_correct,
                        'css_class': 'correct' if is_correct else 'incorrect'  # Classe pour la bonne/mauvaise réponse
                    })
                except Question.DoesNotExist:
                    results.append({
                        'question': f"Question {question_id} introuvable",
                        'selected_answer': value,
                        'correct_answer': None,
                        'is_correct': False,
                        'css_class': 'incorrect'
                    })

        # Calcul du pourcentage de réussite
        percentage = (score / total) * 100 if total > 0 else 0

        # Retourner les résultats dans le contexte
        return render(request, 'quiz_results.html', {
            'results': results,
            'score': score,
            'total': total,
            'percentage': percentage
        })
    else:
        # Si ce n'est pas une requête POST, rediriger vers la page d'accueil du quiz
        return render(request, 'home_quiz.html', {})

@api_view(['GET'])
def get_categories(request):
    try:
        categories = Categorie.objects.filter(active=True)
        data = [
            {
                "id": cat.id,
                "libelle": cat.libelle,
                "image": request.build_absolute_uri(cat.image.url) if cat.image else None,
                "slug": cat.slug,
            }
            for cat in categories
        ]
        return JsonResponse({"status": True, "data": data}, status=200)
    except Exception as e:
        return JsonResponse({"status": False, "message": str(e)}, status=500)


@api_view(['GET'])
def get_quiz(request):
    try:
        categorie_slug = request.GET.get('categorie')
        question_objs = Question.objects.filter(active=True)
        
        if categorie_slug:
            question_objs = question_objs.filter(categorie__slug=categorie_slug)

        question_objs = list(question_objs)
        data = []
        random.shuffle(question_objs)

        for question_obj in question_objs:
            data.append({
                "categorie": question_obj.categorie.libelle,
                "question": question_obj.question,
                "answer": question_obj.get_answer()
            })

        return JsonResponse({"status": True, "data": data}, status=200)
    except Exception as e:
        return JsonResponse({"status": False, "message": str(e)}, status=500)
    