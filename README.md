# BlueStorm

Implementação de API com autenticação para BlueStorm usando Python com o web framework Flask.

## Instruções de Uso

Para rodar essa API localmente:

```
git clone https://izcoser/bluestorm
cd bluestorm
python -m pip install -r requirements.txt # Instala o Flask, a única dependência.
python -m flask --app api run
```

Ou usando o Docker:
```
docker run --publish 8000:5000 izcoser/bluestorm
```

Os endpoints disponíveis são listados abaixo:

### GET

- /patients
- /pharmacies
- /transactions

### POST

- /create_auth

### Obtendo a autenticação:

O endpoints ```GET``` precisam do token de autenticação para retornarem dados. Usando o módulo ```requests```, o token pode ser obtido dessa forma:

```
>>> r = requests.post('http://0.0.0.0:8000/create_auth')
>>> r.json()
{'token': 'JWCNDP4AO238KIM'}
```

### Usando a autenticação:

```
>>> r = requests.get('http://0.0.0.0:8000/patients', headers={"token": "JWCNDP4AO238KIM"})
```

Os exemplos acima foram executados com a aplicação rodando via Docker. O endereço http será ```http://127.0.0.1:5000``` se executando diretamente do arquivo Python.

## Testes

Testes automatizados foram desenvolvidos usando o módulo nativo Python ```unittest```.

Para rodar os testes, basta executar o comando ```python tests.py -v```.

## Padrão de formatação de código

Todos os arquivos Python seguem um padrão de formatação automática, de acordo com o software [Black](https://github.com/psf/black).
