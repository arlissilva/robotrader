# 🤖 Robô de Trade com IA e PostgreSQL

Este projeto é um robô de day trade com IA (LightGBM), comunicação com MT5 via socket TCP, armazenamento de candles em PostgreSQL, interface web em React, e backtests baseados em dados reais.

## 🔧 Estrutura

- `robot_trader/` - Backend com IA e socket TCP
- `web_interface/` - Interface React
- `backtests/` - Scripts de simulação
- `scripts/` - Instalação e execução local/Docker
- `docker-compose.yml` - Orquestração com PostgreSQL

## 🚀 Como rodar

### Local

```bash
cd scripts
./install.sh         # ou install.bat no Windows
./run_architecture.sh  # ou run_architecture.bat
```

### Docker

```bash
docker compose up --build
```

## 🌐 Interface Web

Acesse: http://localhost:5173  
Backend: http://localhost:8000

## 📊 Backtest com dados reais

```bash
python backtests/executar_backtest.py 30
```

## 🧠 IA com LightGBM

- Treinamento: `robot_trader/ai/treinar_modelo.py`
- Modelo salvo em: `robot_trader/ai/modelo_lightgbm.pkl`
- Dados armazenados no banco PostgreSQL

## 🧩 Banco de Dados

- Acesso padrão:
  ```
  DB_URL=postgresql://postgres:postgres@localhost:5432/robotrader
  ```
  ou para Docker:
  ```
  DB_URL=postgresql://postgres:postgres@db:5432/robotrader
  ```

## ✅ Requisitos

- Python 3.10+
- PostgreSQL
- Docker (opcional)

---
Desenvolvido para testes com conta demo no MT5.