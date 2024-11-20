from django.shortcuts import render

from blog.models import Blog

# Create your views here.
def blog(request):
    blogs = Blog.objects.all().filter(is_available=True)
    context = {
        'blogs':blogs,
    }
    return render(request, 'blog/blog.html',context)


def blog_detail(request, blog_slug):
    try:
        single_blog = Blog.objects.get(slug = blog_slug)
    except Exception as e:
        raise e
    
    context = {
        'single_blog':single_blog,
    }
    return render(request,'blog/blog_detail.html',context)