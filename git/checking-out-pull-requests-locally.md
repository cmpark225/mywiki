1. Find the ID Number of the inactive pull request. This is the sequence of digits right after the pull request's title


2. Fetch the reference to the pull request based on its ID number, creating a new branch in the process
```
$git fetch origin pull/ID/head:BRANCHNAME
```

3. Switch to the new branch that's based on this pull request:
```
$git checkout BRANCHNAME
switched to branch BRANCHNAME
```
