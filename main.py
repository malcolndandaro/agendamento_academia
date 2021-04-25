import datetime
import smtplib
import email.utils
import imaplib
import email
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from Agendador import agenda_academia
import os
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', filename='C:\\Users\\Malcoln\\Desktop\\agendamento_academia\\log.log', encoding='utf-8')



email_remetente = os.environ.get('EMAIL_REMETENTE')
password_remetente = os.environ.get('PASSWORD_REMETENTE')
email_destinatario = os.environ.get('EMAIL_DESTINATARIO')

smtp_server = 'smtp.gmail.com'
porta = 587
data_inicio = str((datetime.date.today()).strftime("%d/%m/%Y"))

def envia_email(assunto_email, msg_email, envio_resposta='envio'):

    recipients = [email_destinatario]
    cc = [email_destinatario]
    recipientes_cc = [email_destinatario]

    msg = MIMEMultipart()
    msg['From'] = email_remetente
    msg['To'] = ", ".join(recipients)
    msg['Cc'] = ", ".join(cc)
    msg['Subject'] = (str(assunto_email))
    msg['Message-ID'] = email.utils.make_msgid()

    body = msg_email
    msg.attach(MIMEText(body, 'plain'))
    if envio_resposta == 'resposta':
        img_data = open("C:\\Users\\Malcoln\\Desktop\\agendamento_academia\\Confirmacao.png", 'rb').read()
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
        dados = mail.search(None, 'SUBJECT', f'Agendamento@de@Academia:@{data_inicio}') # RFC822 @ Entra no lugar do Espaço
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


assunto_email = f'Agendamento de Academia: {data_inicio}'
msg_email = 'Deseja agendar a academia hoje?'
print('enviando email')
envia_email(assunto_email, msg_email)

agora = data_inicio

while data_inicio == agora:
    logging.info('Disparando consulta_email()')
    retorno = consulta_email()
    logging.info(f'Retorno:{retorno}')
    if retorno == 'sim':
        logging.info('Chamando função "agenda_academia()"')
        try:
            agenda_academia(p_data=data_inicio, p_horario='10:00 - 11:00')
        except Exception as e:
            logging.warning(f'{e}')
            exit()
        else:
            logging.info('Enviando email de confirmação')
            envia_email('Agendamento Confirmado', 'Agendamento confirmado com sucesso', 'resposta')
            exit()
    else:
        logging.info('Aguardando para consultar novamente o status do retorno')
        time.sleep(30)
        agora = str((datetime.date.today()).strftime("%d/%m/%Y"))
