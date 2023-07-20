import zipfile
import os
import time
import stat
import time
import sys
import shutil


inicio = time.time()

diretorioBase = r'C://Users/danie/Downloads'

pathArquivosEmpresa = diretorioBase + '/Empresas'
##Argumento 1 = Caminho onde os arquivos de Empresas da receita federal estao extraidos
#pathArquivosEmpresa = sys.argv[1]

pathArquivosEstabelecimento = diretorioBase + '/Estabelecimentos'
###Argumento 2 = Caminho onde os arquivos de Estabelecimentos da receita federal estao extraidos
#pathArquivosEstabelecimento = sys.argv[2]

diretorioDestino = diretorioBase + '/RelatorioEmpresas'
###Argumento 3 = Caminho onde os arquvios zip deverao ser alocados
#diretorioDestino = sys.argv[3]

nomePastas = diretorioBase + '/Pastas.txt'
###Argumento 4 = Caminho onde os ranges de pastas estao mapeados
#nomePastas = sys.argv[4]

listaPastas = []

##Deleta a pasta destino existente se houver
#if os.path.isdir(diretorioDestino):
#    for item in os.listdir(diretorioDestino):
#        shutil.rmtree(diretorioDestino)
#    #    caminho_item = os.path.join(diretorioDestino, item)
#    #    if os.path.isdir(caminho_item):
#    #       shutil.rmtree(caminho_item) Excluir apenas as pastas não zipadas

#Cria pastas destinos
with open(nomePastas, "r") as nomePasta:
    for linha in nomePasta:
        if(linha.__contains__('\n')):
            nomePastaEmpresas = linha[:-1]
        else:
            nomePastaEmpresas = linha
        listaPastas.append(nomePastaEmpresas)
        caminhoPastaEmpresas = os.path.join(diretorioDestino, nomePastaEmpresas)
        os.makedirs(caminhoPastaEmpresas, exist_ok=True)
        permissao = stat.S_IRUSR | stat.S_IWUSR | stat.S_IXUSR
        os.chmod(caminhoPastaEmpresas, permissao)
        
fim = time.time()
print("===============================")
print("PASTAS GERADAS")
print("===============================")
print("TEMPO DE PROCESSAMENTO (Segundos):")
print(fim - inicio)
print("===============================")
print("LENDO ARQUIVOS DA RECEITA")

#Le e processa arquivos de empresa
arquivosEmpresa = os.listdir(pathArquivosEmpresa)

for arquivo in arquivosEmpresa:
    if arquivo.endswith('.EMPRECSV'):
        caminho_antigo = os.path.join(pathArquivosEmpresa, arquivo)
        novo_nome = os.path.splitext(arquivo)[0] + '.CSV'
        caminho_novo = os.path.join(pathArquivosEmpresa, novo_nome)
        os.rename(caminho_antigo, caminho_novo)

inicio = time.time()
arquivosEmpresa = os.listdir(pathArquivosEmpresa)
lista = []
for arquivo in arquivosEmpresa:
    listaPastas.clear()
    if arquivo.__contains__('K3241'):
        with open(nomePastas, "r") as nomePasta:
                for linha in nomePasta:
                    if(linha.__contains__('\n')):
                        nomePastaEmpresas = linha[:-1]
                    else:
                        nomePastaEmpresas = linha
                    listaPastas.append(nomePastaEmpresas)

        caminhoArquivo = os.path.join(pathArquivosEmpresa, arquivo)
        inicioOrdenacao = time.time()
        with open(caminhoArquivo, 'rb') as arq_emp:
            lista = list(arq_emp)

            arq_emp.close

            ultimoCaminhoRetornado = ""
            arrayEmp = [];

            inicioOrdenacao = time.time()
            print("===============================")
            print('ORDENANDO ARQUIVO: ' + arquivo)
            lista_ordenada = sorted (lista, key = lambda dado: int(dado[1:9]), reverse = False)

            fimOrdenacao = time.time()
            print("===============================")
            print('TEMPO ORDENACAO ARQUIVO: ' + arquivo)
            print(fimOrdenacao - inicioOrdenacao)

            inicioEscrita = time.time()
            print("===============================")
            print("ESCREVENDO ARQUIVO: " + arquivo)
            for linha_emp in lista_ordenada:
                cnpjBase = linha_emp[1:9]
                if cnpjBase:
                    if listaPastas.__len__() > 1 and int(cnpjBase) >= int(listaPastas[1][0:8]):
                        while(listaPastas.__len__() > 1 and int(cnpjBase) >= int(listaPastas[1][0:8])):
                            listaPastas.pop(0)
                              
                    caminhoRetornado = diretorioDestino + '/' + listaPastas[0] + '/' + 'empresas.txt'
                    
                    if ultimoCaminhoRetornado != caminhoRetornado:
                        if len(arrayEmp) != 0:
                            with open(ultimoCaminhoRetornado, 'ab') as arqCnpj:
                                for val in arrayEmp:
                                        arqCnpj.write(val)
                            arqCnpj.close()
                            arrayEmp.clear()
                            ultimoCaminhoRetornado = caminhoRetornado
                        else:
                            arrayEmp.append(linha_emp) 
                            ultimoCaminhoRetornado = caminhoRetornado
                    else:
                        arrayEmp.append(linha_emp)
                        ultimoCaminhoRetornado = caminhoRetornado
            if len(arrayEmp) != 0:
                with open(ultimoCaminhoRetornado, 'ab') as arqCnpj:
                    for val in arrayEmp:
                        arqCnpj.write(val)
                arqCnpj.close()
                arrayEmp.clear()
                ultimoCaminhoRetornado = caminhoRetornado    
            fimEscrita = time.time()
            print("===============================")
            print("TEMPO DE ESCRITA DO ARQUIVO:")
            print(fimEscrita - inicioEscrita)
            print()

