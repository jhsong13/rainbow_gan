from PIL import Image, ImageFilter
import os
import random


def box_make(original_image, random_count):
    width, height=original_image.size
    box_image=[0]*random_count
    box=[0]*random_count

    for i in range(0, random_count):
        box_width_left = random.randrange(1,int(width/4))
        box_height_top = random.randrange(1,int(height/4))

        box_width_range = random.randrange(box_width_left+1, width-box_width_left)
        box_height_range = random.randrange(box_height_top+1, height-box_height_top)
    
        #(가로 시작점, 세로 시작점, 가로 범위, 세로 범위)
        box[i]=(box_width_left, box_height_top, box_width_range, box_height_range)
        print(i+1,' box blur radius :', end=" ")
        box_image[i] = box_blur(original_image, box[i])
        

    return box_image, box



def box_blur(original_image,box):

    box_image=original_image.crop(box)

    #for i in range(0,10):
    #    if not os.path.isfile('Dataset/before_blur_'+str(i)+'.jpg'):
    #        box_image.save('Dataset/before_blur_'+str(i)+'.jpg')
    #        break;

    blur_radius=random.randrange(1,5)
    print(blur_radius)
    box_image=box_image.filter(ImageFilter.GaussianBlur(radius=blur_radius)) #블러처리

    #for i in range(0,10):
    #    if not os.path.isfile('Dataset/blur_box_'+str(i)+'.jpg'):
    #        box_image.save('Dataset/blur_box_'+str(i)+'.jpg')
    #        break;

    return box_image

def box_paste(original_image, box, box_image):
    original_image.paste(box_image, box)


def blurImage(Image_address): #파일경로 입력
    
    im=Image.open(Image_address)

    dir_name=os.path.split(Image_address) #폴더 경로 추출

    random_count=random.randrange(1,4)
    print('number of box : ',random_count)
    box_image, box = box_make(im, random_count)

    for i in range(0, random_count):
        print('box range : ',box[i])
        box_paste(im, box[i], box_image[i])

    im.save(dir_name[0]+'/real.jpg',dpi=(100,100)) #같은 폴더 real.jpg로 저장
    #print('blurImage return address : '+dir_name[0]+'/real.jpg')

    return dir_name[0]+'/real.jpg' #저장된 경로 리턴
