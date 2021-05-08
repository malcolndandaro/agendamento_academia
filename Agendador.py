from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import os
import logging


# Log
path = os.getcwd()
path_log= f'{path}/log.log'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s',
                    datefmt='%d/%m/%Y %H:%M:%S', filename=f'{path_log}', encoding='utf-8')



# Default values
EMAIL = os.environ.get('LOGIN_ACADEMIA')
PASSWORD = os.environ.get('PASSWORD_ACADEMIA')
cidade = 'SP - Ribeirão Preto'
data = '25/04/2021'
horario = '10:00 - 11:00'


def agenda_academia(p_email=EMAIL, p_password=PASSWORD, p_cidade=cidade,
                    p_data=data, p_horario=horario):
    """ Utiliza o Selenium para navegadar no site da academia.

        Aceita alguns parametros, porem caso não sejam informados, 
        é utilizado os valores padrões.

        As linhas relacionadas ao chrome_options fazem o chrome abrir no background(modo headless).

        As chamados do time.sleep() foi necessaria devido a variação do tempo
        de loading da pagina, o que faz o Seleneium não encontrar os elementos.

        A navegação foi construida utilizando o selector/id/tag necessario em cada momento,
        a estrutura do site não é ideal, existem "ids" repetidos.  

    """
    # Parametros do Selenium
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    navegador = webdriver.Chrome(executable_path=f'{path}/driver/chromedriver.exe', options=chrome_options)


    # Entrando no site
    navegador.get("https://www.formulaacademia.com.br/cliente/treinos")
    navegador.maximize_window()
    time.sleep(5)

    # Aceitando os Cookies
    botao_cookies = navegador.find_element_by_css_selector('body > div > div > a')
    botao_cookies.click()


    # Interagindo com os campoos
    campo_email = navegador.find_element_by_id('login-email')
    campo_email.send_keys(p_email)
    campo_password = navegador.find_element_by_id('login-password')
    campo_password.send_keys(p_password)
    navegador.save_screenshot(f'{path}/screenshots/screenshot_teste.png')


    # Clicando no botao "Entrar"
    botao_entrar = navegador.find_element_by_id('login-confirm')
    botao_entrar.click()
    time.sleep(5)

    # Depois de logar, acessar o URL do agendamento
    navegador.get('https://www.formulaacademia.com.br/cliente/agendamentos')
    time.sleep(5)


    # Clicando no botao "Novo Horario"
    try:
        botao_novo_horario = navegador.find_element_by_css_selector('body > app-root > ng-component > app-schedules-list > div > div > div.btn-container.text-center.pt-4.ng-star-inserted > button')
        botao_novo_horario.click()
    except:
        botao_novo_horario = navegador.find_element_by_id('empty-button')
        botao_novo_horario.click()


    # Pesquisando a academia
    try:
        time.sleep(5)
        pesquisa_academia = navegador.find_element_by_css_selector('body > app-root > ng-component > app-schedules-create > main > div > form > div:nth-child(3) > div > input')
        pesquisa_academia.click()
        time.sleep(1)
        # Escolhendo Ribeirão Preto
        ribeirao_preto = navegador.find_element_by_xpath(f'//*[contains(text(), "{p_cidade}")]')
        ribeirao_preto.click()
        time.sleep(1)
        # Escolhendo a data
        campos_data_e_hora = navegador.find_elements_by_tag_name('ng-select')
        campo_data = campos_data_e_hora[0]
        campo_data = campo_data.find_elements_by_tag_name('span')[0]
        campo_data.click()
        time.sleep(1)
        opcao_data_agendamento = navegador.find_element_by_xpath(f'//*[contains(text(), "{p_data}")]')
        opcao_data_agendamento.click()
        # Escolhendo a Hora
        hora = campos_data_e_hora[1]
        campo_hora = hora.find_elements_by_tag_name('span')[0]
        campo_hora.click()
        opcao_horario_agendamento = navegador.find_element_by_xpath(f'//*[contains(text(), "{p_horario}")]')
        opcao_horario_agendamento.click()
        time.sleep(1)
        # Selecionando o botao "Agendar"
        form = navegador.find_element_by_tag_name('form')
        botao_agendar = form.find_elements_by_tag_name('button')[1]
        print('clicando')
        botao_agendar.click()
        time.sleep(2)
        # Clicando no botao "SIM" da Popup "Agendar Horario"
        botao_sim = navegador.find_element_by_css_selector('body > app-root > app-modal-confirm > div > div > div > div.modal-footer > button.btn.btn-primary.col')
        botao_sim.click()
        time.sleep(5)
        botao_ok = navegador.find_element_by_css_selector('body > app-root > app-modal-confirm > div > div > div > div.modal-footer > button')
        botao_ok.click()
        time.sleep(2)
        # Aperta o PAGE_DOWN 3 vezes para melhorar a screenshot
        for i in range(2):
            navegador.find_element_by_tag_name('body').send_keys(Keys.PAGE_DOWN)
        navegador.save_screenshot(f'{path}/screenshots/Confirmacao.png')
        navegador.close()
    except Exception as e:
        navegador.save_screenshot(f'{path}/screenshots/Exception.png')
        logging.warning(f'{e}')
        raise
        
    
