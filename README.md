# Criar um arquivo README.md (ou .readme) com o conteúdo fornecido
readme_content = """
# Coletor e Previsor de Temperatura com OpenWeather e Random Forest

Este projeto coleta dados meteorológicos em tempo real da API **OpenWeather**, armazena em um banco de dados SQLite e permite treinar um modelo de **Random Forest** para prever a temperatura com base em variáveis como sensação térmica, umidade, pressão e velocidade do vento.

## Configurações iniciais

No início do código, definimos algumas configurações importantes:

```python
API_KEY = "SUA_CHAVE_DO_OPENWEATHER"
CITY = "Jandira,BR"
DB_NAME = "weather_data.db"
MODEL_FILE = "model_weather.joblib"
```

- `API_KEY`: Chave da API OpenWeather.
- `CITY`: Cidade para coletar os dados.
- `DB_NAME`: Nome do banco SQLite.
- `MODEL_FILE`: Arquivo onde o modelo de previsão será salvo.

## Banco de Dados (SQLite)

Funções responsáveis por armazenar e recuperar dados do SQLite:

- `criar_tabela()`: Cria a tabela weather caso ela não exista.
- `inserir_dado(dado)`: Insere um registro de dados meteorológicos no banco.
- `obter_dados()`: Recupera todos os dados da tabela em um DataFrame do pandas.

## Coleta de Dados da API OpenWeather

Função: `coletar_dado_tempo_real()`

- Faz uma requisição à API OpenWeather.
- Retorna um dicionário com os dados de temperatura, sensação térmica, umidade, pressão e velocidade do vento.

Exemplo de saída:

```json
{
    "timestamp": "2025-10-07 14:00:00",
    "temperature": 24.5,
    "feels_like": 25.0,
    "humidity": 80,
    "pressure": 1013,
    "wind_speed": 3.5
}
```

## Treinamento do Modelo (Random Forest)

Função: `treinar_modelo()`

- Recupera os dados do banco.
- Usa as colunas:
  - **Entrada (X):** `feels_like`, `humidity`, `pressure`, `wind_speed`
  - **Saída (y):** `temperature`
- Divide os dados em treino e teste (80%/20%).
- Treina o modelo `RandomForestRegressor` e salva no arquivo `.joblib`.
- Mostra a precisão (R²) do modelo no conjunto de teste.

## Previsão de Temperatura

Função: `prever_temperatura(feels_like, humidity, pressure, wind_speed)`

- Carrega o modelo salvo.
- Recebe as variáveis de entrada e retorna a previsão da temperatura.

## Execução principal

- Cria a tabela do banco, se necessário.
- Inicia a coleta de dados da cidade especificada a cada 30 segundos.
- Insere os dados coletados no banco e imprime no console.
- Interrompendo o script (`CTRL+C`) é possível encerrar a coleta e depois treinar o modelo com:

```python
from tech_challenge_openweather import treinar_modelo
treinar_modelo()
```

## Observações

- Substitua `API_KEY` pela sua chave válida do OpenWeather.
- A coleta contínua gera um histórico de dados que permite treinar o modelo com mais precisão.
- O modelo pode ser usado posteriormente para prever temperaturas com base em outras variáveis meteorológicas.
"""

# Salvar o arquivo como .readme (você pode renomear para README.md se quiser)
with open("README.readme", "w", encoding="utf-8") as f:
    f.write(readme_content)

"Arquivo README.readme criado com sucesso!"