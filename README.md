# Library-system
>## 复现django + python完成的图书管理系统。第一个学习django的案例。

### 安装依赖
```
pip install Django -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 创建项目和APP
```
django-admin startproject booktest
cd booktest
django-admin startapp book_managerment
```

### 在 booktest\booktest\settings.py 中找到INSTALLED_APPS这一项，修改为
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'book_managerment'
]
```

### 修改booktest\book_managerment\models.py
```
from django.db import models

class Author(models.Model):
    name = models.CharField(max_length=32)
    age = models.SmallIntegerField()
    gender_choices = (
        (0, "女"),
        (1, "男"),
        (2, "保密"),
    )
    gender = models.SmallIntegerField(choices=gender_choices)
    tel = models.CharField(max_length=32)
    addr = models.CharField(max_length=64)
    birthday = models.DateField()


class Book(models.Model):
    title = models.CharField(max_length=32)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    pub_date = models.DateField()
    publish = models.ForeignKey("Publish", on_delete=models.CASCADE)
    authors = models.ManyToManyField("Author")


class Publish(models.Model):
    name = models.CharField(max_length=32)
    city = models.CharField(max_length=64)
    email = models.EmailField()
```

### 生成迁移文件：根据模型类生成创建表的语句
`python manage.py makemigrations`
### 执行迁移：根据第一步生成的语句在数据库中创建表
`python manage.py migrate`


### 插入数据
## VScode中安装SQLite, 右键db文件, 插入数据, 右键关联db.sqlite3文件, run quey
```

insert into book_managerment_publish(id, name, city, email)
values (1, "华山出版社", "华山", "hs@163.com"),
       (2, "明教出版社", "黑木崖", "mj@163.com");

insert into book_managerment_author(id, name, age, gender, tel, addr, birthday)
values (1, "令狐冲", 25, 1, 13432335433, "华山", "1994-5-23"),
       (2, "任我行", 58, 1, 13943454554, "黑木崖", "1961-8-13"),
       (3, "任盈盈", 23, 0, 13878934322, "黑木崖", "1996-5-20");

INSERT INTO book_managerment_book(id, title, price, pub_date, publish_id)
VALUES (1, "独孤九剑", 200, "2019-1-7", 1),
       (2, "吸星大法", 180, "2019-1-7", 2),
       (3, "葵花宝典", 280, "2019-3-15", 2);

INSERT INTO book_managerment_book_authors(id, book_id, author_id)
VALUES (1, 1, 1),
       (2, 1, 2),
       (3, 2, 2);
```

### 打开booktest/booktest/settings.py文件
```
LANGUAGE_CODE = 'zh-Hans'
TIME_ZONE = 'Asia/Shanghai'
```

### 创建管理员
```
python manage.py createsuperuser
```

### 打开booktest\booktest\admin.py文件
```
from django.contrib import admin
from .models import *


class BookModal(admin.StackedInline):
    model = Book


@admin.register(Publish)
class PublishAdmin(admin.ModelAdmin):
    inlines = [BookModal]
    list_display = ('id', 'name', 'city', 'email', 'books')
    fields = ('name', 'city', 'email')
    list_filter = ['city']
    search_fields = ['name', 'city']

    def books(self, obj):
        return [book.title for book in obj.book_set.all()]


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'price', 'pub_date', "publish_name", "author")
    fields = ('title', 'price', 'pub_date', "authors")
    search_fields = ['title', 'price', 'pub_date']

    def author(self, obj):
        return [author.name for author in obj.authors.all()]

    def publish_name(self, obj):
        return obj.publish.name

    filter_horizontal = ('authors',)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'age', 'gender', 'tel', 'addr', 'birthday', 'books')
    fields = ('name', 'age', 'gender', 'tel', 'addr', 'birthday')
    list_filter = ['gender']
    search_fields = ['name', 'age', 'gender', 'tel', 'addr', 'birthday']

    def books(self, obj):
        return [book.title for book in obj.book_set.all()]
```

### 创建目录booktest/templates/admin/
### 新增文件base_site.html
```
{% extends "admin/base.html" %}

{% block title %}图书后台管理系统{% endblock %}

{% block branding %}
    <h1 id="site-name"><a href="{% url 'admin:index' %}">图书后台管理系统</a></h1>
{% endblock %}

{% block nav-global %}{% endblock %}
```

### 启动
`python manage.py runserver`
- 参考自[https://mp.weixin.qq.com/s/btuBRt182ReO_pfaFffG2A]