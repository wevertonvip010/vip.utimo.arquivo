#!/usr/bin/env python3
"""
Script para criar usuário administrador no sistema VIP Mudanças
"""

import os
import sys

# Adicionar o diretório src ao path para imports funcionarem
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from flask import Flask
from config import Config
from database import db
from models.user import User

def create_admin_user():
    """Criar usuário administrador"""
    
    # Configurar Flask app
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Inicializar banco de dados
    db.init_app(app)
    
    with app.app_context():
        try:
            # Criar todas as tabelas
            db.create_all()
            print("Tabelas do banco de dados criadas/verificadas.")
            
            # Verificar se usuário admin já existe
            admin_user = User.query.filter_by(email="admin@vip.com.br").first()
            
            if admin_user:
                print("Usuário admin já existe!")
                print(f"Email: {admin_user.email}")
                print(f"Nome: {admin_user.name}")
                print(f"Role: {admin_user.role}")
                
                # Perguntar se quer atualizar a senha
                resposta = input("Deseja atualizar a senha? (s/n): ").lower()
                if resposta == 's':
                    admin_user.set_password("123456")
                    db.session.commit()
                    print("Senha atualizada para: 123456")
                else:
                    print("Senha não alterada.")
            else:
                # Criar novo usuário admin
                new_admin = User(
                    email="admin@vip.com.br",
                    name="Administrador VIP",
                    role="admin"
                )
                new_admin.set_password("123456")
                
                db.session.add(new_admin)
                db.session.commit()
                
                print("✅ Usuário administrador criado com sucesso!")
                print("📧 Email: admin@vip.com.br")
                print("🔑 Senha: 123456")
                print("👤 Role: admin")
                
        except Exception as e:
            print(f"❌ Erro ao criar usuário admin: {e}")
            return False
    
    return True

if __name__ == "__main__":
    print("🚀 Criando usuário administrador do sistema VIP Mudanças...")
    print("=" * 50)
    
    success = create_admin_user()
    
    if success:
        print("=" * 50)
        print("✅ Script executado com sucesso!")
        print("Agora você pode fazer login no sistema com:")
        print("Email: admin@vip.com.br")
        print("Senha: 123456")
    else:
        print("❌ Falha na execução do script.")
        sys.exit(1)

