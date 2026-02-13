git checkout -b $branchName
        git config --local user.name "GitHub Actions"
        git config --local user.email ""

        # Check each modified tracked po file.
        failures=
        tempfile=$(mktemp --tmpdir="$RUNNER_TEMP")
        # Take each \0-separated path from stdin
        while IFS= read -r -d $'\0' path <&3; do
          echo -n "Checking $path... "
          if output=$(uv run source/l10nutil.py checkPo "$path"); then
            # Add files that don't produce errors.
            echo Ok
            git add "$path"
          else
            # This file produced errors.
            echo Failed
            echo "$output" >&2
            echo "$output" >> $tempfile
            echo "----------" >> $tempfile
            # Append the language code to $failures
            # by stripping /LC_MESSAGES/nvda.po,
            # and getting the basename (the trailing path component)
            failures+="$(basename ${path%/LC_MESSAGES/nvda.po}), "
          fi
        # Substitute getting modified files into stdin
        done 3< <(git ls-files --modified -z source/locale/**.po)
        if [[ $failures ]]; then
          # $failures is not empty
          echo "has_failures=true" >> "$GITHUB_OUTPUT"
          echo "invalid_pofile_locales=${failures%, }" >> "$GITHUB_OUTPUT"
          echo "invalid_pofile_reports<<EOF"$'\n'"$(cat $tempfile)"$'\n'EOF >> $GITHUB_OUTPUT
        else
          echo "has_failures=false" >> "$GITHUB_OUTPUT"
        fi

        # Add modified tracked xliff files.
        git add -u user_docs

        # Check if there are any changes to commit
        if git diff --staged --quiet; then
          echo "No changes to commit"
          echo "has_changes=false" >> $GITHUB_OUTPUT
        else
          git commit -m "Update tracked translations from Crowdin"
          echo "has_changes=true" >> $GITHUB_OUTPUT
        fi
