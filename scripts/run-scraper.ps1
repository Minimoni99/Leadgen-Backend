param()

$root = Resolve-Path ..\
Set-Location $root

if (-not (Test-Path -Path ".env")) {
    Write-Host ".env file not found. Copy .env.example to .env and configure scraper/proxy settings."
    exit 1
}

$env = @{}
Get-Content .env | ForEach-Object {
    if ($_ -match '^(\s*#|\s*$)') { return }
    $parts = $_ -split('=', 2)
    if ($parts.Count -eq 2) {
        $env[$parts[0].Trim()] = $parts[1].Trim()
    }
}

function Get-EnvValue($name, $default) {
    if ($env.ContainsKey($name) -and $env[$name]) { return $env[$name] }
    return $default
}

$scraperImage = Get-EnvValue 'SCRAPER_IMAGE' 'gosom/google-maps-scraper:latest'
$outputDir = Get-EnvValue 'SCRAPER_OUTPUT_DIR' 'output'
$depth = Get-EnvValue 'SCRAPER_DEPTH' '1'
$concurrency = Get-EnvValue 'SCRAPER_CONCURRENCY' '2'
$emailFlag = Get-EnvValue 'SCRAPER_EMAIL' 'false'
$exitInactivity = Get-EnvValue 'SCRAPER_EXIT_INACTIVITY' '3m'
$proxyFile = Get-EnvValue 'PROXY_FILE' ''
$proxyList = Get-EnvValue 'PROXIES' ''
$proxyProtocol = Get-EnvValue 'PROXY_PROTOCOL' 'http'
$proxyHost = Get-EnvValue 'PROXY_HOST' ''
$proxyPort = Get-EnvValue 'PROXY_PORT' ''
$proxyUser = Get-EnvValue 'PROXY_USER' ''
$proxyPass = Get-EnvValue 'PROXY_PASS' ''

$proxyArgs = @()
if ($proxyFile) {
    if (-not (Test-Path -Path $proxyFile)) {
        Write-Host "Proxy file '$proxyFile' not found."
        exit 1
    }
    $proxyArgs += '-proxies-file'
    $proxyArgs += '/proxies.txt'
} elseif ($proxyList) {
    $proxyArgs += '-proxies'
    $proxyArgs += $proxyList
} elseif ($proxyHost) {
    if (-not $proxyPort) {
        Write-Host "PROXY_PORT is required when PROXY_HOST is set."
        exit 1
    }
    $proxyArgs += '-proxies'
    if ($proxyUser -and $proxyPass) {
        $proxyArgs += "$proxyProtocol://$proxyUser:$proxyPass@$proxyHost:$proxyPort"
    } else {
        $proxyArgs += "$proxyProtocol://$proxyHost:$proxyPort"
    }
}

if (-not (Test-Path -Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir | Out-Null
}

$queryFile = Join-Path $PWD 'seeds\queries.txt'
if (-not (Test-Path -Path $queryFile)) {
    Write-Host "Seed query file not found: $queryFile"
    exit 1
}

$outFile = Join-Path $PWD "$outputDir\scraper-results.csv"

$volumeArgs = @(
    '-v', "$PWD/seeds/queries.txt:/queries.txt:ro",
    '-v', "$PWD/$outputDir:/out"
)
if ($proxyFile) {
    $volumeArgs += '-v'
    $volumeArgs += "$PWD/$proxyFile:/proxies.txt:ro"
}

$dockerArgs = @('run', '--rm') + $volumeArgs + @(
    $scraperImage,
    '-input', '/queries.txt',
    '-results', '/out/scraper-results.csv',
    '-depth', $depth,
    '-c', $concurrency,
    '-exit-on-inactivity', $exitInactivity
)

if ($emailFlag -eq 'true') {
    $dockerArgs += '-email'
}
if ($proxyArgs.Count -gt 0) {
    $dockerArgs += $proxyArgs
}

Write-Host "Running scraper container: $scraperImage"
Write-Host "Output file: $outFile"

docker @dockerArgs
