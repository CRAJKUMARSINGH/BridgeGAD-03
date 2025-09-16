# Test All Bridge Applications Script
# Created: 16-Sep-2025
# Purpose: Test and run all Bridge* applications systematically

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "BRIDGE APPLICATIONS TESTING SCRIPT" -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

$apps = @(
    "BridgeGAD-00", "BridgeGAD-01", "BridgeGAD-02", "BridgeGAD-03", 
    "BridgeGAD-04", "BridgeGAD-05", "BridgeGAD-06", "BridgeGAD-07",
    "BridgeGAD-08", "BridgeGAD-09", "BridgeGAD-10", "BridgeGAD-11",
    "BridgeGAD-12", "Bridge-Causeway-Design", "BridgeDraw", "Bridge_Slab_Design"
)

$baseDir = "C:\Users\Rajkumar"
$currentPort = 8510

foreach ($app in $apps) {
    $appPath = Join-Path $baseDir $app
    
    Write-Host "`n----------------------------------------" -ForegroundColor Yellow
    Write-Host "Testing: $app" -ForegroundColor Yellow
    Write-Host "Path: $appPath" -ForegroundColor Gray
    
    if (Test-Path $appPath) {
        Set-Location $appPath
        
        # Check for main Python files
        $pythonFiles = @("app.py", "streamlit_app.py", "enhanced_bridge_app.py", "main.py")
        $foundFile = $null
        
        foreach ($file in $pythonFiles) {
            if (Test-Path $file) {
                $foundFile = $file
                break
            }
        }
        
        if ($foundFile) {
            Write-Host "Found main file: $foundFile" -ForegroundColor Green
            
            # Check for requirements.txt
            if (Test-Path "requirements.txt") {
                Write-Host "Installing dependencies..." -ForegroundColor Cyan
                pip install -r requirements.txt -q
            }
            
            # Try to run the app
            Write-Host "Starting $foundFile on port $currentPort..." -ForegroundColor Cyan
            Start-Process PowerShell -ArgumentList "-Command", "cd '$appPath'; streamlit run $foundFile --server.port $currentPort" -WindowStyle Minimized
            
            $currentPort++
            Start-Sleep 2
        } else {
            Write-Host "No main Python file found" -ForegroundColor Red
        }
        
        # List directory contents
        Write-Host "Directory contents:" -ForegroundColor Gray
        Get-ChildItem | Format-Table Name, Length -AutoSize | Out-String | Write-Host
        
    } else {
        Write-Host "Directory not found!" -ForegroundColor Red
    }
}

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "TESTING COMPLETE" -ForegroundColor Cyan
Write-Host "Check http://localhost:8510+ for running apps" -ForegroundColor Green
Write-Host "=========================================" -ForegroundColor Cyan