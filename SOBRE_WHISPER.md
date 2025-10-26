# <h1 align="center"><font color="gree">🎤 Tudo Sobre o Whisper no Projeto</font></h1>

<font color="pink">Senior Data Scientist.: Dr. Eddy Giusepe Chirinos Isidro</font>

## 🤔 O que é o Whisper?

**Whisper** é um modelo de reconhecimento de fala (Speech-to-Text) criado pela OpenAI que converte áudio em texto com alta precisão.

---

## 🆓 Whisper Open Source vs API Whisper

Existem **DUAS versões** do Whisper:

### 1️⃣ **Whisper Open Source** ← **Você está usando esta!**

```python
import whisper
model = whisper.load_model("base")
result = model.transcribe("audio.wav")
```

**Características:**
- ✅ **100% GRATUITO**
- ✅ **Sem limite de uso**
- ✅ **Não precisa de API Key**
- ✅ **Roda localmente** (offline após download do modelo)
- ✅ **Open source** (código aberto)
- ✅ **99 idiomas suportados** (incluindo português)
- ⚠️ Precisa de FFmpeg instalado
- ⚠️ Usa recursos da sua máquina (CPU/RAM)

**Instalação:**
```bash
pip install openai-whisper
```

**Pacote:** `openai-whisper` (no PyPI)

---

### 2️⃣ **Whisper API** (OpenAI Cloud)

```python
from openai import OpenAI
client = OpenAI(api_key="sk-...")
transcription = client.audio.transcriptions.create(
    model="whisper-1",
    file=audio_file
)
```

**Características:**
- 💰 **Pago** ($0.006 por minuto de áudio)
- 🔑 **Precisa de API Key** da OpenAI
- ☁️ **Roda nos servidores** da OpenAI (precisa de internet)
- ⚡ **Mais rápido** (usa GPUs potentes da OpenAI)
- 🔒 **Comercial** (código fechado)
- ✅ **Multi-idioma** incluindo português

**Instalação:**
```bash
pip install openai
```

**Pacote:** `openai` (SDK oficial)

---

## 🎯 Qual Estamos Usando?

No nosso projeto, usamos o **Whisper Open Source** porque:

1. ✅ **É GRÁTIS** - sem custos de API
2. ✅ **Privacidade** - áudio não sai da sua máquina
3. ✅ **Funciona offline** - após baixar o modelo
4. ✅ **Controle total** - podemos escolher qual modelo usar

---

## 🇧🇷 Suporte a Português

### ✅ **SIM! O Whisper suporta português perfeitamente!**

O Whisper foi treinado em **680,000 horas de áudio** em **99 idiomas**, incluindo:
- 🇧🇷 **Português Brasileiro**
- 🇵🇹 **Português de Portugal**

### Como configuramos no código:

```python
result = model.transcribe(
    audio_file,
    language="pt",  # ← Força reconhecimento em português
    fp16=False,      # Para CPU (não GPU)
)
```

**Por que especificar `language="pt"`?**
- ⚡ **Mais rápido** - não precisa detectar o idioma
- 🎯 **Mais preciso** - foca apenas no português
- 🚫 **Evita erros** - não confunde com espanhol/italiano

---

## 📊 Modelos Disponíveis

O Whisper Open Source tem **5 modelos** com diferentes tamanhos:

| Modelo | Tamanho | RAM Necessária | Velocidade | Precisão | Download |
|--------|---------|----------------|------------|----------|----------|
| `tiny` | ~39M parâmetros | ~1 GB | 🚀 Muito rápida | ⭐⭐ Básica | ~75 MB |
| `base` | ~74M parâmetros | ~1 GB | 🚀 Rápida | ⭐⭐⭐ Boa | ~142 MB |
| `small` | ~244M parâmetros | ~2 GB | 🏃 Média | ⭐⭐⭐⭐ Muito boa | ~466 MB |
| `medium` | ~769M parâmetros | ~5 GB | 🚶 Lenta | ⭐⭐⭐⭐⭐ Excelente | ~1.5 GB |
| `large` | ~1550M parâmetros | ~10 GB | 🐌 Muito lenta | ⭐⭐⭐⭐⭐ Máxima | ~2.9 GB |

