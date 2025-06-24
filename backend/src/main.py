import os
import sys
# Adicionar o diretório pai ao path para imports funcionarem
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
from database import db # Importar a instância do SQLAlchemy
from models.user import User # Importar o modelo User diretamente

# Importar blueprints
from routes.auth import auth_bp
from routes.clientes import clientes_bp
from routes.leads import leads_bp
from routes.licitacoes import licitacoes_bp
from routes.dashboard import dashboard_bp
from routes.ia import ia_bp
from routes.documentos import documentos_bp
from routes.whatsapp import whatsapp_bp
from routes.integracoes import integracoes_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))

# Configurações
app.config.from_object(Config)

# CORS
CORS(app, origins=Config.CORS_ORIGINS)

# JWT
jwt = JWTManager(app)

# Inicializar banco de dados
db.init_app(app)

# Função para criar tabelas e usuário admin padrão
def init_db_and_user():
    with app.app_context():
        db.create_all()
        # Verificar se já existe usuário admin
        try:
            admin_user = User.query.filter_by(email="admin@vip.com.br").first()
            if not admin_user:
                new_user = User(
                    email="admin@vip.com.br",
                    name="Administrador VIP",
                    role="admin"
                )
                new_user.set_password("123456") # Definir a senha usando o método set_password
                db.session.add(new_user)
                db.session.commit()
                print("Usuário admin padrão criado: admin@vip.com.br / 123456")
        except Exception as e:
            print(f"Erro ao criar usuário admin: {e}")

# Registrar blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(clientes_bp, url_prefix='/api/clientes')
app.register_blueprint(leads_bp, url_prefix='/api/leads')
app.register_blueprint(licitacoes_bp, url_prefix='/api/licitacoes')
app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
app.register_blueprint(ia_bp, url_prefix='/api/ia')
app.register_blueprint(documentos_bp, url_prefix='/api/documentos')
app.register_blueprint(whatsapp_bp, url_prefix='/api/whatsapp')
app.register_blueprint(integracoes_bp, url_prefix='/api/integracoes')

@app.route('/api/health', methods=['GET'])
def health_check():
    """Endpoint de verificação de saúde"""
    return {"status": "ok", "message": "VIP Mudanças API está funcionando"}, 200

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    """Servir arquivos estáticos do frontend"""
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    init_db_and_user() # Chamar a função de inicialização do DB e criação do usuário
    print("Iniciando servidor VIP Mudanças...")
    print("Running on http://127.0.0.1:5000/")
    app.run(host='127.0.0.1', port=5000, debug=True)


