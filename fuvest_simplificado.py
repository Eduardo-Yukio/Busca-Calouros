import typer
import re
import pandas as pd
import io
from pypdf import PdfReader
from typing import List
from rich.console import Console
from rich.text import Text
from tqdm import tqdm

app = typer.Typer()
console = Console()


def parse_page(page_text: list[str], data: list[tuple[str, str, str]]):
    """Extrai os cursos, escolas e nomes de alunos da página."""
    curso = None
    escola = None

    for i, t in enumerate(page_text):
        if t[0].isalpha():
            curso_potencial = t
            escola_potencial = page_text[i + 1] if i + 1 < len(page_text) else None

            if escola_potencial and escola_potencial[0].isalpha():
                escola = escola_potencial
                curso = curso_potencial
                continue

        # Remove o CPF e a numeração do começo
        t = re.sub(r"^\d{1,3}(?:\.\d{3})*", "", t).strip()
        if t:
            data.append((curso, escola, t))


def load_pdf(file_path: str) -> PdfReader:
    """Carrega um PDF de um caminho local ou URL."""
    if file_path.startswith("http"):
        try:
            import requests
        except ImportError:
            console.print(
                "[bold red]Para baixar PDFs de URLs, instale o pacote requests:[/bold red] pip install requests"
            )
            raise typer.Exit(1)

        try:
            console.print(f"[cyan]Baixando PDF de {file_path}...[/cyan]")
            response = requests.get(file_path, stream=True, timeout=15)
            response.raise_for_status()

            total_size = int(response.headers.get("content-length", 0))
            chunk_size = 1024  # 1KB
            pdf_file = io.BytesIO()

            with tqdm(
                total=total_size, unit="B", unit_scale=True, desc="Download", ncols=80
            ) as bar:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    pdf_file.write(chunk)
                    bar.update(len(chunk))
            console.print("[green]Download concluído! Processando...[/green]")
            return PdfReader(pdf_file)

        except requests.RequestException as e:
            console.print(f"[bold red]Erro ao baixar o PDF:[/bold red] {e}")
            raise typer.Exit(1)
    else:
        try:
            return PdfReader(file_path)
        except Exception as e:
            console.print(f"[bold red]Erro ao abrir o arquivo:[/bold red] {e}")
            raise typer.Exit(1)


def trata_filtros(filtros: List[str]) -> List[str]:
    """Troca o caracter '-', geralmente usado no nome do curso ou na escola, por '−' (U+2212) que é o caracter de fato usado no PDF."""
    return [f.replace("-", "−") for f in filtros]


@app.command()
def extrair_nomes(
    file_path: str = typer.Argument(..., help="Caminho do arquivo PDF ou URL"),
    filtros: List[str] = typer.Option(
        [], "--filtro", "-f", help="Filtro de escolas (opcional, pode repetir)"
    ),
):
    """Extrai os nomes dos alunos aprovados do PDF especificado."""

    reader = load_pdf(file_path)
    data = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            linhas = text.split("\n")[4:-3]  # Remove cabeçalho e rodapé
            parse_page(linhas, data)

    df = pd.DataFrame(data, columns=["curso", "escola", "nome"])

    if filtros:
        filtros = trata_filtros(filtros)
        df = df[df["escola"].isin(filtros)]

    if df.empty:
        console.print(
            "[bold red]Nenhum aluno encontrado para os filtros especificados.[/bold red]"
        )
        raise typer.Exit()

    for curso, grupo in df.groupby("curso"):
        console.print(Text(f"\nCurso: {curso}", style="bold yellow"))

        for nome in grupo["nome"]:
            console.print(Text(nome, style="green"))

        console.print(Text("=" * 20, style="blue"))


if __name__ == "__main__":
    app()
