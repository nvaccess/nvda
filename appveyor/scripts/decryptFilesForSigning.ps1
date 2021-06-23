    if(!$env:APPVEYOR_PULL_REQUEST_NUMBER) {
     openssl enc -d -md sha256 -aes-256-cbc -pbkdf2 -salt -pass pass:$env:secure_authenticode_pass -in authenticode.pfx.enc -out authenticode.pfx
     if($LastExitCode -ne 0) {
      $errorCode=$LastExitCode
      Add-AppveyorMessage "Unable to decrypt authenticode certificate"
     }
     openssl enc -md md5 -aes-256-cbc -d -pass pass:$env:secure_ssh_pass -in ssh_id_rsa.enc -out ssh_id_rsa
     if($LastExitCode -ne 0) {
      $errorCode=$LastExitCode
      Add-AppveyorMessage "Unable to decrypt ssh key"
     }
     # Install ssh stuff.
     copy ssh_id_rsa $env:userprofile\.ssh\id_rsa
     if ($errorCode -ne 0) { $host.SetShouldExit($errorCode) }
    }
