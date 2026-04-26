# Future Design Refactor (Commit 435ecfcf80eecceea96dc6f8c6391a85bd41fadd)

## Context
Commit `435ecfcf80eecceea96dc6f8c6391a85bd41fadd` contains a complete visual redesign with new CSS color palette, typography, layout structure (hero section, sticky nav, card-based posts, newsletter signup, etc.) and refactored HTML templates.

## Goal
Apply the new design **without changing functionality**.

## Scope Rules
- ✅ Change **layout** (position, grid, spacing, visual structure)
- ✅ Change **styling** (colors, fonts, shadows, transitions)
- ✅ Reorder **buttons/links** on the page
- ✅ Update **CSS classes** and semantic structure
- ❌ Do **NOT** create new buttons/links
- ❌ Do **NOT** change link destinations or actions
- ❌ Do **NOT** add new features or Django logic
- ❌ Do **NOT** break existing functionality

## Key Changes from Commit
### CSS Changes
- Primary color: `#0055ff` (royal blue) → `#0ea5e9` (sky blue)
- Font sizing: `html { font-size: 62.5%; }` → `100%` (impacts all `rem` units)
- Removed CSS custom properties for individual spacing/font-sizes (simplified)
- Added new component classes: `.page`, `.hero`, `.nav`, `.btn`, `.featured`, `.posts-grid`, `.post-card`, `.newsletter`, `.dark-demo`
- Added responsive breakpoint: `@media (max-width: 768px)`

### HTML Structure Changes
- **`base.html`**: `.blog-wrapper` flex layout → simpler `.page` container
- **`_header.html`**: Complex search + multi-item menu → Simple sticky `.nav` with logo + 4 links
- **`index.html`**: Flat card grid → Hero section + "Recentes" labeled posts grid
- **`post.html`**: Simplified layout, reduced meta info, cleaner structure
- **`_pagination.html`**: FontAwesome icons → Unicode symbols (`⟨⟩`)
- **`_post-card.html`**: Complete card layout rewrite (new image heights, body flex layout, footer with date/reading time)
- **`_footer.html`**: Centered text → 2-column grid layout with links

## Button/Link Mapping (PRESERVE THESE)
Before implementing, verify current buttons and map to new positions:

### Current (Verify in templates)
- Header nav: `/post/`, `/page/`, `#About`, `#Contact`, `#Support` (5 items)
- Search form (if kept)
- Post card "Read" links → post detail pages
- Pagination controls → first/prev/next/last functionality

### New Design (From commit)
- Sticky nav with logo + 4 links: "Início" (→ `/`), "Posts" (→ `/post/`), "Páginas" (→ `/page/`), "Sobre" (→ `#`)
- Hero section CTA buttons: "Ler artigos" (→ `/post/`) + "Sobre" (→ `#`)
- Post cards: "leia mais" arrow links
- Pagination: Unicode arrows, same functionality
- Newsletter signup (NEW FORM — needs analysis)
- Footer links: same navigation

### ⚠️ CRITICAL: Newsletter Form
The new design includes a newsletter signup section (`.newsletter-form`). This is **new UI** but check:
- Does it require a new Django model/view?
- Or is it just placeholder HTML?
- If new, this violates the "no new features" rule → discuss with user first

## Pre-Implementation Checklist
- [ ] Inventory all current buttons/links in `djangoapp/blog/templates/` (count, destinations, labels)
- [ ] Compare with new design buttons (how many match?)
- [ ] Test CSS isolation — can new CSS apply without breaking old HTML?
- [ ] Verify Django context — no logic tied to CSS class names?
- [ ] Check FontAwesome usage — old design uses icons, new uses Unicode
- [ ] Resolve newsletter form scope (new feature or placeholder?)

## Execution Strategy
1. **Backup current CSS**: `cp djangoapp/blog/static/blog/css/style.css style.css.backup`
2. **Apply new CSS wholesale** from commit
3. **Update HTML templates**:
   - Rename/add classes only (don't change `href`, `action`, `method`)
   - Preserve all Django template tags (`{% for %}`, `{{ variable }}`, `{% include %}`)
   - Update FontAwesome `<i>` tags to Unicode if needed
4. **Handle newsletter form**: Decide scope (UI-only vs functional)
5. **Test in browser**: All links work, no broken layouts, responsive on 768px
6. **Run Django server**: `python manage.py runserver` (no migrations needed unless newsletter added)

## Risk Areas & Mitigations
| Risk | Impact | Mitigation |
|------|--------|-----------|
| Responsive design | Layout breaks on mobile | Test with DevTools @768px after each change |
| Asset paths | Images not loading | Verify `/static/` paths match (unlikely) |
| django-summernote | Editor styling broken | May need CSS tweaks for `.CodeMirror` classes |
| `backdrop-filter: blur()` | Nav not blurred in old browsers | Add fallback or remove for IE11 support (check requirements) |
| FontAwesome → Unicode | Icons look different | Test icon readability, swap where needed |
| Newsletter form scope | Adds complexity | Clarify with user: UI-only or require backend? |

## Deferred Decisions (Ask Before Executing)
1. **CSS variable strategy**: Keep old spacing/font-size vars for backwards compat, or remove entirely?
2. **Newsletter form**: Include as placeholder UI, or skip until backend is ready?
3. **Commit granularity**: Single large refactor commit, or split CSS + HTML changes?
4. **Browser support**: Support IE11/older? (affects `backdrop-filter`, CSS grid browser support)

## Related Commits
- Current style (to compare): `djangoapp/blog/static/blog/css/style.css` (old variables, old color palette, old components)
- Design commit: `435ecfcf80eecceea96dc6f8c6391a85bd41fadd` (hero, sticky nav, sky blue, Unicode pagination)

## How to Execute Later
```bash
# 1. Checkout the design commit to see exact changes
git show 435ecfcf80eecceea96dc6f8c6391a85bd41fadd

# 2. Extract just the CSS file
git show 435ecfcf80eecceea96dc6f8c6391a85bd41fadd:djangoapp/blog/static/blog/css/style.css > /tmp/new-style.css

# 3. Extract template changes
git show 435ecfcf80eecceea96dc6f8c6391a85bd41fadd -- djangoapp/blog/templates/

# 4. Apply selectively, testing after each file
# (see Execution Strategy above)
```

## Notes
- This plan preserves **all functionality** while applying **new visual design**
- No new Django models, views, or business logic added
- Focus on CSS + HTML structure, not Python code
- User's constraint: "change layout, not features" is the north star
