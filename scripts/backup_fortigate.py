#!/usr/bin/env python3
"""
🔒 Script de Backup Automático do FortiGate via SSH
Autor: Wallison Araujo (WallisonWS)
Descrição: Conecta ao firewall FortiGate via SSH, executa o comando para 
           extrair a configuração completa e salva em um arquivo local estruturado.
Requisitos: pip install paramiko
"""

import os
import time
from datetime import datetime
import paramiko

# --- CONFIGURAÇÕES DO FIREWALL ---
FORTIGATE_IP = "192.168.1.1"       # Altere para o IP do seu FortiGate
FORTIGATE_PORT = 22                # Porta SSH
FORTIGATE_USER = "admin"           # Usuário administrador
FORTIGATE_PASS = "SuaSenhaAqui"    # Senha ou configure chave SSH

# Diretorios de destino
BACKUP_DIR = "./backups/fortigate"
# ---------------------------------

def create_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)
        print(f"📁 Direitório de backup criado: {BACKUP_DIR}")

def fetch_fortigate_config():
    create_backup_dir()
    
    # Define o nome do arquivo com timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = os.path.join(BACKUP_DIR, f"fortigate_backup_{timestamp}.conf")
    
    print(f"⚡ Iniciando conexão SSH com o FortiGate em {FORTIGATE_IP}...")
    
    # Inicializa cliente SSH
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        # Conecta ao FortiGate
        ssh.connect(
            hostname=FORTIGATE_IP,
            port=FORTIGATE_PORT,
            username=FORTIGATE_USER,
            password=FORTIGATE_PASS,
            look_for_keys=False,
            allow_agent=False,
            timeout=15
        )
        
        # Abre um canal shell interativo (necessário para desativar o paging do CLI do FortiOS)
        channel = ssh.invoke_shell()
        time.sleep(1)
        
        # Envia comandos para desativar a paginação temporariamente na sessão
        # e depois exibe toda a configuração
        print("📤 Enviando comandos para extrair a configuração...")
        channel.send("config system console\n")
        time.sleep(0.5)
        channel.send("set output standard\n") # Desativa o '--More--' no terminal
        time.sleep(0.5)
        channel.send("end\n")
        time.sleep(0.5)
        
        # Executa o dump da configuração
        channel.send("show\n")
        time.sleep(5) # Aguarda o FortiGate cuspir toda a configuração
        
        # Lendo o buffer de retorno
        output = ""
        while channel.recv_ready():
            output += channel.recv(65535).decode('utf-8', errors='ignore')
            time.sleep(0.5)
            
        # Limpa o output para remover os primeiros prompts se desejado,
        # mas salvar o output bruto já é suficiente para restauração de desastre.
        
        # Salva a configuração no arquivo
        with open(backup_file, "w", encoding="utf-8") as f:
            f.write(output)
            
        print(f"✅ Backup concluído com sucesso!")
        print(f"📄 Arquivo salvo em: {backup_file}")
        
    except Exception as e:
        print(f"❌ Erro durante o backup: {str(e)}")
    finally:
        ssh.close()
        print("🔌 Conexão SSH encerrada.")

if __name__ == "__main__":
    # Nota: Antes de rodar, certifique-se de configurar o IP e credenciais corretas.
    # Pode ser executado em uma Cron (Linux) ou no Agendador de Tarefas (Windows).
    fetch_fortigate_config()
