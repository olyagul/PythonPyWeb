from django.shortcuts import render
from django.views import View
from django.db.models import Q, Max, Count
from .models import Author, AuthorProfile, Entry, Tag


class TrainView(View):
    def get(self, request):
        max_self_esteem = Author.objects.aggregate(max_self_esteem=Max('self_esteem'))
        self.answer1 = Author.objects.filter(self_esteem=max_self_esteem['max_self_esteem'])

        author_article_count = Author.objects.annotate(article_count=Count('entries'))
        max_count = author_article_count.aggregate(Max('article_count'))['article_count__max']
        self.answer2 = author_article_count.filter(article_count=max_count)

        cinema_entries = Entry.objects.filter(tags__name='Кино')
        music_entries = Entry.objects.filter(tags__name='Музыка')
        self.answer3 = (cinema_entries | music_entries).distinct()

        self.answer4 = Author.objects.filter(gender='ж').count()

        total_authors = Author.objects.count()
        agreed_authors = Author.objects.filter(status_rule=True).count()
        if total_authors > 0:
            self.answer5 = (agreed_authors / total_authors) * 100
        else:
            self.answer5 = 0

        self.answer6 = Author.objects.filter(authorprofile__stage__gte=1, authorprofile__stage__lte=5).distinct()

        max_age = Author.objects.aggregate(Max('age'))['age__max']
        self.answer7 = Author.objects.filter(age=max_age)

        self.answer8 = Author.objects.filter(phone_number__isnull=False).exclude(phone_number='').count()

        self.answer9 = Author.objects.filter(age__lt=25)

        self.answer10 = Author.objects.annotate(article_count=Count('entries')).values('username', 'article_count')

        context = {f'answer{index}': self.__dict__[f'answer{index}'] for index in range(1, 11)}

        return render(request, 'train_db/training_db.html', context=context)