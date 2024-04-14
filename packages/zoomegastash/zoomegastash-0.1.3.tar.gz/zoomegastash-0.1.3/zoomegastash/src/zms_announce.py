from colored import Back, Fore, Style
from tcrutils import custom_zfill, cut_at

from .zms_types import Profile, ProfileInfo, ProfileInfoError

C_GOLD = Fore.YELLOW + Style.BOLD
C_RED = Fore.RED + Style.BOLD
C_WHITE = Fore.WHITE + Style.BOLD
C_RESET = Style.RESET


def _print_error(id, x):
  print(f"{C_RED}Failed to fetch profile info of {C_WHITE}{id}{C_RED}: {C_WHITE}{x['name']}{C_RED}, {C_WHITE}{x['msg']}{C_RESET}")


def profile_info(id: int, x: ProfileInfo | ProfileInfoError) -> None:
  if 'error' in x:
    _print_error(id, x)
    return

  print(f"{C_GOLD}Fetched profile info {C_WHITE}{f'{x['id']:^30}'}{C_GOLD} - [{C_WHITE}{cut_at(x['name'], 25)}{C_GOLD}]{C_RESET}")


def profiles(id: int, x: Profile) -> None:
  if 'error' in x:
    _print_error(id, x)
    return

  print(f"{C_GOLD}Fetched profile {C_WHITE}{f'{x['id']}'}{C_GOLD}")
