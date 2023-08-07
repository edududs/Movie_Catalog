import json
import os
import textwrap
from pathlib import Path

import pip._vendor.requests as requests

API_KEY = os.getenv("API_IMDB_KEY")
SAVE_FOLDER_PATH = Path() / "data"
imdb_api_key = API_KEY
BASE_URL = "https://api.themoviedb.org/3/"
url_language = "pt-BR"


def search_movie(api_key, query):
    """
    Searches for a movie using the specified API key and query.

    Parameters:
        - api_key (str): The API key to authenticate the request.
        - query (str): The search query for the movie.

    Returns:
        - list: A list of dictionaries containing information about the movies found. Each dictionary
          contains the following keys:
          - title (str): The title of the movie.
          - id (int): The ID of the movie.
          - year (str): The release year of the movie.
          Returns None if no movie is found or if there is an error in the request.
    """
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
            movies = []
            for dicts in results:
                move_info = {
                    "title": dicts["title"],
                    "id": dicts["id"],
                    "year": dicts["release_date"][:4],
                }
                movies.append(move_info)
            return movies
        else:
            print("Nenhum filme encontrado com o termo de pesquisa.")
            return None
    else:
        print("Erro na pesquisa do filme.")
        return None


def choose_movie(movies):
    """
    Prompts the user to choose a movie from a given list of movies and returns the ID of the chosen movie.

    Args:
        movies (list): A list of dictionaries representing movies. Each dictionary contains the title, year, and ID of a movie.

    Returns:
        int: The ID of the chosen movie.

    Raises:
        ValueError: If the user enters an invalid movie index.
    """
    while True:
        for index, movie in enumerate(movies):
            print(f'{index+1}. {movie["title"]}\nYear: {movie["year"]}')

        chosen_movie_index = int(input("Escolha o número do filme desejado: "))

        # Verifica se o número escolhido está entro dos limites válidos
        if 1 <= chosen_movie_index <= len(movies):
            # Obtém o ID do filme escolhido
            chosen_movie_id = movies[chosen_movie_index - 1]["id"]
            print(f"ID do filme escolhido: {chosen_movie_id}")
            return chosen_movie_id

        elif chosen_movie_index > len(movies):
            os.system("cls")
            print("\nEscolha um índice dentro das opções fornecidas")

        else:
            print(
                "\nHouve algum erro ao selecionar o ID do filme desejado.\
            \nCertifique-se de que escolheu o corretamente"
            )


def get_movie_details(movie_id, api_key):
    """
    Retrieves details of a movie using its ID.

    Args:
        movie_id (int): The ID of the movie.
        api_key (str): The API key for accessing the movie details.

    Returns:
        dict or None: A dictionary containing the movie details including name, year, plot, image URL, IMDb rating, popularity, genres, languages, production companies, and production countries. Returns None if the movie details cannot be obtained.
    """
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
    """
    Saves a movie to the movie list.

    Args:
        movie_details (dict): A dictionary containing the details of the movie.
            It should have the following keys:
            - "name" (str): The name of the movie.
            - "year" (int): The year of release of the movie.
            - "plot" (str): The plot of the movie.
            - "image_url" (str): The URL of the movie's image.
            - "imdb_rating" (float): The IMDb rating of the movie.
            - "popularity" (float): The popularity score of the movie.
            - "genres" (list[str]): A list of genres associated with the movie.
            - "languages" (list[str]): A list of languages of the movie.
            - "production_companies" (list[str]): A list of production companies involved in the movie.
            - "production_countries" (list[str]): A list of production countries of the movie.

    Returns:
        None

    Raises:
        None
    """
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
    if file_path.exists():
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
    """
    Check if a movie is in a given movie list.

    Parameters:
        movie_info (dict): A dictionary containing information about the movie to be checked.
            It should have the following keys:
                - name (str): The name of the movie.
                - year (int): The year the movie was released.

        movie_list (list): A list of dictionaries, where each dictionary represents a movie.
            Each dictionary should have the following keys:
                - name (str): The name of the movie.
                - year (int): The year the movie was released.

    Returns:
        bool: True if the movie is in the list, False otherwise.
    """
    for movie_entry in movie_list:
        # Verificar se o nome e o ano de lançamento são iguais
        if (
            movie_entry["name"].lower() == movie_info["name"].lower()
            and movie_entry["year"] == movie_info["year"]
        ):
            return True

    return False


def format_movie_details(movie_details):
    """
    Formats the movie details into a string.

    Parameters:
        movie_details (dict): A dictionary containing the details of a movie.
            The dictionary should have the following keys:
            - "name" (str): The name of the movie.
            - "year" (str): The year of release of the movie.
            - "plot" (str): The plot of the movie.
            - "image_url" (str): The URL of the movie's poster image.
            - "imdb_rating" (str): The IMDb rating of the movie.

    Returns:
        str: The formatted movie details as a string.
    """
    formatted_details = f"""\
Nome do Filme: {movie_details["name"]}
Ano de Lançamento: {movie_details["year"]}
Enredo (Plot): {textwrap.fill(movie_details["plot"], width=80)}...
URL da Imagem do Poster: {movie_details["image_url"]}
IMDb Rating: {movie_details["imdb_rating"]} {"💙️" if float(movie_details["imdb_rating"]) > 5.0 else "🌈️"}

"""
    return formatted_details


def show_movie_list():
    """
    Display the movie list.

    This function clears the console screen and displays the list of movies. It first checks if the "movie_list.json" file exists in the specified folder. If the file exists, it reads the contents of the file and prints each movie's name and year. If the file does not exist, it prints a message indicating that the movie list is empty.

    Parameters:
    None

    Returns:
    None
    """
    os.system("cls")
    file_path = Path(SAVE_FOLDER_PATH / "movie_list.json")

    if file_path.exists():
        with open(file_path, "r", encoding="utf8") as arquivo:
            movie_list = json.load(arquivo)

        print("===== Lista de Filmes =====")
        for index, movie in enumerate(movie_list):
            print(f"{index}. {movie['name']} - {movie['year']} ")
    else:
        print("A lista de filmes está vazia.")


def querry_movie():
    """
    Queries a movie using a search term provided by the user and displays the movie details.
    
    Returns:
    None
    """
    search_term = input("Me diga qual filme deseja consultar as informações: ")

    response_search_movie = search_movie(imdb_api_key, search_term)
    movie_id = choose_movie(response_search_movie)
    if movie_id:
        movie_details = get_movie_details(movie_id, imdb_api_key)
        if movie_details:
            formatted_details = format_movie_details(movie_details)
            print(formatted_details)

            saving_question = input("Deseja salvar este filme em uma lista? (s/N): ")
            if saving_question.lower() in ["s", "sim"]:
                save_movie_to_list(movie_details)

            print("=" * 80)
