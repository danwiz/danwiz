from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/ecii-work/ecii-modern-reference')

# RC.13 / v1.0.0-rc.1 dependency security remediation.
# Keep the application on .NET/EF 8, but move Microsoft servicing packages to
# the current 8.0.31 patch and OpenTelemetry to 1.18.0.
for path in root.rglob('*.csproj'):
    text = path.read_text()
    text = text.replace('Version="8.0.8"', 'Version="8.0.31"')
    text = text.replace('Version="1.9.0"', 'Version="1.18.0"')
    path.write_text(text)

# Pin patched transitive dependencies in Infrastructure so the application,
# API, and integration-test dependency graphs cannot fall back to vulnerable
# versions selected by older dependency minimums.
infra = root / 'src/ECII.Infrastructure/ECII.Infrastructure.csproj'
text = infra.read_text()
marker = '    <PackageReference Include="Microsoft.Extensions.Hosting.Abstractions" Version="8.0.1" />'
if marker not in text:
    raise SystemExit('Infrastructure package insertion marker not found')
extra = '''\n    <PackageReference Include="Microsoft.Extensions.Caching.Memory" Version="8.0.1" />\n    <PackageReference Include="System.Text.Json" Version="8.0.6" />\n    <PackageReference Include="SQLitePCLRaw.bundle_e_sqlite3" Version="2.1.13" />'''
if 'Microsoft.Extensions.Caching.Memory" Version="8.0.1"' not in text:
    text = text.replace(marker, marker + extra, 1)
infra.write_text(text)

# Align the EF CLI tool with the serviced EF runtime.
tools = root / '.config/dotnet-tools.json'
text = tools.read_text()
text = text.replace('"version": "8.0.8"', '"version": "8.0.31"')
tools.write_text(text)

# Make the vulnerability audit a release gate rather than informational output.
verify = root / 'scripts/verify-rc1.sh'
text = verify.read_text()
old = '''echo "[5] Vulnerability audit"\ndotnet list ECII.Modern.sln package \\\n  --vulnerable \\\n  --include-transitive \\\n  | tee "$REPORT_DIR/vulnerability-audit.txt"\n'''
new = '''echo "[5] Vulnerability audit"\ndotnet list ECII.Modern.sln package \\\n  --vulnerable \\\n  --include-transitive \\\n  | tee "$REPORT_DIR/vulnerability-audit.txt"\n\nif grep -q "has the following vulnerable packages" "$REPORT_DIR/vulnerability-audit.txt"; then\n  echo "FAIL: dependency vulnerability audit contains known vulnerable packages."\n  exit 4\nfi\n'''
if old not in text:
    raise SystemExit('verify-rc1 vulnerability block not found')
verify.write_text(text.replace(old, new, 1))

# This is the exact source candidate that the final verification run tests.
(root / 'VERSION').write_text('1.0.0-rc.1\n')
program = root / 'src/ECII.Api/Program.cs'
text = program.read_text()
text, count = re.subn(
    r'version\s*=\s*"[^"]+"',
    'version = "1.0.0-rc.1"',
    text,
    count=1)
if count != 1:
    raise SystemExit('Program API version marker not found')
program.write_text(text)

print('Applied ECII security remediation and promoted source candidate to 1.0.0-rc.1')
