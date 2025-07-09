import socket
import json

# Candle de exemplo
candle = {
    "ativo": "WINQ25",
    "open": 141320.0,
    "high": 141325.0,
    "low": 141275.0,
    "close": 141280.0,
    "volume": 190
}

# Conexão com o servidor IA (localhost:5555)
HOST = "127.0.0.1"
PORT = 5555

try:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        msg = json.dumps(candle) + "\n"
        print("📤 Enviando candle:", msg.strip())
        s.sendall(msg.encode())

        resposta = s.recv(1024).decode().strip()
        print("✅ Sinal recebido da IA:", resposta)

except Exception as e:
    print("❌ Erro ao se conectar ao servidor:", e)
