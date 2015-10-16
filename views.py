# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, render_to_response
from forms import PostForm, MediaForm, UploadImgurFileForm, CommentViewForm, CommentChildViewForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#model imports
from .serializers import PostSerializer
from .models import Icon, Category, Post, Media, Comment
from .imgur import *
from itertools import *
#login require imports
from django.contrib.auth.decorators import login_required
#The sitemap important shit
from django.contrib.sitemaps import Sitemap
import datetime

def index( request ) : 
    """
    Index, this is tha main page of the blog
    """
    #Call all the categories    
    categories = Category.objects.all()
    #Call the last 4 posts
    resent_posts = Post.objects.all().order_by( '-timestamp' )[:4]
    #Get last 4 coding posts
    coding_p = Post.objects.filter( category = Category.objects.get( name='Coding' ) ).order_by('-timestamp')[:5]
    #Get last 5 server management posts
    server_p = Post.objects.filter( category = Category.objects.get( name='Server Management' ) ).order_by('-timestamp')[:5]
    #Get last 5 databases posts
    databases_p = Post.objects.filter( category = Category.objects.get( name='Data Bases' ) ).order_by('-timestamp')[:5]
    #Join all the coding posts   
    recent_development_posts = sorted( chain( server_p, databases_p, coding_p ), key=lambda instance: instance.timestamp, reverse=True )
    #Get last 5 recent us posts  
    recent_us_posts = Post.objects.filter( category = Category.objects.get( name='Us' ) ).order_by('-timestamp')[:5]
    #Get last 15 recent news posts
    recent_news_posts = Post.objects.filter( category = Category.objects.get( name='News' ) ).order_by('-timestamp')[:15]
    #Initialize context
    context = {
        
        'title' : 'Code The Fuck Out',
        'blog_title' : 'Code The Fuck Out',
        'blog_des' : 'Un Blog para desarrollo...',
        'categories' : categories, 
        'resent_posts' : resent_posts, 
        'recent_development_posts' : recent_development_posts,
        'recent_us_posts' : recent_us_posts,
        'recent_news_posts' : recent_news_posts
    }
    #Render the blog index template and send context
    return render( request, 'blog/index.html', context )

#End of index funciton view

def about( request ) : 
    """
    Index, this is tha main page of the blog
    """
    #Call all the categories    
    categories = Category.objects.all()
    #Call the last 4 posts
    resent_posts = Post.objects.all().order_by( '-timestamp' )[:4]
    #Get last 4 coding posts
    coding_p = Post.objects.filter( category = Category.objects.get( name='Coding' ) ).order_by('-timestamp')[:5]
    #Get last 5 server management posts
    server_p = Post.objects.filter( category = Category.objects.get( name='Server Management' ) ).order_by('-timestamp')[:5]
    #Get last 5 databases posts
    databases_p = Post.objects.filter( category = Category.objects.get( name='Data Bases' ) ).order_by('-timestamp')[:5]
    #Join all the coding posts   
    recent_development_posts = sorted( chain( server_p, databases_p, coding_p ), key=lambda instance: instance.timestamp, reverse=True )
    #Get last 5 recent us posts  
    recent_us_posts = Post.objects.filter( category = Category.objects.get( name='Us' ) ).order_by('-timestamp')[:5]
    #Get last 15 recent news posts
    recent_news_posts = Post.objects.filter( category = Category.objects.get( name='News' ) ).order_by('-timestamp')[:15]
    #Initialize context
    context = {
        
        'title' : 'Code The Fuck Out',
        'blog_title' : 'Code The Fuck Out',
        'blog_des' : 'Un Blog para desarrollo...',
        'categories' : categories, 
        'resent_posts' : resent_posts, 
        'recent_development_posts' : recent_development_posts,
        'recent_us_posts' : recent_us_posts,
        'recent_news_posts' : recent_news_posts
    }
    #Render the blog index template and send context
    return render( request, 'blog/about.html', context )

#End of about funciton view

@login_required
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
        'blog_des' : 'Un Blog para desarrollo...',
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

def category_detail( request, pk ) :
    """ Category controller """
    #Get category
    cat = Category.objects.get( name = pk )
    #Get the posts of the category
    post_list = Post.objects.filter( category = cat.pk ).order_by('-timestamp')
    #do the pagination logic
    paginator = Paginator( post_list, 5 )
    #initialize the page variable if the request has a page variable
    page = request.GET.get( 'page' )
    #Call all the categories    
    categories = Category.objects.all()
    #Verify the paginations
    try :
        posts = paginator.page( page )
    except PageNotAnInteger :
        # If page is not an integer, deliver first page.
        posts = paginator.page( 1 )
    except EmptyPage :
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page( paginator.num_pages )
    #Context variable
    context = {
        
        'title' : cat.name,
        'blog_title' : 'Code The Fuck Out',
        'blog_des' : 'Categories',
        'categories' : categories,
        'category' : cat,
        'posts' : posts
        
    }
    #Render the view
    return render( request, 'blog/category_detail.html', context )
#End of category_detail controller function

def search( request ) :
    """ 
    Search controller for the search shit that will come out and I don't 
    know what I'm writing 
    """
    if request.method == 'GET' :
        #Get the posts of the category
        post_list = Post.objects.filter( title__icontains=request.GET['query'] ).order_by('-timestamp')
        #do the pagination logic
        paginator = Paginator( post_list, 5 )
        #initialize the page variable if the request has a page variable
        page = request.GET.get( 'page' )
        #Call all the categories    
        categories = Category.objects.all()
        #Verify the paginations
        try :
            posts = paginator.page( page )
        except PageNotAnInteger :
            # If page is not an integer, deliver first page.
            posts = paginator.page( 1 )
        except EmptyPage :
            # If page is out of range (e.g. 9999), deliver last page of results.
            posts = paginator.page( paginator.num_pages )
        #Validate if the list of posts actually has a value
        if len( posts ) == 0 :
            msj = "No parece haber ningún post con esa relación."
        else :
            msj = None
        #Context variable
        context = {
            'title' : 'Búsqueda',
            'blog_title' : 'Code The Fuck Out',
            'categories' : categories,
            'query' : request.GET['query'],
            'posts' : posts,
            'msj' : msj
        }
        #Render the template with the context
        return render( request, 'blog/search.html', context )
    #Context with the 
    context = {
        'title' : 'Búsqueda',
        'blog_title' : 'Code The Fuck Out',
        'categories' : categories,
        'msj' : 'Busqueda incorrecta'
    }
    #REnder the template with the context
    return render( request, 'blog/search.html', context )
#End of search controller

"""
blog site map class
"""
class BlogSitemap( Sitemap ) :
    
    changefreq = "daily"
    priority = 1.0
    lastmod = datetime.datetime.now()
    
    def items( self ) :
        return Post.objects.all()
    #End of items function
    
#End of blog_sitemap class