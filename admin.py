import sys
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError
import concurrent.futures

# ANSI Renk Kodları
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
RESET = "\033[0m"
BOLD = "\033[1m"

BANNER = f"""{CYAN}{BOLD}
 ███████╗ █████╗  ██████╗ ██████╗  ██████╗ ███████╗████████╗██╗  ██╗███████╗███████╗
╚══███╔╝██╔══██╗██╔════╝ ██╔══██╗██╔═══██╗██╔════╝╚══██╔══╝██║  ██║██╔════╝██╔════╝
  ███╔╝ ███████║██║  ███╗██████╔╝██║   ██║███████╗   ██║   ███████║█████╗  █████╗  
 ███╔╝  ██╔══██║██║   ██║██╔══██╗██║   ██║╚════██║   ██║   ██╔══██║██╔══╝  ██╔══╝  
███████╗██║  ██║╚██████╔╝██║  ██║╚██████╔╝███████║   ██║   ██║  ██║███████╗███████╗
╚══════╝╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝ ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚══════╝
                                    [ CORE ADMIN FINDER v2.5 ]
{RESET}"""

COMMON_PATHS = [
    "admin/", "admin/index.php", "admin/login.php", "administrator/",
    "wp-admin/", "wp-login.php", "panel/", "yonetim/", "yonetici/",
    "dashboard/", "login.php", "admin.php", "controlpanel/", "cpanel/",
    "admin/login.html", "admin/dashboard.php", "manage/", "admin_area/"
]

def check_path(base_url, path):
    url = urllib.parse.urljoin(base_url, path)
    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/119.0"}
        )
        with urllib.request.urlopen(req, timeout=3) as response:
            if response.status == 200:
                return (url, 200)
    except HTTPError as e:
        if e.code in [401, 403]:
            return (url, e.code)
    except Exception:
        pass
    return None

def scan_target(target_url):
    if not target_url.startswith(("http://", "https://")):
        target_url = "http://" + target_url
    
    print(f"\n{YELLOW}[*] Hedef Sistem:{RESET} {target_url}")
    print(f"{YELLOW}[*] Tarama Baslatiliyor...{RESET}\n" + "-"*60)
    
    found = []
    start_time = time.time()
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
        futures = {executor.submit(check_path, target_url, path): path for path in COMMON_PATHS}
        for future in concurrent.futures.as_completed(futures):
            res = future.result()
            if res:
                url, status = res
                if status == 200:
                    status_str = f"{GREEN}200 OK{RESET}"
                else:
                    status_str = f"{YELLOW}{status} FORBIDDEN/AUTH{RESET}"
                print(f"{GREEN}[+] BULUNDU:{RESET} {url} [{status_str}]")
                found.append(url)
                
    elapsed = time.time() - start_time
    print("-"*60)
    print(f"{CYAN}[*] Tarama Tamamlandi. Sure: {elapsed:.2f}s | Bulunan: {len(found)}{RESET}\n")

if __name__ == "__main__":
    print(BANNER)
    target = input(f"{BOLD}{CYAN}ZAGROSTHEE@core ~ # {RESET}URL'yi gir (Orn: example.com): ").strip()
    if target:
        scan_target(target)
    else:
        print(f"{RED}[-] Gecerli bir hedef girilmedi.{RESET}")
