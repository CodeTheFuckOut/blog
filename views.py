from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
from forms import PostForm, MediaForm, UploadImgurFileForm, CommentViewForm, CommentChildViewForm

from .serializers import PostSerializer
from .models import Icon, Category, Post, Media, Comment
from .imgur import *
from itertools import *

def index( request ) : 
    """
    Index, this is tha main page of the blog
    """
    #Call all the categories    
    categories = Category.objects.all()
    #Call the last 4 posts
    resent_posts = Post.objects.all().reverse()[:4]
    #Get last 4 coding posts
    coding_p = Post.objects.filter( category = Category.objects.get( name='Coding' )  ).reverse()[:5]
    #Get last 5 server management posts
    server_p = Post.objects.filter( category = Category.objects.get( name='Server Management' )  ).reverse()[:5]
    #Get last 5 databases posts
    databases_p = Post.objects.filter( category = Category.objects.get( name='Data Bases' )  ).reverse()[:5]
    #Join all the coding posts   
    recent_development_posts = chain( server_p, databases_p, coding_p )
    #Get last 5 recent us posts  
    recent_us_posts = Post.objects.filter( category = Category.objects.get( name='Us' )  ).reverse()[:5]
    #Get last 15 recent news posts
    recent_news_posts = Post.objects.filter( category = Category.objects.get( name='News' )  )[:15]
    #Initialize context
    context = {
        
        'title' : 'Code The Fuck Out!!!',
        'blog_title' : 'Code The Fuck Out',
        'blog_des' : 'We fucking do development',
        'categories' : categories, 
        'resent_posts' : resent_posts, 
        'recent_development_posts' : recent_development_posts,
        'recent_us_posts' : recent_us_posts,
        'recent_news_posts' : recent_news_posts
    }
    #Render the blog index template and send context
    return render( request, 'blog/index.html', context )

#End of index funciton view

def new_post( request ) :
    """
    New_post
    function that returns the new post view
    returns a rendered view and recieves a request
    """    
    #Validate the request is a post method and not a get
    if request.method == 'POST':
        #initialize the post form with what the post sends
        post_form = PostForm( request.POST, prefix="post_form")
        instance = post_form.save( commit = False )
        instance.save()
        #for for reading all the files
        for count, x in enumerate( request.FILES.getlist( "files" ) ) :
            #call the funciton porcess_file
            save_image( x, instance.id )
        #initialize a context object
        context = {
    
            'title' :  'add a new post',
            'post_form' : post_form
            
        }
        #reutrn the view again but with the post form validated
        return render( request, 'admin_uploads/new_post.html', context )
    #If it is a get pettition
    else:
        #initialize the post form with nothing
        post_form = PostForm(prefix="post_form")
    #initialize a context object 
    context = {
    
        'title' :  'add a new post',
        'post_form' : post_form
        
    }
    #return a rendered view with the form that has nothing
    return render( request, 'admin_uploads/new_post.html', context )
    
#End of the new_post method

def post_detail( request, pk ) :
    """
    post detail
    function that returns a view with a post shit
    """
    # Post validation
    if request.method == 'POST' :
        comment_form = CommentViewForm( request.POST, prefix='comment_form' )
        instance = comment_form.save( commit = False )
        p = Post.objects.get( pk = pk )
        instance.post = p
        instance.is_child = False
        instance.save()
    #Comment form
    comment_form = CommentViewForm( prefix = "comment_form" )
    #Call all the categories    
    categories = Category.objects.all()
    #Get the post 
    p = Post.objects.get( pk = pk )
    #get all the post comments
    c = Comment.objects.filter( post = p )
    #Get all the images of the post
    m = Media.objects.filter( post = p )
    #Context variable to the view
    context = {
        
        'title' : 'Code The Fuck Out!!!',
        'blog_title' : 'Code The Fuck Out',
        'blog_des' : 'We fucking do development',
        'categories' : categories, 
        'post' : p,
        'comments' : c,
        'medias' : m,
        'comment_form' : comment_form
        
    }
    #Render the blog index template and send context
    return render( request, 'blog/post_detail.html', context )
    
#End of post detail controller function

def comment_detail( request, pk ) :
    """
    comment detail
    function that returns a view with a comment shit
    """
    # Post validation
    if request.method == 'POST' :
        child_comment_form = CommentChildViewForm( request.POST, prefix = 'child_comment_form' )
        # Get the comment
        c = Comment.objects.get( pk = pk )
        # Get the comments post
        p = c.post
        # create the instance and cancel the commit
        instance = child_comment_form.save( commit = False )
        # Add the child true
        instance.is_child = True
        # Add the post to the comment
        instance.post = p
        # Save the comment
        instance.save()
        # add the comment to the 
        c.threads.add( instance )
        c.save()
    #End of validation
    c = Comment.objects.get( pk = pk )
    p = c.post
    child_comment_form = CommentChildViewForm( prefix = 'child_comment_form' )
    #Call all the categories    
    categories = Category.objects.all()
    #Context variable to the view
    context = {
        
        'title' : 'Code The Fuck Out!!!',
        'blog_title' : 'Code The Fuck Out',
        'blog_des' : 'Comment section',
        'categories' : categories, 
        'post' : p,
        'comment' : c,
        'child_comment_form' : child_comment_form
        
    }
    #Render the comment detail view and send the context
    return render( request, 'blog/comment_detail.html', context )
#End comment_detail controller function

def post_child_comment( request, pk ) :
    """ Post child comment view """
    if request.method == 'POST' :
        comment_form = CommentChildViewForm( request.POST, prefix = 'comment_form' )
        instance = comment_form.save( commit = False )
        p = Post.objects.get( pk = pk )
        instance.post = p
        instance.is_child = True
        instance.save()
    #Comment form if not post

#End of post_child_comment view function