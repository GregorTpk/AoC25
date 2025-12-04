
## Terminology
* **remote-tracking branch**: E.g. `origin/main`: It is a read-only mirror of the corresponding branch in remote. Tracking branches are updated e.g. by `fetch`. See below for getting/setting the tracked branch.
* **upstream branch**: The branch on remote, a local branch pushes to or pulls from. This is not quite the same as a **remote tracking branch**, which only is a local mirror.

## Commands

### Fetch/Pull

`fetch [remote]` retrieves changes from a remote, by default from `origin`. These changes are applied to the remote-tracking branches, e.g. `origin/main`. But neither the local branches, e.g. `main`, nor the working directory are changed.

`pull` on the other hand does a `fetch` and immediately applies the changes on the local branches with `rebase` or `merge` depending on the given arguments.

https://git-scm.com/book/en/v2/Git-Branching-Remote-Branches

`git fetch origin`

Fetches changes from origin, moves e.g. origin/master

### Push

`git push <remote> <branch>`

Pushes `<branch>` to `<remote>`. For example `git push origin my_branch`

`git push <remote> <branch>:<remotebranch>`

Pushes `<branch>` but it is called `<remotebranch>` in `<remote>`


### Merge

`git merge <branch>`

Replays changes made on `<branch>` since it diverged from current branch on top of current branch.

**Warning**: Running git merge with non-trivial uncommitted changes is discouraged: while possible, it may leave you in a state that is hard to back out of in the case of a conflict. 

### Stash

Quick way to return to a clean working directory without discarding nor committing changes to tracked files. The stash works like a stack where you can push and pop entries: You can push all changes in the working directory with

`git stash` or more explicitly `git push`

or push only selected files with

`git stash push path/to/file`.

You can pop the last entry from the stash with

`git stash pop`.

You can see all entries on the stash with

`git stash list`.

**Note**: Only tracked files can be stashed. If you want to stash a new file, that is not indexed by git, you need to do `git add path/to/file` before you stash it.


## Scenarios

#### Commited to Wrong Branch

Let's assume, you forgot to create a new branch first and have accidentally committed onto `main`. If you have not pushed already, you can fix it by

`git reset --soft HEAD~1` to undo the commit and add the undone changes to the staging area

`git checkout my_branch` or `git checkout -b my_new_branch`

`git commit`

#### Get/Set Upstream Branch

If you want to pull/push onto/from a local branch `my_branch` and get a fatal error, that no upstream branch is set you can do so by

`git branch --set-upstream-to=origin/<branch> my_branch`.

You can view the set upstream branches with

`git branch -vv`

and it is saved in .git/config as

```
[branch "my_branch"]
remote = origin
merge = refs/heads/my_branch
```
