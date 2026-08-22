param()

$root = Resolve-Path ..\
Set-Location $root

$python = Get-Command py -ErrorAction SilentlyContinue
$docker = Get-Command docker -ErrorAction SilentlyContinue

if ($null -ne $python) {
    py -m pytest -q
    exit $LASTEXITCODE
}

if ($null -ne $docker) {
    docker compose run --rm tool pytest -q
    exit $LASTEXITCODE
}

Write-Host "Neither Python nor Docker are available. Install one and rerun this script."
exit 1
