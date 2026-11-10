param(
    [string]$Python = "python",
    [int]$TimeoutSeconds = 600
)

$ErrorActionPreference = "Stop"
$testFiles = @(Get-ChildItem tests/test_*.py | Sort-Object Name | ForEach-Object { $_.FullName })
$failedFiles = @()

foreach ($testFile in $testFiles) {
    Write-Host "::group::$testFile"
    $process = Start-Process -FilePath $Python -ArgumentList @("-m", "pytest", "-q", "`"$testFile`"") -NoNewWindow -PassThru
    $null = $process.Handle  # cache the handle so ExitCode is readable after exit
    if ($process.WaitForExit($TimeoutSeconds * 1000)) {
        $testExitCode = $process.ExitCode
    }
    else {
        # A hung file (e.g. a modal dialog) must not stall the whole run.
        & taskkill /T /F /PID $process.Id | Out-Null
        $testExitCode = "timeout after ${TimeoutSeconds}s"
    }
    Write-Host "::endgroup::"

    if ($testExitCode -ne 0) {
        $failedFiles += $testFile
        Write-Host "$testFile failed: $testExitCode"
    }
}

if ($failedFiles.Count -gt 0) {
    throw "Failing test files: $($failedFiles -join ', ')"
}
