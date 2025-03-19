#!/bin/bash

# Esperar o MySQL estar pronto (pode ser necessário ajustar o tempo de espera)
echo "Aguardando o MySQL iniciar..."
sleep 10

# Executar as migrações do Alembic
echo "Executando as migrações do Alembic..."
alembic upgrade head

# Iniciar o aplicativo FastAPI
echo "Iniciando o FastAPI..."
#uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
