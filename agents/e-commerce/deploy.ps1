<#
    指令：.\deploy.ps1 [-dev | -qa | -prod
    Write-Host
    警示：-ForegroundColor Red
    成功：-ForegroundColor Green
    輸出：-ForegroundColor Gray
    執行：-ForegroundColor Cyan
#>

param(
    [switch]$dev,
    [switch]$qa,
    [switch]$prod
)

$environment = ""
$envVarsDict = @{}

# 本機執行Docker
function Dev-Run-Docker {
    Write-Host "Check docker status" -ForegroundColor Cyan
    $dockerOutput = & docker info 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Docker is not installed or not running." -ForegroundColor Red
        exit 1
    }
    else {
        Write-Host "Docker is running." -ForegroundColor Green
    }

    $agent = "e-commerce-agent"
    Write-Host "Agent: $agent" -ForegroundColor Gray

    $port = 8080
    Write-Host "Port: $port" -ForegroundColor Gray

    # 執行 Docker build
    Write-Host "Docker build" -ForegroundColor Cyan
    docker build -t "$agent`:latest" .

    # 執行 Docker run
    Write-Host "Docker run" -ForegroundColor Cyan
    docker run -p ${port}:${port} -e ENV=$environment "$agent`:latest"
}

# 從環境文件中讀取變數到字典
function Read-EnvFile {
    param(
        [Parameter(Mandatory = $true)]
        [string]$filePath
    )
    
    Write-Host "Read file:$filePath " -ForegroundColor Gray
    if (Test-Path $filePath) {
        $envContent = Get-Content $filePath | Where-Object { $_ -notmatch '^\s*#' -and $_ -match '\S' }
        
        foreach ($line in $envContent) {
            $parts = $line -split '=', 2
            if ($parts.Count -eq 2) {
                $key = $parts[0].Trim()
                $value = $parts[1].Trim()
                $envVarsDict[$key] = $value
            }
        }
        
        Write-Host "Successfully loaded variables from $filePath" -ForegroundColor Green
    }
    else {
        Write-Host "Warning: $filePath file not found" -ForegroundColor Yellow
    }
}

try {
    if ($dev) { 
        $environment = "dev"
    }
    if ($qa) {
        $environment = "qa"
    }
    if ($prod) {
        $environment = "prod"
    }

    Write-Host "Environment: $environment"
    $envVarsDict["ENV"] = $environment

    if ($environment -eq "") {
        Write-Host "Usage: .\deploy.ps1 [-dev | -qa | -prod]" -ForegroundColor Red
        exit 1
    }
    
    if ($environment -eq "dev") {
        Dev-Run-Docker
        return
    }
    
    # 讀取共用的 .env
    $envPath = ".\.env"
    Read-EnvFile -filePath $envPath

    $envPath = ".\.env.$environment"
    Read-EnvFile -filePath $envPath

    Write-Host "Environment Variables"
    Write-Host ($envVarsDict | ConvertTo-Json) -ForegroundColor Gray
    
    $projectId = $envVarsDict["GOOGLE_CLOUD_PROJECT"]
    Write-Host "ProjectId: $projectId"
    
    $location = $envVarsDict["GOOGLE_CLOUD_LOCATION"]
    Write-Host "Location: $location" 

    Write-Host "Cloud run deploy" -ForegroundColor Cyan
    $envVarsString = (
        $envVarsDict.GetEnumerator() |
        ForEach-Object { "$($_.Key)=$($_.Value)" } |
        Sort-Object
    ) -join ','
    
    gcloud run deploy e-commerce-agent-service `
        --source . `
        --region $location `
        --project $projectId `
        --allow-unauthenticated `
        --set-env-vars="$envVarsString"

    # gcloud run deploy e-commerce-agent-service --source . --region $location --project $projectId --allow-unauthenticated --set-env-vars="ENV=qa,SHOP_ID=2,GOOGLE_GENAI_USE_VERTEXAI=1,GOOGLE_CLOUD_PROJECT=arch-qa-454806,GOOGLE_CLOUD_LOCATION=us-central1,ROOT_AGENT_MODEL=gemini-2.0-flash-001,COMPLAINT_AGENT_MODEL=gemini-2.0-flash-001,ORDER_AGENT_MODEL=gemini-2.0-flash-001,FAQ_AGENT_MODEL=gemini-2.0-flash-001"
    
}
catch {
    Write-Host $_ -ForegroundColor Red
}
finally {

}