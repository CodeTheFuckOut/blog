#imports and libs
from django.contrib import admin
from .forms import  IconForm, CategoryForm, PostForm, MediaForm, CommentForm
from .models import Icon, Category, Post, Media, Comment

#Icon admin 
class IconAdmin( admin.ModelAdmin ) :
    
    list_display = [ "__unicode__", "timestamp", "updated" ]
    form = IconForm
    
#End IconAdmin class

#Category admin class 
class CategoryAdmin( admin.ModelAdmin ) :
    
    list_display = [ "__unicode__", "icon", "timestamp", "updated" ]
    form = CategoryForm
    
#End Category admin class

#Admin clss 
class PostAdmin( admin.ModelAdmin ) :
    
    list_display = [ "__unicode__", "category", "user", "timestamp", "updated" ]
    form = PostForm

#End post admin class

# Media Admin
class MediaAdmin( admin.ModelAdmin ) :
    
    list_display = [ '__unicode__', 'post' ]
    form = MediaForm
    
#End of Media admin class

class CommentAdmin( admin.ModelAdmin ) :
    
    list_display = [ 'author', 'post', 'timestamp', 'updated' ]
    form = CommentForm

#End of comment admin class

#export all the admin classes to the admin site view
admin.site.register( Icon, IconAdmin )
admin.site.register( Category, CategoryAdmin )
admin.site.register( Post, PostAdmin )
admin.site.register( Media, MediaAdmin )
admin.site.register( Comment, CommentAdmin )