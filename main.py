import os
import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()

# Configurações de conexão
API_KEY = os.getenv("API_KEY")
url = "https://v3.football.api-sports.io/standings"
querystring = {"season": "2024", "league": "71"}
headers = {"x-apisports-key": API_KEY}

print("Iniciando extração de dados...")

# Extração
resposta = requests.get(url, headers=headers, params=querystring)

if resposta.status_code != 200:
    print(f"Erro de conexão: HTTP {resposta.status_code}")
    exit()

dados_json = resposta.json()

if not dados_json.get('response'):
    print("Erro: Dados não encontrados. Verifique a API Key ou parâmetros.")
    exit()

print("Processando e estruturando dados...")

# Transformação
classificacao = dados_json['response'][0]['league']['standings'][0]
linhas_tabela = []

for time_data in classificacao:
    linhas_tabela.append({
        'posicao': time_data['rank'],
        'time': time_data['team']['name'],
        'id_time': time_data['team']['id'],
        'pontos': time_data['points'],
        'jogos': time_data['all']['played'],
        'vitorias': time_data['all']['win'],
        'empates': time_data['all']['draw'],
        'derrotas': time_data['all']['lose'],
        'gols_pro': time_data['all']['goals']['for'],
        'gols_contra': time_data['all']['goals']['against'],
        'saldo_gols': time_data['goalsDiff']
    })

df = pd.DataFrame(linhas_tabela)

# Enriquecimento
df['aproveitamento_pct'] = round((df['pontos'] / (df['jogos'] * 3)) * 100, 2)

# Exportação
arquivo_saida = 'dataset_brasileirao.csv'
df.to_csv(arquivo_saida, index=False, encoding='utf-8')

# Logs de finalização e exibição
colunas_exibicao = ['posicao', 'time', 'pontos', 'saldo_gols', 'aproveitamento_pct']

print("\n--- TOP 4 (G4) ---")
print(df[colunas_exibicao].head(4).to_string(index=False))

print("\n--- CLASSIFICAÇÃO COMPLETA ---")
print(df[colunas_exibicao].to_string(index=False))

print(f"\nPipeline concluído. Arquivo exportado: {arquivo_saida}")

# Estatísticas individuais do clube
time_alvo = "Gremio" 
print(f"\nBuscando estatísticas detalhadas para: {time_alvo}...")

try:
    id_alvo = df.loc[df['time'] == time_alvo, 'id_time'].values[0]
except IndexError:
    print(f"Erro: Time '{time_alvo}' não encontrado no dataset.")
    exit()

url_stats = "https://v3.football.api-sports.io/teams/statistics"
params_stats = {"season": "2024", "league": "71", "team": id_alvo}

resposta_stats = requests.get(url_stats, headers=headers, params=params_stats)

if resposta_stats.status_code == 200:
    stats_json = resposta_stats.json().get('response', {})
    
    if not stats_json:
        print("Dados detalhados indisponíveis para este time.")
    else:
        # Extração defensiva usando .get() para evitar KeyErrors
        maior_vitoria_casa = stats_json.get('biggest', {}).get('wins', {}).get('home', 'N/D')
        clean_sheets = stats_json.get('clean_sheet', {}).get('total', 0)
        sem_marcar = stats_json.get('failed_to_score', {}).get('total', 0)
        penaltis = stats_json.get('penalty', {}).get('scored', {}).get('total', 0)
        
        print(f"\n--- ESTATÍSTICAS: {time_alvo.upper()} ---")
        print(f"Maior vitória em casa: {maior_vitoria_casa}")
        print(f"Jogos sem sofrer gol: {clean_sheets}")
        print(f"Jogos sem marcar: {sem_marcar}")
        print(f"Pênaltis convertidos: {penaltis}")
        print("-" * 35)
else:
    print(f"Falha na API de estatísticas (HTTP {resposta_stats.status_code}).")