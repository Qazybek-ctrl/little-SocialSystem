from django.urls import path, re_path


from .views import ThreadView, InboxView

app_name = 'chatsystem'
urlpatterns = [
    path("", InboxView.as_view()),
    path("<slug>/", ThreadView.as_view(), name='msg'),
]