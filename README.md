# Movie Catalog Script

O Movie Catalog Script é uma ferramenta que utiliza a API do IMDb para buscar informações sobre filmes, incluindo nome, ano de lançamento, nota do IMDb e outros detalhes. Com esse script, você pode automatizar a coleta de informações sobre filmes e criar listas personalizadas com detalhes relevantes.

## Funcionalidades

- **Busca Automática:** O script permite buscar informações sobre filmes utilizando a API do IMDb. Basta inserir o nome do filme e o script retorna detalhes como título, ano de lançamento, sinopse, classificação no IMDb e popularidade.
- **Salvando na Lista:** Você pode salvar os detalhes de um filme em uma lista, que é armazenada em um arquivo JSON. Isso permite criar uma lista personalizada de filmes com suas informações relevantes.
- **Busca Avançada:** O script permite realizar uma busca avançada por filmes, considerando o nome e o ano de lançamento.
- **Integração com a API do IMDb:** O script utiliza a API do IMDb para obter informações atualizadas sobre os filmes.

## Requisitos

Antes de usar o script, você precisará atender aos seguintes requisitos:

- Python 3.x instalado no seu sistema.
- Uma chave de API do IMDb. (Você pode obter uma chave de API gratuitamente no site do IMDb.)

## Como Usar

1. Clone o repositório: `git clone https://github.com/seu-usuario/movie-catalog-script.git`
2. Crie uma conta e obtenha uma chave de API do IMDb.
3. Crie um arquivo `key.py` na mesma pasta do script e adicione sua chave de API conforme o exemplo abaixo:

```python
# key.py
API_IMDB_KEY = "sua_chave_de_api_aqui"
```

4. Execute o script: `python movie_catalog.py`
5. Siga as instruções do menu para buscar informações sobre filmes e salvar na lista.

## Lista de Filmes

O script permite criar uma lista de filmes personalizada. A lista é armazenada em um arquivo JSON chamado `movie_list.json`. Você pode editar e visualizar sua lista de filmes sempre que desejar.

## Observações

- Certifique-se de possuir uma conexão com a internet para que o script possa buscar os dados dos filmes na API do IMDb.
- Este script é um projeto de demonstração e pode ser adaptado e estendido para atender às suas necessidades específicas.

## Licença

Este projeto está licenciado sob a [Licença MIT](LICENSE).

## Autor

- Eduardo Lima (@edududs)

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para criar pull requests ou reportar problemas.

Espero que esse README atenda às suas necessidades! Sinta-se à vontade para personalizá-lo de acordo com as especificidades do seu projeto. Obrigado por compartilhar o seu script com a comunidade e bom trabalho no desenvolvimento da sua aplicação!
