# Sync database figures with generated images
# Adds missing heroes/mortals and updates Uranus->Ouranos

$baseUrl = "https://etymython-mnovne7bma-uc.a.run.app"

$missingFigures = @(
    @{ greek_name = "Αχιλλέας"; english_name = "Achilles"; figure_type = "Hero"; description = "Greatest warrior of the Trojan War"; domain = "warfare, heroism"; symbols = "heel, armor, spear" }
    @{ greek_name = "Κασσάνδρα"; english_name = "Cassandra"; figure_type = "Mortal"; description = "Trojan princess cursed with prophecy never believed"; domain = "prophecy, tragedy"; symbols = "laurel, flames of Troy" }
    @{ greek_name = "Εκάτη"; english_name = "Hecate"; figure_type = "Deity"; description = "Goddess of magic, crossroads, and the moon"; domain = "magic, witchcraft, crossroads"; symbols = "torch, keys, dogs" }
    @{ greek_name = "Ηρακλής"; english_name = "Heracles"; figure_type = "Hero"; description = "Greatest of Greek heroes, son of Zeus"; domain = "strength, heroism"; symbols = "lion skin, club, twelve labors" }
    @{ greek_name = "Ιάσων"; english_name = "Jason"; figure_type = "Hero"; description = "Leader of the Argonauts"; domain = "adventure, leadership"; symbols = "Golden Fleece, ship Argo" }
    @{ greek_name = "Μέδουσα"; english_name = "Medusa"; figure_type = "Mortal"; description = "Gorgon whose gaze turns mortals to stone"; domain = "transformation, monstrosity"; symbols = "serpent hair, petrifying gaze" }
    @{ greek_name = "Οδυσσέας"; english_name = "Odysseus"; figure_type = "Hero"; description = "Cunning hero of the Odyssey"; domain = "cunning, adventure"; symbols = "bow, Trojan horse, ship" }
    @{ greek_name = "Ορφέας"; english_name = "Orpheus"; figure_type = "Mortal"; description = "Legendary musician and poet"; domain = "music, poetry"; symbols = "lyre, music" }
    @{ greek_name = "Περσεφόνη"; english_name = "Persephone"; figure_type = "Olympian"; description = "Queen of the underworld and goddess of spring"; domain = "spring, underworld"; symbols = "pomegranate, flowers, torch" }
    @{ greek_name = "Θησεύς"; english_name = "Theseus"; figure_type = "Hero"; description = "Athenian hero who defeated the Minotaur"; domain = "heroism, leadership"; symbols = "thread, labyrinth, sword" }
    @{ greek_name = "Τύχη"; english_name = "Tyche"; figure_type = "Deity"; description = "Goddess of fortune and prosperity"; domain = "fortune, luck, prosperity"; symbols = "cornucopia, wheel, rudder" }
)

Write-Host "Adding missing figures to database..." -ForegroundColor Cyan

foreach ($figure in $missingFigures) {
    Write-Host "  Adding $($figure.english_name)..." -ForegroundColor Yellow
    try {
        $body = @{
            greek_name = $figure.greek_name
            english_name = $figure.english_name
            figure_type = $figure.figure_type
            description = $figure.description
            domain = $figure.domain
            symbols = $figure.symbols
            role = ""
        } | ConvertTo-Json
        
        $result = Invoke-RestMethod -Uri "$baseUrl/api/v1/figures" -Method Post -Body $body -ContentType "application/json" -ErrorAction Stop
        Write-Host "    ✓ Added (ID: $($result.id))" -ForegroundColor Green
    } catch {
        Write-Host "    ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

# Fix Uranus->Ouranos if needed
Write-Host "`nChecking for Uranus/Ouranos mismatch..." -ForegroundColor Cyan
$figures = Invoke-RestMethod -Uri "$baseUrl/api/v1/figures" -Method Get
$uranus = $figures | Where-Object { $_.english_name -eq "Uranus" }
if ($uranus) {
    Write-Host "  Found Uranus (ID: $($uranus.id)), updating to Ouranos..." -ForegroundColor Yellow
    $body = @{
        english_name = "Ouranos"
        greek_name = "Ουρανός"
    } | ConvertTo-Json
    
    try {
        Invoke-RestMethod -Uri "$baseUrl/api/v1/figures/$($uranus.id)" -Method Put -Body $body -ContentType "application/json"
        Write-Host "    ✓ Updated Uranus → Ouranos" -ForegroundColor Green
    } catch {
        Write-Host "    ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
    }
}

Write-Host "`n✓ Database sync complete!" -ForegroundColor Green
Write-Host "Refresh https://etymython-mnovne7bma-uc.a.run.app/app to see all images" -ForegroundColor Cyan
