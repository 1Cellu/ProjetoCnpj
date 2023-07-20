import zipfile
import time
import sys
import os
import re
from os import listdir
from os.path import isfile, join

inicioBusca = time.time()

diretorioBase = r'C://Users/danie/Downloads'

diretorio = diretorioBase + '/RelatorioEmpresas'

cnpjCliente = "49930514000135"
#cnpjCliente = sys.argv[1]

pastaCnpj = diretorio
#pastaCnpj = sys.argv[2]

##dirPy = diretorio
#dirPy = os.path.dirname(os.path.abspath(__file__))   

arquivos = [a for a in listdir(pastaCnpj) if isfile(join(pastaCnpj, a))]
arquivos = { a : {} for a in arquivos }

valorInicio = 0
valorFim = 0

for chave in arquivos:
    if chave.count('.zip') > 0 :
        arq = chave
        arq = arq.replace('.zip', '')
        arq = arq.replace('-', ' ')
        arq = arq.split(' ')
        arquivos[chave] = arq
        arquivos[chave] = [int(c) for c in arquivos[chave]]

        valorInicio = arquivos[chave][0]
        valorFim = arquivos[chave][1]

        if valorInicio <= int(cnpjCliente[0:8]) and int(cnpjCliente[0:8]) <= valorFim:
            arquivo = chave
            break

retorno = bytes("","iso-8859-1")

stories_zip = zipfile.ZipFile(pastaCnpj + "\\" + arquivo)
file = stories_zip.read("empresas.txt")

retornoEmpresa = ""

pos = file.find(bytes(cnpjCliente[0:8], "iso-8859-1"))
if pos >= 0:
    Cnpj = cnpjCliente[0:8]
    retornoEmpresa = file[pos:len(file)]
    retornoEmpresa = retornoEmpresa[0:retornoEmpresa.find(bytes("\r\n", "iso-8859-1"))].decode("iso-8859-1")

retornoEstabelecimento = ""

file = stories_zip.read("estabelecimentos.txt")

def encontrar_linhas_com_cnpj_bytes(file, cnpjCliente):
    cnpj_regex = re.compile(rb'"(\d{8})";"(\d{4})";"(\d{2})"')
    lista = file.split(b"\n")
    for linha in lista:
        match = cnpj_regex.search(linha)
        if match:
            cnpj_encontrado = match.group(1) + match.group(2) + match.group(3)
            if cnpj_encontrado.decode("iso-8859-1") == cnpjCliente:
                linha_encontrada = linha.strip()[1:len(linha)].decode("iso-8859-1")
                break

    return linha_encontrada

retornoEstabelecimento = encontrar_linhas_com_cnpj_bytes(file, cnpjCliente)

if(retornoEstabelecimento != "" and retornoEmpresa != ""):
    linha_est = retornoEstabelecimento.split('";"')
    linha_emp = retornoEmpresa.split('";"')
    if linha_est[0] == linha_emp[0]:
        cnpj = linha_est[0] + linha_est[1] + linha_est[2]
        TipoEmpresa = linha_est[3]
        RazaoSocial = linha_emp[1]
        NomeFantasia = linha_est[4]

        SituacaoCadastral = linha_est[5]
        DataSituacaoCadastral = "" if linha_est[6] == "--" else linha_est[6][:4] + "-" + linha_est[6][4:6] + "-" + linha_est[6][6:8]
        MotivoSituacaoCadastral = linha_est[7]

        NaturezaJuridica = linha_emp[2]
        DataAbertura = "" if linha_est[10] == "" else linha_est[10][:4] + "-" + linha_est[10][4:6] + "-" + linha_est[10][6:8]
        CnaePrincipal = linha_est[11]

        TipoLogradouro = linha_est[13]
        Logradouro = linha_est[14]
        Numero = linha_est[15]
        Complemento = linha_est[16]
        Bairro = linha_est[17]
        Cep = linha_est[18]
        Uf = linha_est[19]
        Municipio = linha_est[20]

        Telefone = linha_est[21] + linha_est[22]
        Telefone2 = linha_est[23] + linha_est[24]

        Email = linha_est[27]
        Porte = linha_emp[5]

        SituacaoEspecial = linha_est[28]
        DataSituacaoEspecial = "" if linha_est[29] == "" or linha_est[29] == '\"' else linha_est[29][:4] + "-" + linha_est[29][4:6] + "-" + linha_est[29][6:8]

        Separador = ";@"

        retorno = cnpj + Separador + TipoEmpresa + Separador + RazaoSocial + Separador + NomeFantasia + \
        Separador + SituacaoCadastral + Separador + DataSituacaoCadastral + Separador + MotivoSituacaoCadastral + \
        Separador + NaturezaJuridica + Separador + DataAbertura + Separador + CnaePrincipal + Separador + TipoLogradouro + \
        Separador + Logradouro + Separador + Numero + Separador + Complemento + Separador + Bairro + Separador + Cep + \
        Separador + Uf + Separador + Municipio + Separador + Telefone + Separador + Telefone2 + Separador + Email + \
        Separador + Porte + Separador + SituacaoEspecial + Separador + DataSituacaoEspecial
                                    
else:
    print("Erro: CNPJ do prestador nao encontrado.")
print(retorno)

FimBusca = time.time()
print("TEMPO DE BUSCA:")
print(FimBusca - inicioBusca)
print()