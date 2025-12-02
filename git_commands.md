
### Fetch

https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches

`git fetch origin`

Fetches changes from origin, moves e.g. origin/master

### Push

`git push <remote> <branch>`
<<<<<<< Updated upstream
Pushes `<branch>` to `<remote>`
`git push <remote> <branch>:<remotebranch>`
=======

Pushes `<branch>` to `<remote>`

`git push <remote> <branch>:<remotebranch>`

>>>>>>> Stashed changes
Pushes `<branch>` but it is called `<remotebranch>` in `<remote>`


### Merge

`git merge <branch>`

Replays changes made on `<branch>` since it diverged from current branch on top of current branch.

*Warning*: Running git merge with non-trivial uncommitted changes is discouraged: while possible, it may leave you in a state that is hard to back out of in the case of a conflict. 
