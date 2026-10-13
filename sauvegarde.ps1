# Sauvegarde automatique : commit + push toutes les $Minutes minutes, sans passer par Claude
# (continue donc de tourner quand la limite d'usage coupe la session).
#   .\sauvegarde.ps1            boucle toutes les 10 min
#   .\sauvegarde.ps1 -Once      une seule sauvegarde
# Un fichier d'extraction en cours d'ecriture peut etre pris a moitie : sans gravite, la sauvegarde
# suivante le remplace, et l'historique git garde chaque etat.
param([int]$Minutes = 10, [switch]$Once)
$g = "C:\Program Files\Git\cmd\git.exe"
Set-Location $PSScriptRoot
do {
    if (-not (Test-Path ".git\index.lock")) {   # une autre commande git tourne : on passe ce tour
        & $g add -A 2>$null
        & $g diff --cached --quiet
        if ($LASTEXITCODE -ne 0) {
            & $g commit -q -m "Sauvegarde automatique $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
            & $g push -q origin main
            "$(Get-Date -Format 'HH:mm') sauvegarde poussee : $(& $g log --oneline -1)"
        }
    }
    if (-not $Once) { Start-Sleep -Seconds ($Minutes * 60) }
} while (-not $Once)
