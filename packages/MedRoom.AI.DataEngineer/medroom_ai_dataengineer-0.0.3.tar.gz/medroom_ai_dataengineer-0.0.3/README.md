# MedRoom.AI.DataEngineer

O `MedRoom.AI.DataEngineer` é um pacote que encapsula funções comuns e genéricas, proporcionando uma solução padronizada para o pré-processamento de texto e avaliação de modelos de Machine Learning.

## :arrow_down: Instalação

#### Instalar o Pacote
```bash
!pip install MedRoom.AI.DataEngineer
```

## :book: Uso 

### :one: Pré-processamento de Texto 

#### Importar Bibliotecas Necessárias
```python
import nltk
import spacy

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('rslp')
spacy.cli.download("pt_core_news_sm")
```

#### Utilizando o Pré-processador de Texto
```python
from medroom.dna.processors.utils.textclean import TextPreprocessor

preprocessor = TextPreprocessor()
text = "Exemplo de não texto para preprocessamento classificação ando!"
processed_text = preprocessor.preprocess_text(text, use_lemmatization=True, use_stemming=False)

print(processed_text)
```

### :two: Avaliação de Modelos de Machine Learning

#### Importar e Usar a Classe de Avaliação
```python
from medroom.dna.processors.utils.evalmetrics import ModelEvaluator

# Suponha que `predictions` e `y_test` são suas predições e rótulos reais, respectivamente.
evalmetrics = ModelEvaluator()
```

#### Métricas de Avaliação Disponíveis

- **Acurácia**
  ```python
  evalmetrics.accuracy(y_test, predictions)
  ```
  
- **Relatório de Classificação**
  ```python
  evalmetrics.classification_report(y_test, predictions)
  ```
  
- **ROC-AUC**
  ```python
  evalmetrics.roc_auc(y_test, predictions)
  ```
  
- **Matriz de Confusão**
  ```python
  evalmetrics.confusion_matrix(y_test, predictions)
  ```
  
## :notebook: Tutorial Interativo

Para um aprendizado mais prático e interativo, oferecemos um tutorial em formato de Jupyter Notebook. Ele guia você através do uso prático das classes e funções disponíveis no `MedRoom.AI.DataEngineer`, abrangendo desde o pré-processamento de texto até a avaliação do modelo.

- [Acesse o Tutorial Interativo](https://github.com/MedRoomGitHub/MedRoom.AI.Notebooks/blob/develop/Tutoriais/Sprint11_MedRoomAIDataEngineer.ipynb)

Baixe o notebook e execute-o localmente, ou explore-o diretamente no GitHub para uma compreensão aprofundada das funcionalidades disponíveis no pacote `MedRoom.AI.DataEngineer`.

## :wrench: Como Adicionar Novas Funções Utilitárias

#### 1. **Crie um novo arquivo `.py`**:
   - No diretório `/MedRoom.AI.DataEngineer/medroom/dna/processors/utils/`, crie um novo arquivo `.py` para a sua função. Por exemplo, para uma função de visualização de dados, você pode criar um arquivo chamado `dataviz.py`.

#### 2. **Importe as bibliotecas necessárias**:
   - No início do seu arquivo, importe todas as bibliotecas e pacotes necessários. Isso pode variar dependendo da função que você está implementando.

#### 3. **Estruture sua classe**:
   - Defina uma classe principal para encapsular suas funções. Dentro dessa classe, você pode criar métodos estáticos para cada função utilitária.
   - Se possível, siga a convenção de nomeação e estrutura do arquivo `evalmetrics.py`.

#### 4. **Escreva sua função**:
   - Dentro da classe, defina sua função utilitária como um método estático.
   - Adicione documentação (docstrings) para sua função, explicando brevemente o que ela faz, seus parâmetros e o que ela retorna.
   - Garanta que sua função segue os padrões e práticas de codificação do repositório.

#### 5. **Teste sua função**:
   - Antes de finalizar, teste sua função para garantir que ela funcione conforme o esperado.

#### 6. **Adicione dependências (se necessário)**:
   - Se sua função utilitária requer bibliotecas ou pacotes adicionais, adicione-os ao arquivo `requirements.txt` para garantir que os usuários possam instalá-los facilmente.

#### 7. **Atualize o README**:
   - Adicione uma breve descrição e um exemplo de uso da sua nova função utilitária ao README do repositório para ajudar outros desenvolvedores a entender e usar sua função.

#### 8. **Crie o arquivo `.whl`**:
   - Após fazer todas as modificações e adições necessárias, gere o novo arquivo `.whl` executando o seguinte comando no terminal:
   ```bash
   python setup.py sdist bdist_wheel
   ```

## :rocket: Configuração e Upload para o PyPI

Se você é um colaborador e deseja enviar uma nova versão do `MedRoom.AI.DataEngineer` para o PyPI, siga os passos abaixo:

### 1. **Preparação do Pacote**:
   Empacote seu código para distribuição usando:
   ```bash
   python setup.py sdist bdist_wheel
   ```

### 2. **Instalação do Twine**:
   Se você ainda não tem o Twine instalado, adicione-o ao seu ambiente. O Twine é uma ferramenta indispensável para publicar pacotes Python no PyPI:
   ```bash
   pip install twine
   ```

### 3. **Upload para o PyPI**:
   Com o Twine instalado, você pode carregar facilmente seu pacote no PyPI:
   ```bash
   twine upload dist/*
   ```
   Nota: Para fazer o upload no PyPI, é necessário fornecer um nome de usuário e senha. Se você tiver a autenticação de dois fatores (2FA) ativada para sua conta no PyPI, precisará usar um Token de API em vez de sua senha habitual. Para mais detalhes sobre as credenciais e outras informações relacionadas, consulte nossa [documentação no Notion](https://www.notion.so/MedRoom-AI-DataEngineer-5d3ea0613d0b411795496fbc8319fa09).

### 4. **Instalação a partir do PyPI**:
   Depois de publicar seu pacote no PyPI, ele pode ser instalado em qualquer ambiente usando:
   ```bash
   !pip install MedRoom.AI.DataEngineer
   ```
