from pypdf import PdfReader
import re
import pandas as pd

print("\n\nOlá, este programa foi feito para auxiliar a busca pelos mais novos ingressantes da USP pela FUVEST!")
print("Em caso de erro ou problemas com o código, encaminhe-me um email ou uma mensagem pelo twitter.")
print("e-mail: eduardoyukio.ishihara@usp.br")
print("Twitter: @EduardoYukio_\n\n\n")




# Abre o arquivo
try:
    arquivo = 'fuvest_aprovados.pdf'
    reader = PdfReader(arquivo)

except:
    try:
        arquivo = 'fuvest_2025_chamada_1.pdf'
        reader = PdfReader(arquivo)

    except:
        print("Alguma coisa deu errada!")
        print("Verifique se o arquvivo de aprovados está na mesma pasta que este código.")

        try:
            reader = PdfReader(arquivo)

        except:
            print("Essa não, parece que o nome do arquivo não está batendo com a minha base.")
            print("Mude o nome do arquivo para 'fuvest_aprovados.pdf' e execute o programa novamente!")


print("A partir de agora, definiremos os cursos e seus respectivos códigos de carreira!")
print("Lembre-se que a licenciatura é separada do bacharelado e cada período também é separado (diurno, norturno...).\n\n")

num = int(input("Você deseja buscar os bixos de quantos cursos? (Insira apenas números)\n").strip())

print("\n\nAgora, perguntarei o nome de cada curso e o código da fuvest.")
print("Sugiro que vocês escreva o nome dos cursos como 'Matemática - licenciatura - manhã' ou 'Estatística - Integral")
print("Escreva os códigos de forma completa. Exemplos: '765−50', '715−07'. Não se esqueça do zero!\n\n")

cursos = {}
for i in range(num):
    curso  = input(f"Nome do {i+1}º curso: ")
    codigo = input(f"Código do {i+1}º curso: ")
    print("\n")
    codigo = codigo.replace("-", '−')
    cursos[curso] = codigo

print("Eu registrei os seguintes cursos e códigos:")

for a,b in cursos.items():
    print(f'{a:25} - {b}')

print("\nSe estiverem errados, execute o código novamente!\n")
input("Podemos continuar? Aperte enter para prosseguuir! ")
print("\n\n\n")

num_pag = len(reader.pages)
#print(f'Há um total de {num_pag} páginas.')




# Divide cada página em pessoas
i = 0

content = []

while i < num_pag:
    # getting a specific page from the pdf file
    page = reader.pages[i]
    text = page.extract_text().split('\n')[3:-3]
    content.append(text)
    i += 1




# Remove os separadores de letras ('AAAAAAAAAAAAAAAAAA')
i = 0
while i < num_pag:
    page = content[i]
    aux = []
    
    page_len = len(page)

    j = 0
    while j < page_len:
        item = page[j]
        if len(item) == 1:
            j += 2
        else:
            aux.append(item)
            j += 1

    content[i] = aux
    i += 1




# Cria um df com os bixos
name   = []
code   = []
for page in content:
    for person in page:
        code.append(person[-6:])
        name.append(person[:-15])

df = pd.DataFrame({'name': name, 'code': code})




# Imprime os nomes dos bixos
for degree in cursos:
    degree_code = cursos[degree]

    print(f"{degree} - {degree_code} \n")

    list_names = df.loc[df['code'] == degree_code]["name"]
    for person in list_names:
        print(person)
    
    print("\n\n\n")
