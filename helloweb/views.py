from django.http import HttpResponse
import datetime

from django.views import View


def index(request):
    return HttpResponse("""
    <h1>Hello from Django !</h1>
    <p>Test base url</p>
    """)


def current_datetime(request, anything=None):
    now = datetime.datetime.now()
    return HttpResponse(f"""
    <h1>Current datetime:</h1>
    <p>{now}</p> """)


class CurrentDatetime(View):
    def get(self, request):
        now = datetime.datetime.now()
        return HttpResponse(f"""
            <h1>Current datetime:</h1>
            <p>{now}</p> """)
