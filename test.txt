function Generate-ParameterBlackoutLogo {
    param(
      [string]$Text = "Parameter Blackout",
      [int]$Width = 40,
      [int]$Height = 10
    )
  
    # Calculate padding for centering the text
    $padding = [Math]::Floor(($Width - $Text.Length) / 2)
  
    # Build the logo string
    $logo = ""
    for ($i = 0; $i -lt $Height; $i++) {
      if ($i -eq [Math]::Floor($Height / 2)) { # Middle row for text
        $logo += " " * $padding + $Text + " " * $padding + "`n"
      } else {
        $logo += "*" * $Width + "`n" # Border rows
      }
    }
  
    return $logo
  }
  
  # Display the logo
  $logo = Generate-ParameterBlackoutLogo
  Write-Host $logo
  

  $customLogo = Generate-ParameterBlackoutLogo -Text "PARAMETER BLACKOUT" -Width 50 -Height 12
  Write-Host $customLogo
  
##############################################################################################################  
  
# Define file paths
$inputFile = "C:\Users\GlitchAnand\Desktop\Programs\ParameterBlackout-powershell\log.txt"
$outputFile = "C:\Users\GlitchAnand\Desktop\Programs\ParameterBlackout-powershell\op.txt"
$sensitiveFile = "C:\Users\GlitchAnand  \Desktop\Programs\ParameterBlackout-powershell\mask_string.txt"

# Regular expressions for sensitive data (pre-compiled for performance)
$patterns = @{
    "IP Addresses"        = [regex]::new('\b(?:\d{1,3}\.){3}\d{1,3}\b', "Compiled")
    "Email IDs"           = [regex]::new('\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b', "Compiled, IgnoreCase")
    #"Hostnames"           = [regex]::new('\b(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,6}\b', "Compiled, IgnoreCase")
    "Credit Card Numbers" = [regex]::new('\b(?:\d[ -]*?){13,19}\b', "Compiled")
    "Account Numbers"     = [regex]::new('\b\d{8,16}\b', "Compiled")
    #Change the domain name. For example: Domain\GlitchAnand --> Domain\Masked
    "Domain Usernames"      = [regex]::new('\b(Domain[\\/])([A-Za-z0-9._-]+)\b', "Compiled")
}


$sensitiveStrings = Get-Content $sensitiveFile | Where-Object { $_ -match '\S' } | ForEach-Object { $_.Trim() }

# Open file streams
$reader = [System.IO.StreamReader]::new($inputFile)
$writer = [System.IO.StreamWriter]::new($outputFile)
$buffer = @()  # Buffer for storing masked lines before writing
$bufferSize = 1000  # Number of lines to buffer before writing
$lineNumber = 0  # Track line numbers

try {
    while ($null -ne ($line = $reader.ReadLine())) {
        $lineNumber++
        $originalLine = $line  # Save original line before modifications
        $masked = $false  # Flag to track if this line is modified

        # Mask predefined sensitive patterns
        foreach ($key in $patterns.Keys) {
            if ($patterns[$key].IsMatch($line)) {
                #Change the domain name.
                if ($key -eq "Domain Usernames") {
                    $line = $patterns[$key].Replace($line, '$1MASKED')
                } elseif ($patterns["Email IDs"].IsMatch($line)) {
                    #Write-Output "Before Masking: $line"
                    # Replace the entire email with 'MASKEDEMAIL'
                    $line = $patterns["Email IDs"].Replace($line, 'MASKEDEMAIL')
                    #Write-Output "After Masking: $line"
                } else {
                    $line = $patterns[$key].Replace($line, 'MASKED')
                }
                Write-Output "Possible $key found. Masking in line number $lineNumber"
                $masked = $true
            }
        }

        # Mask strings from "tomask.txt"
        foreach ($sensitive in $sensitiveStrings) {
            $escapedSensitive = [regex]::Escape($sensitive)  # Ensure safe replacement

            #if ($sensitive -match '=$' -or $sensitive -match '=\S   *$') 
            if ($sensitive -match '=$'){
                # Mask only the value after '='
                $regex = [regex]::new("($escapedSensitive)\s*(\S+)", "Compiled")
                if ($regex.IsMatch($line)) {
                    $line = $regex.Replace($line, "$sensitive MASKED")
                    Write-Output "Possible sensitive assignment ($sensitive) found. Masking in line number $lineNumber"
                    $masked = $true
                }
            } else {
                # Mask the entire occurrence of the sensitive string
                $regex = [regex]::new($escapedSensitive, "Compiled")
                if ($regex.IsMatch($line)) {
                    $line = $regex.Replace($line, "MASKED")
                    Write-Output "Possible sensitive keyword ($sensitive) found. Masking in line number $lineNumber"
                    $masked = $true
                }
            }
        }

        # Add to buffer
        $buffer += $line
        if ($buffer.Count -ge $bufferSize) {
            $writer.WriteLine($buffer -join "n")
            $buffer = @()  # Clear buffer
        }
    }

    # Write remaining buffer
    if ($buffer.Count -gt 0) {
        $writer.WriteLine($buffer -join "`n")
    }

} catch {
    Write-Error "An error occurred: $_"
} finally {
    $reader.Close()
    $writer.Close()
}

Write-Output "Masking completed. Output saved to: $outputFile"