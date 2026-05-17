# Sistema de Locação de Veículos — Módulo de Locações

Este repositório contém a implementação do módulo de **CRUD e Gerenciamento de Locações de Veículos**, desenvolvido para a disciplina de Linguagem de Programação Orientada a Objetos (LPOO). O projeto expande a estrutura base da locadora usando uma arquitetura em camadas e uma interface gráfica desktop.

## Funcionalidades Implementadas

O gerenciamento de locações foi dividido em duas visões principais:
1. **Tela do Usuário da Locadora:** Focada no dia a dia operacional. Permite fazer novas reservas, registrar a retirada do veículo (locar), realizar devoluções com cálculo automático de diárias e cancelar reservas pendentes.
2. **Tela do Administrador:** Um ambiente de gerenciamento livre (CRUD completo) que permite criar, editar, visualizar e remover qualquer registro para fins de correção de dados e auditoria.

---

## Estrutura do Projeto (MVC + DAO)

O sistema foi estruturado seguindo o padrão **MVC (Model-View-Controller)** com persistência de dados via **DAO (Data Access Object)** no banco de dados PostgreSQL:

### Model (`Locacao`)
Representa a entidade de negócio. Guarda os dados fundamentais do contrato (IDs, veículo, datas e valores) e controla o ciclo de vida da locação através do atributo `status` (mapeado como `enum` com os estados: `"reservado"`, `"locado"`, `"devolvido"` e `"cancelado"`).

### View (Interface Gráfica)
Construída com **Tkinter**. A `JanelaPrincipal` (`tk.Tk`) gerencia a barra de menus do sistema, e todas as outras telas secundárias herdam de `tk.Toplevel`, abrindo como janelas filhas.
- `JanelaLocacaoUsuario`: Tela operacional com a tabela (Treeview) e botões que mudam de acordo com o status da locação.
- `JanelaNovaReserva`: Formulário que filtra e mostra apenas os veículos disponíveis no período escolhido.
- `JanelaListagemLocacoes` & `JanelaCadastroLocacao` (Admin): Telas exclusivas para o administrador manipular os dados livremente.

### Controller (`LocacaoController`)
O intermediário entre a View e o DAO. Cuida de todas as **regras de negócio e validações**, como impedir devoluções de carros que não foram retirados, consistência das datas (início e fim) e a lógica do cálculo financeiro das diárias.

### DAO (`LocacaoDAO`)
Responsável por isolar e executar os comandos SQL no PostgreSQL. Além do CRUD básico herdado de `GenericDAO`, traz a lógica de consulta `buscar_veiculos_disponiveis()`, que garante que um veículo reservado ou locado não apareça como disponível no mesmo período.

---

## Detalhamento de Aprendizado

- **Dificuldades Encontradas:** No início do desenvolvimento, tive problemas para configurar o ambiente virtual (`.venv`) e instalar o gerenciador de pacotes (`pip`) para conectar o driver do PostgreSQL. Na parte de interface, a dificuldade era como organizar as janelas, já que antes eu usava uma janela independente para cada "menu" e a visualização ficava poluída. Entender o comportamento do `tk.Toplevel` e como passar dados corretamente entre as telas também exigiu bastante teste.
  
- **Como resolvi:** Resolvi pesquisando direto na documentação do Tkinter e revisando os exemplos e conceitos passados nas aulas. Estudei a fundo como trabalhar com a barra de menus nativa (`tk.Menu`) para limpar a navegação.
  
- **Principal Aprendizado:** O maior aprendizado foi entender a dependência entre as visões do sistema e como elas se interligam entre si. Foi essencial compreender como a estrutura de menus do Tkinter centraliza o fluxo.

---

## Declaração de Uso de IA

- [ ] **Nenhuma IA foi utilizada** na elaboração deste código.
- [x] **Utilizei IA** como ferramenta de apoio.

- **Ferramenta(s):** Gemini / ChatGPT.
- **Finalidade:** Geração de código repetitivo (*boilerplate*) para acelerar a montagem das telas no Tkinter e auxílio na sintaxe de consultas SQL de data do PostgreSQL.
- **Validação:** Todo o código gerado por IA foi revisado, testado no ambiente local e compreendido antes de ser integrado ao projeto.

---

## Fluxo de Navegação e Hierarquia de Telas

O diagrama abaixo ilustra como as visões se interligam a partir do menu principal da aplicação, respeitando a dependência mútua e a hierarquia do Tkinter (`tk.Tk` ➔ `tk.Toplevel`):

JanelaPrincipal (tk.Tk)
│
├── [ Menu: Cadastro ]
│         │
│         └── Locações (Admin) ➔ JanelaListagemLocacoes (tk.Toplevel)
│                                       │
│                                       └── (Botões: Novo / Editar)
│                                                 │
│                                                 └──➔ JanelaCadastroLocacao (tk.Toplevel) [CRUD Irrestrito] 
│
└── [ Menu: Ação ]
│
└── Locar Veículo ➔ JanelaLocacaoUsuario (tk.Toplevel)
│
└── (Botão: Nova Reserva)
│
└── ➔ JanelaNovaReserva (tk.Toplevel) [Validações de Negócio]


### Ciclo de Sincronização (wait_window)

Quando uma tela de formulário ou ação é aberta, o fluxo funciona da seguinte forma:

1. **Abertura:** A tela de listagem (`JanelaLocacaoUsuario` ou `JanelaListagemLocacoes`) invoca a tela filha de cadastro/reserva como um `tk.Toplevel`.
2. **Bloqueio Retentor:** A tela pai executa o método `self.wait_window(janela_filha)`. Isso congela temporariamente a execução da listagem enquanto o usuário opera no formulário.
3. **Persistência e Fechamento:** O usuário salva os dados (enviando as alterações via `Controller` para o `DAO` no PostgreSQL). Ao terminar, a janela filha se fecha (`destroy`).
4. **Atualização Automática:** Com o fechamento da filha, o bloqueio do `wait_window` é liberado na tela pai, que executa imediatamente o método `self.carregar_dados()`, atualizando a tabela com as informações novas vindas do banco.

---

## Estrutura do Banco de Dados (PostgreSQL)

O sistema utiliza o banco de dados relacional **PostgreSQL** para garantir a persistência e a integridade das informações da locadora.

**Nome do Banco de Dados:** `bd_lpoo_locadora_veiculos`

### Script SQL de Criação das Tabelas

Abaixo está o script utilizado para estruturar o banco de dados, contendo a tabela de veículos e a  tabela de locações, devidamente interligadas por chave estrangeira:

```sql

CREATE TABLE tb_veiculos (
    vei_id           SERIAL PRIMARY KEY,
    vei_placa        CHAR(7) UNIQUE NOT NULL,
    vei_categoria    VARCHAR(20) NOT NULL,
    vei_taxa_diaria  NUMERIC(10, 2) NOT NULL,
    vei_estado_atual VARCHAR(20),
    vei_tipo         VARCHAR(20) NOT NULL
);

CREATE TABLE tb_locacoes (
    loc_id           SERIAL PRIMARY KEY,
    loc_veiculo      CHAR(7) NOT NULL,
    loc_data_in      DATE NOT NULL,
    loc_data_fim     DATE,
    total_diarias    INT NOT NULL,
    valor_total      DECIMAL(10, 2) NOT NULL,
    status           VARCHAR(20) NOT NULL, 
    FOREIGN KEY (loc_veiculo) REFERENCES tb_veiculos(vei_placa)
);