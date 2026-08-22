param()

$python = Get-Command py -ErrorAction SilentlyContinue
if ($null -ne $python) {
    py -m leadgen.cli init
    exit $LASTEXITCODE
}

Write-Host "Python launcher not found. Install Python or use Docker."
Write-Host "To use Docker: run `docker compose build tool`"
Write-Host "Then run `docker compose run --rm tool init`"
exit 1
