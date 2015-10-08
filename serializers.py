#Libraries
from rest_framework import serializers
from .models import Post, Category

"""
Category serializer
"""
class CategorySerializer( serializers.ModelSerializer ) :
    
    """
    Meta class
    """
    class Meta :
        
        model = Category
        fields = ( 'id', 'name', 'description' )

    #End of meta class
    
#End of category serialiser class

"""
Post serialiser
"""
class PostSerializer( serializers.ModelSerializer ) :
    
    category = CategorySerializer
    
    """
    Meta class
    """
    class Meta :
        
        model = Post
        fields = ( 'id', 'title', 'content','category' )

    #End of meta class
    
#End of PostSerialiser class