from typing import Any
import subprocess
from pathlib import Path
import os
from mcp.server.fastmcp import FastMCP

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

mcp = FastMCP("locust")

@mcp.tool(name="run_locust", description="Run Locust with the given configuration.")
async def run_locust(test_file: str, host: str = os.getenv("LOCUST_HOST", "http://localhost:8089"), 
                    users: int = int(os.getenv("LOCUST_USERS", "100")), 
                    spawn_rate: int = int(os.getenv("LOCUST_SPAWN_RATE", "10")), 
                    runtime: str = os.getenv("LOCUST_RUNTIME", "30s"), 
                    headless: bool = os.getenv("LOCUST_HEADLESS", "true").lower() == "true") -> Any:
    """
    Run Locust with the given configuration.
    
    Args:
        test_file: Path to the Locust test file
        host: Target host URL to load test
        users: Number of concurrent users to simulate
        spawn_rate: Rate at which users are spawned per second
        runtime: Duration of the test (e.g., "30s", "1m", "5m")
        headless: Whether to run in headless mode (no web UI)
    """
    locust_bin = os.getenv("LOCUST_BIN", "locust")
    cmd = [locust_bin, "-f", test_file, "--host", host]
    
    if headless:
        cmd.extend(["--headless"])
        cmd.extend(["-u", str(users)])
        cmd.extend(["-r", str(spawn_rate)])
        cmd.extend(["-t", runtime])
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {
            "status": "success",
            "output": result.stdout,
            "error": result.stderr
        }
    except subprocess.CalledProcessError as e:
        return {
            "status": "error",
            "output": e.stdout,
            "error": e.stderr
        }
    
if __name__ == "__main__":
    mcp.run(transport="stdio")