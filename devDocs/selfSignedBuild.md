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

Using PowerShell in your NVDA source directory:
```ps1
$password = ConvertTo-SecureString -String <Password> -Force -AsPlainText 
Export-PfxCertificate -cert "Cert:\CurrentUser\My\<Certificate Thumbprint>" -FilePath <PathToNVDASource/local.pfx> -Password $password
```

### Import the certificate

1. Open `local.pfx` using the default file handler "Certificate Import Wizard"
1. Install to the Local Machine, continue to the next screen
1. Confirm the correct file is selected, continue to the next screen
1. Enter your password, continue to the next screen
1. Choose the location for the certificate to be stored: "Trusted Root Certification Authorities"
1. Finish the import

### Using the certificate

When running a scons command, append `certFile=local.pfx certPassword=<Password>`.

#### Example: building a self-signed installer

From Command Prompt in your NVDA source directory:
```cmd
scons launcher certFile=local.pfx certPassword=<Password>
```
