# =====================================================
# GXP (Guided eXecution Protocol) Profile Snippet
# =====================================================
#
# Copy the line below into your PowerShell profile
# ($PROFILE) to make GXP commands available in every session.
#
# . "C:\path\to\gxp\adapters\grok\ai-workflow\gxp.ps1"
#
# Then reload your profile with:
# . $PROFILE
# =====================================================

$gxpPath = "C:\path\to\gxp\adapters\grok\ai-workflow\gxp.ps1"

if (Test-Path $gxpPath) {
    . $gxpPath
} else {
    Write-Warning "GXP helper not found at $gxpPath. Update the path in your profile."
}
