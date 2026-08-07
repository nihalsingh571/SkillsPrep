# Appendix A: The Ultimate Git Industry Cheat Sheet

Welcome to the ultimate Git cheat sheet for production engineering. This guide goes beyond basic commands, diving into internals, production practices, common pitfalls, and interview insights. Master this, and you will navigate source control like a true Senior Engineer.

---

## SECTION 1: Git Internals (Briefly — for interview depth)

Understanding Git internals is critical for senior roles. Git is fundamentally a **content-addressable filesystem** built on a key-value data store.

### The Object Model
Git stores data using four primary object types, each identified by a SHA-1 hash (40-character hex string).
- **Blob (Binary Large Object):** Represents file content. It stores *only* the data, not the filename or metadata.
- **Tree:** Represents a directory. It contains pointers (hashes) to blobs (files) and other trees (subdirectories), along with their filenames and permissions.
- **Commit:** Represents a snapshot in time. It points to a single top-level tree object, along with author details, timestamp, commit message, and pointers to parent commit(s).
- **Tag:** An object that points to a specific commit, often containing a message, tagger details, and a GPG signature.

### How Commits Link
Each commit points to its parent commit(s) (except the initial commit). This forms a Directed Acyclic Graph (DAG) of history.
- **Why this matters:** When you change a past commit, its SHA-1 hash changes. Because all subsequent commits point to their parents, their hashes must also change. This is why history rewrites (like rebase) are destructive and create entirely new commit objects.

### References (Refs)
- **HEAD:** A symbolic reference pointing to the current branch or commit you have checked out. Internally, it usually contains a path like `ref: refs/heads/main`.
- **Branches:** Simply lightweight, movable pointers to a specific commit. When you commit, the branch pointer moves forward automatically.

### The Index (Staging Area)
The index is a binary file (`.git/index`) that sits between your working directory and the repository. It tracks the state of the trees that will become the *next* commit. When you `git add`, Git hashes the file, stores it as a blob in the object database, and updates the index to point to that blob.

### `.git` Directory Structure
- `objects/`: The object database (blobs, trees, commits, tags).
- `refs/`: Pointers to commits (branches, tags, remotes).
- `HEAD`: The current branch pointer.
- `index`: The staging area.
- `config`: Repository-specific configuration.

---

## SECTION 2: Repository Management

Managing the lifecycle and configuration of repositories.

### `git init`
- **Purpose:** Initializes a new, empty Git repository in the current directory.
- **Syntax:** `git init`
- **Real Example:** `mkdir new-project && cd new-project && git init`
- **Production Usage:** Used when starting a new service from scratch.
- **Common Mistakes:** Running it in the home directory by accident (`~/.git` is a nightmare).
- **Interview:** "What actually happens when you run git init?" -> It creates the `.git` directory structure.

### `git clone`
- **Purpose:** Copies an existing remote repository to your local machine.
- **Syntax:** `git clone <url>`
- **Real Example:** `git clone git@github.com:org/repo.git`
- **Production Usage:** Getting the codebase. 
  - **Shallow Clone:** `git clone --depth 1 <url>` (Only fetches the latest commit; huge time saver for CI/CD pipelines).
  - **Single Branch:** `git clone --single-branch --branch main <url>` (Saves bandwidth for massive repos).
- **Common Mistakes:** Cloning into an already nested git repository.

### `git remote`
- **Purpose:** Manages connections to other repositories.
- **Syntax:** `git remote [add|remove|rename|set-url] <name> <url>`
- **Real Example:** `git remote add upstream git@github.com:original/repo.git` (For forked repos).
- **Production Usage:** Keeping a fork synced with the upstream parent repo. Checking remotes with `git remote -v`.
- **Common Mistakes:** Forgetting to update the remote URL after a repository migration (`git remote set-url origin <new-url>`).

### `git fetch` vs `git pull`
- **Purpose:** Getting updates from the remote.
- **Explanation:** 
  - `git fetch` downloads objects and refs from another repository. It *never* touches your working tree or current branch. It updates `origin/main`.
  - `git pull` is essentially `git fetch` followed immediately by `git merge` (or `git rebase` if configured).
