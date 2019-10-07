# Trabalho

## Práticas inicias

- [x] A cada meio segundo uma fruta deve ser adicionada no tabuleiro. (A snake que "comer", ou seja passar com a cabeça por cima de, uma fruta, ganha 1 ponto e cresce uma unidade.
- [x] Uma snake é destruida se colodir com partes de outra snake (inclusive partes dela mesma).
- [x] Uma vez destruída a snake deve ser removida do tabuleiro. A quantidade de pontos da snake destruída deve ser revertida em frutas que devem aparecer imediatamente no tabuleiro.
- [x] As snakes não são destruídas se colidirem com o final do tabuleiro, elas
devem ser transportadas para a outra extremidade. Como se o tabuleiro fosse
circular.
- [x] As snakes se movem automaticamente na direção do último comando de movimento recebido
	- Os comandos de movimento possíveis são iguais às teclas direcionais
do teclado (cima, baixo, esquerda, direita)
	- As snakes não se movem na diagonal
- [ ] Servidor em processo separado, responsável por por guardar as informações a
respeito dos jogadores, o estado do tabuleiro, a contagem de pontos e a implementação das regras listadas acima.
- [ ] O servidor deve enviar para os cliente o estado do tabuleiro e o estado do jogo para aquele cliente específico, sempre que houver alguma modificação. O servidor também deve receber informações dos clientes a respeito dos comandos do
teclado ou novas conexões.
- [ ] Os clientes devem desenhar uma tela inicial com um botão “conectar” e algum
campo que permita ao usuário preencher com o IP do servidor. Após conectado o cliente deve desenhar o tabuleiro atual recebido pelo servidor e enviar teclas pressionadas pelo usuário se sua cobrinha ainda estiver ativa.

## Cenários a serem implementados

À parte da implementação do jogo, o objetivo deste trabalho é focar no
gerenciamento de IO. Como vimos, o gerenciamento é feito a nível de software(SO) de
três formas distintas: Programada, Orientada à Interrupção e Orientada a DMA. A grande
diferença entre os três casos está no envolvimento da CPU, ou elemento processamento
central nas operações de I/O.
Para simular essas três técnicas e os problemas envolvidos com I/O, podemos
pensar no cenário da Figura 2-B, considerando que o servidor é a CPU e os clientes

representam os dispositivos e usuários a fim de realizar operações de IO. As tarefas
relacionadas com a lógica do jogo representam processamento de dados enquanto tarefas
relacionadas com recebimento e envio de IO advindas dos clientes representam IO =).
O objetivo do gerenciamento de I/O é garantir que a CPU passe o mais tempo
possível fazendo processamento de dados do que esperando I/O ou tratando I/O, para
simular esse comportamento implementaremos três cenários no servidor:

### Cenário 1 - I/O programda

Nesse cenário o servidor deve configurar os sockets de forma não bloqueante e
deve tratar todas as entradas, saídas e processamento em uma thread única:

- [ ] Implemente uma forma de medir quanto tempo o servidor passou processando IO e
quanto tempo ele passou processando a lógica de jogo.
- [ ] Plote, no relatório, um gráfico com os tempos medidos e discuta a respeito dos valores respondendo as seguintes perguntas: Qual a relação entre o tempo de I/O e processamento? Por que o tempo que o servidor gastou em I/O é relevante para o
jogo?

### Cenário 2 - I/O orientada à interrupção

Neste cenário, o servidor é dividido em 2 threads, uma para gerenciar as mensagens
vindas dos clientes conectados e a thread principal fica responsável por processar a lógica do jogo. Assim o servidor deve configurar o socket de servidor de forma não bloqueante e criar uma thread que se responsabilize por gerenciar os sockets e as mensagens vindas de cada cliente. Sempre que houver alguma mensagem vinda de um cliente a thread deve processar a mensagem e enviar para principal para que seja tratada, no entanto, quando quiser enviar o estado do tabuleiro a thread principal deve usar o socket diretamente.

- [ ] Implemente uma forma de medir quanto tempo a thread principal passou
processando IO, nesse caso só no envio de informações, e quanto tempo ela passou
processando a lógica de jogo.
- [ ] Plote, no relatório, um gráfico com os tempos medidos e discuta a respeito dos valores respondendo as seguintes perguntas: Qual a relação entre o tempo de I/O e processamento? Qual a relação entre esse gráfico e o gráfico do Cenário 1? Qual a
vantagem, se existir, de usar essa abordagem em relação à abordagem usada no
cenário 1?

### Cenário 3 - I/O orientada à DMA

Claramente não haverá um controlador de DMA para realizar o trabalho de IO para nós, no entanto podemos simular o comportamento do controlador de DMA através de threads. Este cenário põe na thread do cenário 2 a possibilidade de gerenciar também os envios de mensagem. Para fazer isso reimplemente a thread de processamento de IO para que a thread principal possa controlar quando os dados precisam ser enviados.

- [ ] Nesse caso a thread principal não perde tempo enviando ou recebendo dados, porém
ela precisa adicionar alguma lógica de espera relacionada com I/O, pois a thread
principal não pode continuar enquanto os clientes ainda não receberam todo o
tabuleiro. Para fazer isso a thread de I/O deve avisar à thread principal que o I/O foi
terminado, de alguma forma. Adicione essa lógica de espera e compare a
implementação com as outras duas em termos de complexidade.

# Rodando o projeto

` pipenv install `

` pipenv shell && python snake.py `