### 💡 **Recomendação por uso:**

**Para desenvolvimento/testes:**
- Use `tiny` ou `base` - rápidos e suficientes

**Para uso normal:**
- Use `base` ou `small` - bom equilíbrio

**Para máxima qualidade:**
- Use `medium` ou `large` - se tiver RAM suficiente

**No nosso projeto:**
- **Padrão:** `base` (recomendado)
- **Configurável:** Escolha no sidebar da aplicação!

---

## 🔧 Como Funciona no Nosso Código

### 1. **Carregamento do Modelo**

```python
model = whisper.load_model("base")
```

**O que acontece:**
1. Verifica se o modelo já foi baixado
2. Se não, baixa de: https://openaipublic.azureedge.net/main/whisper/models/
3. Salva em `~/.cache/whisper/`
4. Carrega na memória RAM

**Primeira execução:** Demora mais (download)
**Próximas execuções:** Rápido (modelo já está baixado)

### 2. **Transcrição**

```python
result = model.transcribe(
    audio_path,
    language="pt",
    fp16=False,
)
```

**Parâmetros importantes:**
- `language="pt"` - Força português (mais rápido e preciso)
- `fp16=False` - Usa float32 (necessário para CPU)
- `verbose=False` - Não mostra logs detalhados

**Retorna:**
```python
{
    "text": "Olá, como você está?",
    "segments": [...],  # Detalhes de cada segmento
    "language": "pt"
}
```

### 3. **Fluxo Completo no Chatbot**

```
Usuário fala no microfone
    ↓
streamlit-mic-recorder captura áudio
    ↓
Salva em arquivo temporário .wav
    ↓
FFmpeg processa o áudio
    ↓
Whisper transcreve para texto
    ↓
Limpa arquivo temporário
    ↓
Retorna texto transcrito
```

---

## 🚀 Otimizações Implementadas

### 1. **Cache do Modelo**
```python
# O modelo é carregado apenas uma vez
# Nas próximas chamadas, usa o modelo em memória
model = whisper.load_model("base")
```

### 2. **Idioma Fixo**
```python
# Especificamos português para ser mais rápido
language="pt"
```

### 3. **CPU em vez de GPU**
```python
# fp16=False usa CPU (mais compatível)
fp16=False
```

### 4. **Sem Logs Verbosos**
```python
# Não imprime logs detalhados
verbose=False
```

---

## 📦 Dependências

### Obrigatórias:

1. **openai-whisper** (o modelo)
```bash
pip install openai-whisper
```

2. **FFmpeg** (processamento de áudio)
```bash
# Ubuntu/WSL
sudo apt install ffmpeg

# macOS
brew install ffmpeg

# Windows
# Baixar de: https://www.gyan.dev/ffmpeg/builds/
```

3. **PyTorch** (backend de ML)
```bash
# Instalado automaticamente com openai-whisper
```

### Verificar instalação:

```bash
# Verificar FFmpeg
ffmpeg -version

# Verificar Whisper
python -c "import whisper; print(whisper.__version__)"

# Testar modelo
python -c "import whisper; model = whisper.load_model('tiny'); print('OK!')"
```

---

## 🎛️ Configuração Avançada

### Melhorar Precisão:

```python
result = model.transcribe(
    audio,
    language="pt",
    task="transcribe",  # ou "translate" para traduzir
    temperature=0.0,     # Menos aleatório = mais consistente
    beam_size=5,        # Mais opções = mais preciso (mais lento)
    best_of=5,          # Melhores 5 candidatos
)
```

### Detectar Idioma Automaticamente:

```python
# Não especificar 'language'
result = model.transcribe(audio)  # Detecta automaticamente
detected_language = result["language"]
```

### Usar GPU (se disponível):

