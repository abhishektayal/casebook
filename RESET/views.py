import schema
from django.shortcuts import render_to_response
from django.template import RequestContext
import time

def reset(request):
    #load_form = LoadForm()    
    context = {}
    start=time.asctime()
    schema.drop_schema()
    end=time.asctime()
    context = {
        'start': start,
        'end': end,
    }
    
    return render_to_response('RESET/reset.html', context,
        context_instance=RequestContext(request))
    

    #return render_to_response('LOAD/loadfinish.html', context,
       # context_instance=RequestContext(request))

   # return HttpResponseRedirect('LOAD/loadfinish.html')
	
