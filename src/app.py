import collections
from crypt import methods
from operator import truediv
from pydoc import doc
from re import S
import string
import os
import json
import forms
import subprocess
import pymongo
import hashlib
from bson.objectid import ObjectId
from datetime import datetime, date, timedelta

from flask import Flask
from flask import render_template, jsonify, request, session
from flask import flash, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
client = MongoClient("mongo", 27017) 
database = client.news_db

# Secret key set for session variable
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

spiders=['granadahoy', 'granadadigital', 'ahoragranada']

basedir = os.path.abspath(os.path.dirname(__file__))
ag_data = os.path.join(basedir, 'files/json/ag_data.json')
gh_data = os.path.join(basedir, 'files/json/gh_data.json')
gd_data = os.path.join(basedir, 'files/json/gd_data.json')
bow_data= os.path.join(basedir, 'newspaperscrape/newspaperscrape/bow/bow.txt')


ag_today = os.path.join(basedir, 'files/json/ag_today.json')
gh_today = os.path.join(basedir, 'files/json/gh_today.json')
gd_today = os.path.join(basedir, 'files/json/gd_today.json')

files= [ag_today, gh_today, gd_today]
last_update=""

def np_data(np_name):

    url=""
    np="all"
    if np_name=="granadahoy":
      url= "https://www.granadahoy.com"
      np= "Granada Hoy"
    elif np_name=="ahoragranada":
      url= "https://www.ahoragranada.com"
      np= "Ahora Granada"
    elif np_name=="granadadigital":
      url= "https://www.granadadigital.com"
      np= "Granada Digital"
    
    
    return url, np


def read_bow():
  with open(bow_data, "r") as file:
      words = file.read().split(',')

  word_list= []
  for w in words:
      word_list.append(w)

  return word_list

def news_today():
  now= date.today().isoformat()
  today=now.split("T")[0]

  # Noticias publicadas hoy 
  collection= database.news.find({'date_format': {"$gte" : today}})
  l=list(collection)
  return str(len(l))


@app.route('/')
def index():
  if 'admin' in session:
        admin= session['admin']
        superadmin= session['superadmin']
        return render_template('index.html', admin= admin, superadmin= superadmin, count=news_today())
  return render_template('index.html', count=news_today())


@app.route('/news')
@app.route('/news/<string:np>')
def news(np="all"):
  url, np_name= np_data(np)
  if (np=="all"):
    msj="Todas las noticias encontradas"
    collection= database.news.find().sort("date_format", pymongo.DESCENDING)
    
  else:
    msj="Noticias en " + np_name
    collection= database.news.find({"np":np}).sort("date_format", pymongo.DESCENDING)
  
  l=list(collection)
  t= len(l)
  if 'admin' in session:
    admin= session['admin']
    superadmin=session['superadmin']
    return render_template('list.html', list=l, np=np, msj=msj, url=url, t=t, date_filter=0, admin=admin,superadmin= superadmin, count=news_today())
  else:
     return render_template('list.html', list=l, np=np, msj=msj, url=url, t=t, date_filter=0 , count=news_today())

     
