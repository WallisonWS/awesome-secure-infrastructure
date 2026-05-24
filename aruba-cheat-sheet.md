# 🔌 Aruba Switches CLI Cheat Sheet

Este guia de referência rápida abrange os comandos CLI mais comuns para switches **Aruba (ArubaOS-S / Provision)** e **ArubaOS-CX**. 

---

## 💻 ArubaOS-S (ProCurve / Provision)
*Utilizado em switches como Aruba 2530, 2920, 2930F, 5400R, etc.*

### 1. Modos de Operação
* **Entrar no modo de privilégio (Enable):**
  ```hpe
  enable
  ```
* **Entrar no modo de configuração global:**
  ```hpe
  configure terminal
  ```
* **Sair de um menu / Voltar um nível:**
  ```hpe
  exit
  ```
* **Salvar as configurações atuais (Crucial):**
  ```hpe
  write memory
  ```

### 2. Gerenciamento de VLANs
* **Criar uma VLAN e dar nome:**
  ```hpe
  vlan 10
     name "Rede_Corporativa"
  vlan 20
     name "Rede_Visitantes"
  vlan 99
     name "CFTV_Hikvision"
  ```
* **Configurar Porta de Acesso (Untagged - Apenas 1 VLAN na porta):**
  *No modelo ArubaOS-S, você entra dentro da VLAN e associa as portas a ela.*
  ```hpe
  vlan 10
     untagged 1-10
  ```
  *(Associa as portas físicas de 1 a 10 como portas de acesso na VLAN 10)*

* **Configurar Porta de Tronco / Uplink (Tagged - Múltiplas VLANs trafegando):**
  *Útil para conectar o Switch ao FortiGate ou aos APs UniFi.*
  ```hpe
  vlan 10
     tagged 24
  vlan 20
     tagged 24
  vlan 99
     tagged 24
  ```
  *(Permite que as VLANs 10, 20 e 99 passem marcadas na porta 24)*

### 3. Agregação de Link (LACP / Trunking)
* **Criar um Trunk de portas físicas (ex: portas 21 e 22) usando LACP:**
  ```hpe
  trunk 21-22 trk1 lacp
  ```
* **Associar VLANs ao Trunk criado (`trk1`):**
  ```hpe
  vlan 10
     tagged trk1
  vlan 20
     tagged trk1
  ```

### 4. Comandos de Diagnóstico e Monitoramento
* **Verificar VLANs configuradas:**
  ```hpe
  show vlan
  ```
* **Verificar o estado físico e velocidade das portas:**
  ```hpe
  show interfaces brief
  ```
* **Visualizar vizinhos conectados (LLDP - excelente para ver APs UniFi e FortiGate):**
  ```hpe
  show lldp info remote-device
  ```
* **Ver a tabela de MAC Addresses de uma porta específica:**
  ```hpe
  show mac-address port 5
  ```
* **Verificar o log de erros do Switch:**
  ```hpe
  show log
  ```

---

## ⚡ ArubaOS-CX (Moderno)
*Utilizado em switches como Aruba CX 6000, 6100, 6200, 6300, etc.*

*Diferente do ArubaOS-S, o ArubaOS-CX adota uma sintaxe muito mais próxima do padrão de mercado (estilo Cisco CLI), onde você configura as VLANs diretamente na interface.*

### 1. Criar VLANs
```hpe
config
vlan 10
   name Rede_Corporativa
vlan 20
   name Rede_Visitantes
vlan 99
   name CFTV_Hikvision
```

### 2. Configurar Interfaces
* **Configurar Porta de Acesso (Access):**
  ```hpe
  interface 1/1/1
     no shutdown
     routing
     vlan access 10
  ```
* **Configurar Porta Trunk:**
  ```hpe
  interface 1/1/24
     no shutdown
     vlan trunk allowed 10,20,99
  ```

### 3. Diagnóstico (ArubaOS-CX)
* **Mostrar resumo das interfaces:**
  ```hpe
  show interface brief
  ```
* **Mostrar tabela de MACs aprendidos:**
  ```hpe
  show mac-address-table
  ```
* **Mostrar informações do LLDP:**
  ```hpe
  show lldp neighbor-info
  ```
* **Salvar configuração:**
  ```hpe
  write memory
  ```
