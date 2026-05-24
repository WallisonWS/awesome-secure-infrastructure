#!/usr/bin/env python3
"""
🌐 Cloudflare IP Address Updater for Firewalls
Autor: Wallison Araujo (WallisonWS)
Descrição: Consome os blocos de IP oficiais do Cloudflare (IPv4 e IPv6)
           e gera arquivos de configuração otimizados para FortiGate e pfSense.
           Roda automaticamente no GitHub Actions.
"""

import os
import sys
from datetime import datetime
import urllib.request

# URLs Oficiais do Cloudflare
URL_IPV4 = "https://www.cloudflare.com/ips-v4"
URL_IPV6 = "https://www.cloudflare.com/ips-v6"

# Pasta de saída
OUTPUT_DIR = "ips"

def fetch_ips(url):
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8').strip()
            # Retorna lista de subredes sem linhas vazias
            return [line for line in content.split('\n') if line]
    except Exception as e:
        print(f"[IP_UPDATE] Erro ao buscar IPs da URL {url}: {str(e)}")
        return []

def generate_fortigate_config(ipv4_list, ipv6_list, output_file):
    """Gera script CLI do FortiGate para criar objetos de endereço e o grupo."""
    lines = []
    lines.append("# Script de configuracao automatica de IPs do Cloudflare no FortiGate")
    lines.append(f"# Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lines.append("")
    lines.append("config firewall address")
    
    members = []
    
    # Processa IPv4
    for idx, ip in enumerate(ipv4_list):
        name = f"Cloudflare_IPv4_{idx+1}"
        lines.append(f"    edit \"{name}\"")
        lines.append(f"        set subnet {ip}")
        lines.append("    next")
        members.append(name)
        
    # Processa IPv6
    for idx, ip in enumerate(ipv6_list):
        name = f"Cloudflare_IPv6_{idx+1}"
        lines.append(f"    edit \"{name}\"")
        lines.append(f"        set subnet6 {ip}")
        lines.append("    next")
        members.append(name)
        
    lines.append("end")
    lines.append("")
    
    # Cria o grupo de endereços
    lines.append("config firewall addrgrp")
    lines.append("    edit \"Group_Cloudflare_IPs\"")
    member_str = " ".join([f"\"{m}\"" for m in members])
    lines.append(f"        set member {member_str}")
    lines.append("    next")
    lines.append("end")
    lines.append("")
    
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[IP_UPDATE] FortiGate CLI config salvo em: {output_file}")

def generate_pfsense_aliases(ipv4_list, ipv6_list, output_file):
    """Gera lista limpa de subredes para colar no Alias do pfSense."""
    lines = []
    lines.append("# Lista de IPs do Cloudflare para colar no Alias do pfSense")
    lines.append(f"# Gerado em: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    lines.append("")
    
    # Une as duas listas
    all_ips = ipv4_list + ipv6_list
    for ip in all_ips:
        lines.append(ip)
        
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print(f"[IP_UPDATE] pfSense alias list salvo em: {output_file}")

def update_readme(date_str):
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print(f"[IP_UPDATE] Erro: README.md nao encontrado.")
        return
        
    # Seção para colar no README
    ip_section = f"""<!-- CLOUDFLARE_IPS_START -->
### 🌐 IPs Cloudflare Atualizados
*   **Última verificação automática:** {date_str} (UTC)
*   💾 **[FortiGate CLI Config Script](ips/cloudflare_fortigate.conf)**: Objeto de endereços e grupo prontos para o FortiOS.
*   💾 **[pfSense Alias Network List](ips/cloudflare_pfsense_aliases.txt)**: Lista limpa de subredes IPv4 e IPv6 para colar no alias do pfSense.
<!-- CLOUDFLARE_IPS_END -->"""

    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    start_tag = "<!-- CLOUDFLARE_IPS_START -->"
    end_tag = "<!-- CLOUDFLARE_IPS_END -->"
    
    if start_tag in content and end_tag in content:
        before = content.split(start_tag)[0]
        after = content.split(end_tag)[1]
        new_content = before + ip_section + after
    else:
        # Se as tags não existirem, adiciona ao final do arquivo
        new_content = content + "\n\n" + ip_section
        
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("[IP_UPDATE] README.md atualizado com os links de IPs.")

def main():
    # Cria pasta de saída se não existir
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        
    print("[IP_UPDATE] Buscando IPs oficiais do Cloudflare...")
    ipv4_ips = fetch_ips(URL_IPV4)
    ipv6_ips = fetch_ips(URL_IPV6)
    
    if not ipv4_ips or not ipv6_ips:
        print("[IP_UPDATE] Erro: Nao foi possivel obter a lista de IPs completa do Cloudflare. Operacao cancelada.")
        sys.exit(1)
        
    print(f"[IP_UPDATE] Encontrados {len(ipv4_ips)} blocos IPv4 e {len(ipv6_ips)} blocos IPv6.")
    
    # Caminhos dos arquivos gerados
    fortigate_file = os.path.join(OUTPUT_DIR, "cloudflare_fortigate.conf")
    pfsense_file = os.path.join(OUTPUT_DIR, "cloudflare_pfsense_aliases.txt")
    
    # Gera as configurações
    generate_fortigate_config(ipv4_ips, ipv6_ips, fortigate_file)
    generate_pfsense_aliases(ipv4_ips, ipv6_ips, pfsense_file)
    
    # Atualiza o README
    date_str = datetime.now().strftime("%d/%m/%Y as %H:%M")
    update_readme(date_str)
    
    print("[IP_UPDATE] Concluido com sucesso!")

if __name__ == "__main__":
    main()
