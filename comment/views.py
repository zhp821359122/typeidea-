from django.shortcuts import render,redirect
from django.views.generic import TemplateView
from .forms import CommentForm

# Create your views here.


class CommentView(TemplateView):
    http_method_names = ['post']
    template_name = 'comment/result.html'

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        target = request.POST.get('target')

        if comment_form.is_valid():
            instance = comment_form.save(commit=False)
            instance.target = target
            instance.save()
            return redirect(target)
        else:
            context = {
                'form': comment_form,
                # 'target': target,
            }
            return self.render_to_response(context)
# def add_comment(request):
#     if request.method == 'POST':
#         form_obj = CommentForm(request.POST)
#         if form_obj.is_valid():
#             comment_obj = form_obj.save(commit=False)
#             comment_obj.target = request.POST.get('target')
#             comment_obj.save()
#             return redirect(request.POST.get('target'))