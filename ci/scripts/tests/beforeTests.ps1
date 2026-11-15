New-Item -ItemType directory -Path testOutput
New-Item -ItemType directory -Path testOutput\unit
New-Item -ItemType directory -Path testOutput\install
New-Item -ItemType directory -Path testOutput\system
New-Item -ItemType directory -Path testOutput\lint
New-Item -ItemType directory -Path testOutput\license
curl https://github.com/nvaccess/nvdaL10n/releases/latest/download/l10nUtil.exe -L -o miscDeps/tools/l10nUtil.exe
