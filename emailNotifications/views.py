from django.shortcuts import render

from accounts.models import User
from datetime import datetime
from .utils import send_email_with_html_body

def create_views(request, *args, **kwargs):
    """This views helps to create and account for testing sending email"""
    cxt = {}
    if request.method == 'POST':
        email = request.POST.get('email')
        
        subject = "test Email"
        template = 'email.html'
        context = {
            'date' :datetime.today().date,
            'email' : email
        }   
        receivers = [email]
        has_send = send_email_with_html_body(
            subject = subject,
            receivers = receivers,
            template = template,
            context = context
            )
        if has_send :
            cxt = {'msg' : 'envoyer avec succes'}
        else :
            cxt =  {'msg' : 'envois d\'email echoue'}
            
    return render(request,'index.html', cxt)        