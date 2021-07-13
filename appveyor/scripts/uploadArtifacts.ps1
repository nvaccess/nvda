$ErrorActionPreference = "Stop";
# Upload artifacts, preserving directory structure.
$uploadFromFolder = "output\"
if( Test-Path $uploadFromFolder ){
	$root = Resolve-Path .\
	$output = Resolve-Path $uploadFromFolder
	$paths = [IO.Directory]::GetFiles($output.Path, '*.*', 'AllDirectories')
	$paths | % {
		Push-AppveyorArtifact $_ -FileName $_.Substring($root.Path.Length + 1)
	}
}
