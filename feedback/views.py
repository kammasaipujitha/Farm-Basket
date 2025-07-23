from django.shortcuts import render

# Create your views here.

def feedback_form(request):
    # Placeholder: In real code, handle form submission
    return render(request, 'feedback/feedback_form.html', {'form': {}, 'cancel_url': '#'})
