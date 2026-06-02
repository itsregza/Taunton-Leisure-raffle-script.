import csv
import json
import os
import random
import sys
import time
import urllib.parse
import requests

root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
vendor = os.path.join(root, "vendor")
if os.path.isdir(vendor) and vendor not in sys.path:
    sys.path.insert(0, vendor)
here = os.path.dirname(os.path.abspath(__file__))
import tls_client

timeout = 45
settings_url = "https://mc.us9.list-manage.com/signup-form/settings?u=adf15cc4af5cf5baf9c8af1b8&id=006312e1f0&for_preview=0&c=dojo_request_script_callbacks.dojo_request_script0"
subscribe_url = "https://mc.us9.list-manage.com/subscribe/landing-page?u=adf15cc4af5cf5baf9c8af1b8&id=8f038a299b&f_id=006312e1f0"

settings_hdrs = {
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "referer": "https://go.tauntonleisure.com/",
    "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "script",
    "sec-fetch-mode": "no-cors",
    "sec-fetch-site": "cross-site",
    "sec-fetch-storage-access": "active",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
}
    
submit_hdrs = {
    "accept": "*/*",
    "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
    "content-type": "application/x-www-form-urlencoded",
    "origin": "https://go.tauntonleisure.com",
    "priority": "u=1, i",
    "referer": "https://go.tauntonleisure.com/",
    "sec-ch-ua": '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
}

first_names = [
    "james", "john", "robert", "michael", "william", "david", "richard", "joseph",
    "thomas", "christopher", "charles", "daniel", "matthew", "anthony", "mark",
    "donald", "steven", "paul", "andrew", "joshua", "kenneth", "kevin", "brian",
    "george", "timothy", "ronald", "jason", "edward", "jeffrey", "ryan", "jacob",
    "gary", "nicholas", "eric", "jonathan", "stephen", "larry", "justin", "scott",
    "brandon", "mary", "patricia", "jennifer", "linda", "elizabeth", "barbara",
    "susan", "jessica", "sarah", "karen", "nancy", "lisa", "betty", "helen",
    "sandra", "donna", "carol", "ruth", "sharon", "michelle", "laura", "kimberly",
    "deborah", "dorothy", "emma", "olivia", "sophia", "charlotte", "amelia", "mia",
    "harper", "evelyn", "lily", "grace", "chloe", "ella", "victoria", "hannah",
    "zoe", "isla", "freya", "poppy", "ruby", "florence", "alice", "emily",
    "alexander", "benjamin", "caleb", "dylan", "ethan", "felix", "gabriel", "henry",
    "isaac", "jack", "kyle", "liam", "mason", "noah", "owen", "peter", "quinn",
    "ruben", "samuel", "tyler", "victor", "wyatt", "zachary", "adam", "blake",
    "cameron", "derek", "evan", "frank", "graham", "harry", "ian", "jake", "keith",
    "luke", "marcus", "nathan", "oscar", "philip", "quentin", "roger", "sean",
    "trevor", "vincent", "wesley", "xavier", "aaron", "bradley", "connor", "damian",
    "elliot", "frederick", "gareth", "harrison", "isaiah", "jordan", "kieran", "logan",
    "maxwell", "nathaniel", "oliver", "patrick", "riley", "simon", "theodore", "austin",
    "bryce", "carter", "diego", "elijah", "finn", "grayson", "hunter", "ivan", "jaxon",
    "leo", "miles", "nolan", "parker", "tristan", "weston", "zane", "alfie", "archie",
    "freddie", "toby", "stanley", "arthur", "teddy", "reggie", "louie", "reuben",
]
last_names = [
    "smith", "johnson", "williams", "brown", "jones", "garcia", "miller", "davis",
    "rodriguez", "martinez", "wilson", "anderson", "thomas", "taylor", "moore",
    "jackson", "martin", "lee", "thompson", "white", "harris", "clark", "lewis",
    "walker", "hall", "young", "king", "wright", "hill", "green", "hernandez", "lopez",
    "gonzalez", "perez", "sanchez", "ramirez", "robinson", "allen", "scott", "torres",
    "nguyen", "flores", "adams", "nelson", "baker", "rivera", "campbell", "mitchell",
    "carter", "roberts", "gomez", "phillips", "evans", "turner", "diaz", "parker",
    "cruz", "edwards", "collins", "reyes", "stewart", "morris", "morales", "murphy",
    "cook", "rogers", "reed", "cooper", "bailey", "bell", "richardson", "cox", "howard",
    "ward", "peterson", "gray", "watson", "brooks", "kelly", "sanders", "price",
    "bennett", "wood", "barnes", "ross", "henderson", "coleman", "jenkins", "perry",
    "powell", "long", "patterson", "hughes", "washington", "butler", "simmons", "foster",
    "gonzales", "bryant", "alexander", "russell", "griffin", "hayes", "myers", "ford",
    "hamilton", "graham", "sullivan", "wallace", "woods", "cole", "west", "jordan",
    "owens", "reynolds", "fisher", "ellis", "harrison", "gibson", "mcdonald", "marshall",
    "ortiz", "murray", "freeman", "wells", "webb", "simpson", "stevens", "tucker",
    "porter", "hunter", "hicks", "crawford", "henry", "boyd", "kennedy", "warren",
    "dixon", "ramos", "chapman", "fletcher", "palmer", "holmes", "stone", "grant",
    "barrett", "sharp", "walsh", "frost", "hunt", "banks", "shaw", "fox", "lane",
    "mills", "payne", "holland", "burke", "lowe", "newman", "parsons", "higgins",
]


