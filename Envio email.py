import datetime
import email.utils
import smtplib
import imaplib
import email
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from main import agenda_academia
import os

email_remetente = os.environ.get('EMAIL_REMETENTE')
password_remetente = os.environ.get('PASSWORD_REMETENTE')
email_destinatario = os.environ.get('EMAIL_DESTINATARIO')

print(email_remetente)
print(password_remetente)
print(email_destinatario)

smtp_server = 'smtp.gmail.com'
porta = 587
hora_inicio = str((datetime.date.today()).strftime("%d/%m/%Y"))

def envia_email(assunto_email, msg_email, envio_resposta='envio'):

    recipients = ['dmalcoln@gmail.com']
    cc = ['dmalcoln@gmail.com']
    recipientes_cc = ['dmalcoln@gmail.com']

    msg = MIMEMultipart()
    msg['From'] = 'malcolnpython@gmail.com'
    msg['To'] = ", ".join(recipients)
    msg['Cc'] = ", ".join(cc)
    msg['Subject'] = (str(assunto_email))
    msg['Message-ID'] = email.utils.make_msgid()

    body = msg_email
    msg.attach(MIMEText(body, 'plain'))
    if envio_resposta == 'resposta':
        img_data = open('Confirmacao.png', 'rb').read()
        image = MIMEImage(img_data, name='Confirmacao.png')
        msg.attach(image)
    server = smtplib.SMTP(smtp_server, porta)
    server.starttls()
    server.login(email_remetente, password_remetente)
    text = msg.as_string()
    server.sendmail(email_remetente, recipientes_cc, text)
    server.quit()


def consulta_email():
    try:
        mail = imaplib.IMAP4_SSL(smtp_server)
        mail.login(email_remetente, password_remetente)
        mail.select('inbox')
        dados = mail.search(None, 'SUBJECT', f'Agendamento@de@Academia:@{hora_inicio}') # RFC822 @ Entra no lugar do Espaço
        lista_ids = str(dados[1]).replace("[b'",'')
        lista_ids = str(lista_ids).split(' ')

        for id in lista_ids[-1]:
            status, dados = mail.fetch(str(id), '(RFC822)')  # i is the email id
            msg = email.message_from_bytes(dados[0][1])
            body = msg.get_payload()[0]
            if str(body).find('sim') >= 1:
                return 'sim'
            elif str(body).find('nao') >= 1:
                return 'nao'
            else:
                return 'Nao foi possivel localizar'
    except Exception as e:
        print(e)
        return print('Exception na tentativa de consultar o Email')


assunto_email = f'Agendamento de Academia: {hora_inicio}'
msg_email = 'Deseja agendar a academia hoje?'
print('enviando email')
envia_email(assunto_email, msg_email)

agora = hora_inicio

while hora_inicio == agora:
    print('Entrando no While')
    retorno = consulta_email()
    if retorno == 'sim':
        print(retorno)
        agenda_academia(p_horario='10:00 - 11:00')
        envia_email('Agendamento Confirmado', 'Agendamento confirmado com sucesso', 'resposta')
        exit()
    else:
        print(retorno)
        print('Aguardando 10 minutos...')
        time.sleep(300)
        agora = str((datetime.date.today()).strftime("%d/%m/%Y"))