@app.route('/date_filter')
@app.route('/news/date_filter')
@app.route('/news/<string:np>/date_filter')
@app.route('/news/<string:np>/date_filter')
def news_filter_by_date(np="all"):

  url, np_name= np_data(np)

  start= request.args['start'] # Obtenemos los parametros
  end= request.args['end']
  start_format = datetime.strptime(start, '%Y-%m-%d')
  end_format= datetime.strptime(end, '%Y-%m-%d')


  if np=="all": # Y no hay filtro de periodico
    msj="Todas las noticias encontradas"
    collection = database.news.find( {'date_format': {'$lte': end_format.isoformat(), '$gte':start_format.isoformat()}}).sort("date_format", pymongo.DESCENDING)
    t= database.news.count_documents({'date_format': {'$lte': end_format.isoformat(), '$gte':start_format.isoformat()}})
  else: # Y hay filtro de periodico
    msj="Noticias en " + np_name
    collection = database.news.find({"np": np, 'date_format': {'$lte': end_format.isoformat(), '$gte':start_format.isoformat()}}).sort("date_format", pymongo.DESCENDING)
    t= database.news.count_documents({"np": np, 'date_format': {'$lte': end_format.isoformat(), '$gte':start_format.isoformat()}})
  msj2= "Noticias publicadas entre el " + start + " y el " + end

  if 'admin' in session:
    admin= session['admin']
    superadmin=session['superadmin']
    return render_template('list.html', list=collection, np=np, msj=msj, msj2=msj2, t=t, url=url, date_filter=1, admin=admin, superadmin=superadmin , count=news_today())
  else:
     return render_template('list.html', list=collection, np=np, msj=msj, msj2=msj2, t=t, url=url, date_filter=1, count=news_today())

@app.route('/content_filter')
@app.route('/news/content_filter')
@app.route('/news/<string:np>/content_filter')
def news_filter_by_content(np="all"):
  url, np_name= np_data(np)
  
  cad= request.args['str'] # Obtenemos los parametros

  if np=="all": # Si no hay filtro de periodico
    msj="Todas las noticias encontradas"
    news = database.news.find().sort("date_format", pymongo.DESCENDING)
  else: # Si hay filtro de periodico
    msj="Noticias en " + np_name
    news = database.news.find({"np": np}).sort("date_format", pymongo.DESCENDING)

  collection= [new for new in news if cad in new['content'].lower()]
  t=len(collection)

  msj2= "Noticias que contienen ``" + cad + "´´"

  if 'admin' in session:
    admin= session['admin']
    superadmin=session['superadmin']
    return render_template('list.html', list=collection, np=np, msj=msj, msj2=msj2, t=t, url=url, cad=cad, date_filter=0, admin=admin, superadmin=superadmin , count=news_today())
  else:
     return render_template('list.html', list=collection, np=np, msj=msj, msj2=msj2, t=t, url=url, cad=cad, date_filter=0, count=news_today())

@app.route("/content_date_filter")
def news_content_and_date_filter():

  start= request.args['start'] # Obtenemos los parametros
  end= request.args['end']
  cad= request.args['str']
  start_format = datetime.strptime(start, '%Y-%m-%d')
  end_format= datetime.strptime(end, '%Y-%m-%d')

  msj="Todas las noticias encontradas"
  news = database.news.find( {'date_format': {'$lte': end_format.isoformat(), '$gte':start_format.isoformat()}}).sort("date_format", pymongo.DESCENDING)
  
  collection= [new for new in news if cad in new['content'].lower()]
  t=len(collection)
  msj2=  "Noticias publicadas entre el " + start + " y el " + end + " que contienen ``" + cad + "´´"
 

  if 'admin' in session:
    admin= session['admin']
    superadmin=session['superadmin']
    return render_template('list.html', list=collection, np="all", msj=msj, msj2=msj2, cad=cad, t=t, date_filter=0, admin=admin, superadmin=superadmin, count=news_today())
  else:
     return render_template('list.html', list=collection, np="all", msj=msj, msj2=msj2, cad=cad, t=t, date_filter=0, count=news_today())

@app.route('/view_new/<string:id>')
@app.route('/news/view_new/<string:id>')
@app.route('/news/<string:np>/view_new/<string:id>')
@app.route('/content_filter/view_new/<string:id>')
@app.route('/news/content_filter/view_new/<string:id>')
def show_new(id, np=""):
  new= database.news.find({'_id': ObjectId(id)})
  if 'admin' in session:
    admin= session['admin']
    superadmin=session['superadmin']
    return render_template('new_page.html', admin=admin, superadmin=superadmin, new=new , count=news_today())
  else:
     return render_template('new_page.html', new=new , count=news_today())



############################ ADMIN TASKS ##############################

