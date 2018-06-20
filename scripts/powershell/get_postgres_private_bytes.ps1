$value = Get-Process -name "postgres" | Measure-Object -Property 'PrivateMemorySize' -Sum | select sum
Write-Host("{0}" -f [math]::Truncate($value.Sum))