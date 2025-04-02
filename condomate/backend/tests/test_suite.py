import asyncio
import sys
from datetime import datetime
from typing import List, Dict, Any
import aiohttp
from tqdm import tqdm
from colorama import init, Fore, Style

# Initialize colorama for Windows support
init()

class TestSuite:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.results: List[Dict[str, Any]] = []
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    def print_header(self, text: str):
        print(f"\n{Fore.CYAN}{'='*50}")
        print(f"{text.center(50)}")
        print(f"{'='*50}{Style.RESET_ALL}\n")

    def print_result(self, test_name: str, success: bool, message: str = ""):
        status = f"{Fore.GREEN}✓ PASSED{Style.RESET_ALL}" if success else f"{Fore.RED}✗ FAILED{Style.RESET_ALL}"
        print(f"{status} - {test_name}")
        if message and not success:
            print(f"{Fore.YELLOW}  Message: {message}{Style.RESET_ALL}")

    async def test_health(self) -> bool:
        """Test the health check endpoint."""
        try:
            async with self.session.get(f"{self.base_url}/api/v1/health") as response:
                data = await response.json()
                success = response.status == 200 and data["status"] == "healthy"
                self.print_result("Health Check", success)
                return success
        except Exception as e:
            self.print_result("Health Check", False, str(e))
            return False

    async def test_auth(self) -> bool:
        """Test authentication endpoints."""
        success = True
        try:
            # Test registration
            async with self.session.post(
                f"{self.base_url}/api/v1/auth/register",
                json={
                    "email": "test@example.com",
                    "password": "testpassword123",
                    "full_name": "Test User"
                }
            ) as response:
                success &= response.status in [200, 409]  # 409 if user already exists

            # Test login
            async with self.session.post(
                f"{self.base_url}/api/v1/auth/login",
                data={"username": "test@example.com", "password": "testpassword123"}
            ) as response:
                success &= response.status == 200
                if success:
                    self.token = (await response.json())["access_token"]
                    self.session.headers.update({"Authorization": f"Bearer {self.token}"})

            self.print_result("Authentication", success)
            return success
        except Exception as e:
            self.print_result("Authentication", False, str(e))
            return False

    async def test_users(self) -> bool:
        """Test user management endpoints."""
        try:
            async with self.session.get(f"{self.base_url}/api/v1/users/me") as response:
                success = response.status == 200
                self.print_result("User Profile", success)
                return success
        except Exception as e:
            self.print_result("User Profile", False, str(e))
            return False

    async def test_payments(self) -> bool:
        """Test payment endpoints."""
        success = True
        try:
            # Test getting payments
            async with self.session.get(f"{self.base_url}/api/v1/payments") as response:
                success &= response.status == 200

            self.print_result("Payments", success)
            return success
        except Exception as e:
            self.print_result("Payments", False, str(e))
            return False

    async def test_calendar(self) -> bool:
        """Test calendar endpoints."""
        success = True
        try:
            # Test getting events
            async with self.session.get(f"{self.base_url}/api/v1/calendar") as response:
                success &= response.status == 200

            self.print_result("Calendar", success)
            return success
        except Exception as e:
            self.print_result("Calendar", False, str(e))
            return False

    async def test_documents(self) -> bool:
        """Test document endpoints."""
        success = True
        try:
            # Test getting documents
            async with self.session.get(f"{self.base_url}/api/v1/documents") as response:
                success &= response.status == 200

            self.print_result("Documents", success)
            return success
        except Exception as e:
            self.print_result("Documents", False, str(e))
            return False

    async def run_all_tests(self):
        """Run all tests with progress bars."""
        self.print_header("Starting CondoMate Test Suite")
        print(f"{Fore.CYAN}Base URL: {self.base_url}{Style.RESET_ALL}\n")

        tests = [
            ("Health Check", self.test_health),
            ("Authentication", self.test_auth),
            ("User Management", self.test_users),
            ("Payments", self.test_payments),
            ("Calendar", self.test_calendar),
            ("Documents", self.test_documents)
        ]

        total_success = 0
        total_tests = len(tests)

        for test_name, test_func in tqdm(tests, desc="Running Tests", unit="test"):
            success = await test_func()
            if success:
                total_success += 1

        # Print summary
        self.print_header("Test Summary")
        print(f"{Fore.CYAN}Total Tests: {total_tests}")
        print(f"Passed: {Fore.GREEN}{total_success}{Style.RESET_ALL}")
        print(f"Failed: {Fore.RED}{total_tests - total_success}{Style.RESET_ALL}")
        print(f"Success Rate: {Fore.CYAN}{(total_success/total_tests)*100:.1f}%{Style.RESET_ALL}")

async def main():
    """Main entry point for the test suite."""
    async with TestSuite() as suite:
        await suite.run_all_tests()

if __name__ == "__main__":
    asyncio.run(main()) 