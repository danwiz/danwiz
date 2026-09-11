from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/ecii-work/ecii-modern-reference')

# Final hardening candidate dependency security baseline.
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

# Final-release authentication hardening.
# In production/OIDC mode, require an authenticated principal by default for
# every endpoint unless it is explicitly marked anonymous. Demo mode keeps the
# existing local-development behavior because authorization middleware is only
# enabled for OIDC mode.
program = root / 'src/ECII.Api/Program.cs'
text = program.read_text()
if 'using Microsoft.AspNetCore.Authorization;' not in text:
    text = 'using Microsoft.AspNetCore.Authorization;\n' + text

old_auth = '    builder.Services.AddAuthorization();'
new_auth = '''    builder.Services.AddAuthorization(options =>\n    {\n        options.FallbackPolicy = new AuthorizationPolicyBuilder()\n            .RequireAuthenticatedUser()\n            .Build();\n    });'''
if old_auth not in text:
    raise SystemExit('OIDC AddAuthorization marker not found')
text = text.replace(old_auth, new_auth, 1)

# Health and root metadata are intentionally public for operational probes and
# service identification. Swagger remains controlled separately by config.
root_marker = '''app.MapGet("/", () => Results.Ok(new\n{\n    service = "ECII Modern Reference API",\n    version = "1.0.0-rc.1",\n    evidenceBoundary = "Modern clean-room reconstruction; no historical production banking integration."\n}));'''
root_replacement = '''app.MapGet("/", () => Results.Ok(new\n{\n    service = "ECII Modern Reference API",\n    version = "1.0.0-final-candidate",\n    evidenceBoundary = "Modern clean-room reconstruction; no historical production banking integration."\n})).AllowAnonymous();'''
if root_marker not in text:
    raise SystemExit('Root endpoint marker not found')
text = text.replace(root_marker, root_replacement, 1)

health_marker = 'app.MapHealthChecks("/health");'
if health_marker not in text:
    raise SystemExit('Health endpoint marker not found')
text = text.replace(health_marker, 'app.MapHealthChecks("/health").AllowAnonymous();', 1)

ready_marker = '''app.MapHealthChecks("/health/ready", new HealthCheckOptions\n{\n    Predicate = check => check.Name == "database"\n});'''
ready_replacement = '''app.MapHealthChecks("/health/ready", new HealthCheckOptions\n{\n    Predicate = check => check.Name == "database"\n}).AllowAnonymous();'''
if ready_marker not in text:
    raise SystemExit('Readiness endpoint marker not found')
text = text.replace(ready_marker, ready_replacement, 1)

# This is a final-release candidate, not yet the immutable v1.0.0 release.
(root / 'VERSION').write_text('1.0.0-final-candidate\n')
text, count = re.subn(
    r'version\s*=\s*"[^"]+"',
    'version = "1.0.0-final-candidate"',
    text,
    count=1)
if count != 1:
    raise SystemExit('Program API version marker not found')
program.write_text(text)

print('Applied ECII final hardening: dependency security + OIDC fallback authorization')
