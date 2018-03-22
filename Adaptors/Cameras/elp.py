import cv2
import sys
import time

class ELP():
    def __init__(self, images_folder):
            self.images_folder = images_folder
            if not self.images_folder.endswith("/"):
                self.images_folder = "%s/" % (self.images_folder)

    def take_capture(self, filename):
            if not filename.endswith(".png"):
                filename = "%s.png" % (filename)
            image_path = "%s%s" % (self.images_folder,filename)
            print "elp - 1 - ", image_path
            try: 
                print "elp - 2 - "
                cap = cv2.VideoCapture(0)
                cap.set(3,1280)
                cap.set(4,720)
                if not cap.isOpened():
                    while not cap.isOpened():
                        print "Camera capture not open ... trying to fix it..."
                        cap.open()
                        time.sleep(1)
                else:
                    print "elp - 2 - "
                    ret, frame = cap.read()
                    cv2.imwrite(image_path,frame)
                    #cap.release()
                    print "Picture taken", image_path
            except Exception as e:
                  print "Oops! something went wrong %s" % (e)
            finally:
                cap.release()
            time.sleep(1)
            #return image_path

def init(images_folder):
    return ELP(images_folder)

