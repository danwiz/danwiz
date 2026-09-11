from pathlib import Path
import re
import sys

root = Path(sys.argv[1] if len(sys.argv) > 1 else '/tmp/ecii-work/ecii-modern-reference')


def replace_once(path: Path, pattern: str, replacement: str, label: str):
    text = path.read_text()
    updated, count = re.subn(pattern, replacement, text, count=1, flags=re.MULTILINE)
    if count != 1:
        raise SystemExit(f'{label}: expected exactly one replacement, got {count}')
    path.write_text(updated)


# RC.8 — explicit collection navigation mappings.
replace_once(
    root / 'src/ECII.Infrastructure/Persistence/AccountingConfigurations.cs',
    r'builder\.HasMany<AccountingEntry>\("_entries"\)\s*\.WithOne\(\)\s*\.HasForeignKey\(x => x\.JournalId\)\s*\.OnDelete\(DeleteBehavior\.Cascade\);',
    '''builder.HasMany(x => x.Entries)\n            .WithOne()\n            .HasForeignKey(x => x.JournalId)\n            .OnDelete(DeleteBehavior.Cascade);\n\n        builder.Navigation(x => x.Entries)\n            .UsePropertyAccessMode(PropertyAccessMode.Field);''',
    'AccountingJournal.Entries')

replace_once(
    root / 'src/ECII.Infrastructure/Persistence/PaymentConfiguration.cs',
    r'builder\.HasMany<PaymentEvent>\("_events"\)\s*\.WithOne\(\)\s*\.HasForeignKey\(x => x\.PaymentId\)\s*\.OnDelete\(DeleteBehavior\.Restrict\);',
    '''builder.HasMany(x => x.Events)\n            .WithOne()\n            .HasForeignKey(x => x.PaymentId)\n            .OnDelete(DeleteBehavior.Restrict);\n\n        builder.Navigation(x => x.Events)\n            .UsePropertyAccessMode(PropertyAccessMode.Field);''',
    'Payment.Events')

# RC.9 — SQLite-safe outbox retry filtering.
repo = root / 'src/ECII.Infrastructure/Persistence/SettlementRepositories.cs'
text = repo.read_text()
start = text.index('    public async Task<IReadOnlyList<OutboxMessage>> GetPendingAsync(')
end = text.index('\n}\n\n\npublic sealed class OutboxAdminRepository', start)
replacement = '''    public async Task<IReadOnlyList<OutboxMessage>> GetPendingAsync(\n        int take,\n        CancellationToken cancellationToken)\n    {\n        var now = DateTimeOffset.UtcNow;\n\n        if (_db.Database.IsSqlite())\n        {\n            var candidates = await _db.OutboxMessages\n                .Where(x =>\n                    x.DeadLetteredAt == null &&\n                    (x.Status == OutboxStatus.Pending ||\n                     x.Status == OutboxStatus.Failed))\n                .ToListAsync(cancellationToken);\n\n            return candidates\n                .Where(x =>\n                    x.Status == OutboxStatus.Pending ||\n                    x.NextAttemptAt == null ||\n                    x.NextAttemptAt <= now)\n                .OrderBy(x => x.OccurredAt)\n                .Take(take)\n                .ToList();\n        }\n\n        return await _db.OutboxMessages\n            .Where(x =>\n                x.DeadLetteredAt == null &&\n                (x.Status == OutboxStatus.Pending ||\n                 (x.Status == OutboxStatus.Failed &&\n                  (x.NextAttemptAt == null || x.NextAttemptAt <= now))))\n            .OrderBy(x => x.OccurredAt)\n            .Take(take)\n            .ToListAsync(cancellationToken);\n    }'''
repo.write_text(text[:start] + replacement + text[end:])

# RC.10 — demo authorization and SQLite-safe reconciliation summary.
auth = root / 'src/ECII.Api/Security/AdminAuthorization.cs'
text = auth.read_text()
if 'return Results.Forbid();' not in text:
    raise SystemExit('AdminAuthorization: expected Results.Forbid() not found')
auth.write_text(text.replace(
    'return Results.Forbid();',
    'return Results.StatusCode(StatusCodes.Status403Forbidden);', 1))

