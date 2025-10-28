# <h1 align="center"><font color="gree">AI Job Interviewer with CrewAI</font></h1>

<font color="pink">Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro</font>


Neste repositório você poderá treinar para sua próxima entrevista com o poder dos sistemas multiagentes. Este estudo está baseado no tutorial de [The Neural Maze: Miguel Otero Pedrido]() e do [Alessandro Romano]().

![](https://substackcdn.com/image/fetch/$s_!xENR!,f_auto,q_auto:good,fl_progressive:steep/https%3A%2F%2Fsubstack-post-media.s3.amazonaws.com%2Fpublic%2Fimages%2Fde2d6a82-0559-47aa-af9b-e145c36df538_1536x1024.png)

## <font color="red">✨ Funcionalidades</font>

- 🤖 **Entrevista Interativa com IA** usando CrewAI
- 🎤 **Reconhecimento de Voz** com Whisper (Open Source)
- 💬 **Interface Amigável** com Streamlit
- 🇧🇷 **Suporte completo ao Português Brasileiro**
- 🎯 **Perguntas Personalizadas** por empresa e cargo
- 📊 **Avaliação Automática** das suas respostas
- 🔄 **Perguntas de Follow-up** baseadas nas suas respostas
- 🆓 **100% Gratuito** - sem custos de API para reconhecimento de voz

## <font color="red">🎤 Reconhecimento de Voz</font>

Este projeto usa **Whisper Open Source** da OpenAI para converter sua voz em texto:

- ✅ **GRATUITO** - sem custos de API
- ✅ **Sem limites de uso**
- ✅ **Não precisa de API Key do Whisper**
- ✅ **Funciona offline** (após download do modelo)
- ✅ **Português Brasileiro** perfeitamente suportado
- ✅ **Modelos configuráveis** (tiny, base, small, medium, large)

📖 **Leia mais:** [SOBRE_WHISPER.md](SOBRE_WHISPER.md)

## <font color="red">🚀 Instalação Rápida</font>

### Pré-requisitos Essenciais:

1. **FFmpeg** (obrigatório para reconhecimento de voz):
```bash
sudo apt update && sudo apt install -y ffmpeg
```

2. **Dependências Python**:
```bash
uv sync
```

3. **Executar a aplicação**:
```bash
streamlit run chatbot_ui.py --server.address localhost
```

📖 **Guias completos:**
- [INSTALACAO_RAPIDA.md](INSTALACAO_RAPIDA.md) - Setup completo passo a passo
- [SOLUCAO_PROBLEMAS_MICROFONE.md](SOLUCAO_PROBLEMAS_MICROFONE.md) - Troubleshooting do microfone
- [SOBRE_WHISPER.md](SOBRE_WHISPER.md) - Tudo sobre reconhecimento de voz

---

## <font color="red">🛠️ Ferramentas de Desenvolvimento</font>

Neste projeto utilizamos **Ruff** para linting/formatação e **pdbp** para debugging, garantindo código limpo e de alta qualidade.


### <font color="blue">Instalação</font>

As ferramentas de desenvolvimento já estão configuradas no `pyproject.toml`. Para instalá-las, siga os passos abaixo:

```bash
# Para instalar elas no pyproject.toml:
uv add --dev ruff pdbp black

# Instalar dependências de desenvolvimento (quando já tiver no pyproject.toml)
uv sync --group dev
```

Isso instalará:
- `ruff>=0.9.3` - Linter e formatter super rápido
- `pdbp>=1.6.1` - Debugger melhorado
- `black>=25.9.0` - Formatter alternativo


## <font color="red"> Ruff - Linter e Formatter</font>

### <font color="blue">O que é o Ruff?</font>

**``Ruff``** é um linter e formatter para ``Python`` extremamente rápido (escrito em ``Rust``), que substitui várias ferramentas:

- ✅ `flake8` (linting)
- ✅ `black` (formatação)
- ✅ `isort` (organização de imports)
- ✅ `pylint` (análise de código)

**Vantagem:** 10-100x mais rápido que as ferramentas tradicionais!

### <font color="blue">Comandos Principais</font>

| Comando | Descrição |
|---------|-----------|
| `uv run ruff check .` | Verifica problemas no código |
| `uv run ruff check . --fix` | Corrige problemas automaticamente |
| `uv run ruff format .` | Formata todo o código |
| `uv run ruff check arquivo.py` | Verifica um arquivo específico |
| `uv run ruff check . --watch` | Monitora mudanças em tempo real |
| `uv run ruff format arquivo.py` | Formata um arquivo específico |



### <font color="blue">Quando Usar?</font>

**Durante o desenvolvimento:**
```bash
# Antes de fazer commit:
uv run ruff check . --fix    # Corrigir problemas
uv run ruff format .          # Formatar código
```

**Em CI/CD:**
```bash
# Verificar se o código está limpo:
uv run ruff check .
```

**Workflow recomendado:**
```bash
# 1. Verificar problemas:
uv run ruff check .

# 2. Corrigir automaticamente o que for possível:
uv run ruff check . --fix

# 3. Formatar código:
uv run ruff format .

# 4. Verificar novamente:
uv run ruff check .
```


### <font color="blue">Exemplo de Uso</font>

**Antes de executar o Ruff:**
```python
import os
import sys
from crewai import Agent, Task  # Imports desorganizados
def minha_funcao( x,y ):  # Formatação ruim
    if x>y:return x  # Sem espaços
```

**Depois de executar `uv run ruff format .` e `uv run ruff check . --fix`:**
```python
import os
import sys

from crewai import Agent, Task  # Imports organizados

def minha_funcao(x, y):  # Formatação correta
    if x > y:  # Espaçamento adequado
        return x
```


### <font color="blue">Regras de Linting (Códigos)</font>

O **``Ruff``** verifica seu código usando diferentes conjuntos de regras. Cada letra representa um grupo:

| Código | Nome | O que verifica |
|--------|------|----------------|
| **``E``** | pycodestyle errors | Erros de estilo (espaçamento, indentação) |
| **``F``** | Pyflakes | Erros de lógica (variáveis/imports não usados) |
| **``I``** | isort | Organização e ordenação de imports ``uv run ruff check chatbot_ui.py --select I --fix`` | 
| **``N``** | pep8-naming | Convenções de nomes (snake_case, PascalCase) |
| **``W``** | pycodestyle warnings | Avisos de estilo menos críticos |
| **``B``** | flake8-bugbear | Bugs comuns e armadilhas do Python |
| **``C4``** | flake8-comprehensions | Melhorias em list/dict comprehensions |
| **``UP``** | pyupgrade | Sintaxe moderna do Python |
| **``PL``** | Pylint | Análise de código avançada |
| **``RUF``** | Ruff-specific | Regras específicas do Ruff |

**Exemplo de erros comuns:**
- **``F401``**: Import não utilizado
- **``E501``**: Linha muito longa (>120 caracteres)
- **``W292``**: Falta linha vazia no final do arquivo
- **``I001``**: Imports desorganizados


### <font color="blue">Configuração do Ruff</font>

#### <font color="yellow">``Opção 1:`` Arquivo separado `ruff.toml` (usado neste projeto)</font>

**Criação:** O arquivo `ruff.toml` é criado **manualmente** na raiz do projeto.

**Estrutura do arquivo:**
```toml
# Python version
target-version = "py310"

# Line length
line-length = 120

# Exclude directories
exclude = [
    ".git",
    ".ruff_cache",
    ".venv",
    "build",
    "dist",
]

# Linting rules
[lint]
select = ["E", "F", "I", "N", "W", "B", "C4", "UP", "PL", "RUF"]
```

**No `pyproject.toml`, adicione:**
```toml
[tool.ruff]
extend = "ruff.toml"
```

#### <font color="yellow">``Opção 2:`` Tudo no `pyproject.toml` (alternativa mais simples)</font>

Se preferir ter tudo em um arquivo, coloque no ``pyproject.toml``:

```toml
[tool.ruff]
line-length = 120
target-version = "py310"
exclude = [".git", ".venv", "build", "dist"]

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "B", "C4", "UP", "PL", "RUF"]
```

#### <font color="yellow">O que acontece sem configuração?</font>

Se você **não criar** arquivo de configuração, o ``Ruff`` funciona com padrões:
- `line-length = 88` (padrão do ``Black``)
- Apenas regras básicas (`E`, `F`)
- Funciona perfeitamente, mas menos customizado


### <font color="blue">📏 Tamanho de Linha Recomendado</font>

| Tamanho | Contexto | Quando usar |
|---------|----------|-------------|
| **``79``** | PEP 8 tradicional | Padrão antigo |
| **``88``** | Black (padrão) | Open-source, padrão moderno |
| **``100-105``** | Moderado | Projetos pessoais |
| **``120``** | Google Style | **Recomendado** - bom equilíbrio ⭐ |
| **``140+``** | Liberal | Apenas para monitores grandes |

**Neste projeto usamos `120` caracteres** - um bom equilíbrio entre legibilidade e praticidade.


## <font color="red">🐛 pdbp - Python Debugger Plus</font>

### <font color="blue">O que é o pdbp?</font>

**``pdbp``** é uma versão melhorada do debugger padrão do Python (``pdb``), com:

- ✅ Syntax highlighting colorido
- ✅ Autocompletar comandos
- ✅ Interface mais amigável
- ✅ Melhor visualização de variáveis


### <font color="blue">Como Usar</font>

**1. Adicionar breakpoint no código:**
```python
import pdbp

def my_function(x, y):
    result = x + y
    pdbp.set_trace()  # ⬅️ Pausa aqui para debug
    return result
```

**2. Comandos úteis durante debug:**
| Comando | Descrição |
|---------|-----------|
| `n` (next) | Próxima linha |
| `s` (step) | Entrar na função |
| `c` (continue) | Continuar até próximo breakpoint |
| `p variavel` | Imprimir valor da variável |
| `l` (list) | Mostrar código ao redor |
| `q` (quit) | Sair do debugger |
| `h` (help) | Ajuda |


### <font color="blue">Exemplo Prático de Debugging</font>

```python
import pdbp
from crewai import Agent, Task

def processar_resposta(resposta: str) -> dict:
    print("Processando resposta...")
    
    # Adicionar breakpoint para investigar
    pdbp.set_trace()  # ⬅️ Debugger pausa aqui
    
    resultado = {
        "texto": resposta,
        "tamanho": len(resposta)
    }
    return resultado

# Executar
resposta = processar_resposta("Minha resposta da entrevista")
```

**Quando executar, você verá:**
```
> /path/to/file.py(8)processar_resposta()
-> resultado = {
(Pdbp) p resposta          # Ver valor da variável
'Minha resposta da entrevista'
(Pdbp) n                   # Próxima linha
(Pdbp) p resultado         # Ver resultado
{'texto': 'Minha resposta da entrevista', 'tamanho': 30}
```


### <font color="blue">Alternativa Moderna: `breakpoint()`</font>

Python 3.7+ tem suporte nativo a ``breakpoint()``:

```python
def my_function(x, y):
    result = x + y
    breakpoint()  # ⬅️ Usa pdbp automaticamente se instalado
    return result
```

**Vantagem:** Não precisa importar, funciona automaticamente com ``pdbp``!


## <font color="red">🚀 Checklist de Qualidade de Código</font>

Antes de fazer commit, execute:

- `uv run ruff check . --fix` - Corrigir problemas automaticamente
- `uv run ruff format .` - Formatar código
- `uv run ruff check .` - Verificar se tudo está OK
- Remover todos os `pdbp.set_trace()` do código e os `breakpoint()`
- Testar o código se está funcionando corretamente

---

``NOTA IMPORTANTE:`` 

Use melhor o ``breakpoint()`` para debugging, pois é mais moderno e tem mais features. Para usar o breacpoint() você não precisa importar nada, porque ele é nativo do Python.




Thank God!