- **Production Usage:** Always prefer `git fetch` then inspect changes (e.g., `git log origin/main`) before merging, or use `git pull --rebase` to avoid merge commits.
- **Interview:** "What is the difference between fetch and pull?" -> Fetch gets data safely; pull gets data and integrates it forcefully.

### `git config`
- **Purpose:** Set configuration variables.
- **Syntax:** `git config [--global|--local] <key> <value>`
- **Real Example:** `git config --global user.name "John Doe"`
- **Production Usage:** Setting up GPG keys (`commit.gpgsign`), default branch names (`init.defaultBranch main`), and aliases.

---

## SECTION 3: Staging and Committing

Moving changes from the working directory to the object database.

### `git add`
- **Purpose:** Adds changes to the index (staging area).
- **Syntax:** `git add <file>`
- **Real Example:** `git add .` (stages all changes) or `git add src/main.rs`.
- **Production Usage:** 
  - `git add -p` (patch mode): Interactively choose which chunks of a file to stage. Essential for clean, atomic commits when you've done messy work.
- **Common Mistakes:** Blindly running `git add .` and committing compiled binaries or secrets.

### `git commit`
- **Purpose:** Records changes to the repository.
- **Syntax:** `git commit -m "message"`
- **Real Example:** `git commit -m "feat(auth): implement JWT validation"`
- **Production Usage:** Enforcing conventional commits. Using `git commit -S` to GPG sign commits.
- **Interview:** "What makes a good commit?" -> Atomic (one logical change), well-documented, passes tests.

### `git commit --amend`
- **Purpose:** Modifies the *most recent* commit.
- **Syntax:** `git commit --amend`
- **Real Example:** Forgot a file? `git add forgotten-file.txt` then `git commit --amend --no-edit`. Typo in message? `git commit --amend -m "new message"`.
- **Production Usage:** Cleaning up local history before pushing.
- **Common Mistakes:** Amending a commit that has *already been pushed* to a shared branch (causes divergence).
- **Interview:** "Why shouldn't you amend pushed commits?" -> It changes the SHA-1 hash, forcing others to resolve conflicts if they pull.

### Unstaging (`reset HEAD` and `restore --staged`)
- **Purpose:** Removing files from the staging area without losing working directory changes.
- **Syntax:** 
  - Legacy: `git reset HEAD <file>`
  - Modern: `git restore --staged <file>`
