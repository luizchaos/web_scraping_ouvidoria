from bs4 import BeautifulSoup
import requests 
import csv
import time

URL_Base = "http://web.transparencia.pe.gov.br/ModuloCidadao/atendimento_detail.xhtml?atendimentoId="

anos = range(10, 20)
csv_final = []

for n in anos:
    protocolos = range(1, 50000)

    for x in protocolos:
        URL_Final = URL_Base + "20" + str(n) + str(x)
        print(URL_Final)
        r = requests.get(URL_Final)

        print(r.status_code)
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
        # print(linha)
        csv_final.append(linha)
        time.sleep(2)

# print(csv_final)
with open('dados_ouvidoria.csv', 'w', newline='', encoding="utf-8") as file:
    file.write('\ufeff')
    writer = csv.writer(file, delimiter=';')
    writer.writerow(["TIPO", "PROTOCOLO", "ORGAO", "TIPO_RESPOSTA", "ASSUNTO", "DATA_PERGUNTA", "PERGUNTA", "DATA_RESPOSTA", "RESPOSTA"])
    writer.writerows(csv_final)