#-------------------------- USERS MANAGEMENT --------------------------#

@app.route('/user_manage')
def user_manage():

    if session['superadmin']=="1":
      admin= session['admin']
      superadmin= session['superadmin']

      users= database.admin.find()
      return render_template('user_manage.html', admin= admin, superadmin= superadmin, users= users , count=news_today()) 
    else:
      return redirect(url_for('error_403'))

    


@app.route('/register', methods=['POST'])
def registrar():
  if 'superadmin' in session:
    if request.method=='POST':

      if (request.form['superadmin']=="0"):
        rol="Gestor"
      else:
        rol="Superadministrador"

      clave = request.form['pwd'].encode('utf-8')
      pwd=hashlib.md5(clave).hexdigest()
      
      admin= {
          "name": request.form['name'],
          "surname": request.form['surname'],
          "username": request.form['username'],
          "pwd": pwd,
          "superadmin": request.form['superadmin'],
          "rol": rol
      }
      
      database.admin.insert_one(admin)

      flash('Usuario regitrado con éxito.')
      return redirect(url_for('user_manage'))
  else:
      return redirect(url_for('error_403'))


@app.route('/adminlogin')
def login():
    login_form=forms.LoginForm(request.form)
    return render_template('login.html', form= login_form)

@app.route('/entry', methods=['GET', 'POST'])
def entry():
    error = None
    login_form= forms.LoginForm()
    if request.method == 'POST':
        document= database.admin.find_one({"username":request.form['username']})
        if not document:
          error = 'Usuario no existente, prueba de nuevo'
        else:
          name= document['name']
          username= document['username']
          pwd= document['pwd']
          superadmin= document['superadmin']
          if request.form['username']!= username or hashlib.md5(request.form['pwd'].encode()).hexdigest() != pwd:
             error = 'Credenciales incorrectos, prueba de nuevo'
          else:
              session['admin']=  name
              session['username'] = username
              session['superadmin']= superadmin

              flash('Sesión iniciada con éxito. Bienvenid@, {}'.format(name))
              return redirect(url_for('index'))
    return render_template('login.html', error= error, form=login_form)

@app.route('/logout')
def logout():
  if 'admin' in session:
    session.pop('admin')
    session.pop('username')
    session.pop('superadmin')
  
  flash('Se ha cerrado la sesión con éxito')
  return redirect(url_for('index'))

@app.route('/user_data_form/<id>')
def datos_user(id):
    if 'admin' in session:
      document= database.admin.find({"_id":ObjectId(id)})
      return render_template('user_data.html', user= document[0], admin=session['admin'], superadmin= session['superadmin'] , count=news_today())

@app.route('/modify_user/<string:id>', methods=['POST'])
def datos(id):
    if session['superadmin']=="1":
  
            old_values = database.admin.find_one({"_id": ObjectId(id)}) 

            if request.form['superadmin'] =="1":
              rol= "Superadministrador"
            else:
              rol= "Gestor"
            update = {"$set": {"name": request.form['name'], "surname": request.form['surname'], "username": old_values["username"], "pwd":  hashlib.md5(request.form['pwd'].encode()).hexdigest(), "superadmin":request.form['superadmin'], "rol": rol}}
            
            database.admin.update_one(old_values, update)
            flash('Los datos se han modificado con exito')
            return redirect(url_for('user_manage'))
    else:
      return redirect(url_for('error_403'))

@app.route('/user_manage/deleteuser/<id>',methods=['DELETE'])
@app.route('/deleteuser/<id>',methods=['DELETE'])
def deleteuser(id):
  if session['superadmin']=="1":
    database.admin.delete_one({'_id': ObjectId(id)})
    return "Deleted!"
  else:
    return redirect(url_for('error_403'))


#-------------------------- NEWS MANAGEMENT --------------------------# 


