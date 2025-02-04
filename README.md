## Olá!
Este código foi criado com o objetivo de buscar os calouros na extensa lista da FUVEST.
Para usá-lo, basta inserir quantos cursos você deseja procurar e inserir o código do curso.
Não se preocupe, o programa pergunta na ordem correta as devidas informações!


### Alguns cuidados:

-Não se enqueça de salvar o arquivo pdf com os aprovados na mesma pasta que esse código!!!

-Na hora de inserir o código do curso, há dois compenentes: a carreira e o descritor.
 Exemplos: '312-19', '317-05', '190-58'

 A carreira são os três primeiros digitos e sempre serão três digitos!
 O descritor, em contrapartida, pode ter um ou dois dígitos. Ao inserir no código, não
 se esqueça de sempre colocar o '0' no descritor. Ou seja, se o descritor do curso desejado
 é '6' e a carreira é '145', insira '145-06'.


-Se desejar utilziar o código para a segunda chamada, apague o arquivo da primeira chamada
 da pasta em que está esse programa, coloque o arquivo com a segunda chamada e mude o nome
 do arquivo da segunda chamada para 'fuvest_aprovados.pdf'.



Em caso de dúvidas ou problemas, emcaminha-me um e-mail ou uma mensagem pelo Twitter.
e-mail: eduardoyukio.ishihara@usp.br
Twitter: @EduardoYukio_


### Lista de chamadas simplificada:
Caso o arquivo da lista tenha o layout simplificado, use o algoritmo 'fuvest_simplificado.py'.
Para usá-lo, basta invocar 
```bash
python fuvest_simplificado.py C://caminho/para/o/arquivo/fuvest_aprovados.pdf -f "Instituto de Matemática e Estatística - USP" -f "Outra escola opcional"
```

Também é possível rodar o script através de um link direto do arquivo PDF, como por exemplo:
```bash
python fuvest_simplificado.py https://www.fuvest.br/wp-content/uploads/2021/02/fuvest_aprovados.pdf -f "Instituto de Matemática e Estatística - USP" -f "Outra escola opcional"
```