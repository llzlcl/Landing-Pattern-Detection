import cv2
import numpy as np

frame = cv2.imread('C:\\Users\\lenovo\\a.png',cv2.IMREAD_COLOR)
img_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
cv2.imwrite("C:\\Users\\lenovo\\1.png", img_gray, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
img_gb = cv2.GaussianBlur(img_gray, (5, 5), 0)
cv2.imwrite("C:\\Users\\lenovo\\2.png", img_gb, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
edges = cv2.Canny(img_gb, 100, 200)
cv2.imwrite("C:\\Users\\lenovo\\3.png", edges, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])
mg_fc, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
sp = frame.shape
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

img_dc = frame.copy()
for i in found:
    cv2.drawContours(img_dc, contours, i, (0, 255, 0), 15)
cv2.imwrite("C:\\Users\\lenovo\\4.png", img_dc, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])

draw_img = img_dc.copy()
img_dc = frame.copy()
if len(found)>=3:
    boxes = contours[found[0]]
    j=0
    for i in found:
        j += 1
        if j != 0:
            boxes = np.append(boxes, contours[i], axis=0)
    rect = cv2.minAreaRect(boxes)
    x=int(rect[0][0])
    y=int(rect[0][1])
    w=int(rect[1][0])
    h=int(rect[1][1])
    a=int(rect[2])
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    s1="x="+str(x)+"/"+str(sp[0])
    s4="y="+str(y)+"/"+str(sp[1])
    s2="width="+str(w)+"/"+str(sp[0])
    s5="height="+str(h)+"/"+str(sp[1])
    s3="theta="+str(a)
    cv2.drawContours(draw_img, [box], 0, (0, 0, 255), 15)
cv2.putText(draw_img, s1, (100, 400), cv2.FONT_HERSHEY_PLAIN , 10, (0, 0, 255), 20, False)
cv2.putText(draw_img, s2, (100, 800), cv2.FONT_HERSHEY_PLAIN , 10, (0, 0, 255), 20, False)
cv2.putText(draw_img, s3, (100, 1200), cv2.FONT_HERSHEY_PLAIN , 10, (0, 0, 255), 20, False)
cv2.putText(draw_img, s4, (100, 600), cv2.FONT_HERSHEY_PLAIN , 10, (0, 0, 255), 20, False)
cv2.putText(draw_img, s5, (100, 1000), cv2.FONT_HERSHEY_PLAIN , 10, (0, 0, 255), 20, False)
cv2.imwrite("C:\\Users\\lenovo\\5.png", draw_img, [int(cv2.IMWRITE_PNG_COMPRESSION), 0])


cv2.imshow("capture",draw_img)
cv2.waitKey(0)
cv2.destroyAllWindows()