# Contributing

This project works like a small product team. Every change starts as an issue
on the [project board](https://github.com/users/vkryvosheia/projects/1) and
reaches `main` through a reviewed pull request. Nobody pushes to `main`
directly; GitHub blocks it.

## Workflow

1. **Pick a card from the Ready column.** Assign the issue to yourself and move
   the card to In Progress. Read the whole issue, including *Out of scope* and
   *Depends on*. If something is unclear, ask in the issue before you start.
2. **Create a branch from the issue.** In the issue's right sidebar, under
   *Development*, click **Create a branch**. Change the suggested name to
   follow the [naming rules](#branch-naming) and keep `main` as the source.
   Then check it out locally:

   ```bash
   git fetch origin
   git switch feat/12-product-list
   ```

3. **Do the work.** Commit in small steps with clear messages. Run the tests
   and checks from the [README](README.md#running-tests-and-checks) before you
   push.
4. **Open a pull request** into `main`. Fill in the template. The description
   must contain `Closes #12` (your issue number): that links the PR to the
   issue and closes the issue automatically when the PR is merged.
5. **Review.** Wait for CI to go green and for an approval. Answer every review
   comment, either with a fix or with a reply, and resolve the conversation
   when it's settled; all conversations must be resolved before you can merge.
   Pushing new commits dismisses an earlier approval, so ask for a re-review
   after you push fixes.
6. **Squash and merge.** Once approved and green, merge with **Squash and
   merge** (the only option). All your commits become one commit on `main`, and
   the PR title becomes its message, so make the title a good one-line summary.
   Delete the branch afterwards (GitHub offers a button).
7. **Update your local `main`** before starting the next ticket:

   ```bash
   git switch main
   git pull
   ```

## Branch naming

`<type>/<issue number>-<short-name>`, lowercase, words separated by hyphens:

| Type     | Use for                                  | Example                       |
| -------- | ---------------------------------------- | ----------------------------- |
| `feat/`  | New features or behaviour                | `feat/12-product-list`        |
| `fix/`   | Bug fixes                                | `fix/31-cart-total-rounding`  |
| `chore/` | Tooling, dependencies, config, refactors | `chore/40-upgrade-vite`       |
| `docs/`  | Documentation only                       | `docs/18-api-setup-notes`     |

## Definition of Done

A ticket is done when all of these are true:

- [ ] All acceptance criteria in the issue are met.
- [ ] New backend logic has tests, and CI is green.
- [ ] The PR description explains how to test the change, includes screenshots
      for UI changes, and contains `Closes #N`.
- [ ] Schema changes come with an Alembic migration whose `downgrade()` also
      works (try `uv run alembic downgrade -1`, then `upgrade head` again).
- [ ] No debug leftovers: no `print()` / `console.log()`, commented-out code,
      or stray files.
- [ ] You can explain every line of the change.

## AI tools policy

<!-- TODO(lead): write the AI tools policy. -->

TODO(lead)
