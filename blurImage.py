from PIL import Image, ImageFilter
import os
import random


# 난수를 통해 박스를 만들고 box_blur()를 호출하여 블러처리된 박스이미지와 박스범위를 리턴하는 함수
def box_make(original_image, random_count): # 원본 이미지, 난수(박스의 수)를 입력받는다
    width, height=original_image.size # 원본 이미지의 너비와 높이를 저장
    box_image=[0]*random_count # 박스의 수만큼 초기화
    box=[0]*random_count # 박스의 수만큼 초기화

    for i in range(0, random_count): # 박스의 수만큼 반복
        box_width_left = random.randrange(1,width-5) # 1 ~ (원본이미지의 너비-5)의 난수 생성, 가로 시작점에 해당
        box_height_top = random.randrange(1,height-5) # 1 ~ (원본이미지의 높이-5)의 난수 생성, 세로 시작점에 해당

        box_width_range = random.randrange(box_width_left+1, width) # (가로 시작점+1) ~ 원본이미지의 너비의 난수 생성, 가로 범위 해당
        box_height_range = random.randrange(box_height_top+1, height) # (세로 시작점+1) ~ 원본이미지의 높이의 난수 생성, 세로 범위에 해당
    
        box[i]=(box_width_left, box_height_top, box_width_range, box_height_range) # (가로 시작점, 세로 시작점, 가로 범위, 세로 범위), 박스의 범위를 저장
        print(i+1,' box blur radius :', end=" ")
        box_image[i] = box_blur(original_image, box[i]) # 원본이미지, 박스의 범위를 입력해주고 박스이미지를 리턴받음
        

    return box_image, box # 박스이미지, 박스범위를 리턴


# 입력받은 박스의 범위대로 이미지를 자르고 난수를 통해 블러의 강도를 조절하고 블러처리하여 이미지를 리턴하는 함수
def box_blur(original_image,box): # 원본 이미지, 박스의 범위를 입력받는다.

    box_image=original_image.crop(box) # 원본이미지에 박스의 범위대로 이미지를 자른다.

    #for i in range(0,10): # 박스 이미지를 따로 저장받아 보고싶을 때
    #    if not os.path.isfile('Dataset/before_blur_'+str(i)+'.jpg'):
    #        box_image.save('Dataset/before_blur_'+str(i)+'.jpg')
    #        break;

    blur_radius=random.randrange(1,5) # 1~5의 난수를 생성, 블러의 강도
    print(blur_radius)
    box_image=box_image.filter(ImageFilter.GaussianBlur(radius=blur_radius)) # 블러처리를 한다.

    #for i in range(0,10): # 블러처리 된 박스 이미지를 따로 저장받아 보고싶을 때
    #    if not os.path.isfile('Dataset/blur_box_'+str(i)+'.jpg'):
    #        box_image.save('Dataset/blur_box_'+str(i)+'.jpg')
    #        break;

    return box_image # 블러처리 된 박스이미지를 리턴한다.

# 박스의 이미지를 해당 범위에 붙여넣는 함수
def box_paste(original_image, box, box_image): # 원본이미지, 박스의 범위, 박스이미지를 입력받는다.
    original_image.paste(box_image, box) 
    # 원본이미지(original_image)에서 박스의 범위(box)에 블러처리 된 박스 이미지(box_image)를 덮어쓰기(붙여넣기)한다.


def blurImage(Image_address): # 파일경로 입력
    
    im=Image.open(Image_address) # 이미지 열기

    dir_name=os.path.split(Image_address) # 폴더 경로 추출(dir_name[0])

    random_count=random.randrange(1,4) # 1~4의 난수생성 -> 박스의 수
    print('number of box : ',random_count) # 박스의 개수 출력
    box_image, box = box_make(im, random_count) 
    # 박스를 만들고 블러처리된 박스이미지와 박스범위를 리턴받음 (리스트로 받는다)

    for i in range(0, random_count): # 박스의 수만큼 반복
        print('box range : ',box[i]) # 박스 범위 출력
        box_paste(im, box[i], box_image[i]) # 원본 이미지에 박스이미지를 붙여넣기

    im.save(dir_name[0]+'/real.jpg',dpi=(100,100)) #같은 폴더 real.jpg로 저장
    #print('blurImage return address : '+dir_name[0]+'/real.jpg')

    return dir_name[0]+'/real.jpg' #저장된 경로 리턴
