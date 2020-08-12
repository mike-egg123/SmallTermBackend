# 引入表单类
from django import forms
# 引入 User 模型
from django.contrib.auth.models import User
from .models import Profile

# 登录表单，继承了 forms.Form 类
class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()
# 注册表单
class UserRegisterForm(forms.ModelForm):
    # 复写User
    password = forms.CharField()
    password2 = forms.CharField()

    class Meta:
        model = User
        fields = ('username', 'email')

    # 对两次输入的密码进行检查，如果通过则返回密码
    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            return forms.ValidationError('密码输入不一致，请重新输入。')

# 扩展用户信息的表单
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('phone', 'avatar', 'bio','userid')

