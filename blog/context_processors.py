from .models import Blog

def blog(request):
    blogs = Blog.objects.all()[:3]
    return {'blogs': blogs}
