"""cardalogue URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import (path, include)
from django.conf.urls.static import static, settings
from rest_framework import routers
from cardalogueapi.views import (CardView, CategoryView, CollectionView,
                                 CollectionCommentView, SetView, TagView,
                                 TopicView, TopicCommentView, login_user,
                                 register_user, UserView, CardCollectionView)

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'cards', CardView, 'card')
router.register(r'categories', CategoryView, 'category')
router.register(r'collections', CollectionView, 'collection')
router.register(r'collectioncomments', CollectionCommentView, 'collectioncomment')
router.register(r'sets', SetView, 'set')
router.register(r'tags', TagView, 'tag')
router.register(r'topics', TopicView, 'topic')
router.register(r'topiccomments', TopicCommentView, 'topiccomment')
router.register(r'users', UserView, 'user')
router.register(r'cardcollections', CardCollectionView, 'cardcollection')



urlpatterns = [
    path('admin/', admin.site.urls),
    path('register', register_user),
    path('login', login_user),
    path('', include(router.urls)),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
