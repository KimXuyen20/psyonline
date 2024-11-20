from django.shortcuts import render

from blog.models import Blog

# Create your views here.
def blog(request):
    blogs = Blog.objects.all().filter(is_available=True)
    context = {
        'blogs':blogs,
    }
    return render(request, 'blog/blog.html',context)