# Creating a self-signed build

These instructions are based on Microsoft documentation to [create a self-signed certificate](https://docs.microsoft.com/en-us/windows/msix/package/create-certificate-package-signing).

### WARNING
Copies of NVDA signed by a self-signed certificate will not function on systems where it is not installed as a trusted root certificate, so this is only suitable for personal use.

Following are instructions on how to generate and install a self-signed certificate.
This is not supported and should only be attempted by developers who know what they are doing and are aware of the risks.
If the private key is compromised, this poses a serious security risk to your system. 

Do not forget to [remove the certificate](#remove-the-certificate) when you are done testing.

### Create a self-signed certificate

Using [PKI](https://docs.microsoft.com/en-us/windows/msix/package/create-certificate-package-signing#prerequisite), create a self signed build with a custom name (`FriendlyName`) and publisher (`Subject`).
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

Use PowerShell.
Replace the following in this PowerShell script:
- `<nvdaRepositoryRoot>`: the root of your NVDA repository.
- `<Password>`: a password for the exported certificate file.
- `<Certificate Thumbprint>`: The thumbprint from [creating the certificate](#create-a-self-signed-certificate).
```ps1
cd <nvdaRepositoryRoot>
$password = ConvertTo-SecureString -Force -AsPlainText -String <Password>
Export-PfxCertificate -FilePath local.pfx -Password $password -cert "Cert:\CurrentUser\My\<Certificate Thumbprint>"
```

### Import the certificate

Import the certificate to the Local Machine in the "Trusted Root Certification Authorities" store.

Run PowerShell as Administrator, execute [Import-PfxCertificate
](https://docs.microsoft.com/en-us/powershell/module/pki/import-pfxcertificate).

Replace the following in the PowerShell script:
- `<nvdaRepositoryRoot>`: the root of your NVDA repository.
- `<Password>`: your password for the exported certificate file.
```ps1
cd <nvdaRepositoryRoot>
$password = ConvertTo-SecureString -Force -AsPlainText -String <Password>
Import-PfxCertificate -Password $password -CertStoreLocation "Cert:\LocalMachine\Root" -FilePath local.pfx
```

This should output the same thumbprint. Example Output:
```ps1
   PSParentPath: Microsoft.PowerShell.Security\Certificate::LocalMachine\TrustedPublisher

Thumbprint                                Subject
----------                                -------
148CB69869B802A36B3D8D801BA8D9D0F3C1484F  CN=Test NVDA Build, O=NV Access Dev, C=US
```

For Windows 7, you will need to use an alternative method.
On any supported version of Windows, you can manage certifications through the "Certificate Manager".

### Using the certificate

When running a scons command, append `certFile=local.pfx certPassword=<Password>`.

#### Example: building a self-signed installer

From Command Prompt in your NVDA source directory:
```cmd
scons launcher certFile=local.pfx certPassword=<Password>
```

##### Confirming the certificate is installed correctly

View the certificate for the NVDA launcher:
1. Open file properties on the launcher (`output/nvda_*.exe`)
1. Navigate to Digital Signatures tab
1. Open certificate signature
1. Open View Certificate
   - If the certificate is not imported correctly:
      - **General tab:** "This CA Root certificate is not trusted because it is not in the Trusted Root Certification Authorities store."
      - **Certification Path tab, Certificate Status:** "This CA Root certificate is not trusted because it is not in the Trusted Root Certification Authorities store."
   - If the certificate is imported correctly:
      - **General tab:** "Ensures software came from software publisher. Protects software from alteration after publication"
      - **Certification Path tab, Certificate Status:** "This certificate is OK."

### Remove the certificate

After being finished with testing, remove the certificate from the Local Machine "Trusted Root Certification Authorities" store.
Leaving the certificate installed is potentially a security risk.

The certificate will still be in `Cert:\CurrentUser\My\<Certificate Thumbprint>`.

Use PowerShell, running as administrator.
Replace the following in this PowerShell script:
- `<Certificate Thumbprint>`: The thumbprint from [creating the certificate](#create-a-self-signed-certificate).
```ps1
Remove-Item -DeleteKey -Path "Cert:\LocalMachine\Root\<Certificate Thumbprint>"
```
