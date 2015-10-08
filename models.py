# Libs
from django.db import models
from django.contrib.auth.models import User
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles

#Shit I don't know
LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())

"""
Icon model
"""
class Icon( models.Model ) :
    
    name = models.CharField( max_length= 200 )
    timestamp = models.DateTimeField( auto_now_add = True, auto_now = False )#date uploaded
    updated = models.DateTimeField( auto_now_add = False, auto_now = True )#date updated
  
    def __unicode__( self ) :
        """ unicdode function """
        return self.name
    #End of unicdo function
    
#End of Icon model

"""
Category model
"""
class Category( models.Model ) :
    
    name = models.CharField( max_length = 200 )
    description = models.CharField( max_length = 255, default='' )
    timestamp = models.DateTimeField( auto_now_add = True, auto_now = False )#date uploaded
    updated = models.DateTimeField( auto_now_add = False, auto_now = True )#date updated
    icon = models.ForeignKey( Icon, default=1, unique= False )
    
    def __unicode__( self ) :
        """ unicode function """
        return self.name
    #End of unicode function
    
#End of category model

"""
Post model
"""
class Post( models.Model ) :
    
    title = models.CharField( max_length = 200 )
    content = models.TextField( max_length = None, default='' )
    timestamp = models.DateTimeField( auto_now_add = True, auto_now = False )#date uploaded
    updated = models.DateTimeField( auto_now_add = False, auto_now = True )#date updated
    user = models.ForeignKey( User, default = 1, unique = False )
    category = models.ForeignKey( Category, default = 1, unique = False )
    
    def __unicode__( self ) :
        """ unicode function """
        return self.title
    #End of unicode function
    
#End of post model

"""
Media model is the model where the post saves the all media related to it
"""
class Media( models.Model ) :
    
    url  = models.CharField( max_length = 2048 )
    image_type = models.CharField( max_length = 200 )
    post = models.ForeignKey( Post, unique = False )
    
    def __unicode__( self ) :
        """ unicode function """
        return self.url
    #End of unicode function
    
#End of Media model

"""
Snippets model
"""
class Snippet( models.Model ) :
        
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
        
    """
    Meta class
    """
    class Meta :
        ordering = ( 'created', )
    #End of meta class
    
#End of snippets model

"""
Comment 
model for the comments on the blog
"""
class Comment( models.Model ) :
    
    author = models.CharField( max_length = 200 )
    content = models.TextField( max_length = None, default='' )
    timestamp = models.DateTimeField( auto_now_add = True, auto_now = False )#date uploaded
    updated = models.DateTimeField( auto_now_add = False, auto_now = True )#date updated
    post = models.ForeignKey( Post, default = 1 )
    threads = models.ManyToManyField( 'blog.Comment', blank=True )
    is_child = models.BooleanField( default = False )
    
    def __unicode__( self ) :
        """ unicode function """
        return self.author
    #End of unicode function
    
#End of comment function
        
    