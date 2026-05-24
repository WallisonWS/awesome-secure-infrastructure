# 🔑 Active Directory PowerShell Cheat Sheet

O módulo do **Active Directory** para PowerShell é a ferramenta mais poderosa para administradores de sistemas Windows Server (SysAdmins). Ele permite automatizar tarefas rotineiras, auditorias de segurança e gerenciamento em lote.

> [!NOTE]
> Para usar estes comandos, você precisa ter instalado o módulo do Active Directory (RSAT - Remote Server Administration Tools) ou executá-los diretamente em um Domain Controller (DC).

---

## 👤 Gerenciamento de Usuários

*   **Buscar um usuário específico e exibir propriedades detalhadas:**
    ```powershell
    Get-ADUser -Identity "wallison.araujo" -Properties DisplayName, EmailAddress, LastLogonDate, AccountExpirationDate
    ```
*   **Listar todos os usuários ativos de uma Unidade Organizacional (OU) específica:**
    ```powershell
    Get-ADUser -Filter "Enabled -eq 'True'" -SearchBase "OU=Usuarios,OU=Empresa,DC=dominio,DC=local"
    ```
*   **Criar um novo usuário básico:**
    ```powershell
    New-ADUser -Name "João Silva" -SamAccountName "joao.silva" -UserPrincipalName "joao.silva@dominio.local" -Description "Analista de TI" -Enabled $true -Path "OU=Usuarios,OU=Empresa,DC=dominio,DC=local"
    ```
*   **Desabilitar a conta de um usuário:**
    ```powershell
    Disable-ADAccount -Identity "joao.silva"
    ```
*   **Habilitar a conta de um usuário:**
    ```powershell
    Enable-ADAccount -Identity "joao.silva"
    ```

---

## 🔒 Senhas e Bloqueios de Conta

*   **Desbloquear uma conta de usuário (bloqueada por excesso de tentativas):**
    ```powershell
    Unlock-ADAccount -Identity "joao.silva"
    ```
*   **Verificar se uma conta está bloqueada no momento:**
    ```powershell
    Get-ADUser -Identity "joao.silva" -Properties LockedOut | Select-Object Name, LockedOut
    ```
*   **Resetar a senha de um usuário (solicitando nova senha no próximo logon):**
    ```powershell
    Set-ADAccountPassword -Identity "joao.silva" -Reset -NewPassword (Read-Host -AsSecureString "Digite a nova senha")
    Set-ADUser -Identity "joao.silva" -ChangePasswordAtLogon $true
    ```

---

## 👥 Gerenciamento de Grupos de Segurança

*   **Adicionar um usuário a um grupo de segurança:**
    ```powershell
    Add-ADGroupMember -Identity "Grupo_VPN_Acesso" -Members "joao.silva"
    ```
*   **Remover um usuário de um grupo:**
    ```powershell
    Remove-ADGroupMember -Identity "Grupo_VPN_Acesso" -Members "joao.silva" -Confirm:$false
    ```
*   **Listar todos os membros de um grupo:**
    ```powershell
    Get-ADGroupMember -Identity "Grupo_VPN_Acesso" | Select-Object Name, SamAccountName
    ```

---

## 🛡️ Auditorias de Segurança e Limpeza do AD

*   **Encontrar contas de usuários inativas (sem logon nos últimos 90 dias):**
    ```powershell
    $Limiar = (Get-Date).AddDays(-90)
    Search-ADAccount -AccountInactive -TimeSpan 90.00:00:00 -UsersOnly | Select-Object Name, SamAccountName, LastLogonDate
    ```
*   **Encontrar senhas que nunca expiram (Risco de Segurança):**
    ```powershell
    Get-ADUser -Filter "PasswordNeverExpires -eq 'True' -and Enabled -eq 'True'" -Properties PasswordNeverExpires | Select-Object Name, SamAccountName
    ```
*   **Localizar contas de computadores inativas (desconectados há mais de 120 dias):**
    ```powershell
    Search-ADAccount -AccountInactive -TimeSpan 120.00:00:00 -ComputersOnly | Select-Object Name, SamAccountName, LastLogonDate
    ```

---

## 🖥️ Computadores e OUs

*   **Mover um computador para uma Unidade Organizacional (OU) específica:**
    ```powershell
    Move-ADObject -Identity (Get-ADComputer -Identity "DESKTOP-ABC01").DistinguishedName -TargetPath "OU=Desktops,OU=Computadores,DC=dominio,DC=local"
    ```
*   **Buscar sistemas operacionais de todos os computadores da rede:**
    ```powershell
    Get-ADComputer -Filter * -Properties OperatingSystem | Group-Object OperatingSystem -NoElement
    ```
