"""Windows-only isolated Samurai integration fixture. Requires Docker and staged exes.

All databases, processes, and ports belong to this fixture. No production SQL
configuration, credentials, accounts, or running server binaries are used.
"""
from __future__ import annotations

import argparse
import ctypes
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import time


ROOT = Path(__file__).resolve().parents[3]
FIXTURES = Path(__file__).resolve().parent
BASE = ROOT / "build" / "samurai-test"
RUNTIME = BASE / "runtime"
CONTAINER = "rathena-samurai-validation"
PASSWORD = "samurai_isolated_validation"  # Public, disposable fixture credential.
DATABASE = "samurai_validation"
PORTS = (55120, 55121, 55122)
HIDDEN = subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0
SERVICES = {
    "login-server": ["--login-config", "conf/login-test.conf", "--lan-config", "conf/subnet-test.conf"],
    "char-server": ["--char-config", "conf/char-test.conf", "--inter-config", "conf/inter-test.conf", "--lan-config", "conf/subnet-test.conf"],
    "map-server": ["--map-config", "conf/map-test.conf", "--inter-config", "conf/inter-test.conf", "--log-config", "conf/log-test.conf"],
}


def run(args, **kwargs):
    return subprocess.run(args, check=True, capture_output=True, creationflags=HIDDEN, **kwargs)


def write(relative, text):
    target = RUNTIME / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding="utf-8", newline="\n")


def process_path(pid):
    kernel = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel.OpenProcess.restype = ctypes.c_void_p
    kernel.QueryFullProcessImageNameW.argtypes = [ctypes.c_void_p, ctypes.c_uint32, ctypes.c_wchar_p, ctypes.POINTER(ctypes.c_uint32)]
    kernel.CloseHandle.argtypes = [ctypes.c_void_p]
    handle = kernel.OpenProcess(0x1000, False, int(pid))
    if not handle:
        return None
    try:
        length = ctypes.c_uint32(32768)
        buffer = ctypes.create_unicode_buffer(length.value)
        if kernel.QueryFullProcessImageNameW(handle, 0, buffer, ctypes.byref(length)):
            return Path(buffer.value).resolve()
        return None
    finally:
        kernel.CloseHandle(handle)


def process_records():
    path = BASE / "processes.json"
    return json.loads(path.read_text()) if path.exists() else []


def require_stopped():
    for record in process_records():
        if process_path(record["pid"]) == Path(record["exe"]).resolve():
            raise RuntimeError("The isolated stack is running. Run the stop command first.")


def stop():
    if not (BASE / ".samurai-test-owned").exists():
        raise RuntimeError("No fixture ownership marker; refusing to stop any process.")
    for record in process_records():
        if record["name"] not in SERVICES:
            raise RuntimeError("Unexpected process in fixture state.")
        expected = (RUNTIME / (record["name"] + ".exe")).resolve()
        if process_path(record["pid"]) != expected:
            continue
        kernel = ctypes.WinDLL("kernel32", use_last_error=True)
        kernel.OpenProcess.restype = ctypes.c_void_p
        kernel.TerminateProcess.argtypes = [ctypes.c_void_p, ctypes.c_uint32]
        kernel.CloseHandle.argtypes = [ctypes.c_void_p]
        handle = kernel.OpenProcess(0x1001, False, int(record["pid"]))
        if handle:
            try:
                kernel.TerminateProcess(handle, 0)
            finally:
                kernel.CloseHandle(handle)
    (BASE / "processes.json").write_text("[]\n")
    state = BASE / "container.json"
    if state.exists():
        data = json.loads(state.read_text())
        inspected = subprocess.run(["docker", "inspect", data["id"]], capture_output=True, creationflags=HIDDEN)
        if inspected.returncode == 0:
            info = json.loads(inspected.stdout)[0]
            if info["Config"].get("Labels", {}).get("codex.samurai.validation") != "true":
                raise RuntimeError("Container ownership label does not match.")
            run(["docker", "stop", data["id"]])
    print("Stopped only the isolated fixture. Logs and test data remain in", BASE)


def sql(source):
    state = json.loads((BASE / "container.json").read_text())
    info = json.loads(run(["docker", "inspect", state["id"]]).stdout)[0]
    if info["Config"].get("Labels", {}).get("codex.samurai.validation") != "true":
        raise RuntimeError("Container ownership label does not match.")
    return run(["docker", "exec", "-i", state["id"], "mariadb", "-uroot", "-p" + PASSWORD, DATABASE], input=source.encode()).stdout.decode()


