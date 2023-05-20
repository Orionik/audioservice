# -*- coding: utf-8 -*-
from fastapi import FastAPI, Request, Depends, HTTPException, Form
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship
from sqlalchemy.orm import joinedload, contains_eager
from sqlalchemy.orm import Session
from sqlalchemy import select
import os
import xml.etree.ElementTree as xml

import crud, models, schemas
from database import SessionLocal, engine, Base


Base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="templates")

app = FastAPI()


# Dependency
def get_db(request: Request):
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Вход в учётную запись
@app.post("/user/")
async def create_upload_files(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if username=='admin' and password=='admin':
        return templates.TemplateResponse('index.html', {'request': request})
    stream = str(crud.check_password(db, password = password, user_id = username)[0])
    return templates.TemplateResponse("BB.html", {"request": request, "stream": "http://127.0.0.1:7788/"+stream})


# Регистрация
@app.post("/singup/")
async def singup(request: Request, id: str = Form(...), hashed_password: str = Form(...), stream:str = Form(...), db: Session = Depends(get_db)):
    createXML("{stream}.xml")
    os.system(".\ezstream -q -c {stream}.xml")
    return crud.create_user(db=db, id=id, hashed_password=hashed_password, stream=stream)


# Переход на старницу регистрации
@app.get("/singup/")
async def singup(request: Request):
    return templates.TemplateResponse('singup.html', {'request': request})


# Переход на старницу авторизации
@app.get("/user/")
async def login(request: Request):
    return templates.TemplateResponse('login.html', {'request': request})


def createXML(filename, url: str, ):
    """
    Созаёт XML файл для ezstream
    """
    appt = xml.Element("ezstream")
    
    
    # создаем дочерний суб-элемент
    url = xml.SubElement(appt, "url")
    url.text = 'http://127.0.0.1:7788/' + url
    
    sourcepassword = xml.SubElement(appt, "sourcepassword")
    sourcepassword.text = "hackme"
    
    format = xml.SubElement(appt, "format")
    format.text = "MP3"
    
    filename = xml.SubElement(appt, "filename")
    filename.text = "music/{url}.m3u"
    
    stream_once = xml.SubElement(appt, "stream_once")
    stream_once.text = "0"
    
    shuffle = xml.SubElement(appt, "shuffle")
    shuffle.text = "1"
    
    svrinfoname = xml.SubElement(appt, "svrinfoname")
    svrinfoname.text = "Radio-server"

    svrinfourl = xml.SubElement(appt, "svrinfourl")
    svrinfourl.text = 'http://127.0.0.1:7788/' + url

    svrinfogenre = xml.SubElement(appt, "svrinfogenre")
    svrinfogenre.text = 'pop'

    svrinfodescription = xml.SubElement(appt, "svrinfodescription")
    svrinfodescription.text = "pop music"

    svrinfobitrate = xml.SubElement(appt, "svrinfobitrate")
    svrinfobitrate.text = "128"

    svrinfochannels = xml.SubElement(appt, "svrinfochannels")
    svrinfochannels.text = "2"

    svrinfosamplerate = xml.SubElement(appt, "svrinfosamplerate")
    svrinfosamplerate.text = "44100"

    svrinfopublic = xml.SubElement(appt, "svrinfopublic")
    svrinfopublic.text = "0"

    
    tree = xml.ElementTree(appt)
    with open(filename, "ab") as fh:
        tree.write(fh)

#py -m uvicorn main:app --reload