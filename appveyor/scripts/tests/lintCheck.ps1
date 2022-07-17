if ($env:APPVEYOR_PULL_REQUEST_NUMBER -or $env:APPVEYOR_REPO_BRANCH.StartsWith("try-")) {
	$lintOutput = (Resolve-Path .\testOutput\lint\)
	$lintSource = (Resolve-Path .\tests\lint\)
	$flake8Output = "$lintOutput\Flake8.txt"
	# When Appveyor runs for a pr,
	# the build is made from a new temporary commit,
	# resulting from the pr branch being merged into its base branch.
	# Therefore to create a diff for linting, we must fetch the head of the base branch.
	# In a PR, APPVEYOR_REPO_BRANCH points to the head of the base branch. 
	# Additionally, we can not use a clone_depth of 1, but must use an unlimited clone.
	if($env:APPVEYOR_PULL_REQUEST_NUMBER) {
		git fetch -q origin $env:APPVEYOR_REPO_BRANCH
		$msgBaseLabel = "PR"
	} else {
		# However in a pushed branch, we must fetch master.
		git fetch -q origin master:master
		$msgBaseLabel = "Branch"
	}
	.\runlint.bat FETCH_HEAD "$flake8Output" 
	if($LastExitCode -ne 0) {
		Set-AppveyorBuildVariable "testFailExitCode" $LastExitCode
		Add-AppveyorMessage "FAIL: Lint check. See test results for more information."
	} else {
		Add-AppveyorMessage "PASS: Lint check."
	}
	Push-AppveyorArtifact $flake8Output
	$junitXML = "$lintOutput\PR-Flake8.xml"
	py "$lintSource\createJunitReport.py" "$flake8Output" "$junitXML"
	Push-AppveyorArtifact $junitXML
	$wc = New-Object 'System.Net.WebClient'
	$wc.UploadFile("https://ci.appveyor.com/api/testresults/junit/$($env:APPVEYOR_JOB_ID)", $junitXML)
}
