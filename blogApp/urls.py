from . import views
from django.urls import path


app_name='blog'
urlpatterns = [
   
    path("",views.index,name="BlogHome"),
    path("blog/",views.post_list,name='post_list'),
    path('blog/tag/<slug:tag_slug>/',views.post_list,name='post_list_by_tag'),
    # path('post/<int:id>/',views.post_details,name='post_detail'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:post>/',views.post_details,name='post_detail'),
    path('blog//share/<int:post_id>/',views.post_share,name='post_share'),
    path('blog/comment/<int:post_id>/', views.post_comment,name='post_comment'),
    path('blog/search/', views.search,name='search'),

#    User registration
    path('accounts/register/',views.RegistrationView.as_view(),name='register'),
    # path('accounts/login/',views.UserLoginView.as_view(),name='login'),
    path('accounts/login/',views.UserLogin,name='login'),
    path('accounts/logout/',views.UserLogout,name='logout'),
    path('accounts/profile/',views.UserProfileView.as_view(),name='profile'),



    # path('blog/addblog/',views.AddBlogView.as_view(),name='add-blog')
    path('blog/addblog/',views.addBlog,name='addblog'),
    path('blog/deleteblog/<int:id>/',views.blog_delete,name='blog_delete'),
    path('blog/updateblog/<slug>/',views.blog_update,name='blog_update'),


]