- **Real Example:** `git restore --staged .env` (Oops, didn't mean to stage the secrets file).

---

## SECTION 4: Branching

Branches isolate work streams.

### `git branch`
- **Purpose:** List, create, or delete branches.
- **Syntax:** `git branch [-a|-r|-d|-D|-m] <branchname>`
- **Real Example:** `git branch -d feature-x` (Delete branch if fully merged). `git branch -D feature-x` (Force delete unmerged branch).
- **Production Usage:** `git branch -a` (List local and remote branches). `git branch -m old new` (Rename branch).

### `git checkout` vs `git switch`
- **Purpose:** Switch branches or restore working tree files.
- **Syntax:** `git checkout <branch>` OR `git switch <branch>`
- **Explanation:** `git checkout` was historically overloaded (it did branching AND file restoration). `git switch` (introduced in Git 2.23) is purpose-built *only* for changing branches, making it safer and more intuitive.
- **Real Example:** `git switch main` vs `git checkout main`.

### Creating Branches
- **Legacy:** `git checkout -b <new-branch>`
- **Modern:** `git switch -c <new-branch>`
- **Production Usage:** Creating feature branches off `main`.

### Tracking Branches
- **Purpose:** Link a local branch to a remote branch.
- **Syntax:** `git branch -u origin/<branch>`
- **Real Example:** `git branch -u origin/main` (Sets upstream so `git pull` knows where to pull from).

### Orphan Branches
- **Purpose:** Create a branch with no commit history (disconnected from DAG).
- **Syntax:** `git checkout --orphan <branch>`
- **Real Example:** `git checkout --orphan gh-pages`.
- **Production Usage:** Hosting documentation or compiled assets entirely separate from source code history.

---

## SECTION 5: Merging and Rebasing

Integrating changes from one branch to another. This is the heart of collaboration.

### `git merge`
- **Purpose:** Joins two or more development histories together.
- **Syntax:** `git merge <branch>`
- **Explanation:** 
  - **Fast-forward (`--ff`):** If the target branch hasn't diverged, Git just moves the pointer forward. No merge commit.
  - **No fast-forward (`--no-ff`):** Forces a merge commit even if a fast-forward is possible.
- **Production Usage:** Use `--no-ff` when merging feature branches to `main` to preserve the feature's historical grouping.

### `git merge --squash`
- **Purpose:** Combines all commits from the merged branch into a single set of staged changes.
- **Syntax:** `git merge --squash <branch>` then `git commit`
- **Production Usage:** Taking 50 "wip" commits from a feature branch and squashing them into one clean commit on main.

### `git rebase`
- **Purpose:** Reapplies commits on top of another base tip. Rewrites history.
- **Syntax:** `git rebase <base>`
- **Real Example:** While on `feature`, run `git rebase main`.
- **Internals:** Git rewinds your branch, fast-forwards to the new base, and replays your commits one by one. New SHAs are generated.
- **Interactive Rebase:** `git rebase -i HEAD~5`. Opens an editor to pick, drop, squash, reword, or fixup the last 5 commits.
- **Rebase --onto:** `git rebase --onto main feature-old feature-new` (Move `feature-new` from `feature-old` to `main`).
- **Production Usage:** Keeping feature branches up-to-date with main without cluttering history with merge commits. Cleaning local commits before PR.

### Merge vs Rebase Comparison
| Feature | `git merge` | `git rebase` |
| :--- | :--- | :--- |
| **History** | Preserves exact history & chronological order. | Rewrites history into a clean, linear progression. |
| **Commits** | Adds a merge commit (if diverged). | Creates entirely new commit objects (new SHAs). |
| **Conflicts** | Resolve all conflicts once at the merge commit. | Resolve conflicts per-commit as they are replayed. |
| **Safety** | Non-destructive. Safe for shared branches. | Destructive. **NEVER REBASE A PUBLIC/SHARED BRANCH.** |

### Conflict Resolution
When rebase or merge halts due to conflicts:
1. Open conflicting files and edit (look for `<<<<<<< HEAD`).
2. `git add <resolved-file>`
3. `git rebase --continue` (or `git commit` if merging).

---

## SECTION 6: Remote Operations

Moving data across the network.

### `git push`
- **Purpose:** Update remote refs along with associated objects.
- **Syntax:** `git push <remote> <branch>`
- **Real Example:** `git push origin main`

### Force Pushing
- **Syntax:** `git push --force` vs `git push --force-with-lease`
- **Explanation:** Rewriting history (rebase, amend) requires force pushing.
  - `--force`: Blindly overwrites the remote. Dangerous.
  - `--force-with-lease`: Checks if the remote branch has been updated by someone else since your last fetch. If so, it aborts.
- **Production Usage:** ALWAYS use `--force-with-lease` when force pushing.

### Push Extras
- **Push Tags:** `git push --tags` (Normal push doesn't push tags).
- **Delete Remote Branch:** `git push origin :branch-name` (or `git push origin -d branch-name`).
- **Set Upstream:** `git push -u origin feature/xyz` (Push and set tracking simultaneously).

### `git pull --rebase`
- **Purpose:** Fetches updates and rebases your local commits on top of them.
- **Production Usage:** Preferred over standard `git pull` to avoid useless "Merge branch 'main' of..." commits in history.

### `git fetch --all --prune`
- **Purpose:** Fetches from all remotes and deletes local tracking branches that no longer exist on the remote. Keeps your local repo clean.

---

## SECTION 7: Cherry-Pick

Surgically applying commits.

### `git cherry-pick`
- **Purpose:** Apply the changes introduced by some existing commits.
- **Syntax:** `git cherry-pick <commit-hash>`
- **Real Example:** `git cherry-pick 9fceb02`
- **Range:** `git cherry-pick A..B` (Applies commits from A to B).
- **No Commit:** `git cherry-pick --no-commit <hash>` (Applies changes to working directory but pauses before committing).
- **Production Usage:** 
  - A bug fix is merged to `main`, but needs to be backported to the `release/1.0` branch.
- **Pitfalls:** Cherry-picking creates a *duplicate* commit with a different SHA. If the branches are later merged, Git can usually handle it, but it creates messy history.
- **Interview:** "How do you move a specific commit from one branch to another?" -> Cherry-pick.

---

## SECTION 8: Undoing Changes

The most terrifying part of Git, made simple.

### `git revert`
- **Purpose:** Given one or more existing commits, revert the changes that the related patches introduce, and record some **new** commits that record them.
- **Syntax:** `git revert <hash>`
- **Production Usage:** Safest way to undo a commit on a shared branch (like `main`). It moves history forward.
- **Interview:** "Difference between revert and reset?" -> Revert creates a new commit undoing the changes (safe for public). Reset moves the branch pointer backward (destructive, dangerous for public).

### `git reset`
- **Purpose:** Reset current HEAD to the specified state.
- **Syntax:** `git reset [--soft|--mixed|--hard] HEAD~1` (moves back one commit).
- **Modes:**
  - `--soft`: Moves HEAD back. Keeps working directory and staging area identical to before. (Perfect for squashing).
  - `--mixed` (Default): Moves HEAD back. Unstages everything. Keeps working directory changes.
  - `--hard`: Moves HEAD back. DESTROYS all staged and working directory changes. Permanent data loss (unless committed and found in reflog).
- **Production Usage:** `git reset --hard origin/main` (Throw away local mess and exactly match the remote).

### File Restoration
- **Discard working directory changes:** `git restore <file>`
- **Unstage file:** `git restore --staged <file>`

### Undo Comparison Matrix
| Command | Modifies History? | Working Directory Safe? | Use Case |
| :--- | :--- | :--- | :--- |
| `revert` | No (Adds new commit) | Yes | Public branch mistakes. |
| `reset --soft` | Yes (Rewinds) | Yes | Combining local commits. |
| `reset --mixed` | Yes (Rewinds) | Yes | Un-committing to rework chunks. |
| `reset --hard` | Yes (Rewinds) | **NO** | Throwing away all local work. |

---

## SECTION 9: Stashing

Saving incomplete work.

### `git stash`
- **Purpose:** Temporarily shelves (or stashes) changes you've made to your working copy.
- **Syntax:** `git stash` (or `git stash push -m "wip: auth logic"`)
- **Real Example:** You are halfway through a feature, production breaks, you need to switch to main to hotfix.
- **List Stashes:** `git stash list`
- **Apply Stash:** 
  - `git stash pop`: Applies stash and deletes it from stash list.
  - `git stash apply`: Applies stash but keeps it in the list (good if applying to multiple branches).
- **Drop Stash:** `git stash drop stash@{0}`
- **Branch from Stash:** `git stash branch feature-x` (Creates branch and applies stash).
- **Include Untracked:** `git stash -u` (By default, untracked files aren't stashed).
- **Specific Files:** `git stash push file1.js`

---

## SECTION 10: Tags

Marking release points.

### Lightweight vs Annotated
- **Lightweight:** Just a pointer to a commit.
  - `git tag v1.0.0`
- **Annotated:** A full object in the Git database with a tagger, date, message, and signature.
  - `git tag -a v1.0.0 -m "Release 1.0.0"`
- **Production Usage:** Always use annotated tags for actual software releases.

### Tag Operations
- **Pushing Tags:** `git push origin --tags`
- **Signed Tags:** `git tag -s v1.0.0` (Requires GPG key. Ensures authenticity).
- **Semantic Versioning:** Industry standard: `MAJOR.MINOR.PATCH` (e.g., `v2.4.1`).
- **Delete Remote Tag:** `git push origin :refs/tags/v1.0.0`

---

## SECTION 11: Reflog

The ultimate safety net.

### `git reflog`
- **Purpose:** Manages reflog information. It records every time the tip of branches (HEAD) is updated, even if history was rewritten.
- **Syntax:** `git reflog`
- **Internals:** Stored locally in `.git/logs/`. Defaults to keeping entries for 30-90 days.
- **Production Usage:** 
  - **Recover from hard reset:** Find the SHA before the reset in the reflog, then `git reset --hard <SHA>`.
  - **Recover deleted branch:** Find the SHA of the branch tip, then `git branch recovered-branch <SHA>`.
- **Interview:** "How do you recover a commit that was accidentally hard reset?" -> Use `git reflog` to find the orphaned SHA, then `git reset --hard` or `git checkout` to it. As long as it was committed locally, Git hasn't garbage collected it yet.

---

## SECTION 12: Bisect

Debugging via binary search.

### `git bisect`
- **Purpose:** Use binary search to find the commit that introduced a bug.
- **Syntax:**
  1. `git bisect start`
  2. `git bisect bad` (Current commit is broken).
  3. `git bisect good <commit-hash>` (A past commit known to work).
  4. Git checks out a commit halfway between. You test the code.
  5. Type `git bisect good` or `git bisect bad`.
  6. Repeat until Git identifies the exact commit that broke the code.
  7. `git bisect reset` (to return to original state).
- **Automated Bisect:** `git bisect run ./test.sh`. Git will automatically run the script and mark good/bad based on the exit code (0 = good, non-zero = bad).
- **Production Usage:** "The app worked 2 weeks ago, now it doesn't, and there are 500 commits between now and then. Find the bug."

---

## SECTION 13: Worktrees

Multiple working directories for one repo.

### `git worktree`
- **Purpose:** Manage multiple working trees attached to the same repository.
- **Syntax:** `git worktree add <path> <branch>`
- **Real Example:** `git worktree add ../hotfix-branch hotfix-123`
- **Why?** You are compiling a massive feature branch, and a critical bug drops. Switching branches requires stashing, rebuilding, clearing node_modules, etc. With worktrees, you just checkout a branch into a completely separate directory on your filesystem, sharing the same `.git` object database.
- **Cleanup:** `git worktree remove ../hotfix-branch`

---

## SECTION 14: Submodules

Repositories inside repositories.

### `git submodule`
- **Purpose:** Allows you to keep a Git repository as a subdirectory of another Git repository.
- **Syntax:** `git submodule add <url> <path>`
- **Real Example:** `git submodule add git@github.com:org/shared-lib.git libs/shared`
- **Cloning a repo with submodules:** `git clone --recurse-submodules <url>`
- **Updating:** `git submodule update --init --recursive`
- **Production Reality:** Submodules are notoriously painful because they point to specific SHAs, not branches. Developers constantly forget to commit the updated submodule pointer or push the submodule changes, breaking CI.
- **Alternatives:** `git subtree`, or better yet, proper package managers (npm, pip, cargo, maven).

---

## SECTION 15: Hooks

Automating actions locally.

### Git Hooks
- **Purpose:** Custom scripts executed automatically when specific Git events occur.
- **Internals:** Stored in `.git/hooks/`.
- **Key Hooks:**
  - `pre-commit`: Runs before commit. Used for linters, formatters (Prettier), secret scanning (TruffleHog).
  - `commit-msg`: Runs to validate the commit message format (Conventional Commits).
  - `pre-push`: Runs before pushing. Used to run the full test suite.
- **Production Usage:** 
  - Using tools like **Husky** (Node.js) or **pre-commit** (Python/General) to enforce hooks across the entire team, since `.git/hooks/` is not committed to the repository by default.

**Example `.pre-commit-config.yaml`:**
```yaml
repos:
-   repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.4.0
    hooks:
    -   id: trailing-whitespace
    -   id: end-of-file-fixer
    -   id: check-yaml
```

---

## SECTION 16: Advanced Logging

Extracting history effectively.

### `git log`
- **The Best Log:** `git log --oneline --graph --all --decorate` (Visualizes branches, merges, and tags in the terminal).
- **Filter by Author:** `git log --author="Nihal"`
- **Filter by Time:** `git log --since="2 weeks ago" --until="yesterday"`
- **File History:** `git log -p <file>` (Shows the full diff of every change made to a file).
- **Follow Renames:** `git log --follow <file>` (Tracks a file's history even if it was renamed).

### `git blame`
- **Purpose:** Shows what revision and author last modified each line of a file.
- **Syntax:** `git blame <file>`
- **Production Usage:** Figuring out who to ask about a cryptic line of code.

### `git shortlog`
- **Purpose:** Summarize `git log` output.
- **Syntax:** `git shortlog -sn` (Shows a ranked list of contributors by commit count).

---

## SECTION 17: Searching

Finding code and history.

### `git grep`
- **Purpose:** Print lines matching a pattern in the working tree.
- **Syntax:** `git grep "TODO"`
- **Why not regular grep?** `git grep` only searches tracked files, ignoring `.git/`, `.gitignore` matches, and build artifacts. It is blazingly fast.

### The Pickaxe (`git log -S` / `-G`)
- **Purpose:** Search through commit history for changes to strings.
- **Syntax:** 
  - `git log -S "password"` (Finds commits where the number of occurrences of "password" changed — e.g., it was added or removed).
  - `git log -G "^function init"` (Finds commits where the diff matches the regex).
- **Production Usage:** "Who deleted the database connection string and when?"

---

## SECTION 18: Sparse Checkout and Large Repos

Handling monorepos and massive codebases.

### `git sparse-checkout`
- **Purpose:** Check out only a subset of the repository.
- **Syntax:** `git sparse-checkout init --cone` then `git sparse-checkout set <dir1> <dir2>`
- **Production Usage:** Working in a massive monorepo where checking out the whole tree takes minutes and crashes your IDE.

### Partial Clones
- **Syntax:** `git clone --filter=blob:none <url>`
- **Explanation:** Clones the repo structure (commits/trees) but downloads blobs (file contents) dynamically *only* when you checkout a commit containing them. Massive time saver.

### Git LFS (Large File Storage)
- **Purpose:** Replaces large files (audio, video, datasets) with text pointers inside Git, while storing the file contents on a remote server.
- **Why?** Git's object database chokes on large binary files because it compresses and stores entire snapshots.

---

## SECTION 19: Git Workflows

How teams collaborate.

### 1. GitFlow
- **Structure:** `main` (production), `develop` (integration), `feature/*` (new work), `release/*` (prep for prod), `hotfix/*` (urgent prod fixes).
- **When to use:** Software with scheduled, versioned releases (e.g., mobile apps, desktop software).
- **Pros:** Highly structured.
- **Cons:** Extremely heavy, leads to "merge hell", slows down delivery.

### 2. GitHub Flow
- **Structure:** `main` (always deployable), `feature/*` branches created off main. Pull Request -> Review -> Merge -> Deploy.
- **When to use:** Continuous Deployment (SaaS, Web Apps).
- **Pros:** Simple, fast, encourages small continuous updates.

### 3. Trunk-Based Development
- **Structure:** Everyone commits directly to `main` (the trunk) multiple times a day.
- **Enablers:** Feature flags (to hide incomplete work), heavy automated testing.
- **When to use:** High-velocity teams (FAANG), elite DevOps performers.
- **Pros:** Eliminates merge conflicts entirely, fastest possible delivery.
- **Cons:** Requires immense discipline and mature CI/CD.

---

## SECTION 20: Signing and Security

Proving you wrote the code.

### Commit Signing
- **Purpose:** Cryptographically signs commits to prove they came from you and were not tampered with.
- **GPG Signing:** `git commit -S -m "msg"`. Requires GPG keys configured locally and uploaded to GitHub/GitLab.
- **SSH Signing:** Newer and simpler. Uses your existing SSH authentication keys to sign commits. `git config --global gpg.format ssh`.
- **Verification:** `git log --show-signature`
- **GitHub Vigilant Mode:** A GitHub setting that flags any unsigned commit as "Unverified," protecting against commit spoofing (where someone sets `git config user.email` to your email).

---

## SECTION 21: Aliases Cheat Sheet

Save thousands of keystrokes. Add these to `~/.gitconfig`:

```ini
[alias]
    # The essentials
    st = status -sb
    co = checkout
    sw = switch
    ci = commit
    br = branch
    
    # Advanced Logging
    lg = log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit
    
    # Amending
    amend = commit --amend --no-edit
    
    # Rebasing
    ri = rebase -i HEAD~5
    rc = rebase --continue
    ra = rebase --abort
    
    # Syncing
    sync = pull --rebase origin main
    
    # Undoing
    unstage = restore --staged
    uncommit = reset --soft HEAD~1
    nuke = reset --hard HEAD
    
    # Diffing
    df = diff
    dc = diff --cached
```

---

## SECTION 22: Cleaning

Removing garbage.

### `git clean`
- **Purpose:** Remove untracked files from the working tree.
- **Syntax:** `git clean -fd`
- **Nuclear Option:** `git clean -fdx` (Removes untracked files AND ignored files, like `node_modules` or `target`. Resets repo to a pristine state).
- **Crucial Rule:** Always run `git clean -n` (dry run) first to see what will be deleted, as this data is untracked and **CANNOT BE RECOVERED**.

---

## END OF APPENDIX

### One-Page Quick Reference (Top 50)
1. `git init` - Create repo
2. `git clone <url>` - Copy repo
3. `git status` - View state
4. `git add .` - Stage all
5. `git add -p` - Stage chunks
6. `git commit -m ""` - Commit
7. `git commit --amend` - Fix last commit
8. `git push` - Upload
9. `git push --force-with-lease` - Upload rewrite
10. `git pull --rebase` - Download & integrate cleanly
11. `git fetch` - Download safely
12. `git branch` - List branches
13. `git switch -c <name>` - Create & switch branch
14. `git checkout <commit>` - View old state
15. `git merge <branch>` - Join branches
16. `git rebase main` - Move branch onto main
17. `git rebase -i HEAD~3` - Edit history
18. `git stash` - Save WIP
19. `git stash pop` - Restore WIP
20. `git log --oneline` - Short history
21. `git reflog` - Safety net history
22. `git reset --soft HEAD~1` - Uncommit
23. `git reset --hard HEAD~1` - Destroy uncommitted
24. `git revert <sha>` - Safe undo
25. `git cherry-pick <sha>` - Copy one commit
26. `git clean -fd` - Remove untracked
27. `git restore <file>` - Discard changes
28. `git restore --staged <file>` - Unstage
29. `git tag -a v1.0` - Create release
30. `git bisect start` - Start debugger
... (And 20 more derived from sections above: `git worktree`, `git submodule`, `git remote`, `git grep`, etc.)

### Common Disasters & Recovery
- **"I committed to main instead of a feature branch!"**
  `git branch feature` (save state to new branch), `git reset --hard HEAD~1` (rewind main), `git switch feature` (continue work).
- **"I hard reset and lost a commit!"**
  `git reflog` (find SHA), `git reset --hard <SHA>`.
- **"I committed a password!"**
  If pushed: Rotate the password immediately (it's compromised).
  If local: `git reset --soft HEAD~1`, remove password, `git add`, `git commit`.

### Production Workflow Matrix
- **Solo Dev:** Main branch, direct commits.
- **Open Source:** Fork, branch, PR, merge.
- **Enterprise SaaS:** Feature branches, PR, Squash & Merge to Main, CI/CD auto-deploys.
- **Regulated (Fintech):** GitFlow, signed commits, strict branch protections, multiple approvals required.
