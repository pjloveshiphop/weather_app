from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm


# Create your views here.

def index(request):
    
    url='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=7990b5ed77bdb10e5658d7bec52c5586' 
    
    err_msg=''
    message=''
    message_class=''

    if request.method=='POST':
        form=CityForm(request.POST)

        if form.is_valid():
            new_city= form.cleaned_data['name']
            isDuplicate=City.objects.filter(name=new_city).count()
            
            if isDuplicate==0:
                r=requests.get(url.format(new_city)).json()
                
                if r['cod']==200:
                    form.save()
                else:
                    err_msg='Not a valid city name!!'
            else:
                    err_msg="City exists in database already"
        if err_msg:
            message=err_msg
            message_class='is-danger'
        else:
            message='City has been added successfully!'
            message_class='is-success'
        

    form=CityForm()

    cities=City.objects.all()
    weather_data=[]
    
    for city in cities:


        r=requests.get(url.format(city)).json()
        #print(r.text)

        
        city_weather={
            "city": city.name,
            "temperature": r['main']['temp'],
            "description": r['weather'][0]['description'],
            "icon": r['weather'][0]['icon'],
            
        }

        weather_data.append(city_weather)
    #print(weather_data)

    context={
        'weather_data': weather_data, 
        'form': form,
        'message': message,
        'message_class': message_class
    
    }

    return render(request, 'weather/weather.html', context)


#delete 
def delete_city(request, city_name):
    City.objects.get(name=city_name).delete()

    return redirect('home')