#Le e processa arquivos de estabelecimento
arquivosEstabelecimento = os.listdir(pathArquivosEstabelecimento)
for arquivo in arquivosEstabelecimento:
    if arquivo.endswith('.ESTABELE'):
        caminho_antigo = os.path.join(pathArquivosEstabelecimento, arquivo)
        novo_nome = os.path.splitext(arquivo)[0] + '.CSV'
        caminho_novo = os.path.join(pathArquivosEstabelecimento, novo_nome)
        os.rename(caminho_antigo, caminho_novo)

arquivosEstabelecimento = os.listdir(pathArquivosEstabelecimento)
inicioLeitura = time.time()
for arquivo in arquivosEstabelecimento:
    listaPastas.clear()
    if arquivo.__contains__('K3241'):
        with open(nomePastas, "r") as nomePasta:
                for linha in nomePasta:
                    if(linha.__contains__('\n')):
                        nomePastaEmpresas = linha[:-1]
                    else:
                        nomePastaEmpresas = linha
                    listaPastas.append(nomePastaEmpresas)
        caminhoArquivo = pathArquivosEstabelecimento + '/' + arquivo
        with open(caminhoArquivo, 'rb') as arq_est:
            inicioOrdenacao = time.time()
            print("===============================")
            print('ORDENANDO ARQUIVO: ' + arquivo)
            lista = list(arq_est)
            lista_ordenada = sorted (lista, key = lambda dado: int(dado[1:9]), reverse = False)
            arq_est.close()
            fimOrdenacao = time.time()
            print("===============================")
            print('TEMPO ORDENACAO ARQUIVO: ' + arquivo)
            print(fimOrdenacao - inicioOrdenacao)
            ultimoCaminhoRetornado = ''
            arrayLista = []
            inicioEscrita = time.time()
            print("===============================")
            print("ESCREVENDO ARQUIVO: " + arquivo)
            for linha_est in lista_ordenada:
                cnpjBase = linha_est[1:9];
                if cnpjBase:
                    if listaPastas.__len__() > 1 and int(cnpjBase) >= int(listaPastas[1][0:8]):
                        while(listaPastas.__len__() > 1 and int(cnpjBase) >= int(listaPastas[1][0:8])):
                            listaPastas.pop(0)

                    caminhoRetornado = diretorioDestino + '/' + listaPastas[0] + '/' + 'estabelecimentos.txt'
                    
                    if ultimoCaminhoRetornado != caminhoRetornado:
                        if len(arrayLista) != 0:
                            with open(ultimoCaminhoRetornado, 'ab') as arqCnpj:
                                for val in arrayLista:
                                    arqCnpj.write(val)
                            arqCnpj.close()
                            arrayLista.clear()
                            arrayLista.append(linha_est)
                            ultimoCaminhoRetornado = caminhoRetornado
                        else:
                            arrayLista.append(linha_est)
                            ultimoCaminhoRetornado = caminhoRetornado
                    else:
                        arrayLista.append(linha_est)
                        ultimoCaminhoRetornado = caminhoRetornado

            if len(arrayLista) != 0:
                with open(ultimoCaminhoRetornado, 'ab') as arqCnpj:
                    for val in arrayLista:
                        arqCnpj.write(val)
                arqCnpj.close()
                arrayLista.clear()
                ultimoCaminhoRetornado = caminhoRetornado 
            arq_est.close()
            fimEscrita = time.time()
            print("===============================")
            print("TEMPO DE ESCRITA DO ARQUIVO:")
            print(fimEscrita - inicioEscrita)
            print()

#Gera aquivos Zip
print("===============================")
print("GERANDO ARQUIVOS ZIP")
inicioZip = time.time()            
def zipar_pasta(pasta):
    with open(nomePastas, "r") as nomePasta:
        for linha in nomePasta:
            if(linha.__contains__('\n')):
                nomePastaEmpresas = linha[:-1]
            else:
                nomePastaEmpresas = linha
            nome_zip = pasta + '/' + nomePastaEmpresas + '.zip'
            with zipfile.ZipFile(nome_zip, 'w', zipfile.ZIP_DEFLATED) as arquivo_zip:
                for pasta_raiz, _, arquivos in os.walk(pasta + '/' + nomePastaEmpresas):
                    for arquivo in arquivos:
                        caminho_completo = os.path.join(pasta_raiz, arquivo)
                        arquivo_zip.write(caminho_completo, os.path.relpath(caminho_completo, pasta + '/' + nomePastaEmpresas))
            arquivo_zip.close()
    print("===============================")
    print(f'Pasta {pasta} zipada com sucesso!')
    fimZip = time.time()
    print("===============================")
    print("TEMPO DE ESCRITA DOS ARQUIVOS ZIP:")
    print(fimZip - inicioZip)
    print()

pasta_principal = diretorioDestino
zipar_pasta(pasta_principal)

fim = time.time()
print("TEMPO DE PROCESSAMENTO TOTAL:")
print(fim - inicio)
print()

#Exclui as antigas pastas usadas para criar o zip
def excluir_pastas_nao_zip(caminho):
    for nome_arquivo in os.listdir(caminho):
        caminho_completo = os.path.join(caminho, nome_arquivo)
        if os.path.isdir(caminho_completo) and not nome_arquivo.endswith('.zip'):
            shutil.rmtree(caminho_completo)
            print("A pasta " + caminho_completo + " foi excluida com sucesso")
            
pasta_principal = diretorioDestino
excluir_pastas_nao_zip(pasta_principal)