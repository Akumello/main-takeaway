from django.shortcuts import render
from main_takeaway.language_processor import extract_web


def index(request):
    context = {'output': extract_web('https://www.seriouseats.com/taste-test-the-best-ketchup')}
    return render(request, 'index.html', context)
