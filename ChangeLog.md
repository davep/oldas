# OldAS ChangeLog

## v0.6.0

**Released: 2026-01-25**

- Updated `Subscriptions.move` so that any form of "empty" for the
  `target_folder` is seen as a "remove folder" operation.
  ([#28](https://github.com/davep/oldas/pull/28))

## v0.5.0

**Released: 2026-01-24**

- Added `Subscription.folder_id`.
  ([#25](https://github.com/davep/oldas/pull/25))

## v0.4.0

**Released: 2026-01-21**

- Added `ArticleIDs.full_ids`.
  ([#10](https://github.com/davep/oldas/pull/10))
- Added `ArticleIDs.mark_read`.
  ([#10](https://github.com/davep/oldas/pull/10))
- Added `ArticleIDs.mark_unread`.
  ([#10](https://github.com/davep/oldas/pull/10))
- Added `Subscriptions.add`. ([#17](https://github.com/davep/oldas/pull/17))
- Added `Subscriptions.remove`.
  ([#18](https://github.com/davep/oldas/pull/18))
- Added `Folders.rename`. ([#19](https://github.com/davep/oldas/pull/19))
- Added `Folders.remove`. ([#20](https://github.com/davep/oldas/pull/20))
- Added `Subscriptions.rename`.
  ([#21](https://github.com/davep/oldas/pull/21))
- Added `Subscriptions.move`.
  ([#22](https://github.com/davep/oldas/pull/22))

## v0.3.1

**Released: 2026-01-07**

- Fix incompatibility with older Pythons.
  ([#8](https://github.com/davep/oldas/pull/8))

## v0.3.0

**Released: 2026-01-07**

- Added `ArticleIDs` and related classes, providing methods for loading up a
  list of pure article IDs. ([#4](https://github.com/davep/oldas/pull/4))
- Exposed `Prefix` and related code.
  ([#5](https://github.com/davep/oldas/pull/5))
- Exposed `State` and related code.
  ([#5](https://github.com/davep/oldas/pull/5))
- Exposed `oldas.types`. ([#5](https://github.com/davep/oldas/pull/5))

## v0.2.0

**Released: 2026-01-04**

- Added support for loading up the alternates for an article.
  ([#2](https://github.com/davep/oldas/pull/2))

## v0.1.0

**Released: 2026-01-01**

- Initial alpha release.

## v0.0.1

**Released: 2025-10-14**

- Initial placeholder package to test that the name is available in PyPI.

[//]: # (ChangeLog.md ends here)
