import json
import os
import textwrap
from pathlib import Path

import requests

from key import API_IMDB_KEY

SAVE_FOLDER_PATH = Path() / "data"
imdb_api_key = API_IMDB_KEY
BASE_URL = "https://api.themoviedb.org/3/"
url_language = "pt-BR"


def search_movie(api_key, query):
    base_url = f"{BASE_URL}search/movie"
    params = {"api_key": api_key, "query": query, "language": url_language}

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        results = response.json()["results"]
        if results:
            # Para este exemplo, retornaremos apenas o ID do primeiro
            # filme encontrado na pesquisa.

            # Você pode modificar esta função para lidar com vários
            # resultados, se necessário.
            return results[0]["id"]
        else:
            print("Nenhum filme encontrado com o termo de pesquisa.")
            return None
    else:
        print("Erro na pesquisa do filme.")
        return None


def get_movie_details(movie_id, api_key):
    base_url = f"{BASE_URL}movie/{movie_id}"
    params = {
        "api_key": api_key,
        "append_to_response": "videos,images",
        "language": url_language,
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        movie_data = response.json()
        movie_name = movie_data["title"]
        movie_year = movie_data["release_date"][
            :4
        ]  # Extrair apenas os 4 digitos do ano dos dados de lançamento
        movie_plot = movie_data["overview"]
        imdb_rating = movie_data["vote_average"]
        popularity = movie_data["popularity"]

        # Obter a URL da imagem de poster do filme
        # (geralmente disponível em várias resoluções)
        poster_url = ""
        if "poster_path" in movie_data:
            poster_url = (
                f"https://image.tmdb.org/t/p/original{movie_data['poster_path']}"
            )

        # Extrair informações adicionais
        genres = ", ".join(genre["name"] for genre in movie_data.get("genres", []))
        languages = ", ".join(
            lang["name"] for lang in movie_data.get("spoken_langages", [])
        )
        production_companies = ", ".join(
            comp["name"] for comp in movie_data.get("production_companies", [])
        )
        production_countries = ", ".join(
            country["name"] for country in movie_data.get("production_countries", [])
        )

        return {
            "name": movie_name,
            "year": movie_year,
            "plot": movie_plot,
            "image_url": poster_url,
            "imdb_rating": imdb_rating,
            "popularity": popularity,
            "genres": genres,
            "languages": languages,
            "production_companies": production_companies,
            "production_countries": production_countries,
        }
    else:
        print("Não foi possível obter os detalhes do filme.")
        return None


def save_movie_to_list(movie_details):
    SAVE_FOLDER_PATH.mkdir(exist_ok=True)
    file_path = Path(SAVE_FOLDER_PATH / "movie_list.json")

    # Criar um dicionário com as informações do filme
    movie_info = {
        "name": movie_details["name"],
        "year": movie_details["year"],
        "plot": movie_details["plot"],
        "image_url": movie_details["image_url"],
        "imdb_rating": movie_details["imdb_rating"],
        "popularity": movie_details["popularity"],
        "genres": movie_details["genres"],
        "languages": movie_details["languages"],
        "production_companies": movie_details["production_companies"],
        "production_countries": movie_details["production_countries"],
    }

    movie_list = []
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf8") as file:
            movie_list = json.load(file)

    for movie_entry in movie_list:
        # Verificar se o nome e o ano de lançamento são iguais
        if (
            movie_entry["name"].lower() == movie_info["name"].lower()
            and movie_entry["year"] == movie_info["year"]
        ):
            print("O filme já está na lista. Não será adicionado novamente.")
            return

    # Adicionar o novo filme à lista
    movie_list.append(movie_info)

    # Escrever a lista de filmes completa no arquivo JSON
    with open(file_path, "w", encoding="utf8") as file:
        json.dump(movie_list, file, ensure_ascii=False, indent=2)

    print("Filme salvo com sucesso.")


def is_movie_in_list(movie_info, movie_list):
    for movie_entry in movie_list:
        # Verificar se o nome e o ano de lançamento são iguais
        if (
            movie_entry["name"].lower() == movie_info["name"].lower()
            and movie_entry["year"] == movie_info["year"]
        ):
            return True

    return False


def format_movie_details(movie_details):
    formatted_details = f"""\
Nome do Filme: {movie_details["name"]}
Ano de Lançamento: {movie_details["year"]}
Enredo (Plot): {textwrap.fill(movie_details["plot"], width=80)}...
URL da Imagem do Poster: {movie_details["image_url"]}
IMDb Rating: {movie_details["imdb_rating"]}

"""
    return formatted_details


def print_menu():
    os.system("cls")
    print("===== Menu =====")
    print("1. Exibir sua lista de filmes")
    print("2. Consultar informações de um filme da internet")
    print("3. Sair")


def show_movie_list():
    os.system("cls")
    file_path = os.path.join(SAVE_FOLDER_PATH, "movie_list.json")

    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf8") as arquivo:
            movie_list = json.load(arquivo)

        print("===== Lista de Filmes =====")
        for index, movie in enumerate(movie_list):
            print(f"{index}. {movie['name']} - {movie['year']} ")
    else:
        print("A lista de filmes está vazia.")


def querry_movie():
    search_term = input("Me diga qual filme deseja consultar as informações: ")

    movie_id = search_movie(imdb_api_key, search_term)

    if movie_id:
        movie_details = get_movie_details(movie_id, imdb_api_key)
        if movie_details:
            formatted_details = format_movie_details(movie_details)
            print(formatted_details)

            saving_question = input("Deseja salvar este filme em uma lista? (s/N): ")
            if saving_question.lower() in ["s", "sim"]:
                save_movie_to_list(movie_details)

            print("=" * 80)


while True:
    print_menu()
    choice = input("Escolha uma opção: ")
    if choice == "1":
        show_movie_list()
    elif choice == "2":
        querry_movie()
    elif choice == "3":
        break
    else:
        print("Opção inválida!\nPor favor, insira uma opção válida.")
    input()

print("Programa encerrado.")
