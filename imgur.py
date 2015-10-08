#Libraries
from imgurpython import ImgurClient
from .models import Media, Post
from django.conf import settings
import os, json

#this variables are the ones that the imgur api give us after registering the aplication
client_id = 'a9e5cbb0585d300'
client_secret = '534f7fa674d788358fdced77e7e30e90336fa766'
# Set te client_id on the imgurClient method and the client_secret variables
client = ImgurClient(client_id, client_secret)

"""
Process file
this method process the file as we wish
Gets a file and returns nothing jet
"""
def save_image( file, post_id ) :
    # define the destination path and name to write, wb is for the writing in bites
    with open(  os.path.join( settings.BASE_DIR, 'static_pro', str( file ) ), 'wb+') as destination:
        # a iteration with the file bites
        for chunk in file.chunks() :
            # writing each bite on the destination path 
            destination.write( chunk )
        # post on imgur and give the imgur response     
        json_shit = client.upload_from_path( os.path.join( settings.BASE_DIR, 'static_pro', str( file ) ), config=None, anon=True)
        # save the media row and give the file
        media = Media()
        media.url = json_shit['link']
        media.post = Post.objects.get( id = post_id )
        media.save()
        # remove the temporal file on the server to make space
        os.remove( os.path.join( settings.BASE_DIR, 'static_pro', str( file ) ) )
#End of the save_image function