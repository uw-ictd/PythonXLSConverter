from django.http import HttpResponse
from django.shortcuts import render_to_response
from django import forms
from models import ConversionLogItem

import datetime
import tempfile
import os
import json
import warnings
import xlsform2
from zipfile import ZipFile

SERVER_TMP_DIR = '/tmp'

class UploadFileForm(forms.Form):
    file  = forms.FileField()

def json_workbook(request):
    error = None
    warningsList = None
    #Make a randomly generated directory to prevent name collisions
    temp_dir = tempfile.mkdtemp(dir=SERVER_TMP_DIR)
    output_filename = 'formDef.json'
    out_path = os.path.join(temp_dir, output_filename)
    fo = open(out_path, "wb+")
    fo.close()
    #ConversionLogItem().save()
    
    try:
        with warnings.catch_warnings(record=True) as w:
            xlsform2.convert_json_workbook(json.loads(request.POST['workbookJson']), out_path)
            warningsList = [str(wn.message) for wn in w]
    except Exception as e:
        error = str(e)
    return HttpResponse(json.dumps({
        'dir': os.path.split(temp_dir)[-1],
        'name' : output_filename,
        'error': error,
        'warnings': warningsList,
    }, indent=4), mimetype="application/json")
    
def index(request):
    if request.method == 'POST':
        error = None
        warningsList = None
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            filename, ext = os.path.splitext(request.FILES['file'].name)
            
            #Make a randomly generated directory to prevent name collisions
            temp_dir = tempfile.mkdtemp(dir=SERVER_TMP_DIR)
            output_filename = 'formDef.json'
            out_path = os.path.join(temp_dir, output_filename)
            fo = open(out_path, "wb+")
            fo.close()
            #ConversionLogItem().save()
            
            try:
                with warnings.catch_warnings(record=True) as w:
                    xlsform2.convert_excel_workbook(request.FILES['file'], out_path)
                    warningsList = [str(wn.message) for wn in w]
            except Exception as e:
                error = str(e)
            
            return render_to_response('xlsform2/upload.html', {
                'form': form,#UploadFileForm(),#Create a new empty form
                'dir': os.path.split(temp_dir)[-1],
                'name' : output_filename,
                'error': error,
                'warnings': warningsList,
            })
        else:
            #Fall through and use the invalid form
            pass
    else:
        form = UploadFileForm() #Create a new empty form
        
    return render_to_response('upload.html', {
        'form': form,
    })
    
def download(request, path):
    """
    Serve a downloadable file
    """
    fo = open(os.path.join(SERVER_TMP_DIR, path))
    data = fo.read()
    fo.close()
    response = HttpResponse(mimetype='application/octet-stream')
    response.write(data)
    return response

#def download_zip(request):
#
#    try:
#        myzip = ZipFile('test.zip', 'w')
#        myzip.write(output_path, os.path.basename(output_path))
#    except: 
#        pass
#    finally:
#        myzip.close()
