from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect

from .algorithms import algo, util
from .forms import Form, ParseForm, SearchImagesForm
from .models import Image

import datetime
import re

# Create your views here.


def index(request):

    if request.POST:

        form = Form(request.POST)

        if form.is_valid():

            curr_algo = form.cleaned_data["algo"]
            img1 = form.cleaned_data["img1"]
            img2 = form.cleaned_data["img2"]

            # save images into local dir
            obj = algo.Algo(img1, img2)

            if curr_algo == "1":
                obj.aHash()
            if curr_algo == "2":
                obj.pHash_simple()
            if curr_algo == "3":
                obj.pHash()
            if curr_algo == "4":
                obj.dHash_row()
            if curr_algo == "5":
                obj.dHash_col()

            ans = obj.ans
            hash1 = obj.hash1
            hash2 = obj.hash2

            diff = util.diff(hash1, hash2)
            n = int(len(hash1) * 0.8)

            address = "Compare/index.html"
            return render(request, address, {
                "form": form,
                "ans": ans,
                "difference": diff,
                "n": n,
            })
    else:
        address = "Compare/index.html"
        return render(request, address, {
            "form": Form(),
            "ans": "",
        })


# request preprocessing
def preprocess_request(req):
    req = req.lower()
    req = re.sub(r'\s+', ' ', req)
    req = req.strip()
    return req


# create model note
def new_model(image, req):
    model_image = Image.objects.create(
        label=image['image_URL'],
        date=datetime.date.today(),
        request=req,
        title=image['title'],
        domain=image['domain'],
        origin=image['source'],
        history=str(datetime.date.today()),
        rating=str(image['rating']),
        top=image['rating'],
        image=image['origin_image'])
    model_image.save()
    return model_image


def parse(request):

    address = "Compare/parse.html"
    today = datetime.date.today()

    if request.method == "POST":

        form = ParseForm(request.POST)

        if form.is_valid():

            req = form.cleaned_data["req"]
            req = preprocess_request(req)

            N = form.cleaned_data["n"]
            try:
                N = int(N)
                if N < 0 or N > 10:
                    return render(request, address, {
                        "form": form,
                        "message": "Please, fill second field with number from 1 to 10"
                    })
            except:
                return render(request, address, {
                    "form": form,
                    "message": "Please, fill second field with number from 1 to 10"
                })

            links_and_ids = []

            # repeating request for TODAY
            if Image.objects.filter(request=req, date=today).count() > 0:
                return render(request, address, {
                    "form": form,
                    "message": "This request has been today, so to try tomorrow"
                })

            # parsed images
            info = util.download_images_google(req, N)

            # info is empty
            if not info:
                return render(request, address, {
                    "form": form,
                    "message": "Ooops... something goes wrong, please, try later"
                })

            # if images exist by current request (NOT TODAY)
            # then need to check similarity of every image
            if Image.objects.filter(request=req).count() > 0:

                for image in info:

                    # if image doesn't exist with this request and image label
                    # then check its with aHash
                    if Image.objects.filter(request=req, label=image['image_URL']).count() == 0:
                        images_by_req = Image.objects.filter(request=req)

                        is_it_here = False
                        for im in images_by_req:

                            # if we find similar image
                            # update it
                            obj = algo.Algo(image['image_URL'], im.label)
                            obj.aHash()
                            ans = obj.ans

                            if ans >= 95:
                                is_it_here = True
                                id = im.id
                                history = str(im.history) + ' ' + str(today)
                                rating = str(im.rating) + ' ' + str(image['rating'])
                                top = image['rating']
                                Image.objects.filter(id=id).update(history=history, date=today,
                                                                   rating=rating, top=top)
                                print("Already exists")
                                break

                        # new
                        if not is_it_here:
                            # create model note
                            model_image = new_model(image, req)
                            id = model_image.id
                            print("New image")

                    # if this label has already existed
                    # just update and take it
                    else:
                        im = Image.objects.get(request=req, label=image['image_URL'])
                        print(im)
                        id = im.id
                        history = str(im.history) + ' ' + str(today)
                        rating = str(im.rating) + ' ' + str(image['rating'])
                        top = image['rating']
                        Image.objects.filter(id=id).update(history=history, date=today, top=top, rating=rating)
                    links_and_ids.append({
                        "link": image['image_URL'],
                        "id": id,
                    })

            else:
                for image in info:

                    # create model note
                    model_image = new_model(image, req)
                    id = model_image.id

                    links_and_ids.append({
                        "link": image['image_URL'],
                        "id": id,
                    })

            return render(request, address, {
                "form": form,
                "links_and_ids": links_and_ids,
            })
    else:
        return render(request, address, {
            "form": ParseForm()
        })


def image(request, id):

    if Image.objects.filter(id=id).count() > 0:
        image = Image.objects.get(id=id)
        address = "Compare/image.html"
        return render(request, address, {
            'image': image,
        })
    # page doesn't exist
    else:
        address = "Compare/error.html"
        return render(request, address)


# all images, images by query from DB
def images(request):

    address = "Compare/images.html"
    links_and_ids = []
    images = []

    if request.method == "POST":

        form = SearchImagesForm(request.POST)
        
        if form.is_valid():

            req = form.cleaned_data["req"]
            req = preprocess_request(req)
            date = form.cleaned_data["date"]

            # take info of images from query written above
            # remark: __contains is a key that works like substr for field
            images = Image.objects.all()
            if date:
                images = Image.objects.filter(history__contains=date)
            if req:
                images = Image.objects.filter(request=req)
            if req and date:
                images = Image.objects.filter(request=req, history__contains=date)

            # take link of small image and id only
            for image in images:
                links_and_ids.append({
                    "link": image.label,
                    "id": image.id
                })

            return render(request, address, {
                "form": form,
                "links_and_ids": links_and_ids,
            })
    # for start we take all image in DB
    # and do the same that have done earlier
    else:
        images = Image.objects.all()

        for image in images:
            links_and_ids.append({
                "link": image.label,
                "id": image.id
            })

        return render(request, address, {
            "form": SearchImagesForm(),
            "links_and_ids": links_and_ids,
        })



def original_image(request, id):
    address = "Compare/original_image.html"

    info = Image.objects.get(id=id)

    image = info.image
    history = info.history.split(' ')
    rating = info.rating.split(' ')
    history_and_rating = []

    for i in range(len(history)):
        history_and_rating.append({
            "history": history[i],
            "rating": rating[i]
        })

    if image is None:
        image = "https://zashel-nashel.ru/files/watermark/noimage_file.png"

    return render(request, address, {
        "image": image,
        "title": info.title,
        "har": history_and_rating,
    })

