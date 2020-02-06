from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from datetime import datetime
from django.urls import reverse_lazy

from article.models import Post
from article.forms import ArticleForm,ArticleModelForm,CommentForm
from django.contrib import messages


# Create your views here.

def post_detail(request, post_id):
    pk = post_id
    # post = Post.objects.get(id=pk)
    post = get_object_or_404(Post, id=pk, draft=False)
    comments = post.comments.all()
    form = CommentForm(request.POST or None)
    print(post)
    context = {
        'post': post,
        'comments': comments,
        'form' :form
    }
    if request.method == 'POST':
        if form.is_valid():
            form.instance.post = post
            form.save()
            messages.add_message(request,messages.SUCCESS,'basarili')
            return redirect('post_detail',post_id=post.id)
    return render(request, 'article/post_detail.html', context)


def post_list(request):
    queryset = Post.objects.all()
    context = {
        'postlar': queryset
    }
    print(queryset)
    return render(request, 'article/post_list.html', context=context)


def anasayfa(request):
    context = {
        'django': True,
        'flask': True,
        'pehape': False,
        'now': datetime.now()

    }
    return render(request, template_name='article/index.html', context=context)


def create_post(request):
    form = ArticleForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            header = form.cleaned_data['header']
            content = form.cleaned_data['content']
            liked = form.cleaned_data['liked']
            draft = form.cleaned_data['draft']
            post = Post.objects.create(
                header=header, content=content, liked=liked, draft=draft, owner=request.user
            )
            post.save()
            return HttpResponse('nesne yaratıldı')

    else:
        print(request.user)
        return render(request, 'article/post_create.html', {'form': form})

def createPostMF(request):
    form =ArticleModelForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.instance.owner = request.user
            form.save()
            return  HttpResponse('nesne yaratıldı')
    return render(request, 'article/post_create.html', {'form': form})



from django.views.generic import ListView,CreateView,DetailView,FormView,UpdateView,DeleteView

class ArticleListView(ListView):
    model = Post
    template_name = 'article/post_list.html'
    queryset = Post.objects.all()
    context_object_name = 'postlar'


class ArticleCreatView(CreateView):
    model = Post
    form_class = ArticleModelForm
    success_url = reverse_lazy('anasayfa')
    template_name = 'article/post_create.html'

    def form_valid(self, form):
        form.instance.owner=self.request.user
        return super().form_valid(form)

class ArticleDetailView(DetailView,FormView):
    model = Post
    pk_url_kwarg = 'post_id'
    context_object_name = 'post'
    template_name = 'article/post_detail.html'
    form_class = CommentForm
    success_url = reverse_lazy('anasayfa')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        print(self.object)
        return context
    def form_valid(self, form):
       # ujmu,muhmööhmhö,m self.object = self.model.objects.get(id=self.kwargs['post_id'])
        form.instance.post=self.get_object()
        form.save()
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Post
    form_class = ArticleModelForm
    template_name = 'article/post_create.httml'
    succes_url = reverse_lazy('anasyfa')
    succes_message = 'Basari ile güncellendi'
    pk_url_kwarg = 'post_id'

class ArticleDeleteView(LoginRequiredMixin, SuccessMessageMixin,DeleteView):
    model = Post
    template_name = 'article/post_delete.httml'
    pk_url_kwarg = 'post_id'
    success_url = reverse_lazy('anasayfa')

    def delete(self, request, *args, **kwargs):
        messages.add_message(self.request,messages.INFO,self.success_message)
        return super().delete(request , *args,**kwargs)