import cv2
import numpy as np
from . import util
from scipy.fftpack import dct
import math

IMG1 = "Compare/static/original_img_1.png"
IMG2 = "Compare/static/original_img_2.png"
HASH1 = "Compare/static/hash_1.png"
HASH2 = "Compare/static/hash_2.png"


class Algo:
    
    # constructor
    def __init__(self, url1, url2):
        self.im1 = util.get_img(url1, IMG1)
        self.im2 = util.get_img(url2, IMG2)

    # destructor
    def __del__(self):
        pass

    @staticmethod
    def compressing(N, name):
        # discoloration and compressing
        image = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(image, (N, N), interpolation=cv2.INTER_AREA)

        return image

    def get_ans(self, im1, im2):
        # counting of answer and hashes
        self.ans = util.ans(im1, im2)
        self.hash1 = util.hash(im1)
        self.hash2 = util.hash(im2)

        # make quality better
        im1 = util.increase(im1, 480)
        im2 = util.increase(im2, 480)

        # save image hashes
        cv2.imwrite(HASH1, im1)
        cv2.imwrite(HASH2, im2)

    @staticmethod
    def my_dct(x):
        n = len(x)

        DCT = np.empty((n, n))

        for i in range(0, n):
            for j in range(0, n):
                tmp = 0
                for k in range(0, n):
                    tmp += x[i, k] * math.cos((math.pi*j*(2*k + 1))/(2*n))
                DCT[i, j] = 2 * tmp

        return DCT

    def aHash(self):
        # dimension
        N = 8

        # take images
        image1 = self.compressing(N, IMG1)
        image2 = self.compressing(N, IMG2)

        # counting of averages
        avr1 = np.mean(image1)
        avr2 = np.mean(image2)

        # thresholding
        ret, image1 = cv2.threshold(image1, avr1, 255, cv2.THRESH_BINARY)
        ret, image2 = cv2.threshold(image2, avr2, 255, cv2.THRESH_BINARY)

        # computing of answer
        self.get_ans(image1, image2)

    def dHash_row(self):
        # dimension
        N = 8

        # take images
        image1 = self.compressing(N + 1, IMG1)
        image2 = self.compressing(N + 1, IMG2)

        # thresholding
        row1 = np.empty([N, N])
        row2 = np.empty([N, N])

        for x in range(0, N):
            for y in range(0, N):

                if image1[x, y] < image1[x + 1, y]:
                    row1[x, y] = 0
                else:
                    row1[x, y] = 255

                if image2[x, y] < image2[x + 1, y]:
                    row2[x, y] = 0
                else:
                    row2[x, y] = 255

        # computing of answer
        self.get_ans(row1, row2)

    def dHash_col(self):
        # dimension
        N = 8

        # take images
        image1 = self.compressing(N + 1, IMG1)
        image2 = self.compressing(N + 1, IMG2)

        # thresholding
        col1 = np.empty([N, N])
        col2 = np.empty([N, N])

        for x in range(0, N):
            for y in range(0, N):

                if image1[x, y] < image1[x, y + 1]:
                    col1[x, y] = 0
                else:
                    col1[x, y] = 255

                if image2[x, y] < image2[x, y + 1]:
                    col2[x, y] = 0
                else:
                    col2[x, y] = 255

        # computing of answer
        self.get_ans(col1, col2)

    def pHash_simple(self):
        # dimension
        N = 32

        # take images
        image1 = self.compressing(N, IMG1)
        image2 = self.compressing(N, IMG2)

        # Compute the DCT
        DCT1 = dct(image1)
        DCT2 = dct(image2)

        # Reduce the DCT
        dctlowfreq1 = DCT1[0:N // 4, 1:N // 4 + 1]
        dctlowfreq2 = DCT2[0:N // 4, 1:N // 4 + 1]

        # averages
        avr1 = np.mean(dctlowfreq1)
        avr2 = np.mean(dctlowfreq2)

        # thresholding
        ret, image1 = cv2.threshold(DCT1, avr1, 255, cv2.THRESH_BINARY)
        ret, image2 = cv2.threshold(DCT2, avr2, 255, cv2.THRESH_BINARY)

        # computing of answer
        self.get_ans(image1, image2)

    def pHash(self):
        # dimension
        N = 32

        # take images
        image1 = self.compressing(N, IMG1)
        image2 = self.compressing(N, IMG2)

        # Compute the DCT
        DCT1 = dct(image1)
        DCT2 = dct(image2)

        # Reduce the DCT
        dctlowfreq1 = DCT1[0:N // 4, 1:N // 4 + 1]
        dctlowfreq2 = DCT2[0:N // 4, 1:N // 4 + 1]

        # medians
        median1 = np.median(dctlowfreq1)
        median2 = np.median(dctlowfreq2)

        # thresholding
        ret, image1 = cv2.threshold(DCT1, median1, 255, cv2.THRESH_BINARY)
        ret, image2 = cv2.threshold(DCT2, median2, 255, cv2.THRESH_BINARY)

        # computing of answer
        self.get_ans(image1, image2)
