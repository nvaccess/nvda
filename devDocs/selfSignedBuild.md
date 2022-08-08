# Creating a self-signed build

These instructions are based on Microsoft documentation to [create a self-signed certificate](https://docs.microsoft.com/en-us/windows/msix/package/create-certificate-package-signing).

### Prerequisites

From PowerShell running as administrator, install [PKI](https://github.com/PKISolutions/PSPKI#download-and-install-powershell-pki-module-from-the-powershell-gallery-using-powershell):

```ps1
Install-Module -Name PSPKI
```

### Create a self-signed certificate

Using PKI, create a self signed build with a custom name (`FriendlyName`) and publisher (`Subject`).
Other parameters are determined by [MS docs](https://docs.microsoft.com/en-us/windows/msix/package/create-certificate-package-signing#use-new-selfsignedcertificate-to-create-a-certificate).

From PowerShell:
```ps1
New-SelfSignedCertificate -FriendlyName "LocalNVDA" -Type Custom -Subject "CN=Test NVDA Build, O=NVDA Dev, C=US" -KeyUsage DigitalSignature -CertStoreLocation "Cert:\CurrentUser\My" -TextExtension @("2.5.29.37={text}1.3.6.1.5.5.7.3.3", "2.5.29.19={text}")
```

This should output a thumbprint. Example Output:
```ps1
   PSParentPath: Microsoft.PowerShell.Security\Certificate::CurrentUser\My

Thumbprint                                Subject
----------                                -------
148CB69869B802A36B3D8D801BA8D9D0F3C1484F  CN=Test NVDA Build, O=NVDA Dev, C=US
```

### Export certificate as PFX

This [method uses a password](https://docs.microsoft.com/en-us/windows/msix/package/create-certificate-package-signing#password-usage) to handle access.

Using PowerShell:
```ps1
cd <nvdaSourceDirectory>
$password = ConvertTo-SecureString -String <Password> -Force -AsPlainText 
Export-PfxCertificate -cert "Cert:\CurrentUser\My\<Certificate Thumbprint>" -FilePath local.pfx -Password $password
```

### Import the certificate
Run PowerShell as Administrator, execute [Import-PfxCertificate
](https://docs.microsoft.com/en-us/powershell/module/pki/import-pfxcertificate):
```ps1
cd <nvdaSourceDirectory>
$password = ConvertTo-SecureString -String <Password> -Force -AsPlainText
Import-PfxCertificate -Password $password -CertStoreLocation "Cert:\LocalMachine\TrustedPublisher" -FilePath local.pfx
```

This should output the same thumbprint. Example Output:
```ps1
   PSParentPath: Microsoft.PowerShell.Security\Certificate::LocalMachine\TrustedPublisher

Thumbprint                                Subject
----------                                -------
148CB69869B802A36B3D8D801BA8D9D0F3C1484F  CN=Test NVDA Build, O=NV Access Dev, C=US
```

### Using the certificate

When running a scons command, append `certFile=local.pfx certPassword=<Password>`.

#### Example: building a self-signed installer

From Command Prompt in your NVDA source directory:
```cmd
scons launcher certFile=local.pfx certPassword=<Password>
```
