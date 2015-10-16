# Libs
from django.db import models
from django.contrib.auth.models import User

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
    
    def get_absolute_url( self ) :
        return ( "/posts/{0}/" ).format( self.pk )
    #End of get_absolute_url function
    
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
        
    