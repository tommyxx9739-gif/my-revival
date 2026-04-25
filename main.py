import http.server
import socketserver
import os

# CONFIGURACIÓN DE RENDER
# Render asigna un puerto dinámico, esta línea lo detecta automáticamente
PORT = int(os.environ.get("PORT", 8080))
GAME_PORT = 53640 

class RevivalHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Esta es la ruta que buscará el APK de Roblox
        if "/game/Join.ashx" in self.path:
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            
            # El script que el cliente ejecuta para unirse
            # '127.0.0.1' funciona si el servidor corre en el mismo móvil
            # Si corre en Render, aquí deberías poner la IP de quien hostea el mapa
            join_script = f"""
            local client = game:GetService("NetworkClient")
            client:Connect("127.0.0.1", {GAME_PORT}, 0, 20)
            """
            self.wfile.write(join_script.encode())
        else:
            # Respuesta básica para que Render sepa que el servidor está vivo
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"Servidor de Revival Activo")

print(f"Servidor iniciado en el puerto {PORT}")

# El servidor se vincula a '0.0.0.0' para ser accesible desde internet
with socketserver.TCPServer(("0.0.0.0", PORT), RevivalHandler) as httpd:
    httpd.serve_forever()
