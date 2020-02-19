import time, smtplib, os, pyscreenshot
from datetime import datetime
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait	
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from email.mime.image import MIMEImage
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

Servicedesk_email = "dft.servicedesk@dafiti.com.br"
servicedesk_email_login = "servicedesk.robo14@gmail.com"
servicedesk_password = "Sd2019monitoracao"



def comprar(url, site):

	browser.get("https://secure.{}.com.br/customer/account/login/".format(site))
	time.sleep(6)
	#login e senha para entrar no site
	try:
		browser.find_element_by_xpath("""//html/body/div[6]/div[2]/div/div/div/button""").click()
		time.sleep(2)
	except NoSuchElementException:
		pass

	browser.find_element_by_xpath("""//*[@id="LoginForm_email"]""").send_keys(servicedesk_email_login)
	time.sleep(0.6)
	browser.find_element_by_xpath("""//*[@id="LoginForm_password"]""").send_keys(servicedesk_password)
	time.sleep(0.6)
	browser.find_element_by_xpath("""//*[@id="customer-account-login"]""").click()
	time.sleep(5)

	#abre um item
	browser.get(url)
	time.sleep(6)

	#adiciona no carrinho
	browser.find_element_by_xpath("""//*[@id="add-to-cart"]/button""").click()
	time.sleep(7)

	#ir para o carrinho
	browser.get("https://secure.{}.com.br/cart/".format(site))
	time.sleep(6)

	#clicar em finalizar compra
	browser.find_element_by_xpath("""//*[@id="button-finalize-order-1"]""").click()
	time.sleep(4)

	#selecionar o boleto
	browser.find_element_by_xpath("""//*[@id="boleto"]""").click()
	time.sleep(4)

	#clicar em finalizar compra
	browser.find_element_by_xpath("""//*[@id="btn_finalize_order"]""").click()
	time.sleep(2)

	#espera o numero do pedido
	numero_pedido = WebDriverWait(browser, 30).until(EC.visibility_of_element_located((By.XPATH,"""//span[@class="sel-order-nr"]"""))).text

	
	hora = datetime.today()
	#mostra numero do pedido e hora
	pedidos.append((numero_pedido, hora))
	print(numero_pedido, hora, site)




def enviar_email(erro, site):
	#login no email
	de = "servicedesk.robo14@gmail.com"
	para = "dft.servicedesk@dafiti.com.br"
	senha = "Sd2019monitoracao"
	msg = MIMEMultipart()
	msg ['From'] = de
	msg['To'] = para
	msg['Subject'] = "Erro na compra"

	body = "Ocorreu um erro na compra do site [{1}]:\n({0})".format(erro, site)

	# anexa imagem
	image = MIMEImage(open('error.png','rb').read())
	msg.attach(image)
	# anexa o texto
	msg.attach(MIMEText(body, 'plain'))

	s = smtplib.SMTP('smtp.gmail.com', 587)
	s.starttls()
	s.login(de, senha)
	s.sendmail(de, para, msg.as_string())
	print('mensagem enviada')
	s.quit()


# AQUI COMECA RODAR O CODIGO
if __name__ == "__main__":

	chrome_options = webdriver.ChromeOptions()

	prefs = {
	"profile.default_content_setting_values.notifications": 2,
	#"deviceName": "Galaxy S5" 
	}

	#inicia maximizado
	chrome_options.add_argument("--start-maximized")
	chrome_options.add_experimental_option("prefs", prefs)

	browser = webdriver.Chrome(options=chrome_options)
	
	
	browser.set_page_load_timeout(60)

	#lista de skus para buscar
	skus = []
	# Trocar url do produto abaixo
	urls = [
	'https://www.kanui.com.br/Bolsa-Capodarte-Logo-Caramelo-4690776.html',
	'https://www.tricae.com.br/Bolsa-Capodarte-Logo-Caramelo-4690776.html']

	sites = ['kanui','tricae']

	pedidos = []

	# tente
	try:
		
		for url,site in zip(urls,sites):
			comprar(url, site)
		
		

	# exceto erro
	except Exception as erro:
		browser.save_screenshot('error.png')
		enviar_email(erro, site)
		
		raise
	browser.quit()
