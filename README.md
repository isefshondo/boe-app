# Boe's Legacy API

## Overview

Esta API provê <em>endpoints</em> para a autenticação, gestão do usuário e dados relacionados ao gado. Ela permite que os usuários façam seu registro, consigam entrar no aplicativo, atualizar suas informações, deletar sua conta e gerenciar informações relacionadas ao seu gado.

## URL Base

URL base desta API se encontra em: `https://boeapp.onrender.com`

## Autenticação

Para autenticação, a API usa o e-mail e senha. As credenciais são enviadas como JSON no corpo da requisição.

## Endpoints

### Sign Up User

#### Endpoint

`POST /signupUser`

#### Request

```json
{
  "name": "John Doe",
  "email": "john.doe@example.com",
  "password": "yourpassword"
}
```
#### Response

##### Success (Status Code: 200)

```json
{
  "message": "User created successfully!",
  "idUsuario": "user_id",
  "status": 200
}
```

##### Error (Status Code: 400)

```json
{
  "messages": ["Error message 1", "Error message 2"],
  "status": 400
}
```

### Log In User

#### Endpoint

`POST /loginUser`

#### Request

```json
{
  "email": "john.doe@example.com",
  "password": "yourpassword"
}
```
#### Response

##### Success (Status Code: 200)

```json
{
  "userData": {
    "id": "user_id",
    "nome": "John Doe",
    "email": "john.doe@example.com"
  },
  "mensagem": "User logged in successfully!",
  "status": 200
}
```

##### Error (Status Code: 400)

```json
{
  "message": "Error message",
  "status": 400
}
```

##### Not Found (Status Code: 404)

```json
{
  "message": "User not found. Please register first.",
  "status": 404
}
```

### Update User

#### Endpoint

`PUT /updateUser/{id}`
`GET /updateUser/{id}`

#### Request

```json
{
  "name": "New Name",
  "email": "new.email@example.com",
  "password": "newpassword"
}
```
#### Response for PUT method

##### Success (Status Code: 200)

```json
{
  "message": "Data updated successfully",
  "status": 201
}
```

##### Not Found (Status Code: 404)

```json
{
  "message": "User not found",
  "status": 404
}
```

#### Response for GET method

##### Success (Status Code: 200)

```json
{
  "id": "user_id",
  "name": "Mary Smith",
  "email": "marysmith@gmail.com",
  "password": "P4TTERN-PASS",
  "status": 200,
}
```

##### Fail (Status Code: 400 & 404)

```json
{
  "message": "An error has ocurred",
  "status": 400,
}
```

### Get Menu Data

#### Endpoint

`PUT /menu/{id}`

#### Response

##### Success (Status Code: 200)

```json
{
  "userName": "John Doe",
  "registeredCases": 10,
  "positiveCases": 60
}
```

##### Not Found (Status Code: 404)

```json
{
  "message": "User not found",
  "status": 404
}
```

### Delete User

#### Endpoint

`PUT /deleteUser/{id}`

#### Response

##### Success (Status Code: 200)

```json
{
  "message": "User deleted successfully",
  "status": 200
}
```

##### Not Found (Status Code: 404)

```json
{
  "message": "User not found",
  "status": 404
}
```
