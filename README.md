# Escape School API - README

Este README fornece informações sobre como interagir com a API "Escape School", detalhando o uso dos métodos HTTP PUT, POST e GET para gerenciar os dados do jogo.

## Autenticação

Todas as rotas (exceto `/auth/login`) requerem autenticação via token JWT. Você precisará obter um token de acesso enviando uma requisição POST para `/auth/login` com as credenciais corretas (atualmente `{"username": "admin", "password": "password"}`). O token retornado deve ser incluído no header de todas as requisições subsequentes como `x-access-token`.

## Endpoints da API

A API fornece endpoints para gerenciar jogadores, enigmas, salas, progresso do jogador nas salas, progresso geral do jogo e badges.

### Jogadores (`/players`)

* **GET `/players`**:
    * **Descrição:** Retorna uma lista de todos os jogadores.
    * **Headers:** `x-access-token: SEU_TOKEN_JWT`
    * **Resposta (JSON):**
        ```json
        [
            {
                "created_at": "2025-05-14T16:30:00.000Z",
                "id": 1,
                "name": "Jogador 1",
                "updated_at": "2025-05-14T16:30:00.000Z"
            },
            {
                "created_at": "2025-05-14T16:31:00.000Z",
                "id": 2,
                "name": "Jogador 2",
                "updated_at": "2025-05-14T16:31:00.000Z"
            }
        ]
        ```
    * **GET `/players?player_id=<id_do_jogador>`**:
        * **Descrição:** Retorna os detalhes de um jogador específico pelo ID.
        * **Headers:** `x-access-token: SEU_TOKEN_JWT`
        * **Resposta (JSON) para um jogador encontrado:**
            ```json
            {
                "created_at": "2025-05-14T16:30:00.000Z",
                "id": 1,
                "name": "Jogador 1",
                "updated_at": "2025-05-14T16:30:00.000Z"
            }
            ```
        * **Resposta (JSON) para jogador não encontrado (status 404):**
            ```json
            {
                "error": "404 Not Found: The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again."
            }
            ```
    * **POST `/players`**:
        * **Descrição:** Cria um novo jogador.
        * **Headers:** `Content-Type: application/json`, `x-access-token: SEU_TOKEN_JWT`
        * **Corpo da Requisição (JSON):**
            ```json
            {
                "name": "Novo Jogador"
            }
            ```
        * **Resposta (JSON) para criação bem-sucedida (status 201):**
            ```json
            {
                "created_at": "2025-05-14T16:35:00.000Z",
                "id": 3,
                "name": "Novo Jogador",
                "updated_at": "2025-05-14T16:35:00.000Z"
            }
            ```

### Enigmas (`/puzzles`)

* **GET `/puzzles`**: Lista todos os enigmas.
* **GET `/puzzles/<id_do_enigma>`**: Retorna um enigma específico pelo ID.
* **POST `/puzzles`**: Cria um novo enigma.
    * **Corpo da Requisição (JSON):**
        ```json
        {
            "name": "Enigma da Porta",
            "description": "Uma porta trancada com um teclado numérico.",
            "solution": "1234",
            "reward": "Chave da Próxima Sala"
        }
        ```
* **PUT `/puzzles/<id_do_enigma>`**: Atualiza um enigma existente pelo ID.
    * **Corpo da Requisição (JSON):**
        ```json
        {
            "description": "Uma porta trancada com um teclado numérico com números apagados."
        }
        ```

### Salas (`/rooms`)

* **GET `/rooms`**: Lista todas as salas.
* **GET `/rooms/<id_da_sala>`**: Retorna uma sala específica pelo ID.
* **POST `/rooms`**: Cria uma nova sala.
    * **Corpo da Requisição (JSON):**
        ```json
        {
            "name": "Sala Inicial",
            "description": "A sala onde você acordou."
        }
        ```
* **PUT `/rooms/<id_da_sala>`**: Atualiza uma sala existente pelo ID.
    * **Corpo da Requisição (JSON):**
        ```json
        {
            "description": "A sala escura onde você acordou, com uma mesa no centro."
        }
        ```

### Progresso do Jogador na Sala (`/player_room_progress`)

* **GET `/player_room_progress`**: Lista todo o progresso dos jogadores nas salas.
* **GET `/player_room_progress/<id_do_progresso>`**: Retorna um registro de progresso específico pelo ID.
* **GET `/player/<id_do_jogador>/room/<id_da_sala>/progress`**: Retorna o progresso de um jogador específico em uma sala específica.
* **POST `/player_room_progress`**: Cria um novo registro de progresso do jogador na sala.
    * **Corpo da Requisição (JSON):**
        ```json
        {
            "player_id": 1,
            "room_id": 1
        }
        ```
* **PUT `/player_room_progress/<id_do_progresso>`**: Atualiza um registro de progresso do jogador na sala.
    * **Corpo da Requisição (JSON):**
        ```json
        {
            "end_time": "2025-05-14T17:00:00.000Z",
            "time_spent": 300
        }
        ```

### Progresso Geral do Jogo (`/game_progress`)

* **GET `/game_progress`**: Lista todo o progresso geral do jogo.
* **GET `/game_progress/<id_do_progresso>`**: Retorna um registro de progresso geral específico pelo ID.
* **GET `/player/<id_do_jogador>/game_progress`**: Retorna o progresso geral de um jogador específico.
* **POST `/game_progress`**: Cria um novo registro de progresso geral do jogo para um jogador.
    * **Corpo da Requisição (JSON):**
        ```json
        {
            "player_id": 1,
            "current_room_id": 1,
            "game_completed": false
        }
        ```
* **PUT `/game_progress/<id_do_progresso>`**: Atualiza um registro de progresso geral do jogo.
    * **Corpo da Requisição (JSON):**
        ```json
        {
            "current_room_id": 2,
            "game_completed": true,
            "completion_time": "2025-05-14T17:30:00.000Z"
        }
        ```

### Badges (`/badges`)

* **GET `/badges`**: Lista todas as badges.
* **GET `/badges/<id_da_badge>`**: Retorna uma badge específica pelo ID.
* **POST `/badges`**: Cria uma nova badge.
    * **Corpo da Requisição (JSON):**
        ```json
        {
            "name": "Enigmático Iniciante",
            "description": "Resolveu o primeiro enigma.",
            "rule": "puzzles_solved >= 1"
        }
        ```
* **PUT `/badges/<id_da_badge>`**: Atualiza uma badge existente pelo ID.
    * **Corpo da Requisição (JSON):**
        ```json
        {
            "description": "Resolveu pelo menos um enigma."
        }
        ```

### Badges do Jogador (`/player_badges`)

* **GET `/player_badges`**: Lista todas as badges concedidas aos jogadores.
* **GET `/player_badges/<id_da_badge_do_jogador>`**: Retorna uma badge específica do jogador pelo ID.
* **GET `/player/<id_do_jogador>/badges`**: Retorna todas as badges de um jogador específico.
* **POST `/player_badges`**: Concede uma badge a um jogador.
    * **Corpo da Requisição (JSON):**
        ```json
        {
            "player_id": 1,
            "badge_id": 1
        }
        ```
