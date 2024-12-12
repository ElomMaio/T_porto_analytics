import pandas as pd
import json
import re
import os
from pathlib import Path
BASE_DIR = Path(os.getcwd())


# Abrir e carregar o arquivo JSON
with open('todos_os_processos.json', encoding='UTF-8') as f:
    data = json.load(f)

# Construir a estrutura tabular com iteração
data_tabular = []
for item in data:
    tipo_animal = item.get('Tipo_de_animal', ['Não especificado'])
    tipo_procedimento = item.get('Tipo_de_procedimento', ['Não especificado'])
    artigos_infringidos = item.get('Artigos_infringidos', ['Não especificado'])
    documentos_elaborados = item.get('Documentos_elaborados', ['Não especificado'])
    categorias = item.get('Categoria', ['Não especificado'])

    for animal in tipo_animal:
        for procedimento in tipo_procedimento:
            for artigo in artigos_infringidos:
                for documento in documentos_elaborados:
                    for categoria in categorias:
                        n_processo = re.sub(r"[^\d/-]+", "", item.get('Numero_processo_etico', ''))
                        if not n_processo:
                            n_processo = 'Não especificado'
                        n_processo = n_processo[1::] if n_processo.startswith('-') else n_processo
                        data_tabular.append({
                            'numero_processo': n_processo,
                            'denunciante': item.get('Denunciante', 'Não especificado'),
                            'motivacao_denuncia': item.get('Motivacao_da_denuncia', 'Não especificado'),
                            'categoria': categoria,
                            'falha_profissional': item.get('Falha_profissional', 'Não especificado'),
                            'procedencia': item.get('Procedencia', 'Não especificado'),
                            'procedencia_mantida': item.get('Procedencia_mantida', 'Não especificado'),
                            'tipo_animal': animal,
                            'tipo_procedimento': procedimento,
                            'artigo_infringido': artigo,
                            'documento_elaborado': documento
                        })

# Criar o DataFrame
df = pd.DataFrame(data_tabular)

# Filtrar processos procedentes
df_procedentes = df[df['procedencia'] == True]
df_procedentes.to_csv(BASE_DIR / 'procedentes.csv', index=True, encoding='utf-8')
