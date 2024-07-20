import re
import threading
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


email_re = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
username_re = r"^[a-z0-9_-]{3,15}$"
def check_input(input_data):
    if re.fullmatch(email_re, input_data):
        return 'email'
    elif re.fullmatch(username_re, input_data):
        return 'username'
    else:
        return 'phone'
    

    

class EmailThread(threading.Thread):
    def __init__(self,email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send()

class Email:
    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject = data['subject'],
            body=data['body'],
            to = [data['to_email']]
        )
        if data.get('content_type') == 'html':
            email.content_subtype ='html'
        EmailThread(email).start()

def send_email(email,code):
    html_content = render_to_string(
        'email/auth/email_avtivate.html',
        {'code':code}
    )
    Email.send_email(
        {
            'subject':'Royhatdan otish uchun',
            'to_email':email,
            "body": html_content,
            'content_type':'html'
        }
    )

# from django.shortcuts import get_object_or_404
# from .models import Tournament, Match, User

# def generate_pairings(tournament_id):
#     tournament = get_object_or_404(Tournament, id=tournament_id)
#     participants = tournament.participants.all().order_by('-rating')

#     # Pair players based on the Swiss-system tournament rules
#     for i in range(0, len(participants), 2):
#         Match.objects.create(
#             tournament=tournament,
#             round_number=tournament.current_round(),
#             player1=participants[i],
#             player2=participants[i+1] if i+1 < len(participants) else None
#         )