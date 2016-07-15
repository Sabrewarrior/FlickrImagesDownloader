import time
#originally written by Tamara Berg, extended by James Hays

#download images listed in every text file in this directory
# search_result_dir = '/home/ujash/flickr_scripts/search_results/'
search_result_dir = '/home/ujash/images_flickr/3/'
#directory where you want to download the images
output_dir = ['/home/ujash/images_filckr/3/downloads']
#the algorithm will create subdirs and subsubdirs in the above dir.

#with the number of images we're expecting we will need two levels of
#subdirectories.  The first level will be the tag, of which there will be
#roughly 100, then the second level will be subdirs of 1000 images.  The
#images will be named such that they can be traced back to their flickr
#source.

##############################################################################

###########################################################
import fnmatch
import requests
import os
import urllib2
import cStringIO
from scipy.misc import imread
from scipy.misc import imresize
from scipy.misc import imrotate

def url2imageArray(urlReq, timeout = 10, timeoutDelta = 5, maxtries = 3):
    imageArray = None
    while maxtries > 0:
        try:
            stream = urllib2.urlopen(urlReq,timeout=10)
            imageArray = imread(cStringIO.StringIO(stream.read()))
            break
        except:
            timeout += timeoutDelta
            maxtries -= 1
    return imageArray

###
### resizeDims = (width, height)
###
def normalizeArray(imageArray, resizeDims = (1024,768), keepBW = False):
    dims = imageArray.shape
    normArray = None
    rotated = False
    truncated = False
    if not keepBW:
        if len(dims) < 3 or dims[2] < 3:
            return normArray, rotated, truncated
    normalizedArray = None
    landscape = True
    if dims[0] > dims[1]:
        if resizeDims[0] < resizeDims[1]:
            resizeDims[0], resizeDims[1] = resizeDims[1], resizeDims[0]
            rotated = True
    # 16/20x20/16 16x20
    if (float(dims[0])/float(resizeDims[0])) < (float(dims[1])/float(resizeDims[1])):
        #USE float(dims[0])/float(resizeDims[0])
        pass
        #Need to rotate
    else:
        pass
        # USE (float(dims[1])/float(resizeDims[1]) to rotate
    return normArray, rotated, truncated

