# OldAS ChangeLog

## v0.12.0

**Released: 2026-02-08**

- Added `SubscribeResult` as a top-level export.
  ([#47](https://github.com/davep/oldas/pull/47))
- Cleaned up the URLs for some API calls.
  ([#52](https://github.com/davep/oldas/pull/52))
- Added support for some low-level `DEBUG` logging via a passed-in `Logger`
  object. ([#53](https://github.com/davep/oldas/pull/53))

## v0.11.0

**Released: 2026-01-30**

- The `User` class is now exported at the top level of the library.
  ([#41](https://github.com/davep/oldas/pull/41))
- `User.signup_time` is now a `datetime`.
  ([#41](https://github.com/davep/oldas/pull/41))
- Corrected the type of `User.is_blogger_user` (it had been left as `str`
  from very early testing, and has now become a `bool`).
  ([#41](https://github.com/davep/oldas/pull/41))
- Added the `OldASLoginNeeded` exception as a top-level export.
  ([#42](https://github.com/davep/oldas/pull/42))
- Added `Subscriptions.full_id`.
  ([#43](https://github.com/davep/oldas/pull/43))
- Added `Articles.full_id`. ([#44](https://github.com/davep/oldas/pull/44))

## v0.10.0

**Released: 2026-01-28**

- Removed sort-supporting comparison overrides for `Folder` and
  `Subscription`. ([#39](https://github.com/davep/oldas/pull/39))

## v0.9.0

**Released: 2026-01-28**

- Moved away from using `NamedTuple` as the base class for all the
  data-wrapping classes and started using frozen dataclasses.
  ([#36](https://github.com/davep/oldas/pull/36))
- Dropped the `raw` property from all classes.
  ([#36](https://github.com/davep/oldas/pull/36))

## v0.8.0

**Released: 2026-01-28**

- Added `in` support to `Subscriptions.Categories` for easier checking.
  ([#32](https://github.com/davep/oldas/pull/32))

## v0.7.0

**Released: 2026-01-27**

- Make `Folders` sortable by `Folder.name` by default.
  ([#30](https://github.com/davep/oldas/pull/30))
- Make `Subscriptons` sortable by `Subscription.title` by default.
  ([#30](https://github.com/davep/oldas/pull/30))

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
