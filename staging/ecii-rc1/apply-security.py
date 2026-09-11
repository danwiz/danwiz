from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/ecii-work/ecii-modern-reference')

# Final release dependency security baseline.
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
program = root / 'src/ECII.Api/Program.cs'
text = program.read_text()
if 'using Microsoft.AspNetCore.Authorization;' not in text:
    text = 'using Microsoft.AspNetCore.Authorization;\n' + text

old_auth = '    builder.Services.AddAuthorization();'
new_auth = '''    builder.Services.AddAuthorization(options =>\n    {\n        options.FallbackPolicy = new AuthorizationPolicyBuilder()\n            .RequireAuthenticatedUser()\n            .Build();\n    });'''
if old_auth not in text:
    raise SystemExit('OIDC AddAuthorization marker not found')
text = text.replace(old_auth, new_auth, 1)

# Root metadata is intentionally anonymous. Use index slicing rather than an
# exact version string so the patch remains stable across the RC version churn.
root_start = text.index('app.MapGet("/", () => Results.Ok(new')
root_end = text.index('}));', root_start) + len('}));')
root_replacement = '''app.MapGet("/", () => Results.Ok(new\n{\n    service = "ECII Modern Reference API",\n    version = "1.0.0",\n    evidenceBoundary = "Modern clean-room reconstruction; no historical production banking integration."\n})).AllowAnonymous();'''
text = text[:root_start] + root_replacement + text[root_end:]

# Operational probes remain anonymous in OIDC mode.
health_marker = 'app.MapHealthChecks("/health");'
if health_marker not in text:
    raise SystemExit('Health endpoint marker not found')
text = text.replace(health_marker, 'app.MapHealthChecks("/health").AllowAnonymous();', 1)

ready_marker = '''app.MapHealthChecks("/health/ready", new HealthCheckOptions\n{\n    Predicate = check => check.Name == "database"\n});'''
ready_replacement = '''app.MapHealthChecks("/health/ready", new HealthCheckOptions\n{\n    Predicate = check => check.Name == "database"\n}).AllowAnonymous();'''
if ready_marker not in text:
    raise SystemExit('Readiness endpoint marker not found')
text = text.replace(ready_marker, ready_replacement, 1)

# Immutable v1.0.0 release candidate source produced by the final gate.
(root / 'VERSION').write_text('1.0.0\n')
program.write_text(text)

print('Applied ECII v1.0.0 final hardening: dependency security + OIDC fallback authorization')
