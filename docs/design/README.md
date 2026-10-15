# Design references

PNG snapshots of the boards in the
[design canvas](https://claude.ai/artifact/8wmSXR2b3wGdrjB1sWHs24), one file
per board state, rendered 1440 px wide. Tickets embed these images so you can
see the target screen right in the issue.

- The canvas is the source of truth. If an image and the canvas disagree, the
  canvas wins; ask in the issue if you're unsure.
- Match tokens and structure, not pixels (see the style guide).
- The sample content is Ukrainian on purpose: layouts must handle Cyrillic.

| File | Board | State |
| ---- | ----- | ----- |
| [style-guide.png](style-guide.png) | Style guide | — |
| [home.png](home.png) | Home | — |
| [category-results.png](category-results.png) | Category with filters | Results |
| [category-no-results.png](category-no-results.png) | Category with filters | No results |
| [category-loading.png](category-loading.png) | Category with filters | Loading |
| [product-in-stock.png](product-in-stock.png) | Product page | In stock |
| [product-low-stock.png](product-low-stock.png) | Product page | Low stock |
| [product-out-of-stock.png](product-out-of-stock.png) | Product page | Out of stock |
| [product-not-found.png](product-not-found.png) | Product page | Not found |
| [admin-products-list.png](admin-products-list.png) | Admin: products | List |
| [admin-products-rows-selected.png](admin-products-rows-selected.png) | Admin: products | Rows selected |
| [admin-products-delete-dialog.png](admin-products-delete-dialog.png) | Admin: products | Delete dialog |
| [admin-products-empty.png](admin-products-empty.png) | Admin: products | Empty |
| [admin-product-form-edit-saved.png](admin-product-form-edit-saved.png) | Admin: product form | Edit, saved |
| [admin-product-form-new-with-errors.png](admin-product-form-new-with-errors.png) | Admin: product form | New, with errors |
| [admin-categories-editing.png](admin-categories-editing.png) | Admin: categories | Editing a category |
| [admin-categories-delete-blocked.png](admin-categories-delete-blocked.png) | Admin: categories | Delete blocked |

## Known differences from current decisions

- The style guide says prices are stored as integers in kopiyky. The backend
  stores them as decimals instead (`DECIMAL(10,2)`), so `550.10` is a valid
  price.
- Category URLs are shown as `/<slug>` in the admin. The store uses
  `/categories/<slug>`.
