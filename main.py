
import os
import cv2
import argparse

import os
from concurrent.futures import ThreadPoolExecutor

parser = argparse.ArgumentParser()

parser.add_argument('--data_path', type=str,
                    default='./')
parser.add_argument('--dest_path', type=str,
                    default ='./processed_videos')


opt = parser.parse_args()


data_path = opt.data_path #
dest_path = opt.dest_path #

# Define your video processing function

def resize_video(video_path,dest_path):
    cap = cv2.VideoCapture(data_path)

    frame_width, frame_height = int(cap.get(3)), int(cap.get(4))
    fps = cap.get(cv2.CAP_PROP_FPS)
    
    out = cv2.VideoWriter(dest_path, cv2.VideoWriter_fourcc(
        *'mp4v'), fps, (frame_width, frame_height))
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            break


        img_resized = cv2.resize(image, (int(frame_height/2),int(frame_width/2)))

        out.write(img_resized)
    cap.release()
    out.release()


# Video processing on all the videos
def process_video(file_path):
    root =file_path[0]
    file= file_path[1]
    dest_path_new = file_path[2] 
    if not os.path.exists(dest_path_new):      
        os.makedirs(dest_path_new,exist_ok=True)

    video_path = os.path.join(root,file)

    resize_video(video_path,os.path.join(dest_path_new, file) )

                
    # You can return some result if needed
    return f"Processed {video_path}"


def main():
    file_list = []
    for (root,dirs,files) in os.walk(data_path, topdown=True):
        for file in files:
            if file.endswith('.mp4'):
                dest_path_new = root.replace(data_path,dest_path)
                file_list.append([root,file,dest_path_new])

    num_cpus = os.cpu_count()  # This gets the number of available CPU cores
    with ThreadPoolExecutor(max_workers=num_cpus) as executor:
        # Process videos in parallel
        results = list(executor.map(process_video, files))

    # Print the results
    for result in results:
        print(result)

        print ('--------------------------------')


if __name__ == "__main__":
    main()
