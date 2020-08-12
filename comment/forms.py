from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 两个外键和创建时间都会自动填写，此处只需要主题内容即可
        fields = ['body']
