# 🛡️ FortiGate CLI Cheat Sheet

Este guia de referência rápida compila os comandos CLI mais importantes para administração, depuração e cibersegurança em firewalls **FortiGate (FortiOS)**.

---

## ⚙️ Comandos de Configuração Básica e Sistema
* **Entrar no modo de visualização global:**
  ```fortinet
  get system status
  ```
* **Mostrar a configuração atual em formato legível de comandos (similar ao show run):**
  ```fortinet
  show system interface
  ```
* **Salvar alterações e sair de um menu:**
  ```fortinet
  end
  ```
* **Sair sem salvar alterações:**
  ```fortinet
  abort
  ```

---

## 🌐 Roteamento, SD-WAN e Interfaces
* **Mostrar tabela de roteamento ativa (Roteamento de Produção):**
  ```fortinet
  get router info routing-table database
  ```
* **Mostrar apenas as rotas instaladas na FIB (Forwarding Information Base):**
  ```fortinet
  get router info routing-table all
  ```
* **Verificar o status dos links e regras SD-WAN:**
  ```fortinet
  diagnose sys sdwan member
  diagnose sys sdwan service
  ```
* **Verificar a latência, jitter e perda de pacotes dos links via SLA do SD-WAN:**
  ```fortinet
  diagnose sys sdwan health-check status
  ```

---

## 🔒 Políticas de Firewall e Segurança
* **Listar todas as políticas IPv4 configuradas (Zero Trust audit):**
  ```fortinet
  show firewall policy
  ```
* **Verificar tráfego ativo associado a uma política específica (ex: política ID 5):**
  ```fortinet
  diagnose sys session list | grep -A 5 "policy_id=5"
  ```
* **Verificar status dos Filtros Web e DNS:**
  ```fortinet
  diagnose test application urlfilter 1
  diagnose test application dnsproxy 1
  ```

---

## 🔑 Monitoramento de SSL-VPN
* **Verificar usuários conectados na SSL-VPN no momento:**
  ```fortinet
  execute vpn sslvpn list
  ```
* **Desconectar um usuário conectado por SSH/SSL-VPN (ex: usuário "wallison"):**
  ```fortinet
  execute vpn sslvpn cleanup user wallison
  ```
* **Verificar o status do túnel IPsec VPN:**
  ```fortinet
  get vpn ipsec tunnel details
  ```

---

## 🛠️ Diagnóstico e Depuração de Rede (Troubleshooting)
* **Captura de Pacotes (Sniffer) - O "Wireshark" do FortiGate:**
  *Sintaxe: `diagnose sniffer packet <interface> '<filtro>' <nível_detalhe> <limite_contagem>`*
  
  * Capturar tráfego ICMP (ping) na interface `port1` (WAN):
    ```fortinet
    diagnose sniffer packet port1 'icmp' 4 10
    ```
  * Capturar todo o tráfego que vai ou vem do IP do NVR Hikvision (`192.168.99.100`):
    ```fortinet
    diagnose sniffer packet any 'host 192.168.99.100' 4 20
    ```
  * Níveis de detalhe (verbose):
    * `1`: Mostra cabeçalhos dos pacotes.
    * `3`: Mostra cabeçalhos + dados hexadecimais completos.
    * `4`: Mostra cabeçalhos com o nome da interface de entrada/saída.

* **Rastreamento de Fluxo (Packet Flow Trace) - Entender porque um pacote está sendo bloqueado:**
  ```fortinet
  diagnose debug reset
  diagnose debug flow filter addr 192.168.10.15  # IP de origem
  diagnose debug flow show console enable
  diagnose debug flow trace start 100            # Rastrear 100 pacotes
  diagnose debug enable
  ```
  *(Excelente para diagnosticar se uma regra de firewall ou rota está dropando o pacote)*
  
  * **Para parar o trace:**
    ```fortinet
    diagnose debug disable
    diagnose debug flow trace stop
    ```

* **Mostrar consumo de CPU e memória em tempo real por processos:**
  ```fortinet
  diagnose sys top 2 20
  ```
  *(Atualiza a cada 2 segundos, mostrando os 20 principais processos)*