```python
model = whisper.load_model("base", device="cuda")
result = model.transcribe(audio, fp16=True)  # Mais rápido com GPU
```

---

## 🔍 Comparação: Whisper vs Outros

| Serviço | Custo | Precisão PT-BR | API Key | Offline |
|---------|-------|----------------|---------|---------|
| **Whisper Open Source** | ✅ Grátis | ⭐⭐⭐⭐⭐ | ❌ Não precisa | ✅ Sim |
| Whisper API | $0.006/min | ⭐⭐⭐⭐⭐ | ✅ Precisa | ❌ Não |
| Google Speech-to-Text | $0.006-0.024/min | ⭐⭐⭐⭐ | ✅ Precisa | ❌ Não |
| Azure Speech | $1/hora | ⭐⭐⭐⭐ | ✅ Precisa | ❌ Não |
| Amazon Transcribe | $0.024/min | ⭐⭐⭐⭐ | ✅ Precisa | ❌ Não |

**Vencedor para nosso caso:** Whisper Open Source! 🏆

---

## 🐛 Problemas Comuns e Soluções

### ❌ `FileNotFoundError: ffmpeg`

**Causa:** FFmpeg não instalado

**Solução:**
```bash
sudo apt install ffmpeg
```

### ❌ `FP16 is not supported on CPU`

**Causa:** Tentando usar FP16 na CPU

**Solução:** Já resolvemos com `fp16=False` no código! ✅

### ❌ Modelo não baixa / demora muito

**Causa:** Conexão lenta ou firewall

**Solução:**
```bash
# Baixar modelo manualmente
python -c "import whisper; whisper.load_model('base')"
```

### ❌ Transcrição incorreta

**Soluções:**
1. Fale mais devagar e claramente
2. Use um microfone melhor
3. Reduza ruído de fundo
4. Tente um modelo maior (`small` ou `medium`)

---

## 📚 Recursos Adicionais

### Documentação Oficial:
- GitHub: https://github.com/openai/whisper
- Paper: https://arxiv.org/abs/2212.04356
- Blog OpenAI: https://openai.com/research/whisper

### Tutoriais:
- [Whisper Documentation](https://github.com/openai/whisper#python-usage)
- [Model Card](https://github.com/openai/whisper/blob/main/model-card.md)

### Alternativas:
- **Faster-Whisper** (até 4x mais rápido): https://github.com/guillaumekln/faster-whisper
- **Whisper.cpp** (C++ port): https://github.com/ggerganov/whisper.cpp

---

## 💡 Dicas Pro

1. **Use modelo pequeno para testes**
   - Desenvolva com `tiny` ou `base`
   - Use `medium` apenas em produção

2. **Cache o modelo**
   - Carregue uma vez e reutilize
   - Não recarregue a cada transcrição

3. **Otimize o áudio**
   - 16kHz de sample rate é suficiente
   - Mono (1 canal) é suficiente
   - Remova silêncio antes/depois

4. **Especifique o idioma**
   - Sempre use `language="pt"` para português
   - É 2-3x mais rápido que detecção automática

5. **Considere Faster-Whisper**
   - Para produção, pode ser 4x mais rápido
   - Mesma precisão, menos recursos

---

## 🎓 Resumo

**Pergunta:** O Whisper precisa de API Key?
**Resposta:** **NÃO!** O Whisper open source não precisa de nenhuma API key.

**Pergunta:** Suporta português do Brasil?
**Resposta:** **SIM!** Suporta perfeitamente com `language="pt"`.

**Pergunta:** É gratuito?
**Resposta:** **SIM!** 100% gratuito, sem limites, sem custos.

**Pergunta:** Funciona offline?
**Resposta:** **SIM!** Após baixar o modelo, funciona totalmente offline.

**Pergunta:** Qual modelo usar?
**Resposta:** 
- **Testes:** `tiny` ou `base`
- **Uso normal:** `base` ou `small`
- **Máxima qualidade:** `medium` ou `large`

---

**Última atualização:** 26/10/2025

