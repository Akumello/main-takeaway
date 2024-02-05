from django.http import HttpRequest
from django.shortcuts import render
from main_takeaway.language_processor import get_takeaway_output


def index(request: HttpRequest):
    url: str = ''

    if request.method == 'GET':
        url = 'https://www.seriouseats.com/taste-test-the-best-ketchup'
    else:
        url = request.POST['url']

    print(url)

    context = {'output': get_takeaway_output(url)}
    return render(request, 'index.html', context)
