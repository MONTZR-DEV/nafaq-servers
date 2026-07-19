#!/usr/bin/env python3
"""يسحب قائمة VPN Gate الكاملة، يفلتر أسرع 25 سيرفراً،
ويكتبها بصيغة CSV مطابقة تماماً لصيغة VPN Gate الأصلية،
حتى يعمل محلّل (parser) التطبيق الحالي دون أي تعديل."""
import csv
import urllib.request

ENDPOINTS = [
    "https://www.vpngate.net/api/iphone/",
    "https://www.vpngate.net/en/api/iphone/",
]
LIMIT = 25
HEADER = (
    "#HostName,IP,Score,Ping,Speed,CountryLong,CountryShort,"
    "NumVpnSessions,Uptime,TotalUsers,TotalTraffic,LogType,"
    "Operator,Message,OpenVPN_ConfigData_Base64"
)


def fetch():
    last_err = None
    for url in ENDPOINTS:
        try:
            req = urllib.request.Request(
                url, headers={"User-Agent": "NafaqVPN/1.0"}
            )
            with urllib.request.urlopen(req, timeout=45) as resp:
                data = resp.read().decode("utf-8", "ignore")
                if "#HostName" in data:
                    return data
        except Exception as e:  # noqa: BLE001
            last_err = e
    raise SystemExit(f"فشل جلب قائمة VPN Gate: {last_err}")


def parse_line(line):
    return next(csv.reader([line]))


def to_float(value, default):
    try:
        return float(value)
    except (ValueError, TypeError):
        return default


def sort_key(fields):
    ping = to_float(fields[3], 1e9)
    if ping <= 0:
        ping = 1e9                     # ping غير صالح -> للأسفل
    speed = to_float(fields[4], 0)
    score = to_float(fields[2], 0)
    # أقل ping، ثم أعلى سرعة، ثم أعلى تقييم
    return (ping, -speed, -score)


def main():
    raw = fetch()
    lines = raw.splitlines()

    # إيجاد سطر الترويسة
    start = next(
        (i for i, l in enumerate(lines) if l.startswith("#HostName")),
        None,
    )
    if start is None:
        raise SystemExit("لم يتم العثور على ترويسة CSV")

    seen_ips = set()
    entries = []  # (fields, original_line)
    for line in lines[start + 1:]:
        if not line or line.startswith("*"):
            continue
        fields = parse_line(line)
        if len(fields) < 15:
            continue
        if not fields[14].strip():        # يجب أن يحوي إعداد OpenVPN
            continue
        ip = fields[1]
        if ip in seen_ips:                 # إزالة التكرار حسب IP
            continue
        seen_ips.add(ip)
        entries.append((fields, line))

    entries.sort(key=lambda e: sort_key(e[0]))
    top = entries[:LIMIT]

    with open("servers.csv", "w", encoding="utf-8", newline="") as f:
        f.write("*vpn_servers\n")
        f.write(HEADER + "\n")
        for _, original_line in top:
            f.write(original_line + "\n")
        f.write("*\n")

    print(f"تمت كتابة {len(top)} سيرفراً إلى servers.csv")


if __name__ == "__main__":
    main()
