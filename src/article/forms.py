from django import forms
from article.models import Post, Comment


class ArticleForm(forms.Form):
    header = forms.CharField(required=True)
    content = forms.CharField(widget=forms.Textarea)
    liked = forms.IntegerField(required=True)
    draft = forms.BooleanField(required=True)


class ArticleModelForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ['owner', 'image']
        # fields = '__all__'

    def clean_content(self):
        if len(self.cleaned_data.get('content')):
            raise forms.ValidationError('Icerik 50 karakterden fazla olamaz')
        return self.cleaned_data.get('content')

    def clean_header(self):
        header = self.cleaned_data.get('header')
        if Post.objects.filter(header=header).exists():
            raise forms.ValidationError('Bu baslikta bir makale yoktur')
        return header


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        exclude = ['post']

    def clean_content(self):
        if len(self.cleaned_data.get('comment')):
            raise forms.ValidationError('Icerik 20 karakterden fazla olamaz')
        return self.cleaned_data.get('comment')