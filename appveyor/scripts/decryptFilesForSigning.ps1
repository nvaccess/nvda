if(!$env:APPVEYOR_PULL_REQUEST_NUMBER) {
	openssl enc -d -md sha256 -aes-256-cbc -pbkdf2 -salt -pass pass:$env:secure_authenticode_pass -in appveyor\authenticode.pfx.enc -out appveyor\authenticode.pfx
	if($LastExitCode -ne 0) {
		$errorCode=$LastExitCode
		Add-AppveyorMessage "Unable to decrypt authenticode certificate"
	}
	openssl enc -d -md sha256 -aes-256-cbc -pbkdf2 -salt -pass pass:$env:secure_ssh_pass -in appveyor\ssh_id_rsa.enc -out appveyor\ssh_id_rsa
	if($LastExitCode -ne 0) {
		$errorCode=$LastExitCode
		Add-AppveyorMessage "Unable to decrypt ssh key"
	}
	# Install ssh stuff.
	Copy-Item -Path appveyor\ssh_id_rsa -Destination $env:userprofile\.ssh\id_rsa
}
Copy-Item -Path appveyor\ssh_known_hosts -Destination $env:userprofile\.ssh\known_hosts
if ($errorCode -ne 0) { $host.SetShouldExit($errorCode) }
