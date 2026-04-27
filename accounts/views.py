from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import pickle
import os
import numpy as np


model_path=os.path.join(os.path.dirname(__file__),'crop_model.pkl')

model=pickle.load(open(model_path,'rb'))

# Create your views here.

def register(request):
    if request.method =='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.info(request,"Username already exists")
            return redirect('register')
        
        elif User.objects.filter(email=email).exists():
            messages.info(request,"Email already exists")
            return redirect('register')
        
        else:
            User.objects.create_user(username=username, email=email, password=password)
            return redirect('login') # here login means name feild in urls.py for path login, not name of the function

    return render(request, 'register.html')
    


def login_user(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        user=authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)# giving access to that user
            return redirect('home')
        
        else:
            messages.info(request,"Invalid Username or Password")
            return redirect('login')
    else:
        return render(request, 'login.html')

@login_required(login_url='login')
def home(request):
    return render(request,'home.html')


@login_required(login_url='login')
def predict_crop(request):

    if request.method=="POST":
        N=float(request.POST['N'])
        P=float(request.POST['P'])
        K=float(request.POST['K'])
        temp=float(request.POST['temperature'])
        hum=float(request.POST['humidity'])
        ph=float(request.POST['ph'])
        rain=float(request.POST['rainfall'])
        sample=[[N,P,K,temp,hum,ph,rain]]

        # Top 3 predictions
        probs=model.predict_proba(sample)[0]
        classes=model.classes_

        top3 = [
        (crop, round(prob*100,2))
        for crop,prob in sorted(
        zip(classes,probs),
        key=lambda x:x[1],
        reverse=True
        )[:3]
        ]
        return render(request,'result.html',{'top3':top3})

    return render(request,'predict.html')
