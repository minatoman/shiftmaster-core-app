# shifts/views/template_views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def view_generated_shift_template(request):
    return render(request, 'templates_generated/template_shift_3block_colored.html')


@login_required
def template_links_view(request):
    return render(request, 'shifts/template_links.html')