def format_proxy(line):
    line = (line or "").strip()
    if not line:
        return None
    try:
        if "@" in line:
            auth, host = line.split("@", 1)
            user, pwd = auth.split(":", 1)
            ip, port = host.split(":")
            user = urllib.parse.quote(user, safe="")
            pwd = urllib.parse.quote(pwd, safe="")
            url = f"http://{user}:{pwd}@{ip}:{port}"
        else:
            parts = line.split(":")
            if len(parts) == 2:
                url = f"http://{parts[0]}:{parts[1]}"
            elif len(parts) == 4:
                ip, port, user, pwd = parts
                user = urllib.parse.quote(user, safe="")
                pwd = urllib.parse.quote(pwd, safe="")
                url = f"http://{user}:{pwd}@{ip}:{port}"
            else:
                return None
        return {"http": url, "https": url}
    except Exception:
        return None


def json_find(obj, key):
    stack = [obj]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            if key in cur:
                return cur[key]
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
    return None


def run_entry(email, cap_key, proxies):
    print("  solving captcha...", flush=True)
    task = requests.post(
        "https://api.capsolver.com/createTask",
        json={
            "clientKey": cap_key,
            "task": {
                "type": "ReCaptchaV2TaskProxyLess",
                "websiteKey": "6Lexz1YUAAAAAJZknL3EkeY_xBlIKGKGfGwFHhjK",
                "websiteURL": "https://go.tauntonleisure.com/",
            },
        },
        timeout=30,
    ).json()
    cap_id = task.get("taskId")
    if not cap_id:
        print(f"  capsolver: {task}", flush=True)
        return False

    token = None
    for n in range(60):
        resp = requests.post(
            "https://api.capsolver.com/getTaskResult",
            json={"clientKey": cap_key, "taskId": cap_id},
            timeout=30,
        ).json()
        if resp.get("status") == "ready":
            token = (resp.get("solution") or {}).get("gRecaptchaResponse")
            break
        if resp.get("status") == "failed" or resp.get("errorId"):
            print(f"  capsolver: {resp}", flush=True)
            return False
        if n % 5 == 0:
            print(f"  captcha... {n * 2}s", flush=True)
    if not token:
        print("  captcha timed out", flush=True)
        return False
    print("  captcha ok", flush=True)

    fname = random.choice(first_names).title()
    lname = random.choice(last_names).title()
    tried = set()

    while True:
        left = [p for p in proxies if p not in tried]
        if not left:
            print("  out of proxies", flush=True)
            return False
        proxy_line = random.choice(left)
        tried.add(proxy_line)

        sess = tls_client.Session(client_identifier="chrome_146", random_tls_extension_order=True)
        sess.timeout = timeout
        if hasattr(sess, "timeout_seconds"):
            sess.timeout_seconds = timeout
        px = format_proxy(proxy_line)
        if px:
            sess.proxies.update(px)

        print("  settings...", flush=True)
        try:
            r = sess.get(settings_url, headers=settings_hdrs, timeout=timeout)
        except Exception as e:
            if "407" in str(e):
                print("  407, next proxy", flush=True)
                continue
            print(f"  settings: {e}", flush=True)
            return False
        if r.status_code == 407:
            print("  407, next proxy", flush=True)
            continue
        if r.status_code != 200:
            print(f"  settings: {r.status_code}", flush=True)
            return False

        raw = r.text.strip()
        if raw.startswith("(") and raw.endswith(")"):
            raw = raw[raw.index("(") + 1 : raw.rfind(")")]
        data = json.loads(raw)
        honeytime = json_find(data, "honeytime")
        honeypot = json_find(data, "honeypotFieldName")
        if not honeytime:
            print("  no honeytime", flush=True)
            return False

        body = urllib.parse.urlencode({
            "EMAIL": email,
            "FNAME": fname,
            "LNAME": lname,
            "MMERGE28": "I agree",
            honeypot: "",
            "ht": honeytime,
            "g-recaptcha-response": token,
        })

        print("  submit...", flush=True)
        try:
            r = sess.post(subscribe_url, headers=submit_hdrs, data=body, timeout=timeout)
        except Exception as e:
            if "407" in str(e):
                print("  407, next proxy", flush=True)
                continue
            print(f"  submit: {e}", flush=True)
            return False
        if r.status_code == 407:
            print("  407, next proxy", flush=True)
            continue

        txt = (r.text or "").lower()
        if r.status_code == 200 and (
            "success" in txt or "you've been added" in txt or "you&#39;ve been added" in txt
        ):
            out = os.path.join(here, "entries.csv")
            new = not os.path.isfile(out)
            with open(out, "a", encoding="utf-8", newline="") as f:
                w = csv.writer(f)
                if new:
                    w.writerow(["email", "first_name", "last_name", "timestamp"])
                w.writerow([email, fname, lname, time.strftime("%Y-%m-%d %H:%M:%S")])
            print(f"  ok {fname} {lname}", flush=True)
            return True

        print(f"  fail {r.status_code} {(r.text or '')[:200]}", flush=True)
        return False


