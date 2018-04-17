from PIL import Image, ImageFilter;
import os;

def blurImage(Image_address): #파일경로 입력
    
    im=Image.open(Image_address)

    dir_name=os.path.split(Image_address) #폴더 경로 추출

    blur=im.filter(ImageFilter.GaussianBlur) #블러처리
    blur.save(dir_name[0]+'/real.jpg',dpi=(100,100)) #같은 폴더 real.jpg로 저장
    #print('blurImage return address : '+dir_name[0]+'/real.jpg')

    return dir_name[0]+'/real.jpg' #저장된 경로 리턴
