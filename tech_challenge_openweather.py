import requests
import sqlite3
import pandas as pd
import time
from datetime import datetime
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from joblib import dump, load
import os

# =====================================
# CONFIGURAÇÕES INICIAIS
# =====================================
API_KEY = "28ad8aebfb25d0a0982d26846808f831"  # sua chave do OpenWeather
CITY = "Jandira,BR"
DB_NAME = "weather_data.db"
MODEL_FILE = "model_weather.joblib"


# =====================================
# FUNÇÕES DE BANCO DE DADOS
# =====================================
def criar_tabela():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS weather (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            temperature REAL,
            feels_like REAL,
            humidity REAL,
            pressure REAL,
            wind_speed REAL
        )
    """)
    conn.commit()
    conn.close()


def inserir_dado(dado):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO weather (timestamp, temperature, feels_like, humidity, pressure, wind_speed)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        dado["timestamp"],
        dado["temperature"],
        dado["feels_like"],
        dado["humidity"],
        dado["pressure"],
        dado["wind_speed"]
    ))
    conn.commit()
    conn.close()


def obter_dados():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM weather ORDER BY id ASC", conn)
    conn.close()
    return df


# =====================================
# COLETA DE DADOS DA API OPENWEATHER
# =====================================
def coletar_dado_tempo_real():
    url = f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric"
    resposta = requests.get(url)
    dados = resposta.json()

    # --- tratamento de erros ---
    if resposta.status_code != 200 or "main" not in dados:
        print("❌ Erro ao coletar dados do OpenWeather:")
        print("Código HTTP:", resposta.status_code)
        print("Mensagem:", dados.get("message", "Resposta inesperada"))
        return None
    # ----------------------------

    dado = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "temperature": dados["main"]["temp"],
        "feels_like": dados["main"]["feels_like"],
        "humidity": dados["main"]["humidity"],
        "pressure": dados["main"]["pressure"],
        "wind_speed": dados["wind"]["speed"]
    }
    return dado


# =====================================
# TREINAMENTO DO MODELO
# =====================================
def treinar_modelo():
    df = obter_dados()
    if len(df) < 10:
        print("⚠️ Poucos dados para treinar o modelo. Colete mais informações primeiro.")
        return

    X = df[["feels_like", "humidity", "pressure", "wind_speed"]]
    y = df["temperature"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    modelo = RandomForestRegressor(n_estimators=100, random_state=42)
    modelo.fit(X_train, y_train)

    score = modelo.score(X_test, y_test)
    dump(modelo, MODEL_FILE)

    print(f"✅ Modelo treinado com sucesso! Precisão (R²): {score:.3f}")


# =====================================
# PREVISÃO DE TEMPERATURA
# =====================================
def prever_temperatura(feels_like, humidity, pressure, wind_speed):
    if not os.path.exists(MODEL_FILE):
        print("⚠️ Modelo ainda não treinado. Execute a função treinar_modelo() primeiro.")
        return None

    modelo = load(MODEL_FILE)
    entrada = pd.DataFrame([[feels_like, humidity, pressure, wind_speed]],
                           columns=["feels_like", "humidity", "pressure", "wind_speed"])
    previsao = modelo.predict(entrada)[0]
    return previsao


# =====================================
# EXECUÇÃO PRINCIPAL
# =====================================
if __name__ == "__main__":
    criar_tabela()

    print("=== COLETOR DE DADOS DO OPENWEATHER ===")
    print(f"Coletando dados de {CITY} a cada 30 segundos (CTRL+C para parar)...\n")

    try:
        while True:
            dado = coletar_dado_tempo_real()
            if dado:
                inserir_dado(dado)
                print(f"[{dado['timestamp']}] 🌡 Temp: {dado['temperature']}°C | "
                      f"Sensação: {dado['feels_like']}°C | Umidade: {dado['humidity']}%")
            time.sleep(30)
    except KeyboardInterrupt:
        print("\n🛑 Coleta finalizada. Agora você pode treinar o modelo executando:")
        print(">>> from tech_challenge_openweather import treinar_modelo")
        print(">>> treinar_modelo()")