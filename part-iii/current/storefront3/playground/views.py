from django.shortcuts import render
from django.core.mail import send_mail, send_mass_mail, mail_admins, BadHeaderError, EmailMessage

from templated_mail.mail import BaseEmailMessage

from .tasks import notify_customer

def say_hello(request):
    notify_customer.delay('Hello')
    return render(request, 'hello.html', {'name': 'Mosh'})
    
    # * Attaching files with an email.
    # try: 
    #     email = EmailMessage('subject', 'Message with an attached file', 'from@adminsika.com', ['dummy1@sika.com'])
    #     email.attach_file('playground/static/images/pic.jpg')
    #     # send_mail(email=email)
    #     email.send()

    #* Sending templated emails:
    # try: 
    #     message = BaseEmailMessage(
    #         template_name='emails/email.html',
    #         context={'name' : 'Sika'}
    #     )
    #     message.send(['john@sika.com'])
    # except BadHeaderError:
    #     pass

    


    # send_mass_mail('subject_of the mail', 
            #   """
            #     This is the message of the whole email. I'm using a multiline string to format this.
            #     But there must be a better way. :)

            #     Best regards,
            #     Sika.
            #     """
    #           , 'from@sika.com', ['to@sika1.com', 'to@sika2.com']
    #           )
    
    # tt = ('subject of the mass mail','Mass mail', 'from@adminsika.com', 'dummy1@sika.com')
    # send_mass_mail(tt)

    # try:
        # * It will send an email to all the admin(s).
    #     mail_admins('subject', 'message', html_message='message')
    # except BadHeaderError:
    #     pass
