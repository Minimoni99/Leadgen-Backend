param()

Write-Host "This script will help you add Evomi (or other) proxy credentials to .env in this repo."
Write-Host "It runs locally and does NOT send credentials anywhere. Keep .env out of version control."

$envPath = Join-Path $PSScriptRoot "..\..\.env"
if (-not (Test-Path -Path $envPath)) {
    Write-Host "Creating new .env file at $envPath"
    New-Item -ItemType File -Path $envPath | Out-Null
}

function set-env-value($key, $value) {
    $content = Get-Content -Path $envPath -ErrorAction SilentlyContinue
    if ($content -eq $null) { $content = @() }
    $existingIndex = $null
    for ($i = 0; $i -lt $content.Count; $i++) {
        if ($content[$i] -match "^$key=") { $existingIndex = $i; break }
    }
    if ($existingIndex -ne $null) {
        $content[$existingIndex] = "$key=$value"
    } else {
        $content += "$key=$value"
    }
    $content | Set-Content -Path $envPath -Encoding utf8
}

$host = Read-Host "Enter Evomi proxy host (e.g. eu.evomi.com)"
$port = Read-Host "Enter Evomi proxy port (e.g. 8000)"
$user = Read-Host "Enter Evomi proxy username (leave blank for none)"
$pass = Read-Host -AsSecureString "Enter Evomi proxy password (leave blank for none)"
$passPlain = ''
if ($pass) {
    $ptr = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($pass)
    $passPlain = [Runtime.InteropServices.Marshal]::PtrToStringBSTR($ptr)
    [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($ptr)
}

if ($host -and $port) {
    set-env-value "PROXY_PROTOCOL" "http"
    set-env-value "PROXY_HOST" $host
    set-env-value "PROXY_PORT" $port
    if ($user) { set-env-value "PROXY_USER" $user }
    if ($passPlain) { set-env-value "PROXY_PASS" $passPlain }
    Write-Host "Wrote proxy settings to .env (do NOT commit this file)."
    Write-Host "If you prefer a proxies file, create proxies.txt and set PROXY_FILE=proxies.txt in .env."
} else {
    Write-Host "Host and port are required. No changes made."
}

Write-Host "Done. Run scripts/run-scraper.ps1 to start the scraper using these credentials."