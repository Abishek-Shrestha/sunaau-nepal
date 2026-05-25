from django.http import HttpResponse


def home(request):
	return HttpResponse("""
		<h1>Sunaau Nepal</h1>
		<p>The project is running.</p>
	""")


def favicon(request):
	return HttpResponse(status=204)
