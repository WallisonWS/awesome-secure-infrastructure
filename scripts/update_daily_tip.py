#!/usr/bin/env python3
"""
💡 Script de Atualização da Dica do Dia
Autor: Wallison Araujo (WallisonWS)
Descrição: Seleciona uma dica técnica de infraestrutura ou cibersegurança
           da lista e atualiza o README.md na seção correspondente.
           Roda automaticamente no GitHub Actions.
"""

import os
from datetime import datetime

# --- LISTA DE DICAS PRÁTICAS DE TI, REDES E SEGURANÇA ---
TIPS = [
    "**Dica de FortiGate:** Sempre use o comando `diagnose sniffer packet any 'host <IP>' 4 10` para capturar pacotes de um dispositivo específico e entender se o tráfego está chegando no firewall.",
    "**Dica de Aruba:** Use a flag `lacp` ao criar trunks de portas físicas (`trunk 21-22 trk1 lacp`) para garantir negociação dinâmica de links e evitar loops físicos acidentais na rede.",
    "**Dica de pfSense:** Ao isolar uma VLAN de IoT, adicione uma regra de bloqueio explícito no topo do firewall apontando para a rede 'Any' mas permitindo apenas as portas NTP (123) e DNS (53) da sua LAN para os dispositivos funcionarem.",
    "**Dica de Active Directory:** Use o comando `Search-ADAccount -AccountInactive -TimeSpan 90.00:00:00 -UsersOnly` no PowerShell para auditar e listar contas de usuários sem logon há mais de 90 dias.",
    "**Dica de Cibersegurança:** Desative o protocolo WPS nos seus Access Points UniFi e em qualquer roteador. O WPS é vulnerável a ataques de força bruta rápidos e fáceis.",
    "**Dica de FortiGate:** Para monitorar o tráfego da VPN IPsec em tempo real pela CLI, utilize o comando `get vpn ipsec tunnel details`.",
    "**Dica de Windows Server:** Evite logar diretamente como Administrator nos servidores de produção. Use contas individuais com privilégios administrativos temporários (LAPS) ou delegados.",
    "**Dica de Switches:** Em portas onde estão conectados computadores de usuários comuns, ative o recurso **PortFast** (no Aruba, chamado de *spanning-tree port-type admin-edge*) para que a porta suba imediatamente sem esperar a convergência do Spanning Tree.",
    "**Dica de Cibersegurança:** Nunca permita que câmeras Hikvision ou outros dispositivos IoT conversem diretamente com a internet. Force o acesso remoto sempre através de túneis **SSL-VPN** seguros.",
    "**Dica de pfSense:** Se a Web GUI do seu pfSense travar ou não carregar, acesse a CLI/Shell via SSH e escolha a opção `11` para reiniciar o servidor WebConfigurator sem precisar reiniciar todo o firewall.",
    "**Dica de FortiGate:** Ative o recurso **SD-WAN** para balancear carga e garantir redundância ativa entre múltiplos links de internet (Ex: Fibra Principal e Link de Backup).",
    "**Dica de Active Directory:** O cmdlet `Unlock-ADAccount -Identity <usuario>` é o método mais rápido para desbloquear a conta de um usuário bloqueado após errar a senha.",
    "**Dica de Redes:** Configure o recurso **DHCP Snooping** nos seus switches de acesso para impedir que roteadores de visitantes ou dispositivos maliciosos distribuam IPs incorretos na rede corporativa.",
    "**Dica de Cibersegurança:** Restrinja o tráfego inter-VLAN. Computadores de usuários comuns não precisam ter acesso direto às portas de gerenciamento de switches, firewalls e NVRs.",
    "**Dica de UniFi:** Ative o **Client Isolation** (Isolamento de Cliente) na sua rede Wi-Fi de visitantes para impedir que os celulares e notebooks conversem entre si na mesma rede sem fio.",
    "**Dica de Active Directory:** Use o cmdlet `Get-ADUser -Filter \"PasswordNeverExpires -eq 'True'\"` para auditar quais contas possuem senhas que nunca expiram e reverta as desnecessárias.",
    "**Dica de FortiGate:** Quer testar as regras de firewall na CLI? Utilize `diagnose debug flow trace` para rastrear o fluxo completo do pacote e ver qual regra está bloqueando ou permitindo o tráfego.",
    "**Dica de pfSense:** Use o utilitário `pfctl -ss` no terminal para inspecionar todas as conexões (estados) ativas que estão atravessando o firewall no momento.",
    "**Dica de Aruba:** Mantenha sempre o firmware dos switches atualizado para corrigir bugs críticos de rede e brechas de cibersegurança.",
    "**Dica de Cibersegurança:** Implemente a política de privilégio mínimo. Nenhum desenvolvedor ou usuário comum deve possuir permissões de administrador local nas estações de trabalho.",
]

def get_tip_of_the_day():
    # Seleciona uma dica com base no dia do ano
    day_of_year = datetime.now().timetuple().tm_yday
    tip_index = day_of_year % len(TIPS)
    return TIPS[tip_index]

def update_readme():
    readme_path = "README.md"
    
    if not os.path.exists(readme_path):
        print(f"❌ Erro: Arquivo {readme_path} não encontrado no diretório atual.")
        return
        
    tip = get_tip_of_the_day()
    date_str = datetime.now().strftime("%d/%m/%Y")
    
    # Formatação do bloco de dica
    tip_block = f"""<!-- DAILY_TIP_START -->
> [!TIP]
> **Dica de Infraestrutura & Segurança ({date_str}):**
> {tip}
<!-- DAILY_TIP_END -->"""
    
    print(f"⚡ Atualizando a dica para o dia {date_str}...")
    
    with open(readme_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    start_tag = "<!-- DAILY_TIP_START -->"
    end_tag = "<!-- DAILY_TIP_END -->"
    
    if start_tag in content and end_tag in content:
        # Substitui a seção existente
        before = content.split(start_tag)[0]
        after = content.split(end_tag)[1]
        new_content = before + tip_block + after
    else:
        # Se as tags não existirem, adiciona ao final do arquivo ou após uma introdução
        print("⚠️ Tags de dica diária não encontradas. Adicionando ao final do README.")
        new_content = content + "\n\n" + tip_block
        
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    print("✅ README.md atualizado com a dica diária!")

if __name__ == "__main__":
    update_readme()
