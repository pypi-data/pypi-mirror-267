from zeroset import cv0
import cv2

files = cv0.glob("images/*.*")[:3]

imgs = cv0.imreads(files)

edge = cv0.canny(imgs[0])

x = cv0.hconcat(imgs[0], edge)
cv0.imshow("img", x)
cv0.waitKey()
