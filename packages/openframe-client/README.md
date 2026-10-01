# openframe-client

Chocolatey wrapper around the manual bootstrap:

```
Invoke-WebRequest https://<server>/v0/api/assets/download?agent=client&platform=windows -Headers @{'x-machine-id'=<guid>} -OutFile openframe-client.zip
Expand-Archive openframe-client.zip; .\openframe-client.exe install --serverUrl <server> --initialKey <key> --orgId <org> --userId <user>
```

becomes

```
choco install openframe-client -s openframe -y --package-parameters-sensitive `
  "/ServerUrl:test-env.qa.openframe.build /InitialKey:<key> /OrgId:<org> /UserId:<user>"
```

- **Link-only**: the feed holds only this wrapper; the binary comes from the tenant's own server at install time, so one
  package serves every tenant and every build. No checksum can be pinned: the endpoint always returns the current build.
- `--package-parameters-sensitive` (not `--params`) keeps the enrollment key out of `chocolatey.log`.
- `/MachineId` is optional; a new GUID is generated and remembered in `tools/enrollment.json`.
- Not part of `TEST_PACKAGES` in CI: it needs a live tenant and enrollment credentials. Test it by hand on a VM.
- Uninstall assumes `openframe-client.exe uninstall` exists (see the TODO in `chocolateyUninstall.ps1`).
