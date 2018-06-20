$value = Get-Process -name "FgIndexerProc" | Measure-Object -Property 'WorkingSet' -Sum | select sum
Write-Host("{0}" -f [math]::Truncate($value.Sum))