def main():
    cfg = os.path.join(root, "config.json")
    if not os.path.isfile(cfg):
        print("no config.json")
        return 1
    with open(cfg, encoding="utf-8") as f:
        cap_key = json.load(f).get("capsolver_key", "").strip()
    if not cap_key or cap_key == "YOUR-KEY-HERE":
        print("set capsolver_key in config.json")
        return 1

    emails_path = os.path.join(here, "emails.csv")
    proxies_path = os.path.join(here, "proxies.txt")
    entries_path = os.path.join(here, "entries.csv")

    emails = []
    if os.path.isfile(emails_path):
        with open(emails_path, encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        for row in rows:
            e = (row.get("email") or row.get("EMAIL") or "").strip()
            if e and "@" in e:
                emails.append(e)
    if not emails:
        print("add emails to emails.csv")
        return 1

    proxies = []
    if os.path.isfile(proxies_path):
        with open(proxies_path, encoding="utf-8") as f:
            proxies = [ln.strip() for ln in f if ln.strip() and not ln.startswith("#")]
    if not proxies:
        print("add proxies to proxies.txt")
        return 1

    done = set()
    if os.path.isfile(entries_path):
        with open(entries_path, encoding="utf-8", newline="") as f:
            for row in csv.DictReader(f):
                e = (row.get("email") or "").strip().lower()
                if e:
                    done.add(e)

    pending = [e for e in emails if e.lower() not in done]
    if not pending:
        print("nothing to run")
        return 0

    print(f"{len(pending)} entries", flush=True)
    for i, email in enumerate(pending, 1):
        print(f"[{i}/{len(pending)}] {email}", flush=True)
        run_entry(email.strip(), cap_key, proxies)
        if i < len(pending):
            time.sleep(random.uniform(120, 180))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
