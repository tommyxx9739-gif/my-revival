import http.server
import socketserver

# CONFIGURACIÓN
PORT = 8080  # El puerto al que apuntarás en el APK
GAME_PORT = 53640 # El puerto donde correrá el motor del juego

class RevivalHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Esta ruta es la que suelen pedir los clientes antiguos para unirse
        if "/game/Join.ashx" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            
            # El "Ticket" de entrada que el APK lee
            # Reemplaza 'TU_IP' por la IP de tu ZeroTier o localhost
            join_script = f"""
            -- Script de unión básico
            local client = game:GetService("NetworkClient")
            client:Connect("127.0.0.1", {GAME_PORT}, 0, 20)
            """
            self.wfile.write(join_script.encode())
        else:
            self.send_response(404)
            self.end_headers()

print(f"Servidor de Revival activo en el puerto {PORT}")
print("Esperando conexión del APK...")

with socketserver.TCPServer(("", PORT), RevivalHandler) as httpd:
    httpd.serve_forever()
