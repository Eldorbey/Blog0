from .models import Category, Tag
def category(request):
    categories = Category.objects.all()

    return {'categories':categories}


def top_blogs(request):
    categories = Category.objects.all()



def tag(request):

    tags = Tag.objects.all()

    return {'tags':tags}