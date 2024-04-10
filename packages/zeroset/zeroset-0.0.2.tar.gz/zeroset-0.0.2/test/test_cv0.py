from zeroset import cv0

files = cv0.glob("images/*.*")[:3]

imgs = cv0.imreads(files)

img = cv0.hconcat(imgs)

cv0.imshow(img, mode=cv0.IMSHOW_BEST).waitKey()
