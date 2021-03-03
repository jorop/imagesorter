import exifread
import shutil
import os
import sys
import datetime

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if len(sys.argv) < 1:
    print('Please provide directory as argument!')
directory = sys.argv[1] # get the directory we are looking for images
img_files = os.listdir(directory)  # get the files of the directory

for img in img_files:
    date = None
    if allowed_file(img): # check if the file is an image file
        full_path = os.path.join(directory, img)
        with open(full_path, 'rb') as image_file:
            tags = exifread.process_file(image_file, stop_tag='EXIF DateTimeOriginal')
            date_taken = str(tags.get('EXIF DateTimeOriginal'))
            try:
                date_time_obj = datetime.datetime.strptime(date_taken, '%Y:%m:%d %H:%M:%S')
                date = date_time_obj.date() # getting the date in YYYY-MM-DD format
            except ValueError:
                print('Cannot find EXIF')
        if not date:
            print('Using mtime')
            mtime = os.path.getmtime(full_path)
            date_time_obj = datetime.datetime.fromtimestamp(mtime)
            date = date_time_obj.date()
        print('Image: {} - Date: {}'.format(img, date))
        new_directory = 'Sorted/{}'.format(date)
        os.makedirs(new_directory, exist_ok=True)  # make the new directory
        shutil.copyfile(full_path, os.path.join(new_directory, img))  # copy file into the new directory - it will have the format YYYY-MM-DD