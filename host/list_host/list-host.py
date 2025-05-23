import requests
import pandas as pd
import json

# Caminhos dos arquivos
CONFIG_PATH = 'D:/dyna/api/token/relatorio/config.json'  # Caminho do arquivo JSON de configuração
EXCEL_PATH = 'D:/dyna/api/host/list_host/excel/list-host.xlsx'  # Caminho para salvar o arquivo Excel

# Função para carregar configurações do arquivo JSON
def load_config(file_path):
    """Carrega a configuração a partir de um arquivo JSON."""
    try:
        with open(file_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Erro: O arquivo {file_path} não foi encontrado.")
        return {}
    except json.JSONDecodeError:
        print(f"Erro ao decodificar JSON em {file_path}.")
        return {}

# Função para fazer a requisição à API e coletar todas as entidades
def fazer_requisicao_api(url, token):
    """Faz a requisição à API com paginação e retorna todas as entidades."""
    headers = {
        'accept': 'application/json; charset=utf-8',
        'Authorization': f'Api-Token {token}',
    }
    all_entities = []
    next_page_key = None

    while True:
        params = {'nextPageKey': next_page_key} if next_page_key else {'entitySelector': 'type("HOST")'}
        response = requests.get(f'{url}/api/v2/entities', params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            all_entities.extend(data['entities'])
            next_page_key = data.get('nextPageKey')
            if not next_page_key:
                break
        else:
            print(f'Erro {response.status_code}')
            print(f'Erro: {response.text}')
            break

    return all_entities

# Função para processar as entidades coletadas
def processar_entidades(entities):
    """Remove a coluna 'type' do DataFrame."""
    df = pd.json_normalize(entities)
    if 'type' in df.columns:
        df.drop(columns=['type'], inplace=True)
    return df

# Função para salvar os dados no Excel
def salvar_dados_excel(df, file_path):
    """Salva os dados em um arquivo Excel."""
    df.to_excel(file_path, index=False)
    print(f'Dados salvos com sucesso em: {file_path}')

# Função principal
def main():
    print("Iniciando o processo...")

    # Carregar a configuração
    config_data = load_config(CONFIG_PATH)

    if not config_data:
        print("Erro ao carregar a configuração.")
        return

    # Extrair URL e token do JSON
    url = config_data['requests_data'][0]['url']
    token = config_data['requests_data'][0]['token']

    # Fazer a requisição à API e obter todas as entidades
    all_entities = fazer_requisicao_api(url, token)

    # Processar as entidades coletadas
    df = processar_entidades(all_entities)
    print(df)

    # Salvar os dados no Excel
    salvar_dados_excel(df, EXCEL_PATH)

    print('--------- Finalizado -----------.')

if __name__ == "__main__":
    main()
