import os

import func.movie_functions as movie_functions


def print_menu():
    """
    Prints the menu options for the user to choose from.
    """
    os.system("cls")
    print("===== Menu =====")
    print("1. Exibir sua lista de filmes")
    print("2. Consultar informações de um filme da internet")
    print("3. Sair")


while True:
    print_menu()
    choice = input("Escolha uma opção: ")
    if choice == "1":
        movie_functions.show_movie_list()
    elif choice == "2":
        movie_functions.querry_movie()
    elif choice == "3":
        break
    else:
        print("Opção inválida!\nPor favor, insira uma opção válida.")
    input()

print("Programa encerrado.")
