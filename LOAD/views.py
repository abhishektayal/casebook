import parser_new
from django.shortcuts import render_to_response
from django.template import RequestContext
import time
import os

def load(request):
    #load_form = LoadForm()    
    menu=0
    context = {}
    start=time.asctime()
    #parser_new.main() 
    os.system('python /home/ubuntu/casebook/LOAD/parser_new.py')
    end=time.asctime()
    context = {
        'start': start,
        'end': end,
        'menu':menu
    }
    
    return render_to_response('LOAD/loadfinish.html', context,
        context_instance=RequestContext(request))
    

    #return render_to_response('LOAD/loadfinish.html', context,
       # context_instance=RequestContext(request))

   # return HttpResponseRedirect('LOAD/loadfinish.html')
	
