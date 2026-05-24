<#
.SYNOPSIS
    Script de Backup Automático de Switches Aruba via PowerShell e SSH nativo.
.DESCRIPTION
    Conecta ao Switch Aruba (ArubaOS-S ou ArubaOS-CX), solicita a configuração 
    ativa e salva o resultado em um arquivo de texto local com a data atual.
    Utiliza o cliente SSH nativo do Windows (OpenSSH).
.NOTES
    Autor: Wallison Araujo (WallisonWS)
#>

# --- CONFIGURAÇÕES DO SWITCH ---
$SwitchIP   = "192.168.1.2"          # IP do Switch Aruba
$Username   = "admin"                # Usuário SSH do Switch
$BackupDir  = ".\backups\aruba"      # Pasta de destino dos backups
# ------------------------------

# Cria a pasta de backups se não existir
if (-not (Test-Path $BackupDir)) {
    New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
    Write-Host "📁 Pasta de backup criada em: $BackupDir" -ForegroundColor Green
}

# Define o nome do arquivo com a data e hora atual
$Timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$OutputFile = Join-Path $BackupDir "aruba_switch_backup_$Timestamp.cfg"

Write-Host "⚡ Conectando ao Switch Aruba ($SwitchIP) via SSH..." -ForegroundColor Cyan

try {
    # Para automação total sem interrupção de senha, você deve configurar autenticação de chave SSH (SSH Key)
    # ou usar ferramentas como 'plink.exe' (do PuTTY) caso queira embutir a senha em texto claro:
    # Exemplo com plink: plink.exe -ssh -l $Username -pw "SuaSenha" $SwitchIP "show running-config"
    
    # Abaixo está a chamada usando o cliente SSH padrão do Windows (OpenSSH):
    # Nota: Se chaves SSH não estiverem configuradas, o prompt do SSH solicitará a senha interativamente no terminal.
    
    $SshCommand = "show running-config"
    
    # Roda o comando SSH nativo redirecionando o output para o arquivo de destino
    ssh -o StrictHostKeyChecking=no "$Username`@$SwitchIP" "$SshCommand" | Out-File -FilePath $OutputFile -Encoding utf8
    
    # Verifica se o arquivo foi criado e possui conteúdo
    if ((Test-Path $OutputFile) -and ((Get-Item $OutputFile).Length -gt 100)) {
        Write-Host "✅ Backup concluído com sucesso!" -ForegroundColor Green
        Write-Host "📄 Arquivo salvo em: $OutputFile" -ForegroundColor Yellow
    } else {
        Write-Host "⚠️ O backup foi gerado mas parece estar vazio ou muito pequeno. Verifique se a conexão SSH funcionou." -ForegroundColor Warning
    }
}
catch {
    Write-Host "❌ Ocorreu um erro ao tentar realizar o backup: $_" -ForegroundColor Red
}
