from bs4 import BeautifulSoup
import requests 
import csv
import time
import sys

URL_Base = "http://web.transparencia.pe.gov.br/ModuloCidadao/atendimento_detail.xhtml?atendimentoId="

anos = range(10, 21)
protocolos = range(0, 50001)

def gera_protocolos():
    protocolos_arr = []

    for ano in anos:
        for prot in protocolos:
            protocolos_arr.append( "20" + str(ano) + str(prot) )
    
    return protocolos_arr

def get_protocolo_atual():
    with open("protocolo_atual.txt", "r") as protocolo_atual:
        atual = protocolo_atual.read();
        return atual

def write_protocolo_atual(num):
    with open("protocolo_atual.txt", "w") as protocolo_atual:
        protocolo_atual.write(str(num));

def get_protocolo_position(list, atual):
    for i in [i for i,x in enumerate(list) if x == atual]:
        return i

def baixa_protocolos():
    with open('dados_ouvidoria.csv', 'a', newline='', encoding="utf-8") as file:
        writer = csv.writer(file, delimiter=';')

        protocolo_atual  = get_protocolo_atual()

        all_protocolos = gera_protocolos()

        pos = get_protocolo_position(all_protocolos, protocolo_atual)

        pos_final = pos+1

        for p in all_protocolos[pos_final:]:
            URL_Final = URL_Base + str(p)
            # print(URL_Final)
            r = requests.get(URL_Final)

            # print(r.status_code)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html5lib')

                pnlDetalhes = soup.find('div', attrs = {'id':'paiDetailForm:pnlResultadoDetalhes'})

                divResult = pnlDetalhes.find('div', attrs = {'class':'detail-result'})

                divResultAll = divResult.findAll('div')

                i = 0

                linha = []
                for div in divResultAll:
                    

                    if i == 0: #Solicitacao
                        sol = div.text.split("-")
                        # print(sol[0])
                        linha.append(sol[0].strip())#Tipo
                        # print(sol[1])
                        linha.append(sol[1].strip())#Protocolo
                    elif i == 1: #Orgao, Tipo Resposta, Assunto
                        divSpan = div.findAll('span', attrs = {'class':'detail-content'})
                        for sp in divSpan:
                            spn =  sp.text.split(":")
                            # print(spn[1])
                            linha.append(spn[1].strip())#Orgao, Tipo Resposta, Assunto
                    elif i == 2: #Pergunta
                        div_perg_res = div.findAll('span', attrs = {'class':'detail-content'})
                        data_pergunta = div_perg_res[0].text.replace("Pergunta (", "")
                        data_pergunta = data_pergunta.replace("):", "")
                        # print(data_pergunta)
                        linha.append(data_pergunta.strip())#Data Pergunta
                        # print(div_perg_res[1].text)
                        linha.append(div_perg_res[1].text.strip())#Pergunta
                    elif i == 3:
                        div_perg_res2 = div.findAll('span', attrs = {'class':'detail-content'})
                        data_resposta = div_perg_res2[0].text.replace("Resposta (", "")
                        data_resposta = data_resposta.replace("):", "")
                        # print(data_resposta)
                        linha.append(data_resposta.strip())#Data Resposta
                        # print(div_perg_res2[1].text)
                        linha.append(div_perg_res2[1].text.strip())#Resposta
                    i += 1
            else:
                print(r.status_code)
                print(URL_Final)
            writer.writerow(linha)
            write_protocolo_atual(p)

while str(get_protocolo_atual()) != "202050000":
    try:
        baixa_protocolos()
    except KeyboardInterrupt:
        sys.exit(0)
    except:
        print("Tentando denovo!!")