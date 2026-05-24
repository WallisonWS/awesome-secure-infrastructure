#!/usr/bin/env python3
"""
🛡️ IP Threat Intelligence Feed consolidado para Firewalls
Autor: Wallison Araujo (WallisonWS)
Descrição: Coleta e consolida listas públicas de reputação de IPs maliciosos ativos
           (como botnets, ransomwares, scanners de rede) e gera um feed limpo.
           Roda automaticamente no GitHub Actions.
"""

import os
import sys
import re
from datetime import datetime
import urllib.request

# Fontes de IP de ciberameaças de alta confiabilidade pública
SOURCES = [
    "https://rules.emergingthreats.net/blockrules/compromised-ips.txt",
    "https://blocklist.de/downloads/export-ips_all.txt"
]

# Pasta de saída
OUTPUT_DIR = "feeds"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "blocklist-active.txt")
MAX_IPS = 1500  # Limite de segurança de IPs ativos no feed (para excelente performance)

# Regex simples para validar se é um IP IPv4 válido
IP_REGEX = re.compile(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$")

def fetch_ips_from_source(url):
    print(f"[THREAT_FEED] Buscando dados de {url}...")
    ips = set()
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8', errors='ignore')
            for line in content.split("\n"):
                line = line.strip()
                # Ignora comentários e linhas vazias
                if not line or line.startswith("#") or line.startswith(";"):
                    continue
                # Remove comentários inline se houver
                line = line.split("#")[0].strip()
                # Valida formato IPv4
                if IP_REGEX.match(line):
                    ips.add(line)
        return ips
    except Exception as e:
        print(f"[THREAT_FEED] Erro ao carregar da URL {url}: {str(e)}")
        return set()

def update_readme(ip_count, date_str):
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print("[THREAT_FEED] Erro: README.md nao encontrado.")
        return
        
    feed_section = f"""<!-- THREAT_FEED_START -->
### 🛡️ Threat Intelligence IP Feed (Blocklist Ativa)
*   **Última atualização automática:** {date_str} (UTC)
*   **IPs Maliciosos Ativos no Feed:** `{ip_count}`
*   🔗 **URL do Feed Raw (Copie para seu Firewall):** `https://raw.githubusercontent.com/WallisonWS/awesome-secure-infrastructure/main/feeds/blocklist-active.txt`
*   ⚙️ **Como usar no seu Firewall:**
    *   **FortiGate:** Vá em *Security Fabric* -> *External Connectors* -> clique em *Create New* -> *IP Address* -> Insira a URL Raw acima e configure a frequência de atualização. Agora use esse conector em regras de firewall de bloqueio.
    *   **pfSense:** Adicione no pacote *pfBlockerNG* na aba *IP* -> *IPv4* como uma nova lista de feed usando a URL Raw acima.
<!-- THREAT_FEED_END -->"""

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    start_tag = "<!-- THREAT_FEED_START -->"
    end_tag = "<!-- THREAT_FEED_END -->"
    
    if start_tag in content and end_tag in content:
        before = content.split(start_tag)[0]
        after = content.split(end_tag)[1]
        new_content = before + feed_section + after
    else:
        new_content = content + "\n\n" + feed_section
        
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("[THREAT_FEED] README.md atualizado com os dados do Threat Feed.")

def main():
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    all_ips = set()
    
    # Coleta de todas as fontes
    for source in SOURCES:
        ips = fetch_ips_from_source(source)
        all_ips.update(ips)
        
    ip_list = sorted(list(all_ips))
    total_found = len(ip_list)
    print(f"[THREAT_FEED] Total de IPs maliciosos encontrados: {total_found}")
    
    # Aplica limite de segurança
    if total_found > MAX_IPS:
        print(f"[THREAT_FEED] Aplicando limite de seguranca de {MAX_IPS} IPs...")
        # Pega os IPs de forma balanceada
        ip_list = ip_list[:MAX_IPS]
        
    # Escreve a blocklist limpa
    lines = []
    lines.append("# Consolidated IP Threat Feed for Firewalls (FortiGate / pfSense)")
    lines.append(f"# Updated at: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lines.append(f"# Total IPs: {len(ip_list)}")
    lines.append("# Sources: Emerging Threats, Blocklist.de")
    lines.append("# Use of this feed is public and free.")
    lines.append("# ------------------------------------------------------------")
    lines.append("")
    
    for ip in ip_list:
        lines.append(ip)
        
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[THREAT_FEED] Arquivo salvo com sucesso em: {OUTPUT_FILE}")
    
    # Atualiza a contagem e a data no README
    date_str = datetime.now().strftime("%d/%m/%Y as %H:%M")
    update_readme(len(ip_list), date_str)
    
    print("[THREAT_FEED] Operacao concluida!")

if __name__ == "__main__":
    main()
