$port = 8000
$tcp = Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue
if ($tcp) {
    foreach ($conn in $tcp) {
        try {
            echo "Killing process $($conn.OwningProcess) on port $port..."
            Stop-Process -Id $conn.OwningProcess -Force -ErrorAction SilentlyContinue
        } catch {
            echo "Could not kill process $($conn.OwningProcess). It might verify be already dead or requiring admin rights."
        }
    }
    echo "Clean up attempt finished for port $port."
} else {
    echo "No process found on port $port. standard_port_check: Clean."
}
