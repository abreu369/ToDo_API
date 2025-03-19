import sys
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

# Adiciona o diretório 'app' ao caminho de importação
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'main')))
from app.database import Base  # Importa a Base do seu projeto

# Configuração do arquivo de log
config = context.config
fileConfig(config.config_file_name)

# Configuração do banco de dados
target_metadata = Base.metadata  # Referencia a metadata do seu modelo