@app.route('/db_manage')
def db_manage():
  if 'admin' in session:
    log_query= database.log.find({},{'_id':0, "last_update":1}).sort([( '$natural', -1 )] ).limit(1)

    lista_log = list(log_query)  
    if len(lista_log)==0:
        today= datetime.now()
        yesterday = today - timedelta(days = 2)
        database.log.insert_one({'last_update': yesterday.isoformat()})
       

    log= database.log.find({},{'_id':0, "last_update":1}).sort([( '$natural', -1 )] ).limit(1)
    last_update= log[0]['last_update']

    date_time_obj = datetime.strptime(last_update, '%Y-%m-%dT%H:%M:%S.%f')

    s= str(date_time_obj.date())+ " a las " + str(date_time_obj.time())

    return render_template('db_manage.html', admin=session['admin'], superadmin= session['superadmin'], last_update=s, count=news_today())

@app.route('/news/dialy_update')
def actualizacion_diaria():
  if 'admin' in session:
    os.chdir(basedir+"/newspaperscrape")
    subprocess.call(["scrapy", "crawl", "granadahoy", "-O", "../files/json/gh_today.json"])
    subprocess.call(["scrapy", "crawl", "granadadigital", "-O", "../files/json/gd_today.json"])
    subprocess.call(["scrapy", "crawl", "ahoragranada", "-O", "../files/json/ag_today.json"])
    os.chdir(basedir)
    log= database.log.find({},{'_id':0, "last_update":1}).sort([( '$natural', -1 )] ).limit(1)
    last_update= log[0]['last_update']

   
    cont=0
    if os.stat(gh_today).st_size != 0:
      with open (gh_today) as file:
        js= json.load(file)
        for new in js:
          date= new['date_format']
          if date > last_update:
            database.news.insert_one(new)
            cont+=1


    if os.stat(gd_today).st_size != 0:
      with open (gd_today) as file:
        js= json.load(file)
        for new in js:
          date= new['date_format']
          if date > last_update:
            database.news.insert_one(new)
            cont+=1

    if os.stat(ag_today).st_size != 0:
      with open (ag_today) as file:
        js= json.load(file)
        for new in js:
          date= new['date_format']
          if date > last_update:
            database.news.insert_one(new)
            cont+=1
 

    database.log.insert_one({'last_update': datetime.now().isoformat()})
    return str(cont)
  else:
    return redirect(url_for('error_403'))




#-------------------------- BOW MANAGEMENT --------------------------# 

@app.route('/bow_manage')
def bow_manage():
  if 'admin' in session:
    word_list= read_bow()
    return render_template('bow_manage.html', admin=session['admin'], superadmin= session['superadmin'], word_list= word_list, count=news_today())
  else:
    return redirect(url_for('error_403'))


@app.route('/bow/addre')
def add_re():
  if 'admin' in session:
    new_re= request.args['re']

    with open(bow_data, 'a') as file:
      file.write(","+new_re)
      session["bow_modified"]= True

    return render_template('bow_manage.html', admin=session['admin'], superadmin= session['superadmin'], word_list= read_bow(), count=news_today())
  
  else:
    return redirect(url_for('error_403'))

@app.route('/bow/deletere')
def delete_re():
  if 'admin' in session:
    re= request.args['re']

    word_list= read_bow()
    word_list.remove(re)

    with open(bow_data,'w') as file:
      for word in word_list:
        file.write(word+",")

    with open(bow_data, 'rb+') as file:
      file.seek(-1, os.SEEK_END)
      file.truncate()
      
    return render_template('bow_manage.html', admin=session['admin'], superadmin= session['superadmin'], word_list= read_bow(), count=news_today())
  
  else:
    return redirect(url_for('error_403'))



################################################################

@app.errorhandler(404)
def error_404(error):
    return "<h1>Error 404, page not found</h1>", 404

@app.route('/error_403')
def error_403():
    return "<h1>Error 403, Forbidden </h1>", 403

if __name__=='__main__':
  app.run()



app.run(host='0.0.0.0', port=81)
