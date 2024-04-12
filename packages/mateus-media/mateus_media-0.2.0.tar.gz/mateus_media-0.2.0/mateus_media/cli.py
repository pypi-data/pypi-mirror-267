import typer
from pathlib import Path
from .calcular_medias_mensais import calcular_medias_mensais  # Importe a função corretamente
import pandas as pd  # Importe o pandas

app = typer.Typer()


@app.command()
def calcular_medias(file_path: Path, mes: int):
    """
    Calcula as médias horárias de radiação para um mês específico.

    Parameters:
        file_path (Path): O caminho para o arquivo Excel contendo os dados.
        mes (int): O número do mês desejado (entre 1 e 12).
    """
    try:
        # Chamar a função calcular_medias_mensais
        resultado = calcular_medias_mensais(file_path, mes)
        print(
            'Resultado:', resultado
        )  # Adicione esta linha para imprimir o resultado

        # Verificar se resultado é um DataFrame
        if isinstance(resultado, pd.DataFrame):
            # Exibir os resultados
            print('Médias horárias de radiação para o mês selecionado:')
            print(resultado.to_string(index=False))
        else:
            print('Erro: O resultado não é um DataFrame.')

    except FileNotFoundError as e:
        print(f'Erro: {e}')
        raise typer.Abort()


if __name__ == '__main__':
    app()
