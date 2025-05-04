#server/affiche/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils.safestring import mark_safe
from django.contrib import messages
from .models import Performance, Theater, Comment
from .forms import PerformanceForm, CommentForm
from django.forms import inlineformset_factory
import calendar
from datetime import datetime, date, timedelta
from django.http import Http404


class RussianHTMLCalendar(calendar.HTMLCalendar):
    def __init__(self):
        super().__init__()
        self.month_names = [
            '', 'Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
            'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'
        ]
        self.day_abbr = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
        self.today = datetime.now().date()

    def formatmonthname(self, theyear, themonth, withyear=True):
        month_name = self.month_names[themonth]
        if withyear:
            return f'{month_name} {theyear}'
        return month_name

    def formatweekday(self, day):
        return f'<th class="{self.cssclasses[day]}">{self.day_abbr[day]}</th>'

    def formatday(self, day, weekday):
        if day == 0:
            return '<td class="noday">&nbsp;</td>'
        else:
            cssclass = self.cssclasses[weekday]
            if day == self.today.day and self.today.month == self.currentmonth and self.today.year == self.currentyear:
                cssclass += ' current-day'
            return f'<td class="{cssclass}">{day}</td>'



class CalendarView(generic.TemplateView):
    template_name = 'affiche/calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        now = datetime.now()
        
        try:
            year = int(self.request.GET.get('year', now.year))
            month = int(self.request.GET.get('month', now.month))
        except (ValueError, TypeError):
            year = now.year
            month = now.month
        
        # Рассчитываем предыдущий и следующий месяц
        if month == 1:
            prev_month = date(year-1, 12, 1)
            next_month = date(year, month+1, 1)
        elif month == 12:
            prev_month = date(year, month-1, 1)
            next_month = date(year+1, 1, 1)
        else:
            prev_month = date(year, month-1, 1)
            next_month = date(year, month+1, 1)
        
        # Получаем все события для выбранного месяца
        performances = Performance.objects.filter(
            date__year=year,
            date__month=month
        ).order_by('date')
        
        # Группируем события по дням
        events_by_day = {}
        for performance in performances:
            day = performance.date.day
            if day not in events_by_day:
                events_by_day[day] = []
            events_by_day[day].append(performance)
        
        # Создаем календарь с русскими названиями
        cal = RussianHTMLCalendar()
        cal.currentyear = year
        cal.currentmonth = month
        calendar_html = cal.formatmonth(
            theyear=year,
            themonth=month,
            withyear=True
        )
        
        # Заменяем числа дня на список событий
        for day, events in events_by_day.items():
            events_html = f'<div class="day-number">{day}</div>'
            events_html += '<div class="day-events">'
            for event in events:
                events_html += f'''
                    <div class="event-item">
                        <a href="/performance/{event.id}/" class="event-link">
                            {event.date.strftime("%H:%M")} - {event.title}
                        </a>
                    </div>
                '''
            events_html += '</div>'
            
            calendar_html = calendar_html.replace(
                f'>{day}<',
                f'>{events_html}<',
                1
            )
        
        # Форматируем текущий месяц и год в русском формате
        current_month = cal.month_names[month]
        current_month_year = f"{current_month} {year}"
        
        # Форматируем предыдущий и следующий месяцы
        prev_month_name = cal.month_names[prev_month.month]
        next_month_name = cal.month_names[next_month.month]
        
        context.update({
            'calendar': mark_safe(calendar_html),
            'performances': performances,
            'current_month': current_month_year,
            'prev_month': prev_month,
            'next_month': next_month,
            'prev_month_name': f"{prev_month_name} {prev_month.year}",
            'next_month_name': f"{next_month_name} {next_month.year}"
        })
        return context

class PerformanceListView(generic.ListView):
    model = Performance
    template_name = 'affiche/index.html'
    context_object_name = 'performances'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = Performance.objects.select_related('theater').order_by('date')
        
        # Фильтрация по театру
        theater = self.request.GET.get('theater')
        if theater:
            queryset = queryset.filter(theater_id=theater)
        
        # Фильтрация по жанру
        genre = self.request.GET.get('genre')
        if genre:
            queryset = queryset.filter(genre=genre)
        
        # Фильтрация по возрасту
        min_age = self.request.GET.get('min_age')
        if min_age:
            queryset = queryset.filter(min_age__lte=min_age)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theaters'] = Theater.objects.all()
        context['genre_choices'] = Performance.GENRE_CHOICES
        context['current_filters'] = {
            'theater': self.request.GET.get('theater', ''),
            'genre': self.request.GET.get('genre', ''),
            'min_age': self.request.GET.get('min_age', ''),
        }
        return context
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['theaters'] = Theater.objects.all()
        context['genre_choices'] = Performance.GENRE_CHOICES
        context['current_filters'] = {
            'theater': self.request.GET.get('theater', ''),
            'genre': self.request.GET.get('genre', ''),
            'min_age': self.request.GET.get('min_age', ''),
            'max_duration': self.request.GET.get('max_duration', ''),
        }
        return context

class PerformanceDetailView(generic.DetailView):
    model = Performance
    template_name = 'affiche/performance_detail.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        comments = self.object.comments.all()
        for comment in comments:
            comment.can_edit = comment.can_edit(self.request.user)
        context['comments'] = comments
        return context

class PerformanceCreateView(LoginRequiredMixin, UserPassesTestMixin, generic.CreateView):
    model = Performance
    form_class = PerformanceForm
    template_name = 'affiche/performance_form.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        print("Form is valid")
        print("Form data:", form.cleaned_data)
        self.object = form.save()
        print("Object saved:", self.object)
        messages.success(self.request, 'Постановка успешно создана!')
        return redirect(self.object.get_absolute_url())
    
    def form_invalid(self, form):
        print("Form is invalid")
        print("Form errors:", form.errors)
        return super().form_invalid(form)

class PerformanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Performance
    form_class = PerformanceForm
    template_name = 'affiche/performance_form.html'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        self.object = form.save()
        return redirect(self.object.get_absolute_url())

class PerformanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Performance
    template_name = 'affiche/performance_confirm_delete.html'
    success_url = '/'
    
    def test_func(self):
        return self.request.user.is_staff

def scrape_performances(request):
    if request.user.is_authenticated and request.user.is_admin():
        from .utils import scrape_teatrarmii
        scrape_teatrarmii()
        return redirect('affiche:index')
    else:
        return redirect('accounts:login')

class CommentCreateView(LoginRequiredMixin, generic.CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'affiche/performance_detail.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.performance = get_object_or_404(Performance, pk=self.kwargs['pk'])
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.performance.get_absolute_url()


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'affiche/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return comment.can_edit(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment'] = self.object
        return context

    def form_valid(self, form):
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.performance.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = 'affiche/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return comment.can_delete(self.request.user)

    def get_success_url(self):
        return self.object.performance.get_absolute_url()