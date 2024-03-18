import BaseConfig
import os

reso=[
    128,160,320,480,640,1280
]

image_root_path = BaseConfig.INPUT_PATH + "/handshaking"

for res in reso:
    cnt=0
    result=0.0
    for root, dirs, files in os.walk(image_root_path):
        for file in files:
            file_name = file.split('.')[0]
            print(f"file name:{file_name}")
            file_path = BaseConfig.INPUT_PATH + '/handshaking' + '/' + file
            with open(BaseConfig.DETECTION_RESULT + f"/{res}" + '/' + file_name + ".txt", 'r', ) as f:
                temp=f.read()
                if temp==None:
                    continue
                else:
                    li = temp.split('\n')
                    if li !=None:
                        for line in li:
                            word=line.split(' ')
                            if len(word)>1:
                                cnt+=1
                                precision=float(word[1])
                                result+=precision
    with open(BaseConfig.INPUT_PATH + f"/precision.txt","a") as f:
        f.write(str(result/cnt)+'\n')