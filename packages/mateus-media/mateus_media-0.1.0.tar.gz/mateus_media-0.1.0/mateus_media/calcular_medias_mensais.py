import pandas as pd


def calcular_medias_mensais(file_path_radiacoes, mes):
    """
    Calcula as médias horárias de radiação para um mês específico.

    Parameters:
        file_path_radiacoes (str): O caminho para o arquivo Excel contendo os dados.
        mes (int): O número do mês desejado (entre 1 e 12).

    Returns:
        pandas.DataFrame: DataFrame contendo as médias horárias de radiação.

    Raises:
        FileNotFoundError: Se o caminho do arquivo especificado não for encontrado.

    Examples:
        >>> calcular_medias_mensais('dados_de_média.xlsx', 3)
    """
    # Carregar os dados do arquivo Excel
    df = pd.read_excel(file_path_radiacoes)

    # Preencher valores nulos na coluna 'radiacao' com a média da coluna
    df['radiacao'] = df['radiacao'].fillna(df['radiacao'].mean())

    # Filtrar o DataFrame para o mês especificado pelo usuário
    df_mes = df[df['data'].dt.month == mes]

    # Criar um DataFrame vazio para armazenar as médias horárias de todos os dias do mês
    media_horaria_mes = pd.DataFrame(
        columns=['data', 'hora', 'média da radiação']
    )

    # Iterar sobre todos os dias do mês
    dias_do_mes = df_mes['data'].dt.day.unique()

    for dia in dias_do_mes:
        df_dia = df_mes[df_mes['data'].dt.day == dia]
        media_horaria_dia = (
            df_dia.groupby('hora')['radiacao'].mean().reset_index()
        )
        media_horaria_dia['data'] = df_dia['data'].iloc[0].strftime('%d/%m')
        media_horaria_mes = pd.concat(
            [
                media_horaria_mes,
                media_horaria_dia.rename(
                    columns={'radiacao': 'média da radiação'}
                ),
            ]
        )

    # Retornar o DataFrame com as médias horárias
    return media_horaria_mes
