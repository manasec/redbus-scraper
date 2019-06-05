import re
#regex area
coupon_code_pattern = re.compile(r"\b(code|code is|Use|use)(\s[A-Z]{2,}[0-9]*)|\([A-Z]{3,}.+\)")
ods = re.compile(r"[0-9]+[\s%]\s.+|cashback.*\d|get\sFlat.*\.")
minimum = re.compile(r"min.+\d")
chan = re.compile(r"available.+Apps.+|redBus Android or iOS app")
applicable = re.compile(r"\s(ICICI|Rupay).*cards|Amazon Pay|Paytm|MOBIKWIK|PayPal")
constreg = re.compile(r"limit.*|(Once|once|twice).*(email|number)(\.)?|first.*(redBus|Redbus)|\sone.*|cannot.*|twice.*")
#regex area
