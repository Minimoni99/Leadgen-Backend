param()

$root = Resolve-Path ..\
Set-Location $root

$python = Get-Command py -ErrorAction SilentlyContinue
if ($null -ne $python) {
    py -m pip install -e .
}

$docker = Get-Command docker -ErrorAction SilentlyContinue
if ($null -ne $docker) {
    docker compose build tool
    docker compose up -d db
    docker compose run --rm tool init
    Write-Host "Bootstrap complete. Use `docker compose run --rm tool seed` and `docker compose run --rm tool import <csv>` next."
    exit 0
}

if ($null -ne $python) {
    Write-Host "Docker not found. Running local Python package commands."
    py -m leadgen.cli init
    Write-Host "Bootstrap complete. Use `py -m leadgen.cli seed` and `py -m leadgen.cli import <csv>` next."
    exit 0
}

Write-Host "Neither Docker nor Python are available. Install one and rerun this script."
exit 1
