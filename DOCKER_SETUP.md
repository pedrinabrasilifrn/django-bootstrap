# 🐳 Configuração Docker - Ambiente de Desenvolvimento

## 📋 Pré-requisitos

- Docker
- Docker Compose

## 🚀 Configuração Inicial

### 1. Criar arquivo `.env`

Copie o arquivo de exemplo e ajuste conforme necessário:

```bash
cp .env.example .env
```

O arquivo `.env` deve conter (mínimo para desenvolvimento):

```env
DEBUG=True
DJANGO_ENV=development
SECRET_KEY=dev-secret-key-change-in-production
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

### 2. Parar containers antigos (se existirem)

```bash
docker-compose down -v
```

### 3. Construir e iniciar os containers

```bash
docker-compose up -d --build
```

### 4. Verificar os logs

```bash
docker-compose logs -f
```

## 📊 Serviços Disponíveis

- **Web (Django)**: http://localhost:8000
- **Redis**: localhost:6379
- **Celery Worker**: Processamento de tarefas assíncronas
- **Celery Beat**: Agendador de tarefas periódicas

## 🔍 Comandos Úteis

### Ver logs de um serviço específico
```bash
docker-compose logs -f web
docker-compose logs -f celery_worker
docker-compose logs -f celery_beat
```

### Executar comandos Django
```bash
docker-compose exec web python manage.py createsuperuser
docker-compose exec web python manage.py shell
```

### Parar os containers
```bash
docker-compose down
```

### Parar e remover volumes (limpa banco de dados)
```bash
docker-compose down -v
```

### Reconstruir apenas um serviço
```bash
docker-compose up -d --build web
```

## 🐛 Troubleshooting

### Containers não iniciam

1. Verifique se o arquivo `.env` existe e está configurado corretamente
2. Verifique os logs: `docker-compose logs`
3. Tente reconstruir: `docker-compose down -v && docker-compose up -d --build`

### Erro de permissão em arquivos

No Windows, certifique-se de que o Docker Desktop tem acesso à pasta do projeto.

### Banco de dados SQLite

Em desenvolvimento, o Django usa SQLite (arquivo `db.sqlite3`). 
O arquivo é criado automaticamente no primeiro `migrate`.

### Celery não conecta ao Redis

Verifique se o serviço Redis está rodando:
```bash
docker-compose ps redis
```

## 📝 Notas

- **Desenvolvimento**: Usa SQLite (sem necessidade de PostgreSQL)
- **Produção**: Use `docker-compose.prd.yml` com PostgreSQL
- **Auto-reload**: O servidor Django recarrega automaticamente ao modificar arquivos
- **Volumes**: Seu código local é montado no container, mudanças são refletidas imediatamente