program = root / 'src/ECII.Api/Program.cs'
text = program.read_text()
text = text.replace(
    '        payment.Status,\n        payment.CorrelationId,',
    '        payment.Status.ToString(),\n        payment.CorrelationId,', 1)
old_summary = '''    var summary = await db.PaymentSettlements\n        .GroupBy(x => x.Status)\n        .Select(g => new\n        {\n            status = g.Key.ToString(),\n            count = g.Count()\n        })\n        .OrderBy(x => x.status)\n        .ToListAsync(ct);\n\n    return Results.Ok(summary);'''
new_summary = '''    var grouped = await db.PaymentSettlements\n        .GroupBy(x => x.Status)\n        .Select(g => new\n        {\n            Status = g.Key,\n            Count = g.Count()\n        })\n        .ToListAsync(ct);\n\n    var summary = grouped\n        .Select(x => new\n        {\n            status = x.Status.ToString(),\n            count = x.Count\n        })\n        .OrderBy(x => x.status)\n        .ToList();\n\n    return Results.Ok(summary);'''
if old_summary not in text:
    raise SystemExit('Program reconciliation summary block not found')
program.write_text(text.replace(old_summary, new_summary, 1))

# Fresh application/database per payment API test.
tests = root / 'tests/ECII.IntegrationTests/PaymentApiTests.cs'
tests.write_text('''using System.Net;\nusing System.Net.Http.Json;\nusing ECII.Contracts.Payments;\n\nnamespace ECII.IntegrationTests;\n\npublic sealed class PaymentApiTests\n{\n    private static HttpClient CreateClient(out ECIIWebApplicationFactory factory)\n    {\n        factory = new ECIIWebApplicationFactory();\n        var client = factory.CreateClient();\n        client.DefaultRequestHeaders.Add("X-Demo-Subject", "demo-customer");\n        return client;\n    }\n\n    [Fact]\n    public async Task Payment_RequiresIdempotencyKey()\n    {\n        using var client = CreateClient(out var factory);\n        using (factory)\n        {\n            var request = new CreatePaymentRequest(Guid.Parse("44444444-4444-4444-4444-444444444444"), 100m, "JMD", "SCOTIA-SIM", "DEMO-SOURCE");\n            var response = await client.PostAsJsonAsync("/api/payments", request);\n            Assert.Equal(HttpStatusCode.BadRequest, response.StatusCode);\n        }\n    }\n\n    [Fact]\n    public async Task ReplayingSameIdempotencyKey_ReturnsSamePayment()\n    {\n        using var client = CreateClient(out var factory);\n        using (factory)\n        {\n            var request = new CreatePaymentRequest(Guid.Parse("44444444-4444-4444-4444-444444444444"), 100m, "JMD", "SCOTIA-SIM", "DEMO-SOURCE");\n            var key = Guid.NewGuid().ToString("N");\n            using var first = new HttpRequestMessage(HttpMethod.Post, "/api/payments") { Content = JsonContent.Create(request) };\n            first.Headers.Add("Idempotency-Key", key);\n            using var second = new HttpRequestMessage(HttpMethod.Post, "/api/payments") { Content = JsonContent.Create(request) };\n            second.Headers.Add("Idempotency-Key", key);\n            var firstResponse = await client.SendAsync(first);\n            var secondResponse = await client.SendAsync(second);\n            Assert.Equal(HttpStatusCode.Created, firstResponse.StatusCode);\n            Assert.Equal(HttpStatusCode.OK, secondResponse.StatusCode);\n            var firstPayment = await firstResponse.Content.ReadFromJsonAsync<PaymentResponse>();\n            var secondPayment = await secondResponse.Content.ReadFromJsonAsync<PaymentResponse>();\n            Assert.NotNull(firstPayment);\n            Assert.NotNull(secondPayment);\n            Assert.Equal(firstPayment!.PaymentId, secondPayment!.PaymentId);\n        }\n    }\n\n    [Fact]\n    public async Task ReusingIdempotencyKeyWithDifferentPayload_ReturnsConflict()\n    {\n        using var client = CreateClient(out var factory);\n        using (factory)\n        {\n            var key = Guid.NewGuid().ToString("N");\n            var firstRequest = new CreatePaymentRequest(Guid.Parse("44444444-4444-4444-4444-444444444444"), 100m, "JMD", "SCOTIA-SIM", "DEMO-SOURCE");\n            var changedRequest = firstRequest with { Amount = 110m };\n            using var first = new HttpRequestMessage(HttpMethod.Post, "/api/payments") { Content = JsonContent.Create(firstRequest) };\n            first.Headers.Add("Idempotency-Key", key);\n            using var second = new HttpRequestMessage(HttpMethod.Post, "/api/payments") { Content = JsonContent.Create(changedRequest) };\n            second.Headers.Add("Idempotency-Key", key);\n            var firstResponse = await client.SendAsync(first);\n            var secondResponse = await client.SendAsync(second);\n            Assert.Equal(HttpStatusCode.Created, firstResponse.StatusCode);\n            Assert.Equal(HttpStatusCode.Conflict, secondResponse.StatusCode);\n        }\n    }\n}\n''')