def downloadphotos(search_result_dir, output_dir, numComments = 13):
    print('Reading image metadata from', search_result_dir)

    search_results = []
    for root, dirnames, filenames in os.walk(search_result_dir):
        for filename in fnmatch.filter(filenames, '*.txt'):
            search_results.append([root, filename])

    num_results = len(search_results)
    print('Downloading the images from', num_results, 'search results')

    for i in range (0, len(search_results)):
        current_file = search_results[i]
        current_filename_fh = current_file[1][:-4] #cutting off .txt extension

        print('\n !!! Checking for lock on #s\n', current_file[1])

        #The presence of an output directory is a lock
        if not os.path.exists(os.path.join(output_dir,current_file[0], current_filename_fh, 'file')):
            print(' locking', current_file[1])
            #lock the file by creating the output directory
            os.mkdir(os.path.join(output_dir, current_filename_fh))

            # file where the metadata is located
            fid = open(os.path.join(search_result_dir, current_file[0], current_file[1]),'r')
            print(' Reading search results in file #s\n', current_file[1])

            count=0
            dircount=0

            # downloads images, 1000 images per directory
            while True:
                line = fid.readline()
                if not line:
                    break

                #example entry
                # photo: 27642011 8fa8ae33cd 23
                # owner: 72399739@N00
                # title: Mexico City - Chapultepec 03
                # originalsecret: null
                # originalformat: null
                # datetaken: 2005-07-21 14:41:58
                # tags: architecture digital landscape mexico mexicocity infrared trips skyview chapultepec
                # license: 0
                # latitude: 19.420934
                # longitude: -99.181416
                # accuracy: 16
                # interestingness: 2 out of 14

                #odd, it seems like original secret is always the same as the
                #standard secret.  And sometimes, if flickr won't give you the
                #original secret, you can still access the original.  So really
                #no point even looking for that.
                if line.startswith('photo:'):

                    if count%1000==0:
                        dircount = dircount + 1
                        os.mkdir(os.path.join(output_dir, current_filename_fh, str(dircount)))

                    count=count+1

                    line = line.rstrip().split()
                    id = line[1]
                    secret = line[2]
                    server = line[3]
                    farm = line[4]

                    line = fid.readline().rstrip() #original_secret
                    origSecret = line.split()[-1]

                    line = fid.readline().rstrip() #original_format
                    origFormat = line.split()[-1]


                    #save all the metadata in the comment field of the file
                    comment_field = ('id: ' + id + ' '                      #photo_id
                                     + 'secret: ' + secret + ' '            #secret
                                     + 'server: ' + server + ' '            #server
                                     + 'farm: ' + farm + ' '                #farm
                                     + 'origSecret: ' + origSecret + ' '    #original_secret
                                     + 'origFormat: ' + origFormat)         #original_format

                    # Add the rest of the attributes
                    while True:
                        line = fid.readline().rstrip()
                        if not line:
                            break
                        else:
                            comment_field += ' ' + line

                    #dimension = 1024 pixels (but there are bugs).
                    urlReq = 'https://farm' + farm + '.staticflickr.com/' + server +'/' + id +'_'+ secret +'_b.jpg'

                    print('current_image : ' + id + '_' + secret + '_' + server + '_' + farm + '.jpg')

                    #download the file to a temporary, local location
                    #before saving it in the full path in order to minimize network
                    #traffic using the /tmp/ space on any machine.

                    #we want the file name to identify the image still.  not just be numbered.
                    #use the -O [output file name] option
                    #-t specifies number of retries
                    #-T specifies all timeouts, in seconds.  if it times out does it retry?
                    imgArr = url2imageArray(urlReq,timeout=10,timeoutDelta=5, maxtries=2)

                    #cmd = ['wget -t 3 -T 5 --quiet ' url ...
                    #       ' -O ' '/tmp/' + id + '_' + secret + '_' + server + '.jpg' ]
                    dims = imgArr.shape

                    #Normalize the size
                    imresize(imgArr, )
                    try
                        unix(cmd)
                    catch
                        lasterr
                        print('XX!! Error with wget.\n')
                    

                    #we need to check if we got a small error .gif back, in which case
                    #we'll want to try for the original image.
                    current_file_info = dir(['/tmp/' id '_' secret '_' server '_' owner '.jpg'])

                    if(isempty(current_file_info))
                        print('XX!! could not find the temporary file from this iteration \n')
                    else
                        current_file_size = current_file_info.bytes

                        if(current_file_size < 5000) #if the file is less than 20k, or we got an error .gif instead
                            #TODO WEBSAVE
                            print('X  Large version did not exist, trying original\n')
                               #try for the original
                            url = ['https://farm' farm '.staticflickr.com/' server '/' id '_' origSecret '_o.' origFormat]
                            cmd = ['wget -t 3 -T 5 --quiet ' url ...
                                     ' -O ' '/tmp/' id '_' secret '_' server '_' owner '.jpg' ]

                            try
                                unix(cmd)
                            catch
                                lasterr
                                print('XX!! Error with wget.\n')
                            

                            current_file_info = dir(['/tmp/' id '_' secret '_' server '_' owner '.jpg'])
                            if(isempty(current_file_info))

                                print('XX!! could not find the second temporary file from this iteration \n')
                            else
                                current_file_size = current_file_info.bytes

                                if(current_file_size < 5000) #if the file is less than 5k, or we got an error .gif instead
                                    #neither the large nor the original existed
                                    current_file_valid = 0
                                    try
                                        #websave(current_file_info)
                                    catch
                                        pass
                                    
                                    print('X  Original version does not exist\n')
                                else
                                    #the large size did not exist, the original
                                    #size did.  but it could be too small resolution.
                                    #or too large, actually.

                                    current_file_valid = 1
                                    print('!  Original version exists\n')
                                
                            
                        else
                            #the large size file existed and has enough bytes
                            #since it is large size, it's definitely high res
                            print('!  Large version exists\n')
                            current_file_valid = 1
                        


                        if(current_file_valid == 1)
                            # load the image, resize it, remove border, save it.
                            try
                                current_image = imread( ['/tmp/' id '_' secret '_' server '_' owner '.jpg' ] )
                            catch
                                lasterr
                                print('XX!! error loading temporary file, which should have been valid\n')
                            

                            aspect_ratio = size(current_image,2) / size(current_image,1) #width by height
                            min_dim_pixels = min( size(current_image,1) , size(current_image,2) )

                            if(size(current_image,3) == 3 && ... #make sure it's color
                                aspect_ratio <= 1.6 && ...  #we want to allow 800x533 images, barely
                                aspect_ratio >= .625 && ... #we don't want massive images, they'll run matlab out of memory
                                min_dim_pixels >= 400 && ...
                                min_dim_pixels <= 1700)  #1700 min dimension largest allowable size.  This should almost NEVER happen, because if
                                                         #the image had been this big then a 'large' size should have existed

                                current_image = double(current_image) /255
                                current_image = remove_frame(current_image) #delete border

                                min_dim_pixels = min( size(current_image,1) , size(current_image,2) )

                                if(min_dim_pixels >= 400)
                                    #we finally have a completely valid image to save

                                    #resize the max dimension down to 1024
                                    current_image = rescale_max_size(current_image, 1024, 1)

                                    output_filename = [output_dir current_filename_fh '/' sprintf('#.5d', dircount) '/' id '_' secret '_' server '_' owner '.jpg' ]

                                    #lets save all the info we'll need in the comment
                                    #section of the file.  We can retrieve this later
                                    #with imfinfo()
                                    try
                                        imwrite(current_image, output_filename, 'jpg', 'quality', 85, 'comment', comment_field)
                                        print('!! Successfully wrote #s\n', output_filename)
                                    catch
                                        lasterr
                                        print('XX!! error writing final image\n')
                                    
                                else
                                    #we deleted too many pixels from the border
                                    print('XX After border removal, the image is too small (#d pixels).\n', min_dim_pixels)
                                
                            else
                                #print out the correct failure cases
                                if(min_dim_pixels < 400)
                                    print('XX Image is too small (#d pixels).  \n', min_dim_pixels)
                                

                                if(aspect_ratio < .625 || aspect_ratio > 1.6)
                                    print('XX Aspect ratio is bad (#f).\n', aspect_ratio)
                                

                                if(size(current_image,3) ~= 3)
                                    print('XX Image is not a 3 channel image (#d channels)\n', size(current_image,3))
                                

                                if(min_dim_pixels > 1700)
                                    print('XX The original image was huge, and flickr failed to make a large size\n')
                                
                            
                        else
                            #this triggers less often than I would have thought.
                            print('XX Could not find large or original size of this file. Skipping.\n')
                        
                    

                    # delete the temporary file
                    try
                        delete(['/tmp/' id '_' secret '_' server '_' owner '.jpg' ])
                    catch
                        lasterr
                        print('XX!! failed deleting the temporary file\n')
                    

                    # pause inserted here so as not to piss flickr off...
                    # maybe you can take it out?  probably, because the image
                    # processing was slow enough.
                    pause(1)

                
            

            fclose(fid)

        else
            print(' file is locked / already downloaded, skipping\n')
        
     # of all files
