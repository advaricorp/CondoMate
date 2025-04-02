import pytest
import sys
from pathlib import Path
from tqdm import tqdm
from colorama import Fore, Style, init
import time

# Initialize colorama for colored output
init()

def run_tests():
    """Run the test suite with colored output and progress bars."""
    test_dir = Path(__file__).parent
    test_files = list(test_dir.glob("test_*.py"))
    
    print(f"\n{Fore.CYAN}╔══════════════════════════════════╗{Style.RESET_ALL}")
    print(f"{Fore.CYAN}║      CondoMate Test Suite       ║{Style.RESET_ALL}")
    print(f"{Fore.CYAN}╚══════════════════════════════════╝{Style.RESET_ALL}\n")
    
    total_tests = len(test_files)
    passed_tests = 0
    failed_tests = 0
    
    with tqdm(total=total_tests, 
             desc=f"{Fore.CYAN}Running tests{Style.RESET_ALL}",
             bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}") as pbar:
        
        for test_file in test_files:
            test_name = test_file.stem.replace("test_", "").replace("_", " ").title()
            pbar.set_description(f"{Fore.CYAN}Testing {test_name}{Style.RESET_ALL}")
            
            # Run pytest for the current file
            result = pytest.main([
                str(test_file),
                "-v",
                "--color=yes",
                "--no-header",
                "--tb=short"
            ])
            
            if result == 0:
                passed_tests += 1
            else:
                failed_tests += 1
            
            pbar.update(1)
            time.sleep(0.1)  # Small delay for visual effect
    
    # Print summary
    print(f"\n{Fore.CYAN}Test Summary:{Style.RESET_ALL}")
    print(f"{'═' * 40}")
    print(f"{Fore.GREEN}Passed: {passed_tests}{Style.RESET_ALL}")
    print(f"{Fore.RED}Failed: {failed_tests}{Style.RESET_ALL}")
    print(f"Total: {total_tests}")
    print(f"{'═' * 40}\n")
    
    return 0 if failed_tests == 0 else 1

if __name__ == "__main__":
    sys.exit(run_tests()) 