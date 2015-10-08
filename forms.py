# -*- coding: utf-8 -*-
from django import forms
from .models import Icon, Category, Post, Media, Comment

"""
The fucken icon form
"""
class IconForm( forms.ModelForm ) :
    
    """
    Meta class for icon form
    """
    class Meta : 
        model = Icon
        fields = [ 'name' ]
    #End of meta class
    
#End of icon form class 

"""
Category form
"""
class CategoryForm( forms.ModelForm ) :
    
    description = forms.CharField( widget = forms.Textarea )
    
    """
    Meta class for icon form
    """
    class Meta : 
        model = Category
        fields = [ 'name', 'description', 'icon' ]
    #En d of meta class
    
#End of category form class
 
"""
Post form
"""
class PostForm( forms.ModelForm ) : 
    
    content = forms.CharField( widget = forms.Textarea )
    
    """
    Meta class for post form
    """
    class Meta :
        model = Post
        fields = [ 'title', 'content', 'category' ]
    #End of meta class
    
#End of post form class

"""
Media form
"""
class MediaForm( forms.ModelForm ) :
    
    """
    Meta class for media form
    """
    class Meta :
        model = Media
        fields = [ 'url', 'post' ]
    #End of meta class
    
#End of Media form class

"""
Upload imgur file form
"""
class UploadImgurFileForm( forms.ModelForm ) :
    
    file = forms.ImageField( )
    
#End of upload imgur file form class

"""
Comment form Class
"""
class CommentForm( forms.ModelForm ) :
    
    """
    Meta class
    """
    class Meta :
        model = Comment
        fields = [ 'author', 'content', 'post', 'threads', 'is_child' ]
    #End of meta class
    
#End of comment admin form class

"""
Commet view form
this will be directly on the comment section of the posts
"""
class CommentViewForm( forms.ModelForm ) :
    
    author = forms.CharField( widget=forms.TextInput( attrs = { 'placeholder' : 'Author' } ), label="" )
    content = forms.CharField( widget=forms.Textarea( attrs = { 'placeholder' : 'Comment' } ), label="" )
    
    """ 
    Meta class for the comment view form 
    """
    class Meta : 
        model = Comment
        fields = [ 'author', 'content' ]
    #End of meta class
    
#End of comment view form class

"""
Commet view form
this will be directly on the comment section of the posts
"""
class CommentChildViewForm( forms.ModelForm ) :
    
    author = forms.CharField( widget=forms.TextInput( attrs = { 'placeholder' : 'Author' } ), label="" )
    content = forms.CharField( widget=forms.Textarea( attrs = { 'placeholder' : 'Reply' } ), label="" )
    
    """ 
    Meta class for the comment view form 
    """
    class Meta : 
        model = Comment
        fields = [ 'author', 'content' ]
    #End of meta class
    
#End of comment view form class