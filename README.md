# OKX-Withdrawal

 [My Profile](https://github.com/ryu666zaki/) | [My projects](https://github.com/ryu666zaki?tab=repositories) |
  🍩**Donate**: `0x27512edc51cAd8a5277090183858677915CC95c4`

![](image/OKX.png)

### <sub>OKX Withdraw on list of wallets</sub>

### <sup>***❗You need to have Python 3.10+ installed❗***</sup>

### <sup>***❗❗ Add wallets to a whitelist on OKX ❗❗***</sup>

1. **Clone repository** to yours system.

> To do this, open your development environment, such as VSCode or Pycharm. Select the option to clone repo by link and paste the link to this repo.

2. Open terminal in the same folder as `main.py` and run this commands:

```
python3.10 -m venv .venv
source .venv/bin/activate
pip install ccxt
```
3. Put your wallets in `wallet.txt`
4. Change those variables in `main.py` => `API_KEY`, `SECRET`, `PASSPHRASE`, `TOKEN`, `NETWORK`, `AMOUNT`, `MIN_DELAY`, `MAX_DELAY` (lines 5 - 14)
5. Now you're ready to start:
  ```
  python main.py
  ```
  
 🍩**Donate**: `0x27512edc51cAd8a5277090183858677915CC95c4`
