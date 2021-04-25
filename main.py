# Imports
from selenium import webdriver
import time
import os

# Chrome
#chrome_options = Options()
#chrome_options.add_argument("--headless")

email = os.environ.get('LOGIN_ACADEMIA')
password = os.environ.get('PASSWORD_ACADEMIA')
cidade = 'SP - Ribeirão Preto'
data = '25/04/2021'
horario = '10:00 - 11:00'

def agenda_academia(p_email=email, p_password=password, p_cidade=cidade, p_data=data, p_horario=horario ):
    navegador = webdriver.Chrome(executable_path='driver/chromedriver.exe')#, options=chrome_options)

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

    # Clicando no botao "Entrar"
    botao_entrar = navegador.find_element_by_id('login-confirm')
    botao_entrar.click()
    time.sleep(5)

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
    navegador.save_screenshot('Confirmacao.png')
    navegador.close()
