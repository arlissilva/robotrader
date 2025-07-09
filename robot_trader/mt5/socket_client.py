import socket
import threading

class MT5SocketClient:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.sock = None
        self.callback = None
        self.clientes_conectados = []

    def on_message(self, callback):
        self.callback = callback

    def start(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.host, self.port))
        self.sock.listen(5)
        print(f"🔌 Aguardando conexão do MT5 em {self.host}:{self.port}...")
        while True:
            client, addr = self.sock.accept()
            print(f"✅ Cliente conectado: {addr}")
            self.clientes_conectados.append(client)
            threading.Thread(target=self.handle_client, args=(client,), daemon=True).start()

    def handle_client(self, client):
        try:
            while True:
                data = client.recv(1024)
                if not data:
                    print("⚠️ Conexão encerrada pelo cliente. Aguardando novo envio...")
                    break
                mensagem = data.decode("utf-8", errors="ignore").strip()
                print(f"📥 Mensagem recebida: {mensagem}")
                if self.callback:
                    self.callback(mensagem)
        except Exception as e:
            print("❌ Erro na comunicação:", e)
        finally:
            client.close()
            if client in self.clientes_conectados:
                self.clientes_conectados.remove(client)
