# Automação de Abertura de Preventivas – Field Service (YDUQS)

Script desenvolvido em Python para automatizar a abertura de chamados de **preventiva** no ServiceNow, utilizado pelas equipes de Field Service das faculdades do grupo YDUQS.

## Script

Este script automatiza um processo manual repetitivo de abertura de chamados, garantindo:

* Padronização das informações
* Redução de erros humanos
* Ganho de tempo operacional
* Escalabilidade (abertura em massa)

## Instalação

### 1. Clone o repositório
```
git clone <repo-url>
cd preventiva
```

### 2. Crie um ambiente virtual (recomendado)
```
python -m venv venv
venv\Scripts\activate  # Windows
```

### 3. Instale as dependências
```
pip install -r requirements.txt
```

### 4. Instale o Playwright
```
playwright install
```

### 5. Como executar
```
python main.py
```