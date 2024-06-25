import numpy as np
import argparse
import cv2

# region 
#image = cv2.imread(r"C:\Users\ZowieQuickert\Documents\Hm\TP6503-RED-03.jpg")#rotes T-Shirt
image = cv2.imread(r"C:\Users\ZowieQuickert\Documents\Hm\blue_tshirt.jpg")#blaues T-Shirt
#image = cv2.imread(r"C:\Users\ZowieQuickert\Documents\Hm\white-wall.jpg")# White Wall

#build img size
cv2.imshow("test" ,image)
down_width = 500
down_height = 600
down_points = (down_width, down_height)
#crop vectors
x1 = 450#350
y1 = 600#1000
x2 = 700#800
y2 = 800#500

#put a square on the picture were the "hit range should be"
crop_img = image[y1:y2, x1:x2].copy()
cv2.rectangle(image,(x1,y1),(x2,y2),(0,255,0),3)

#resize img so it doesnt fill up the screen :>
resized_down = cv2.resize(crop_img, down_points, interpolation= cv2.INTER_LINEAR)
resized_down2 = cv2.resize(image, down_points, interpolation= cv2.INTER_LINEAR)

#save cropped image for later use
cv2.imwrite(r'C:\Users\ZowieQuickert\Documents\Hm\boop\test.jpg',crop_img)

#Show Pictures for test purpose
cv2.imshow("test" ,resized_down)
cv2.imshow("test2" ,resized_down2)

cv2.waitKey(0)  

# Destroys all the windows created
cv2.destroyAllwindows() 

# endregion


def is_image_mostly_red(image, threshold=95):

    # Konvertiere das Bild von BGR nach HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Definiere die HSV-Grenzwerte für die Farbe Rot
    lower_red1 = np.array([0, 70, 50])
    upper_red1 = np.array([10, 255, 255])
    lower_red2 = np.array([170, 70, 50])
    upper_red2 = np.array([180, 255, 255])
    
    # Erstelle Masken für die beiden Rotbereiche im HSV-Farbraum
    mask1 = cv2.inRange(hsv_image, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv_image, lower_red2, upper_red2)
    
    # Kombiniere die Masken
    red_mask = cv2.bitwise_or(mask1, mask2)
    
    # Berechne den Prozentsatz der roten Pixel
    red_pixel_count = np.count_nonzero(red_mask)
    total_pixel_count = image.shape[0] * image.shape[1]
    red_percentage = (red_pixel_count / total_pixel_count) * 100
    
    # Überprüfe, ob der Prozentsatz der roten Pixel mindestens dem Schwellenwert entspricht
    print(red_percentage >= threshold)
    return red_percentage >= threshold

def is_image_mostly_blue(image, threshold=95):

    # Konvertiere das Bild von BGR nach HSV
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Definiere die HSV-Grenzwerte für die Farbe blau
    lower_blue = np.array([100, 70, 50])
    upper_blue = np.array([130, 255, 255])
    
    # Erstelle Maske für den HSV Frabraum blau
    blue_mask = cv2.inRange(hsv_image, lower_blue, upper_blue)

    # Berechne den Prozentsatz der blauen Pixel
    blue_pixel_count = np.count_nonzero(blue_mask)
    total_pixel_count = image.shape[0] * image.shape[1]
    blue_percentage = (blue_pixel_count / total_pixel_count) * 100
    
    # Überprüfe, ob der Prozentsatz der blauen Pixel mindestens dem Schwellenwert entspricht
    print(blue_percentage >= threshold)
    return blue_percentage >= threshold




def mainfuntion():
    #variables
    blue_score = 0
    red_score = 0
    Team = "red"

    #check for team blue
    if (Team == "blue"):
        if(is_image_mostly_red(crop_img, 95)):
            print("Team blue hit!")
            blue_score += 1
        else:
            print("Team blue miss")

    #check for team red
    elif(Team=="red"):
        if(is_image_mostly_blue(crop_img, 95)):
            print("Team red hit!")
            red_score +=1
        else:
            print("Team red miss")
        
mainfuntion()