# RC.11 — later-added PaymentEvents must be INSERTs.
payment_domain = root / 'src/ECII.Domain/Payments/Payment.cs'
text = payment_domain.read_text()
key_old = '''        new()\n        {\n            Id = Guid.NewGuid(),\n            PaymentId = paymentId,'''
key_new = '''        new()\n        {\n            Id = Guid.Empty,\n            PaymentId = paymentId,'''
if key_old not in text:
    raise SystemExit('PaymentEvent.Create GUID assignment not found')
payment_domain.write_text(text.replace(key_old, key_new, 1))

payment_cfg = root / 'src/ECII.Infrastructure/Persistence/PaymentConfiguration.cs'
text = payment_cfg.read_text()
marker = '''        builder.ToTable("PaymentEvents");\n        builder.HasKey(x => x.Id);'''
if marker not in text:
    raise SystemExit('PaymentEvent configuration marker not found')
payment_cfg.write_text(text.replace(
    marker,
    marker + '\n        builder.Property(x => x.Id).ValueGeneratedOnAdd();', 1))

persistence_tests = root / 'tests/ECII.IntegrationTests/PaymentPersistenceTests.cs'
text = persistence_tests.read_text()
marker = '''    [Fact]\n    public async Task SameCustomerAndIdempotencyKey_IsRejectedByDatabaseConstraint()'''
regression = '''    [Fact]\n    public async Task LaterTransitionEvent_IsInsertedNotUpdated()\n    {\n        await using var database = await TestDatabase.CreateAsync();\n        Guid paymentId;\n        await using (var db = database.CreateContext())\n        {\n            var payment = NewPayment(Guid.NewGuid(), "later-event-key");\n            payment.BeginValidation();\n            payment.Authorize();\n            paymentId = payment.Id;\n            db.Payments.Add(payment);\n            await db.SaveChangesAsync();\n            payment.MarkSourceDebited("SCOTIA-LATER-001");\n            await db.SaveChangesAsync();\n        }\n        await using var verify = database.CreateContext();\n        var events = await verify.PaymentEvents.Where(x => x.PaymentId == paymentId).OrderBy(x => x.Sequence).ToListAsync();\n        Assert.Equal(4, events.Count);\n        Assert.Equal(PaymentEventType.SourceDebited, events[^1].EventType);\n        Assert.Equal("SCOTIA-LATER-001", events[^1].ExternalReference);\n    }\n\n'''
if marker not in text:
    raise SystemExit('PaymentPersistenceTests insertion marker not found')
persistence_tests.write_text(text.replace(marker, regression + marker, 1))

# RC.12 — EF CLI requires Design in the startup project.
api_project = root / 'src/ECII.Api/ECII.Api.csproj'
text = api_project.read_text()
if 'Microsoft.EntityFrameworkCore.Design' not in text:
    marker = '    <PackageReference Include="Microsoft.EntityFrameworkCore.Sqlite" Version="8.0.8" />'
    if marker not in text:
        raise SystemExit('API csproj SQLite package marker not found')
    addition = '''\n    <PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.0.8">\n      <PrivateAssets>all</PrivateAssets>\n      <IncludeAssets>runtime; build; native; contentfiles; analyzers; buildtransitive</IncludeAssets>\n    </PackageReference>'''
    api_project.write_text(text.replace(marker, marker + addition, 1))

(root / 'VERSION').write_text('0.9.10-rc.12\n')
print('Applied ECII runtime patch level 0.9.10-rc.12')
