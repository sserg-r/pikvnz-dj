from contextlib import nullcontext
from django.db.models.fields import NullBooleanField
from django.db.models.query import QuerySet
from django.shortcuts import render
from django.http import HttpResponse
# from djgeojson.serializers import Serializer
from django.views.generic import ListView, TemplateView
from . import models
from django.utils.safestring import mark_safe

class HomePageView (ListView):    
    model=models.Shapes0    
    queryset1 = model.objects.raw('SELECT distinct 1 id, name from testapp_Shapes order by name')
    # queryset2 = mark_safe(Serializer().serialize(model.objects.all()))
    queryset={
            # "base": queryset1,
            # "polyg": queryset2,
            "all":model.objects.order_by('id').all(),
            
    }

    template_name = 'home.html'
    context_object_name = 'hpv'
    
class MapView (ListView):
    template_name = 'map.html'
    # model=models.Shapes 
    # queryset = Serializer().serialize(model.objects.all())
    # queryset = model.objects.all()
    # queryset = mark_safe(Serializer().serialize(model.objects.all()))
    # context_object_name = 'polyg'    

class ListView (ListView):
    template_name = 'list.html'
    
# AJAX
def load_subname(request):
    name_id = request.GET.get('name')
    model=models.Shapes0
    queryset = model.objects.raw(f"SELECT distinct 1 id, subname from testapp_Shapes where name like '{name_id}'")
    return render(request, 'sublist.html', {'subnames': queryset})

import re
def get_mvt(tab, fields, tile):
    z=tile['z']
    lv=0
    if z<10: lv=0
    elif z<14: lv=1
    elif z<16: lv=2
    else: lv=3



    fldstr=", ".join([fl for fl in fields if fl !='geom'])
    query_p=f"select {fldstr}, ST_makevalid(ST_AsMVTGeom(geom, env, 4096, 0, false)) \
        from {tab}, tenv WHERE zlevel={lv} and geom && env"

    query_l=f"select {fldstr}, ST_makevalid(ST_AsMVTGeom(geom, env, 4096, 0, false)) \
        from {tab}, tenv WHERE zlevel={lv-1} and geom && env"

    # query_z3=f"WITH  tenv as (select ST_TileEnvelope({tile['z']}, {tile['x']}, {tile['y']}) as env), \
    #     mvtpoly as ({query_l}), \
    #     mvtpoly_det as ({query_p}) \
    #     SELECT 6 id, (SELECT ST_AsMVT(mvtpoly.*, 'poly') FROM mvtpoly) || (SELECT ST_AsMVT(mvtpoly_det.*, 'poly_det') FROM mvtpoly_det) mvt"

    query_z3=f"WITH  tenv as (select ST_TileEnvelope({tile['z']}, {tile['x']}, {tile['y']}) as env), \
        mvtpoly as ({query_l}), \
        mvtpoly_det as ({query_p}) \
        SELECT 6 id, (SELECT ST_AsMVT(mvtpoly_det.*, 'poly_det') FROM mvtpoly_det) || (SELECT ST_AsMVT(mvtpoly.*, 'poly') FROM mvtpoly) mvt"

    query=f"WITH  tenv as (select ST_TileEnvelope({tile['z']}, {tile['x']}, {tile['y']}) as env), \
        mvtpoly as ({query_p})\
        SELECT 6 id, (SELECT ST_AsMVT(mvtpoly.*, 'poly') FROM mvtpoly)"
    
    # return query
    return query if lv<3 else query_z3

def get_tile1(request, **kwargs):
    tab='testapp_Shapes'
    fields=['id', 'name','subname', 'classmane']
    querystr= get_mvt(tab, fields, kwargs)
    model=models.Shapes0
    queryset = model.objects.raw(querystr)[0]
    
    # print(querystr)
    return HttpResponse(bytes(queryset.mvt), content_type="application/vnd.mapbox-vector-tile")  

# import psycopg2
# from testproj.settings import DATABASES

# class DBConnector(object):
#     def __new__(cls):
#         if not hasattr(cls, 'instance'):
#             cls.instance = super(DBConnector, cls).__new__(cls)
#         return cls.instance

#     def __init__(self):
#         settings=DATABASES['default']
        # dbname=settings['NAME']
        # user=settings['USER']
        # passw=settings['PASSWORD']
        # host=settings['HOST']
        # port=settings['PORT']
        # dbname='gis'
        # user='gis'
        # passw='ss571322rr'
        # host='database-1.c7iiuhyzvsod.eu-west-1.rds.amazonaws.com'
        # port='5432'
        # self.instance = psycopg2.connect(f"dbname={dbname} user={user} password={passw} host={host} port={port}")
            
# def get_tile(request, **kwargs):

#     # if kwargs['z']<13:
#     #     return HttpResponse('')
#     # tab='testapp_Shapes'
#     tab='tiles_data_classed'
#     fields=['id', 'draw_class', 'classes']
#     querystr= get_mvt(tab, fields, kwargs)
#     con = DBConnector()
#     records=None
#     with con.instance.cursor() as cursor:
#         cursor.execute(querystr)
#         records = cursor.fetchone()[1]
#     # print(querystr)
#     response=HttpResponse(bytes(records), content_type="application/vnd.mapbox-vector-tile")
#     # response['Referrer_Policy'] = 'no-referrer'
#     response["Access-Control-Allow-Origin"] = "*"
#     return response

from django.db import connection
def get_tile(request, **kwargs):

    # if kwargs['z']<13:
    #     return HttpResponse('')
    # tab='testapp_Shapes'
    tab='tiles_data_classed'
    fields=['id', 'draw_class', 'classes']
    z,x,y=kwargs['z'], kwargs['x'],kwargs['y']
    # print(kwargs)
    querystr=f"select  mvt from cashed where z={z} and x={x} and y={y}"
    
    # querystr= get_mvt(tab, fields, kwargs)
    # con = DBConnector()
    # records=None
    response=HttpResponse('')
   
    with connection.cursor() as cursor:
        cursor.execute(querystr)        
        rec = cursor.fetchone() 
        if rec: 
            response=HttpResponse(bytes(rec[0]), content_type="application/vnd.mapbox-vector-tile")
            response["Access-Control-Allow-Origin"] = "*"
    # queryset2 = mark_safe(Serializer().serialize(model.objects.all()))
    
    # with con.instance.cursor() as cursor:
    #     cursor.execute(querystr)
    #     rec=cursor.fetchone()
    #     if rec: 
    #         response=HttpResponse(bytes(rec[0]), content_type="application/vnd.mapbox-vector-tile")
    #         response["Access-Control-Allow-Origin"] = "*"
    
        # response['Referrer_Policy'] = 'no-referrer'
       
    return response