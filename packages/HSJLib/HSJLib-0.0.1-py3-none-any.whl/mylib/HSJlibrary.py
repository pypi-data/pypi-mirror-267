
import os
import cv2
from PIL import Image
import numpy as np

def mask_view(input, output):
    # input 폴더에 있는 모든 파일들에 대해 작업을 수행합니다.
    input_folder = input
    output_folder = output

    # 출력 폴더가 없다면 생성합니다.
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # input_folder 폴더에 있는 모든 파일에 대해 반복합니다.
    for filename in os.listdir(input_folder):
        # 파일 경로
        file_path = os.path.join(input_folder, filename)
    
        # 파일이 PNG 형식인지 확인
        if filename.endswith(".png"):
            # PNG 파일을 열어서 이미지로 불러오기
            image = Image.open(file_path)
        
            # 이미지를 넘파이 배열로 변환 (RGB 형식으로 변환)
            image_array = np.array(image.convert("RGB"))

            for i in range(12):
                # 이미지에서 픽셀 값이 i인 부분의 인덱스 찾기
                indices = np.where(np.all(image_array == [i, i, i], axis=-1))

                # 추출된 픽셀을 모두 i*19로 바꿔줍니다.
                image_array[indices] = [i*19, i*19, i*19]

            # 변경된 넘파이 배열을 이미지로 변환
            modified_image = Image.fromarray(image_array)

            # 이미지를 파일로 저장합니다. 새로운 폴더에 저장합니다.
            output_path = os.path.join(output_folder, filename)
            modified_image.save(output_path)

    print("Conversion complete.")

def re_mask(input, output):
    # input 폴더에 있는 모든 파일들에 대해 작업을 수행합니다.
    input_folder = input
    output_folder = output

    # 출력 폴더가 없다면 생성합니다.
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # input_folder 폴더에 있는 모든 파일에 대해 반복합니다.
    for filename in os.listdir(input_folder):
        # 파일 경로
        file_path = os.path.join(input_folder, filename)
    
        # 파일이 PNG 형식인지 확인
        if filename.endswith(".png"):
            # PNG 파일을 열어서 이미지로 불러오기
            image = Image.open(file_path)
        
            # 이미지를 넘파이 배열로 변환 (RGB 형식으로 변환)
            image_array = np.array(image.convert("RGB"))

            for i in range(13):
                # 이미지에서 픽셀 값이 i*19-9이상인 부분의 인덱스 찾기
                """
                0 : < 9
                19 : 10 < 19 < 28
                38 : 29 < 38 < 47
                57 : 48 < 57 < 66
                76 : 67 < 76 < 85
                95 : 86 < 95 < 104
                114 : 105 < 114 < 123
                133 : 124 < 133 < 142
                152 : 143 < 152 < 161
                171 : 162 < 171 < 180
                190 : 181 < 190 < 199
                209 : 200 < 209 < 247
                255 : 248 <
                """
                if i == 12:
                    indices = np.where(np.all(image_array >= [248, 248, 248], axis=-1))
                    # 추출된 픽셀을 모두 255로 바꿔줍니다.
                    image_array[indices] = [255, 255, 255]
                elif i == 11:
                    indices = np.where(np.all(np.logical_and([200, 200, 200] <= image_array, image_array <= [247, 247, 247]), axis=-1))
                    image_array[indices] = [11, 11, 11]
                else:
                    indices = np.where(np.all(np.logical_and([i*19-9, i*19-9, i*19-9] <= image_array, image_array <= [i*19+9, i*19+9, i*19+9]), axis=-1))
                    image_array[indices] = [i, i, i]

            # 변경된 넘파이 배열을 이미지로 변환
            modified_image = Image.fromarray(image_array)

            # 이미지를 파일로 저장합니다. 새로운 폴더에 저장합니다.
            output_path = os.path.join(output_folder, filename)
            modified_image.save(output_path)

    print("Conversion complete.")