def stock_conf(name):
    # Read committed defaults; strip import chains and connection settings.
    original = run(["git", "show", "HEAD:conf/" + name], cwd=ROOT).stdout.decode("utf-8-sig")
    filtered = []
    for line in original.splitlines():
        key = line.split(":", 1)[0].strip()
        if key in ("import", "userid", "passwd") or key.startswith(("map_server_", "char_server_", "login_server_", "log_db_", "ipban_db_")):
            continue
        filtered.append(line)
    return "\n".join(filtered) + "\n"


def setup():
    require_stopped()
    BASE.mkdir(parents=True, exist_ok=True)
    (BASE / ".samurai-test-owned").write_text("Isolated Samurai integration fixture.\n")
    RUNTIME.mkdir(exist_ok=True)
    (RUNTIME / "log").mkdir(exist_ok=True)
    for port in (*PORTS, 33317):
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", port))
    # Copies, never junctions: test writes cannot reach the original data files.
    shutil.copytree(ROOT / "db", RUNTIME / "db", dirs_exist_ok=True)
    tracked = run(["git", "ls-files", "-z", "conf"], cwd=ROOT).stdout.decode().split("\0")
    excluded = {"inter_athena.conf", "login_athena.conf", "char_athena.conf", "map_athena.conf"}
    for relative in filter(None, tracked):
        if Path(relative).name in excluded:
            continue
        source = ROOT / relative
        if source.is_file():
            target = RUNTIME / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    (RUNTIME / "conf" / "import").mkdir(exist_ok=True)
    for source in (ROOT / "conf" / "import-tmpl").iterdir():
        if source.is_file():
            shutil.copy2(source, RUNTIME / "conf" / "import" / source.name)
    write("conf/msg_conf/import/map_msg_eng_conf.txt", "// No test message overrides.\n")
    for source in (ROOT / "npc").rglob("*.yml"):
        target = RUNTIME / source.relative_to(ROOT)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
    for relative in ("npc/other/Global_Functions.txt", "npc/other/CashShop_Functions.txt", "npc/custom/samurai_jobchange.txt"):
        target = RUNTIME / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / relative, target)
    shutil.copy2(FIXTURES / "fixture_npc.txt", RUNTIME / "npc/custom/samurai_test_fixture.txt")
    write("npc/re/scripts_main.conf", "npc: npc/other/Global_Functions.txt\nnpc: npc/other/CashShop_Functions.txt\nnpc: npc/custom/samurai_jobchange.txt\nnpc: npc/custom/samurai_test_fixture.txt\n")
    inter = stock_conf("inter_athena.conf")
    for prefix in ("map_server", "char_server", "login_server", "log_db", "ipban_db"):
        for key, value in (("ip", "127.0.0.1"), ("port", 33317), ("id", "root"), ("pw", PASSWORD), ("db", DATABASE)):
            inter += f"{prefix}_{key}: {value}\n"
    inter += "use_sql_db: no\nlog_inter: no\n"
    write("conf/inter-test.conf", inter)
    write("conf/inter_athena.conf", inter)  # Core loads schema names before CLI options.
    write("conf/map-test.conf", "userid: samurai_validation\npasswd: samurai_validation_only\nchar_ip: 127.0.0.1\nchar_port: 55121\nmap_ip: 127.0.0.1\nbind_ip: 127.0.0.1\nmap_port: 55122\nconsole: no\nconsole_msg_log: 0\nstdout_with_ansisequence: no\nuse_grf: no\ndb_path: db\n" + "".join(f"map: {m}\n" for m in ("prontera", "geffen", "morocc", "payon", "yuno", "lighthalzen", "einbroch", "rachel", "veins")))
    write("conf/char-test.conf", stock_conf("char_athena.conf") + "userid: samurai_validation\npasswd: samurai_validation_only\nserver_name: Samurai Isolated Test\nlogin_ip: 127.0.0.1\nlogin_port: 55120\nchar_ip: 127.0.0.1\nbind_ip: 127.0.0.1\nchar_port: 55121\nconsole: no\nstdout_with_ansisequence: no\nconsole_msg_log: 0\nlog_char: no\npincode_enabled: no\nstart_point: prontera,156,179\n")
    write("conf/login-test.conf", "bind_ip: 127.0.0.1\nlogin_port: 55120\nconsole: no\nstdout_with_ansisequence: no\nlog_login: no\nnew_account: no\nipban_enable: no\nuse_web_auth_token: no\nuse_dnsbl: no\nuse_MD5_passwords: no\nimport: conf/inter-test.conf\n")
    write("conf/log-test.conf", "sql_logs: no\n" + "".join(f"{key}: no\n" for key in ("enable_logs", "log_branch", "log_zeny", "log_cash", "log_commands", "log_npc", "log_chat", "log_mvpdrop", "log_feeding")))
    write("conf/subnet-test.conf", "// Loopback only.\n")
    # GM commands are allowed, but equipment/skill mechanics must not be bypassed.
    write("conf/import/groups.yml", "Header:\n  Type: PLAYER_GROUP_DB\n  Version: 1\nBody:\n  - Id: 99\n    Permissions:\n      all_skill: false\n      all_equipment: false\n      skill_unconditional: false\n      item_unconditional: false\n")
    for name in SERVICES:
        shutil.copy2(ROOT / "build" / "samurai" / (name + ".exe"), RUNTIME / (name + ".exe"))
    for name in ("libmysql.dll", "pcre8.dll", "zlib.dll"):
        shutil.copy2(ROOT / name, RUNTIME / name)
    (BASE / "mariadb-data").mkdir(exist_ok=True)
    created = run(["docker", "run", "--detach", "--rm", "--name", CONTAINER, "--label", "codex.samurai.validation=true", "--publish", "127.0.0.1:33317:3306", "--mount", f"type=bind,source={BASE / 'mariadb-data'},target=/var/lib/mysql", "--env", "MARIADB_ROOT_PASSWORD=" + PASSWORD, "--env", "MARIADB_DATABASE=" + DATABASE, "mariadb:11"])
    (BASE / "container.json").write_text(json.dumps({"name": CONTAINER, "id": created.stdout.decode().strip(), "port": 33317}))
    deadline = time.monotonic() + 45
    while True:
        try:
            sql("SELECT 1;")
            break
        except subprocess.CalledProcessError:
            if time.monotonic() > deadline:
                raise RuntimeError("Isolated MariaDB did not become ready; inspect docker logs.")
            time.sleep(0.5)
    if not sql("SHOW TABLES LIKE 'char';").strip():
        for name in ("main.sql", "logs.sql", "web.sql", "roulette_default_data.sql"):
            sql((ROOT / "sql-files" / name).read_text(encoding="utf-8-sig"))
    # Reset only this fixture's known character/account, inside the labelled test container.
    for table in ("skill", "inventory", "char_reg_num", "char_reg_str", "sc_data", "skillcooldown", "hotkey"):
        sql(f"DELETE FROM `{table}` WHERE char_id=150000;")
    sql("DELETE FROM `char` WHERE char_id=150000; DELETE FROM login WHERE account_id=2000001;")
    sql((FIXTURES / "fixture.sql").read_text())
    print("Fixture ready; no production services changed. Next: run-once, then start.")


