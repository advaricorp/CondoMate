import pytest
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama for colored output
init()

def test_health_endpoint(client):
    """Test the health endpoint with colored progress bar."""
    progress_bar = tqdm(total=3, desc=f"{Fore.CYAN}Testing endpoint accessibility{Style.RESET_ALL}")
    
    # Test 1: Check if endpoint is accessible
    response = client.get("/api/v1/health/")
    assert response.status_code == 200
    progress_bar.update(1)
    
    # Test 2: Check response format
    data = response.json()
    assert "status" in data
    assert "services" in data
    assert "version" in data
    progress_bar.update(1)
    
    # Test 3: Check service statuses
    services = data["services"]
    assert "database" in services
    assert "api" in services
    assert services["database"] == "healthy"
    assert services["api"] == "healthy"
    progress_bar.update(1)
    
    progress_bar.close()

def test_health_endpoint_without_trailing_slash(client):
    """Test the health endpoint without trailing slash."""
    progress_bar = tqdm(total=1, desc=f"{Fore.CYAN}Testing redirect{Style.RESET_ALL}")
    
    response = client.get("/api/v1/health", follow_redirects=True)
    assert response.status_code == 200
    progress_bar.update(1)
    
    progress_bar.close()

if __name__ == "__main__":
    pytest.main(["-v", __file__]) 