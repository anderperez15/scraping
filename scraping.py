from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from webdriver_manager.chrome import ChromeDriverManager
#from webdriver_manager.firefox import GeckoDriverManager
from bs4 import BeautifulSoup
import json

URLS = [
    {'ubicate':True,'coordenada':{'compra':4,'venta':5},'name':'cambix','url':'https://cambix.pe/', 'tag':'span','compra':{ 'class' : 'mat-button-wrapper' },'venta':{ 'class' : 'mat-button-wrapper' }},
    {'ubicate':False,'coordenada':{'compra':0,'venta':1},'name':'dollarhouse','url':'https://app.dollarhouse.pe/calculadora', 'tag':'span','compra':{ 'id' : 'buy-exchange-rate' },'venta':{ 'id' : 'sell-exchange-rate' }},
    {'ubicate':True,'coordenada':{'compra':0,'venta':1},'name':'cambioseguro','url':'https://cambioseguro.com/', 'tag':'span','compra':{ 'data-v-b5022b4c' : '' },'venta':{ 'data-v-b5022b4c' : '' }},
    {'ubicate':False,'coordenada':{'compra':0,'venta':1},'name':'cambiafx','url':'https://cambiafx.pe/', 'tag':'span','compra':{ 'class' : 'txt_compra' },'venta':{ 'class' : 'txt_venta' }},
    {'ubicate':True,'coordenada':{'compra':0,'venta':1},'name':'rextie','url':'https://www.rextie.com/', 'tag':'span','compra':{ 'class' : 'number' },'venta':{ 'class' : 'number' }},
    {'ubicate':False,'coordenada':{'compra':0,'venta':1},'name':'cambistainka','url':'https://cambistainka.com/', 'tag':'strong','compra':{ 'id' : 'lblTCCompra' },'venta':{ 'id' : 'lblTCVenta' }},
    {'ubicate':False,'coordenada':{'compra':0,'venta':1},'name':'acomo','url':'https://acomo.com.pe/', 'tag':'span','compra':{ 'id' : 'current_bid' },'venta':{ 'id' : 'current_offer' }},
    {'ubicate':True,'coordenada':{'compra':1,'venta':2},'name':'dolarsol','url':'https://www.dolarsol.com/', 'tag':'div','compra':{ 'class' : 'field-content' },'venta':{ 'class' : 'field-content' }},
    {'ubicate':True,'coordenada':{'compra':1,'venta':1},'name':'tkambio','url':'https://tkambio.com/', 'tag':'h4','compra':{ 'class' : 'elementor-heading-title elementor-size-default' },'venta':{ 'class' : 'elementor-heading-title elementor-size-default' }},
    {'ubicate':True,'coordenada':{'compra':0,'venta':1},'name':'sbs','url':'https://www.sbs.gob.pe/app/pp/SISTIP_PORTAL/Paginas/Publicacion/TipoCambioPromedio.aspx', 'tag':'td','compra':{ 'class' : 'APLI_fila2' },'venta':{ 'class' : 'APLI_fila2' }},
    {'ubicate':False,'coordenada':{'compra':0,'venta':1},'name':'westernunion','url':'https://www.westernunionperu.pe/cambiodemoneda', 'tag':'button','compra':{ 'id' : 'btnCompra' },'venta':{ 'id' : 'btnVenta' }}
]

options = Options()
options.add_argument("--headless")

class Scraping:

    def runDriverManager(self):
        self.driver = webdriver.Chrome(ChromeDriverManager().install(),options=options)
        #self.driver = webdriver.Firefox(GeckoDriverManager.install())
        self.driver.implicitly_wait(20)

    def close(self):
        print('Ha detenido el programa')
        exit()

    def extract(self):
        while True:
            file = open('data.json')
            data = json.load(file)
            file.close()
            #print(data)
            try:
                self.runDriverManager()
                print('---------- Iniciando ciclo -----------')
                page = []
                for url in URLS:
                    page.append(self.goPage(url))
                data.append(page)
                self.driver.close()

            except (KeyboardInterrupt):
                self.close()
                break
            except :
                print('algo va mal')
            else :
                file = open('data.json','w')
                json.dump(data, file, indent=4)
                file.close()
                print('----------- Guardado -----------------')
                obj = open('data.json','r')
                js = open('script.js','w')
                js.write('window.data ='+obj.read())
                obj.close
                js.close
                #script = open('script.js','w')
                
            time.sleep(60)
            
                    
            



    def goPage(self, page):
        data = {}
        try:
            print(page['name']+' ----> procesando')
            self.driver.get(page['url']) #urllib.request.urlopen(page['url']).read().decode()
            time.sleep(5)
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            if(page['ubicate']):
                tags =  soup.find_all(page['tag'],page['compra'])
                #print(tags)
                if '|' in tags[page['coordenada']['compra']].getText():
                    compra = self.cleam(tags[page['coordenada']['compra']].getText()).split('|')[0]
                    venta = self.cleam(tags[page['coordenada']['venta']].getText()).split('|')[1]
                else:
                    compra = self.cleam(tags[page['coordenada']['compra']].getText())
                    venta = self.cleam(tags[page['coordenada']['venta']].getText())
                    
            else:
                compra = self.cleam(soup.find(page['tag'],page['compra']).getText())
                venta = self.cleam(soup.find(page['tag'],page['venta']).getText())
            #print(page['name'])
            #print(self.cleam(compra))
            #print(self.cleam(venta))
            data['name'] = page['name']
            data['compra'] = compra
            data['venta'] = venta
            data['time'] = time.strftime("%H:%M %d/%m/%y")
            
            #print(page['compra'] == page['venta'])
        except:
            data['name'] = page['name']
            data['compra'] = None
            data['venta'] = None
            data['time'] = time.strftime("%H:%M %d/%m/%y")
        print(data)
        return data

    def cleam(self, line):
        c = ''
        for char in line:
            if char in '1234567890.|':
                c += char
        return c
    

scrap = Scraping()
scrap.extract()