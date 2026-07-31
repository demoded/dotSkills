param(
    [Parameter(Mandatory=$false)]
    [string]$Username = "demoded",

    [Parameter(Mandatory=$false)]
    [string]$ApiKey,

    [Parameter(Mandatory=$false)]
    [string]$Period = "7day",

    [Parameter(Mandatory=$false)]
    [int]$Limit = 10,

    [Parameter(Mandatory=$false)]
    [string]$OutFile = ""
)

# Load ApiKey from .env if not provided
if ([string]::IsNullOrWhiteSpace($ApiKey)) {
    $envPath = Join-Path $env:USERPROFILE ".env"
    if (Test-Path $envPath) {
        $envVars = Get-Content $envPath | Where-Object { $_ -match '=' }
        foreach ($line in $envVars) {
            $name, $value = $line.Split('=', 2)
            if ($name.Trim() -eq "LASTFM_API_KEY") {
                $ApiKey = $value.Trim()
            }
        }
    }
}

if ([string]::IsNullOrWhiteSpace($ApiKey)) {
    Write-Error "LASTFM_API_KEY not found in $envPath and not provided as argument."
    exit 1
}

# Build the Last.fm API URL
$url = "https://ws.audioscrobbler.com/2.0/?method=user.getTopAlbums&user=$Username&period=$Period&limit=$Limit&api_key=$ApiKey&format=json"

try {
    # Use Invoke-WebRequest to get raw response content, preserving UTF-8 encoding
    # (Invoke-RestMethod + ConvertTo-Json re-encodes and mangles non-ASCII characters)
    $response = Invoke-WebRequest -Uri $url -UseBasicParsing -ErrorAction Stop

    if ([string]::IsNullOrWhiteSpace($OutFile)) {
        # Default output path alongside this script
        $OutFile = Join-Path $PSScriptRoot "lastfm_out.json"
    }

    # Write raw UTF-8 content directly — preserves Cyrillic, CJK, etc.
    [System.IO.File]::WriteAllText($OutFile, $response.Content, [System.Text.Encoding]::UTF8)
    Write-Host "Data written to: $OutFile"
}
catch {
    Write-Error "Failed to fetch Last.fm data: $_"
    exit 1
}
