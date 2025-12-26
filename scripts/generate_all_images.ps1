# Generate all mythological figure images sequentially
# This prevents Cloud Run timeout issues by making individual requests

$baseUrl = "https://etymython-mnovne7bma-uc.a.run.app"

Write-Host "Fetching list of figures..." -ForegroundColor Cyan
$figures = Invoke-RestMethod -Uri "$baseUrl/api/v1/images/available-figures" -Method Get
$figureNames = $figures.figures

Write-Host "Found $($figureNames.Count) figures to generate" -ForegroundColor Green
Write-Host "Checking which ones already have images..." -ForegroundColor Cyan

$existing = Invoke-RestMethod -Uri "$baseUrl/api/v1/images/generated" -Method Get
$existingNames = $existing | ForEach-Object { $_.figure_name }

Write-Host "Already generated: $($existingNames.Count)" -ForegroundColor Yellow

$remaining = $figureNames | Where-Object { $_ -notin $existingNames }
Write-Host "`nRemaining to generate: $($remaining.Count)" -ForegroundColor Cyan
Write-Host "Estimated cost: `$$([math]::Round($remaining.Count * 0.04, 2))" -ForegroundColor Yellow
Write-Host "Estimated time: $([math]::Round($remaining.Count * 3 / 60, 1)) minutes`n" -ForegroundColor Yellow

$completed = 0
$failed = 0

foreach ($figureName in $remaining) {
    $completed++
    $percent = [math]::Round(($completed / $remaining.Count) * 100, 1)
    
    Write-Host "[$completed/$($remaining.Count)] ($percent%) Generating: $figureName..." -ForegroundColor Cyan
    
    try {
        $result = Invoke-RestMethod -Uri "$baseUrl/api/v1/images/generate/$figureName" -Method Post -ContentType "application/json"
        
        if ($result.success) {
            Write-Host "  ✓ Success" -ForegroundColor Green
        } else {
            Write-Host "  ✗ Failed: $($result.error)" -ForegroundColor Red
            $failed++
        }
    } catch {
        Write-Host "  ✗ Error: $($_.Exception.Message)" -ForegroundColor Red
        $failed++
    }
    
    # Small delay to avoid rate limiting
    Start-Sleep -Seconds 1
}

Write-Host "`n========================================" -ForegroundColor Green
Write-Host "Generation Complete!" -ForegroundColor Green
Write-Host "Total processed: $completed" -ForegroundColor White
Write-Host "Successful: $($completed - $failed)" -ForegroundColor Green
Write-Host "Failed: $failed" -ForegroundColor Red
Write-Host "========================================`n" -ForegroundColor Green

Write-Host "View your gallery at: $baseUrl/app" -ForegroundColor Cyan
