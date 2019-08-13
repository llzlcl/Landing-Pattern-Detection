import cv2
import numpy as np
help(cv2)
cap = cv2.VideoCapture(0)
succ=all=0.0
x=y=w=h=a=0
s1=s2=s3=s4=s5=""

out = cv2.VideoWriter('output.avi',-1, 10, (640,480))

def getpos(rect):
    x = int(rect[0][0])
    y = int(rect[0][1])
    w = int(rect[1][0])
    h = int(rect[1][1])
    a = int(rect[2])
    s1 = "x=" + str(x) + "/" + str(sp[0])
    s4 = "y=" + str(y) + "/" + str(sp[1])
    s2 = "width=" + str(w) + "/" + str(sp[0])
    s5 = "height=" + str(h) + "/" + str(sp[1])
    s3 = "theta=" + str(a)

def drawpos(img):
    cv2.putText(img, s1, (10, 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3, False)
    cv2.putText(img, s2, (10, 100), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3, False)
    cv2.putText(img, s3, (10, 140), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3, False)
    cv2.putText(img, s4, (10, 80), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3, False)
    cv2.putText(img, s5, (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3, False)
    return img

while(1):
    all+=1.0
    ret, frame = cap.read()
    sp = frame.shape
    img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_gb = cv2.GaussianBlur(img_gray, (5,5),0)
    edges = cv2.Canny(img_gb, 100, 200)
    mg_fc, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if hierarchy is not None :
        hierarchy = hierarchy[0]
    found = []
    for i in range(len(contours)):
        k = i
        c = 0
        while hierarchy[k][2] != -1 :
            k = hierarchy[k][2]
            c = c + 1
        if c >= 5:
            found.append(i)

    draw_img = frame.copy()
    if len(found)>=3:
        succ+=1.0
        boxes = contours[found[0]]
        j=0
        for i in found:
            j += 1
            if j != 0:
                boxes = np.append(boxes, contours[i], axis=0)
        rect = cv2.minAreaRect(boxes)
        x = int(rect[0][0])
        y = int(rect[0][1])
        w = int(rect[1][0])
        h = int(rect[1][1])
        a = int(rect[2])
        s1 = "x=" + str(x) + "/" + str(sp[0])
        s4 = "y=" + str(y) + "/" + str(sp[1])
        s2 = "width=" + str(w) + "/" + str(sp[0])
        s5 = "height=" + str(h) + "/" + str(sp[1])
        s3 = "theta=" + str(a)
        box = cv2.boxPoints(rect)
        box = np.int0(box)
        cv2.drawContours(draw_img, [box], 0, (0, 0, 255), 3)
    cv2.putText(draw_img, str(int(succ/all*100))+"%", (10, 30), cv2.FONT_HERSHEY_PLAIN , 2, (0, 0, 255), 3, False)
    cv2.putText(draw_img, s1, (10, 60), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3, False)
    cv2.putText(draw_img, s2, (10, 120), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3, False)
    cv2.putText(draw_img, s3, (10, 180), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3, False)
    cv2.putText(draw_img, s4, (10, 90), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3, False)
    cv2.putText(draw_img, s5, (10, 150), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 3, False)
    cv2.imshow("capture",draw_img)
    out.write(draw_img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()

