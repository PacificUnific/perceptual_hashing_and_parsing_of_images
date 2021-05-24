# for save images in directory of project like buffer
import os
import requests

# regular expression
import re

# for parsing
from bs4 import BeautifulSoup
from fake_headers import Headers

# for work with images
import cv2
import numpy as np
from . import algo


# consts
GOOGLE_IMAGE = 'https://www.google.com/search?tbm=isch&q='


def get_img(url, name):
    try:
        # try to get image by URL
        p = requests.get(url)
        arr = np.asarray(bytearray(p.content))
        img = cv2.imdecode(arr, -1)
    except:
        # black "image" 32x32
        img = np.zeros((32, 32))

    cv2.imwrite(name, img)


# delete image by path
def delete_image(path):
    os.remove(path)


# "errors" of images
def compare(img1, img2):

    size = img1.size
    Oy = len(img1.T)
    Ox = len(img1)

    cnt = 0
    for x in range(0, Ox):
        for y in range(0, Oy):
            if img1[x, y] != img2[x, y]:
                cnt += 1

    return cnt/size


# get answer
def ans(img1, img2):
    # counting of errors
    errors = compare(img1, img2)
    ans = (1 - errors) * 100
    ans = round(ans)

    return ans


# computing hash
def hash(img):

    Oy = len(img.T)
    Ox = len(img)

    hash = ""
    cnt = 0
    for x in range(0, Ox):
        for y in range(0, Oy):
            if img[x, y] == 0:
                hash += "0"
            else:
                hash += "1"
            # cnt uses for readability hash
            cnt += 1
            if cnt == 4:
                hash += " "
                cnt = 0

    return hash


# computing difference of hashes
def diff(hash1, hash2):

    n = len(hash1)
    diff = 0

    for i in range(0, n):
        if hash1[i] != hash2[i]:
            diff += 1

    return diff


# for better visibility
def increase(initial_image, size):
    # dimension
    N = len(initial_image)
    M = int(size / N)

    image = np.empty((size, size), dtype=int)

    # transformation
    for x in range(0, N):
        for y in range(0, N):
            if initial_image[x, y] == 0:
                tmp = np.zeros((M, M), dtype=int)
            else:
                tmp = np.full((M, M), 255, dtype=int)

            image[x*M:(x+1)*M, y*M:(y+1)*M] = tmp

    return image


####################### parsing


# download from google images
def download_images_google(req, n):

    # take request
    req = re.sub(r'\s+', "+", req)

    # take response from google images
    URL = GOOGLE_IMAGE + req
    response = requests.get(URL)

    # take soup and tag 'table' from it
    soup = BeautifulSoup(response.content, 'html.parser')
    items = soup.find_all('table', class_="TxbwNb", limit=n)

    # take image links
    images = []
    cnt = 0
    for item in items:

        # take small image URL
        small_image = item.find('img', class_='t0fcAb')['src']
        print(f'small image = {small_image}')

        # take origin URL
        reg = r'=[^&]+&'
        origin = item.find('a')['href']
        origin = re.search(reg, origin)[0]
        origin = origin[1:(len(origin)-1)]
        print(f'origin url = {origin}')

        # take domain
        reg = r'//[^/]+/'
        domain = re.search(reg, origin)[0]
        domain = domain[2:(len(domain) - 1)]
        if not (domain[0:4] == 'http'):
            domain = 'http://' + domain

        try:
            # take soup from origin URL
            response = requests.get(origin, headers=Headers().generate())
            origin_soup = BeautifulSoup(response.content, 'html.parser')

            # take title of origin
            title = origin_soup.find('title').text
        except:
            title = "Untitled"

        print(f'title = {title}')

        try:
            all_img = origin_soup.findAll('img')

            # vector images is crash
            all_images = []
            is_found = False
            for im in all_img:
                image = im['src']
                if not (image in all_images):
                    all_images.append(image)

                    try:
                        obj = algo.Algo(small_image, image)
                        obj.aHash()
                        print(obj.ans)
                        if obj.ans >= 95:
                            is_found = True
                            break
                    except:
                        continue

            if not is_found:
                image = None
        except:
            image = None

        print(f'image = {image}')

        cnt += 1

        images.append({
            'image_URL': small_image,
            'source': origin,
            'domain': domain,
            'title': title,
            'rating': cnt,
            'origin_image': image,
        })

        print()

    return images
