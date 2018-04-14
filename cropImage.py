from PIL import Image;
import os;

def cropImage(Image_name): #파일이름(확장자포함) 입력
    dirname='Dataset/'+Image_name #폴더경로 + 파일이름
    im = Image.open(dirname)
    dirname='Dataset/'+os.path.splitext(Image_name)[0] #확장자제거해서 저장
    # ex) Dataset/image.jpg -> Dataset/image

    cropImage = im.crop((0,0,256,256)) #256x256으로 이미지 자르기

    count=0
    while True:
        if not os.path.isdir(dirname+'_'+str(count)): #Dataset/image_0(count) 폴더가 있나?
            os.mkdir(dirname+'_'+str(count)) #폴더를 만든다
            dirname=dirname+'_'+str(count) #만든 폴더 경로로 저장
            break;
        else:
            count=count+1 #폴더가 있을때 카운트 1증가
            
    cropImage.save(dirname+'/'+Image_name) #생성한 폴더로 자른 이미지 저장
    return dirname+'/'+Image_name #저장된 경로 리턴
