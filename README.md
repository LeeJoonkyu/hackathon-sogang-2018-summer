# Parikng For All ( 주차공유 플랫폼 ) v 1.0
Parking For All은 서강대학교 제 4회 해커톤 경진대회에서 `장충체육관`팀이 개발한 주차공유 플랫폼입니다.

## 1. What?
주택가 밀집지역의 핵심 문제인 "주차 공간 부족" 을 해결하기 위한 플랫폼입니다. 공유경제라는 개념을 기반으로 하여 이 문제를 해결하려했고 [예시 사이트](http://49.236.137.192/) 에서 예시를 확인 할 수 있습니다.

## 2. Develop Environment

#### [1] `Ubuntu` 16.0.4
리눅스 환경을 기반으로 하여, 서버를 구축하였고 사이트를 이 서버에서 배포중입니다. 
#### [2] `Django` 2.0.8
`Django` 2.0.8을 이용하여 백엔드 환경을 구성하고, 회원을 관리하는 웹앱(Account)과 게시판을 관리하는 웹앱(Board) 두 개를 만들었습니다. 이 두 개를 함께 사용하여 MTV패턴을 지키면서 주차공유 플랫폼인, Parking For All이 개발되었습니다.
#### [3] `Python` 3.5.2
`pyenv`와 `pip`를 이용하여 개발의 편이를 위해 가상환경을 구성하고, 구성된 가상환경에서 `django`를 이용하여 웹앱을 개발 했습니다.



## 3. Source Code Specification

#### [1] Account
Account, 회원 관리를 위한 웹앱은 `django`에서 제공하는 User 모델을 이용하여 모델 폼을 구성하였습니다.

```
# forms.py
# User Form
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password','first_name','last_name',]
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password' : forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'주소',}),
            'last_name' : forms.TextInput(attrs={'class':'form-control','placeholder':'상세주소',}),
        }
        labels = {
            'username' : '아이디',
            'email' : '이메일',
            'password' : '패스워드',
            'first_name' : '주소',
            'last_name' : '상세주소',
        }
```

| 필드명 | 폼 타입 | 설명 |
| ---- | ---- | -------- |
| username | Text Input | 유저 Id |
| email | Email Input | 유저 Email |
| password | Password Input | 유저 PassWord|
| first\_name| Text Input | 유저 주소 |
| last\_name | Last Input | 유저 상세 주소 |


첫 기획은 `django.contrib.auth.models`의 `User` 모델을 사용하여 username, email, password 를 사용하려 했습니다.

하지만, 기획의 변화에서 주소와 상세주소를 daum api 이용해서 사용자에게 입력받을 필요성이 생겼습니다. 새로 커스텀 모델을 구성하기엔 다른 것도 갈아 엎어야 하기 때문에, 팀에서 협의하여 User 모델에서 제공하는 first_name과 last_name을 조금 바꾸어서 주소와 상세주소로 이용하기로 했습니다.
___

```
# forms.py
# Login Form
class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
                'username':forms.TextInput(attrs={'placeholder':'Username','class':'form-control'}),
                'password':forms.PasswordInput(attrs={'placeholder':'Password','class':'form-control'}),
        }
```

| 필드명 | 폼 타입 | 필수여부 |
| ---- | ---- | -------- |
| username | Text Input | 필수 |
| password | Password Input | 필수 |
___
View는 SignUp과 SignIn을 구성하였으며 에러가 발생할시 페이지를 리다이렉트 시키도록 하엿습니다.

```
# views.py
# SignUp View

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('board:post_list')

        else:
            return HttpResponseRedirect('/error/')

    else:
        form = UserForm()
        return render(request,'Account/adduser.html',{'form':form})
```
단순하게 회원가입을 하려고 POST를 할 때는 form이 다 채워져있는지 검증을 하고, 검증이 되면 가입을 한 후 로그인이 되게 하여 board로 리다이렉트 시켰습니다. 만약에 검증에 실패하면 에러 페이지로 이동하게 하였고, 회원가입 페이지에 처음 도달 헸을 때는 UserForm을 보여주었습니다.
___



```
# views.py
# SignIn View

def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username,password = password)

        if user is not None:
            login(request,user)
            return redirect('board:post_list')
        else:
            return HttpResponseRedirect('/esignin/')
    else:
        form = LoginForm()
        return render(request,'Account/login.html',{'form':form})
```
회원가입과 유사하게 form을 검증하고 검증이 되면 로그인을 하게 했고, 검증 되지 않으면 에러 페이지로 리다이렉트 시켰습니다. 

#### [2] Board
Board에서는 Post를 관리 할 모델이 필요하여 커스텀 Post모델을 구성하였습니다.
Post 모델에는 작성자, 제목, 내용, 생성 수정 시간과 주차 가능 여부를 설정했습니다.
최신순 정렬을 Mete 클래스를 달았고, 제목 으로 게시글을 표시하기 위해 __str__ 함수를 사용했습니다.
```
# model.py
# Post Model

class Post(models.Model):
    name = models.CharField(max_length=150)
    title = models.CharField(max_length=100, verbose_name='주소를 입력하세요')
    detail = models.CharField(max_length=100,verbose_name='주소를 입력하세요')
    is_on = models.IntegerField(default=1)
    content = models.TextField(verbose_name='계좌번호와 희망 요금을 입력하세요')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-id']
    def __str__(self):
        return self.title
```

| 필드명 | 모델 필드 타입 | 설명 |
| ---- | ---- | -------- |
| name | CharField | 글 제목 |
| title | CharField | 주소 |
| detail | CharField | 상세 주소 |
| content| TextField | 글 내용 |
| created_at | DateTimeField | 글 게시시간 ( 자동 입력 ) |
| updated_at | DateTimeField | 글 수정시간 ( 자동 입력 ) |
| is_on | IntegerField | 주차공간 대여가능 여부 |
(ordering에 대한 설명과 포스트에 관한 설명 부탁)
___

```
# views.py
# Post List, Detail

def post_list(request):

    qs = Post.objects.all()
    q = request.GET.get('q','')
    if q:
        qs = qs.filter(title__icontains=q)

    response = render(request, 'board/post_list.html', {
        'post_list' : qs,
        'q' : q,

    })
    return response

def post_detail(request,id):
    post = get_object_or_404(Post,id=id)

    return render(request,'board/post_detail.html',{
        'post' : post
    })
```
리스트의 핵심기능은 검색입니다.

수요자가 키워드를 입력하고 검색하게 하기위해
쿼리셋에 Post 인스턴스를 받아오고,

검색의 GET 요청에 해당하는 키워드를 q에 넣은 다음, 


title__icontains 키워드로
필터링하였습니다.

리턴값으로 모든 객체에 해당하는 쿼리셋인 qs와 키워드 값을 넘겨줌으로써 

리스트함수를 구현했습니다.

또한 디테일 뷰의 경우 해당하는 id값을 넘겨 받아 post_detail.html 로 넘겨주게 했습니다.
___



```
# views.py
# Post Create, Delete

@login_required
def post_create(request):
    ctx = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        detail = request.POST.get('detail')
        content = request.POST.get('content')

        if title and content:
            post = Post.objects.create(
                title=title,
                detail = detail,
                content=content,
                name = request.user.get_username(),
                is_on = 1,
            )
            url = reverse('board:post_detail', kwargs={
                'id': post.id,
            })
            return redirect(url)
        else:
            error_msg={}
            if not title:
                error_msg.update({'title':'제목을 입력해주세요'})
            if not content:
                error_msg.update({'content': '내용을 입력해주세요'})
            ctx.update({'error':error_msg, })

    return render(request,'board/post_create.html', ctx)

@login_required
def post_delete(request,id):
    post = get_object_or_404(Post, id=id)
    post.delete()
    return redirect('board:post_list')
```
 
CRUD에 해당하는 함수입니다. 

create 함수의 경우 POST 요청이 들어왔을때,

title(주소), detail(상세주소), content(계좌와 희망요금)에 

request를 담아두고 이를 객체로 만들어 넘깁니다. 

create가 끝나면 해당 게시글 내용으로 이동합니다.

delete가 끝나면 리스트로 돌아가도록 리디렉션 했습니다.

## 3. Biz Model