def start():
    require_stopped()
    records = []
    for name, args in SERVICES.items():
        with (BASE / (name + ".log")).open("wb") as log:
            proc = subprocess.Popen([str(RUNTIME / (name + ".exe")), *args], cwd=RUNTIME, stdout=log, stderr=subprocess.STDOUT, creationflags=HIDDEN | subprocess.CREATE_NEW_PROCESS_GROUP)
        records.append({"name": name, "pid": proc.pid, "exe": str(RUNTIME / (name + ".exe"))})
        (BASE / "processes.json").write_text(json.dumps(records, indent=2))
    deadline = time.monotonic() + 30
    while time.monotonic() < deadline:
        if "Map Server is now online." in (BASE / "map-server.log").read_text(errors="replace"):
            print("Isolated stack linked on 55120/55121/55122. Test account: samurai_test / samurai-test-only")
            return
        time.sleep(0.25)
    raise RuntimeError("Stack did not link; inspect server logs under " + str(BASE))


def run_once():
    require_stopped()
    with (BASE / "map-run-once.log").open("wb") as log:
        result = subprocess.run([str(RUNTIME / "map-server.exe"), "--run-once", *SERVICES["map-server"]], cwd=RUNTIME, stdout=log, stderr=subprocess.STDOUT, timeout=90, creationflags=HIDDEN)
    output = (BASE / "map-run-once.log").read_text(errors="replace")
    bad = [line for line in output.splitlines() if any(tag in line for tag in ("[Error]", "[Warning]", "[Fatal", "[SQL]"))]
    if result.returncode or bad or "Finished." not in output:
        raise RuntimeError(f"Run-once failed ({result.returncode}):\n" + "\n".join(bad))
    print("Map startup/shutdown passed with no errors or warnings; see map-run-once.log.")


if __name__ == "__main__":
    if os.name != "nt":
        raise SystemExit("This fixture runner targets the Windows staged server binaries.")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("setup", "start", "stop", "run-once"))
    command = parser.parse_args().command
    {"setup": setup, "start": start, "stop": stop, "run-once": run_once}[command]()
