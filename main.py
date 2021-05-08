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

# Log
path = os.getcwd()
path_log= f'{path}/log.log'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', filename=f'{path_log}', encoding='utf-8')


EMAIL_REMETENTE = os.environ.get('EMAIL_REMETENTE')
PASSWORD_REMETENTE = os.environ.get('PASSWORD_REMETENTE')
EMAIL_DESTINATARIO = os.environ.get('EMAIL_DESTINATARIO')
SMTP_SERVER = 'smtp.gmail.com'
PORTA = 587
DATA_INICIO = str((datetime.date.today()).strftime("%d/%m/%Y"))

def envia_email(assunto_email, msg_email, envio_resposta='envio'):

    recipients = [EMAIL_DESTINATARIO]
    cc = [EMAIL_DESTINATARIO]
    recipientes_cc = [EMAIL_DESTINATARIO]

    msg = MIMEMultipart()
    msg['From'] = EMAIL_REMETENTE
    msg['To'] = ", ".join(recipients)
    msg['Cc'] = ", ".join(cc)
    msg['Subject'] = (str(assunto_email))
    msg['Message-ID'] = email.utils.make_msgid()

    body = msg_email
    msg.attach(MIMEText(body, 'plain'))
    if envio_resposta == 'resposta':
        img_data = open(f'{path}/screenshots/Confirmacao.png', 'rb').read()
        image = MIMEImage(img_data, name='Confirmacao.png')
        msg.attach(image)
    server = smtplib.SMTP(SMTP_SERVER, PORTA)
    server.starttls()
    server.login(EMAIL_REMETENTE, PASSWORD_REMETENTE)
    text = msg.as_string()
    server.sendmail(EMAIL_REMETENTE, recipientes_cc, text)
    server.quit()


def consulta_email():
    try:
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(EMAIL_REMETENTE, PASSWORD_REMETENTE)
        mail.select('inbox')
        dados = mail.search(None, 'SUBJECT', f'Agendamento@de@Academia:@{DATA_INICIO}') # RFC822 @ Entra no lugar do Espaço
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



def main():
    assunto_email = f'Agendamento de Academia: {DATA_INICIO}'
    msg_email = 'Deseja agendar a academia hoje?'
    print('enviando email')
    envia_email(assunto_email, msg_email)

    agora = DATA_INICIO

    while DATA_INICIO == agora:
        logging.info('Disparando consulta_email()')
        retorno = consulta_email()
        logging.info(f'Retorno:{retorno}')
        if retorno == 'sim':
            logging.info('Chamando função "agenda_academia()"')
            try:
                agenda_academia(p_data=DATA_INICIO, p_horario='10:00 - 11:00')
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


if __name__=='__main__':
    main()