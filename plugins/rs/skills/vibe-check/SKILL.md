---
name: vibe-check
description: >-
  Audit UI quality across 8 dimensions and catch AI sameness. Scores design
  system compliance, visual hierarchy, spacing, contrast, typography,
  responsive, interactions, and accessibility. Returns a scorecard with
  priority-ordered fixes. TRIGGER on "vibe check", "UI audit", "design review",
  "does this look right", "check my UI", "how does this look" — even without
  naming the skill.
---

# Vibe Check

Audit a UI against 8 quality dimensions. Return a scorecard with priority-ordered fixes.

## When to Run

- After building a new component or page
- Before shipping a feature
- When a UI "feels off" but you can't pinpoint why
- After AI generates UI (catch AI sameness)

## The 8 Dimensions

### 1. Design System Compliance

Values come from the system or were invented ad-hoc:

| Look for | Bad signal |
|----------|-----------|
| Colors | Random hex not in palette |
| Spacing | Values off the 4px/8px grid |
| Typography | Font sizes outside the defined scale |
| Radius | Inconsistent border-radius values |
| Shadows | Mix of system tokens and one-off values |

### 2. Visual Hierarchy

Can the eye read the page in 3 seconds?

- Headings clearly larger than body
- CTAs stand out (color, size, or both)
- Important content weighted above noise
- No "wall of equal" where everything competes

### 3. Spacing & Rhythm

Consistent cadence, not random gaps:

- Vertical rhythm follows a scale (8, 16, 24, 32, 48)
- Grouped elements tighter than section breaks
- No orphaned 5px/13px/17px values
- Breathing room around content blocks

### 4. Color & Contrast

WCAG AA minimum (4.5:1 text, 3:1 large/UI):

- Text on background meets 4.5:1
- Interactive elements meet 3:1 against surroundings
- Color is semantic (red = error, green = success), not decorative
- No two accent colors fighting for attention

### 5. Typography

Readability and hierarchy through type:

- Body: 14-16px, line-height 1.5+
- Headings: clear weight step (400 body → 600 heads)
- Monospace for numbers, IDs, codes
- One display font max. No mixing display fonts.

### 6. Responsive

Works at every breakpoint:

- Mobile (320-375): single column, touch targets 44px+
- Tablet (768-1024): adaptive grid
- Desktop (1024+): full layout
- No horizontal overflow at any width
- Text not too large on mobile

### 7. Interactions & States

Feels alive, not static:

- Hover on interactive elements (color shift, shadow, scale)
- Focus indicators visible (ring, outline)
- Active/pressed state (scale, darken)
- Transitions: 150-200ms micro, 300-400ms macro
- Loading/disabled states exist

### 8. Accessibility

Everyone can use it:

- Semantic HTML (button not div, nav not div)
- ARIA labels on icon-only controls
- Keyboard navigation works (tab order, focus trap in modals)
- Color not the sole indicator of state
- Images have alt text

## AI Sameness Check

Layer on top of the 8 dimensions. Flag the "median of the internet" feel:

| AI default | Problem | Fix |
|-----------|---------|-----|
| Indigo/purple gradients | Training data saturation | Pick an accent that fits the product |
| Three-column icon grid | Every SaaS template | Vary card layouts by content type |
| Centered hero + CTA | Default starting point | Consider split layout, dense dashboard, content-forward |
| Uniform border-radius | `rounded-lg` everywhere | Vary by component role (sharp data, soft interactive) |
| White cards + subtle shadow | Safest surface treatment | Commit to a depth strategy that matches the product |
| Inter/system font everywhere | Statistically safest | Pick typography with personality |
| Decorative gradients | Looks "modern" without meaning | Gradients should be functional, not decorative |

**The test:** Swap your brand name with a competitor's. If the design still works, it's too generic.

## Output Format

### Scorecard

```
Dimension              Score  Status
────────────────────── ────── ───────
Design System          8/10   ✅
Visual Hierarchy       6/10   ⚠️
Spacing & Rhythm       5/10   ⚠️
Color & Contrast       4/10   ❌
Typography             7/10   ✅
Responsive             3/10   ❌
Interactions & States  5/10   ⚠️
Accessibility           6/10   ⚠️
AI Sameness            4/10   ❌
────────────────────── ────── ───────
OVERALL                5.3/10
```

✅ 7+  |  ⚠️ 4-6  |  ❌ <4

### Priority Fixes

Max 5, ordered by impact. Each fix:

1. **What's wrong** — with line number or selector
2. **Why it matters** — one sentence
3. **The exact change** — concrete fix

```
1. [CRITICAL] Contrast: body text #666 on #F0F0F0 = 3.2:1
   Line 42. Fix: text-gray-600 → text-gray-700 (4.6:1)

2. [HIGH] Responsive: 3-col grid on mobile
   Line 15. Fix: grid-cols-1 md:grid-cols-3

3. [HIGH] AI Sameness: indigo gradient on hero
   Line 8. Pick product-specific accent (the design skill can help)

4. [MEDIUM] Spacing: p-4 on cards feels cramped
   Line 22. Fix: p-4 → p-6

5. [MEDIUM] No hover state on cards
   Line 35. Fix: hover:shadow-lg transition-shadow duration-200
```

### Strengths

2-3 things working well. Balance the critique.

## Usage

```
/vibe                  # Audit current file or component
/vibe src/pages/home   # Audit a specific path
```

After fixing, re-run to see the score move.