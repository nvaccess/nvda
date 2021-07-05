$ErrorActionPreference = "Stop";
if(!$env:APPVEYOR_PULL_REQUEST_NUMBER) {
	Try {
		openssl enc -d -md sha256 -aes-256-cbc -pbkdf2 -salt -pass pass:$env:secure_authenticode_pass -in appveyor\authenticode.pfx.enc -out appveyor\authenticode.pfx
	} Catch {
		$errorCode=1
		Add-AppveyorMessage "Unable to decrypt authenticode certificate"
	}
	Try {
		openssl enc -md md5 -aes-256-cbc -d -pass pass:$env:secure_ssh_pass -in appveyor\ssh_id_rsa.enc -out appveyor\ssh_id_rsa
	} Catch {
		$errorCode=1
		Add-AppveyorMessage "Unable to decrypt ssh key"
	}
	# Install ssh stuff.
	Copy-Item -Path appveyor\ssh_id_rsa -Destination $env:userprofile\.ssh\id_rsa
	if ($errorCode -ne 0) { $host.SetShouldExit($errorCode) }
}
Copy-Item -Path appveyor\ssh_known_hosts -Destination $env:userprofile\.ssh\known_hosts
