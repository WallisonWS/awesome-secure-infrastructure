# 🧱 pfSense CLI & Console Cheat Sheet

O **pfSense** (baseado em FreeBSD) é amplamente administrado via interface web. No entanto, a CLI via SSH ou console local oferece um menu interativo extremamente poderoso e ferramentas de baixo nível essenciais para recuperação de desastres e troubleshooting avançado.

---

## 🖥️ Menu Principal do Console (SSH/VGA)
Ao conectar via SSH (se configurado) ou console local, você verá o menu numérico do pfSense:

*   `0) Logout` - Deslogar da sessão.
*   `1) Assign Interfaces` - Reatribuir placas de rede físicas para as interfaces WAN, LAN, VLANs.
*   `2) Set interface(s) IP address` - Configurar IPs estáticos ou DHCP nas interfaces (útil se você perder o acesso Web GUI).
*   `3) Reset webConfigurator password` - Reseta a senha do usuário `admin` para o padrão (`pfsense`).
*   `4) Reset to factory defaults` - Restaura o pfSense para as configurações de fábrica.
*   `5) Reboot system` - Reinicia o firewall.
*   `6) Halt system` - Desliga o equipamento com segurança.
*   `7) Ping host` - Executa um teste de ping.
*   `8) Shell` - Entra no terminal Unix (FreeBSD) para rodar comandos.
*   `11) Restart webConfigurator` - Reinicia o servidor web da interface do pfSense (útil se a página web travar).
*   `15) Restore recent configuration` - Restaura backups de configurações anteriores salvos localmente.

---

## 🐚 Comandos Úteis do Shell (Opção 8)

### 1. Diagnóstico de Rede e Filtros de Pacotes
O pfSense utiliza o **PF (Packet Filter)** do FreeBSD como mecanismo de firewall.

*   **Verificar o status do Firewall (PF):**
    ```bash
    pfctl -si
    ```
*   **Listar todas as regras de firewall ativas carregadas na memória:**
    ```bash
    pfctl -sr
    ```
*   **Visualizar a tabela de estados ativos (conexões atuais):**
    ```bash
    pfctl -ss
    ```
*   **Limpar todos os estados de conexões do firewall (útil após alterar rotas ou failover):**
    ```bash
    pfctl -F state
    ```
*   **Monitorar o tráfego em tempo real em uma interface específica (ex: interface wan `em0`):**
    ```bash
    tcpdump -i em0
    ```
*   **Capturar tráfego filtrando por um IP de destino (ex: host `192.168.99.100`):**
    ```bash
    tcpdump -i any host 192.168.99.100 -nn
    ```

### 2. Controle e Status de Serviços
*   **Verificar se o servidor web (nginx) do pfSense está rodando:**
    ```bash
    ps aux | grep nginx
    ```
*   **Reiniciar o serviço DHCP Server:**
    ```bash
    service dhcpd restart
    ```
*   **Reiniciar o serviço do DNS Resolver (Unbound):**
    ```bash
    service unbound restart
    ```
*   **Visualizar logs do sistema em tempo real:**
    ```bash
    clog -f /var/log/system.log
    ```
    *(Nota: O pfSense utiliza arquivos de log em formato circular binário. Use `clog` em vez de `tail` para lê-los).*

### 3. Informações de Hardware e Sistema
*   **Verificar o uso de CPU, memória e processos ativos (similar ao top do Linux):**
    ```bash
    top -a
    ```
*   **Verificar o uso de espaço em disco nas partições:**
    ```bash
    df -h
    ```
*   **Verificar a temperatura do processador (se compatível):**
    ```bash
    sysctl dev.cpu.0.temperature
    ```
*   **Mostrar as placas de rede físicas reconhecidas pelo sistema:**
    ```bash
    pciconf -lv | grep -B 3 network
    ```
