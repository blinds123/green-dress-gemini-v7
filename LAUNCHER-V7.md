# BULLETPROOF LAUNCHER V7.0 [Optimized Multi-Agent Protocol]

Deploy TikTok landing page with SimpleSwap crypto checkout. **Optimized for speed + token conservation.**

---

## SUBAGENT EXECUTION PROTOCOL

**CRITICAL: All agents MUST be launched using the Task tool with appropriate subagent_type and Claude skills.**

### Subagent Configuration

| Agent | subagent_type | Claude Skills to Load |
|-------|---------------|----------------------|
| 1A: Image Processor | `general-purpose` | None (file operations) |
| 1B: Content Generator | `general-purpose` | `~/.claude/plugins/marketplaces/anthropic-agent-skills/copywriting` |
| 1C: Pool Manager | `general-purpose` | None (API/deployment) |
| 1D: Repository Setup | `general-purpose` | None (git/CLI) |
| 1E: Brand & Design | `general-purpose` | `~/.claude/plugins/marketplaces/anthropic-agent-skills/frontend-design` |
| 1F: Market Research | `general-purpose` | `~/.claude/plugins/marketplaces/anthropic-agent-skills/copywriting` |
| 1G: Layout Guardian | `general-purpose` | `~/.claude/plugins/marketplaces/anthropic-agent-skills/frontend-design` |
| 2A: Page Builder | `general-purpose` | `~/.claude/plugins/marketplaces/anthropic-agent-skills/frontend-design` |
| Tests A-F | `general-purpose` | None (Playwright MCP) |

### Launching Parallel Agents

**Phase 1 Example - Launch ALL 7 agents in ONE message:**
```
Use the Task tool 7 times in a single message:

Task 1: {subagent_type: "general-purpose", prompt: "AGENT 1A: Image Processor..."}
Task 2: {subagent_type: "general-purpose", prompt: "AGENT 1B: Content Generator. Load skill: ~/.claude/plugins/marketplaces/anthropic-agent-skills/copywriting..."}
Task 3: {subagent_type: "general-purpose", prompt: "AGENT 1C: Pool Manager..."}
Task 4: {subagent_type: "general-purpose", prompt: "AGENT 1D: Repository Setup..."}
Task 5: {subagent_type: "general-purpose", prompt: "AGENT 1E: Brand & Design. Load skill: ~/.claude/plugins/marketplaces/anthropic-agent-skills/frontend-design..."}
Task 6: {subagent_type: "general-purpose", prompt: "AGENT 1F: Market Research. Load skill: ~/.claude/plugins/marketplaces/anthropic-agent-skills/copywriting..."}
Task 7: {subagent_type: "general-purpose", prompt: "AGENT 1G: Layout Guardian. Load skill: ~/.claude/plugins/marketplaces/anthropic-agent-skills/frontend-design..."}
```

### Skill Loading in Subagent Prompts

Each subagent prompt MUST include skill loading instruction when applicable:
```
"First, load the Claude skill at ~/.claude/plugins/marketplaces/anthropic-agent-skills/frontend-design using the Skill tool. Then proceed with: [task instructions]"
```

### Available Claude Skills

| Skill Path | Use For |
|------------|---------|
| `anthropic-agent-skills/frontend-design` | SVG design, color palettes, CSS, layout, responsive design |
| `anthropic-agent-skills/copywriting` | Headlines, CTAs, testimonials, sales copy, market research |
| `anthropic-agent-skills/code-review` | Code quality checks |
| `anthropic-agent-skills/testing` | Test generation |

---

## PHASE -2: SETUP (Execute First)

```bash
# Install Playwright MCP + browsers
npm install -g @anthropic-ai/mcp-playwright 2>/dev/null
npx playwright install --with-deps chromium

# Clone Claude skills
git clone https://github.com/anthropics/anthropic-cookbook /tmp/anthropic-cookbook 2>/dev/null
```

**All agents use ultrathink for: SVGs, color palettes, layout decisions, CSS.**

---

## PHASE -1: PREREQUISITES

```bash
npx playwright --version && gh --version && netlify --version && node --version && curl --version
```

---

## PHASE 0: CONFIG (Ask & Wait)

**Core Questions (1-6) - ALL REQUIRED:**

| # | Variable | Description | Example |
|---|----------|-------------|---------|
| 1 | `PRODUCT_NAME` | Product display name | "Secret Jeans" |
| 2 | `PRODUCT_TAGLINE` | Tagline or "auto-generate" for AI creation | "Comfort Meets Style" |
| 3 | `COMPETITION_URL` | **REQUIRED** - Competitor site for deep market research | "https://competitor.com/product" |
| 4 | `OUTPUT_FOLDER` | Full path for deployment files | "/Users/name/project" |
| 5 | `SITE_NAME` | Netlify subdomain | "secretjeans-shop" |
| 6 | `IMAGES_FOLDER` | Full path with `/product/` and `/testimonials/` subfolders | "/Users/name/images" |
| 6b | `PRODUCT_PAGE_URL` | **(Optional)** Product page to scrape images from. If provided, images will be downloaded to IMAGES_FOLDER/product/. Leave blank if providing your own images. | "https://edikted.co.uk/products/..." |

**Pool Configuration (7):**

| # | Variable | Options |
|---|----------|---------|
| 7 | `POOL_MODE` | `existing` (simpleswap-automation-1.onrender.com) OR `new` |

**If new pool (8-12):**

| # | Variable | Default/Format |
|---|----------|----------------|
| 8 | `MERCHANT_WALLET` | `0x1372Ad41B513b9d6eC008086C03d69C635bAE578` |
| 9-11 | Brightdata Creds | `hl_9d12e57c` / `scraping_browser1` / `u2ynaxqh9899` |
| 12 | `POOL_NAME` | Render service name |

**Save to:** `$OUTPUT_FOLDER/state/CONFIG.md`

**Variable Validation (After User Input):**
```bash
# Validate required variables
ERRORS=0

if [ -z "$PRODUCT_NAME" ]; then
  echo "ERROR: PRODUCT_NAME is required"
  ERRORS=$((ERRORS + 1))
fi

if [ -z "$OUTPUT_FOLDER" ]; then
  echo "ERROR: OUTPUT_FOLDER is required"
  ERRORS=$((ERRORS + 1))
elif [ ! -d "$OUTPUT_FOLDER" ]; then
  echo "Creating OUTPUT_FOLDER: $OUTPUT_FOLDER"
  mkdir -p "$OUTPUT_FOLDER/state" "$OUTPUT_FOLDER/images/product" "$OUTPUT_FOLDER/images/testimonials"
fi

if [ -z "$SITE_NAME" ]; then
  echo "ERROR: SITE_NAME is required"
  ERRORS=$((ERRORS + 1))
fi

if [ -z "$IMAGES_FOLDER" ]; then
  echo "ERROR: IMAGES_FOLDER is required"
  ERRORS=$((ERRORS + 1))
elif [ ! -d "$IMAGES_FOLDER" ]; then
  echo "ERROR: IMAGES_FOLDER does not exist: $IMAGES_FOLDER"
  ERRORS=$((ERRORS + 1))
fi

# Validate PRODUCT_PAGE_URL or existing images
if [ -z "$PRODUCT_PAGE_URL" ]; then
  EXISTING_PRODUCTS=$(ls -1 "$IMAGES_FOLDER/product/" 2>/dev/null | wc -l)
  if [ "$EXISTING_PRODUCTS" -eq 0 ]; then
    echo "ERROR: No PRODUCT_PAGE_URL provided and no images in $IMAGES_FOLDER/product/"
    echo "You must either provide a product URL to scrape OR add images manually"
    ERRORS=$((ERRORS + 1))
  fi
fi

if [ "$ERRORS" -gt 0 ]; then
  echo "FATAL: $ERRORS validation errors. Cannot proceed."
  exit 1
fi

echo "✓ All variables validated"
```

---

## PHASE 0.5: IMAGE PREPARATION (2 Parallel Subagents)

**Purpose:** Prepare all images before Phase 1 agents run.

**Launch 2 subagents in ONE message using Task tool (if PRODUCT_PAGE_URL provided, otherwise just Agent 0.5A):**

---

### AGENT 0.5A: Collage Splitter

```
Task tool config: {subagent_type: "general-purpose"}

Prompt:
Split all collage images in the testimonials subdirectory into individual photos.

STEP 1 - VISUAL INSPECTION:
- Use the Read tool to visually inspect 1-2 sample collage images
- Identify: grid layout, border colors, number of images per collage, watermark position
- Confirm bottom-right contains watermark/logo to skip

STEP 2 - SPLIT COLLAGES:
- Run: python ~/Downloads/collage_splitter.py ./testimonials
- If script doesn't exist, create it with these requirements:
  * Use OpenCV connected components to detect individual images
  * Detect border color (usually white) and find contours
  * Extract each sub-image as separate file
  * SKIP the bottom-right image (watermark/logo position)
  * Handle various grid layouts (2x2, 3x3, 2x3, etc.)
- Save extracted images to the SAME folder as the collages
- Use naming: original_name_01.png, original_name_02.png, etc.
- DELETE original collage files after successful extraction
- Process all .png, .jpg, .jpeg, .webp files in the folder

STEP 3 - VERIFY:
- Visually spot-check 2-3 extracted images to confirm quality
- Ensure no watermarks were included

Report back: count of collages processed, images extracted, any errors.
```

**Output:** `state/agent-0.5a.json`
```json
{
  "collages_processed": 5,
  "images_extracted": 18,
  "originals_deleted": 5,
  "errors": [],
  "status": "complete"
}
```

---

### AGENT 0.5B: Product Image Scraper (Only if PRODUCT_PAGE_URL provided)

```
Task tool config: {subagent_type: "general-purpose"}

Prompt:
Download high-quality product images from: $PRODUCT_PAGE_URL
Save to: $IMAGES_FOLDER/product/

STEP 0 - VALIDATION:
- Verify $PRODUCT_PAGE_URL is not empty
- Verify $IMAGES_FOLDER exists
- If either fails, report error and exit immediately

STEP 1 - FETCH PAGE WITH PLAYWRIGHT MCP (Full DOM Access):
- Use Playwright MCP to navigate to $PRODUCT_PAGE_URL
- Wait for page to fully load (networkidle)
- Wait additional 2 seconds for lazy-loaded images
- Take a screenshot for debugging: /tmp/product-page-debug.png

STEP 2 - EXTRACT ALL PRODUCT IMAGES:
Use Playwright to execute JavaScript in browser:
```javascript
// Get all product images from rendered DOM
const images = [];

// Method 1: Product gallery/carousel images
document.querySelectorAll('[data-gallery] img, .product-gallery img, .product-images img, .product__media img').forEach(img => {
  const src = img.dataset.src || img.dataset.zoomImage || img.dataset.large || img.srcset?.split(',').pop()?.trim().split(' ')[0] || img.src;
  if (src && !images.includes(src)) images.push(src);
});

// Method 2: Shopify product.media JSON
const scripts = document.querySelectorAll('script');
scripts.forEach(s => {
  const match = s.textContent?.match(/product\.media.*?(\[.*?\])/s);
  if (match) {
    try { JSON.parse(match[1]).forEach(m => m.src && images.push(m.src)); } catch {}
  }
});

// Method 3: srcset extraction (highest resolution)
document.querySelectorAll('img[srcset]').forEach(img => {
  const srcset = img.srcset.split(',').map(s => s.trim());
  const largest = srcset.reduce((max, curr) => {
    const width = parseInt(curr.match(/(\d+)w/)?.[1] || 0);
    return width > (max.width || 0) ? {url: curr.split(' ')[0], width} : max;
  }, {});
  if (largest.url && !images.includes(largest.url)) images.push(largest.url);
});

// Method 4: data-zoom, data-image attributes
document.querySelectorAll('[data-zoom], [data-image], [data-full-image]').forEach(el => {
  const src = el.dataset.zoom || el.dataset.image || el.dataset.fullImage;
  if (src && !images.includes(src)) images.push(src);
});

return images;
```

STEP 3 - MAXIMIZE RESOLUTION:
For each URL found, apply Shopify CDN optimization:
```bash
# Remove size suffixes and add max resolution
url=$(echo "$url" | sed -E 's/_(pico|icon|thumb|small|compact|medium|large|grande|original|master|[0-9]+x[0-9]*)//g')
# Add _2048x2048 before extension
url=$(echo "$url" | sed -E 's/(\.[a-zA-Z]+)(\?|$)/_2048x2048\1\2/')
```

STEP 4 - DOWNLOAD WITH VALIDATION AND RETRY:
```bash
mkdir -p "$IMAGES_FOLDER/product/"
counter=1
for url in "${image_urls[@]}"; do
  output_file="$IMAGES_FOLDER/product/product-$(printf '%02d' $counter).jpeg"

  # Retry up to 3 times
  for attempt in 1 2 3; do
    curl -L "$url" \
         -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
         -o "$output_file" \
         --connect-timeout 10 \
         --max-time 30 \
         -s -f

    # Validate download
    if [ -f "$output_file" ] && [ $(stat -f%z "$output_file" 2>/dev/null || stat -c%s "$output_file") -gt 10240 ]; then
      echo "✓ Downloaded product-$(printf '%02d' $counter).jpeg ($(stat -f%z "$output_file" || stat -c%s "$output_file") bytes)"
      break
    else
      echo "✗ Attempt $attempt failed for $url"
      rm -f "$output_file"
      sleep 2
    fi
  done

  ((counter++))
done
```

STEP 5 - DUPLICATE DETECTION:
Before visual verification, run deduplication on downloaded images:
```bash
# Install imagehash if not present
pip install imagehash Pillow 2>/dev/null

# Run dedup script or inline Python
python3 << 'EOF'
import os
from pathlib import Path

try:
    from PIL import Image
    import imagehash
    PHASH = True
except ImportError:
    PHASH = False
    print("imagehash not available, using file size comparison")

folder = Path(os.environ.get('IMAGES_FOLDER', '.')) / 'product'
images = list(folder.glob('*.jpeg')) + list(folder.glob('*.jpg')) + list(folder.glob('*.png'))

hashes = {}
duplicates = []

for img_path in images:
    if PHASH:
        try:
            h = imagehash.phash(Image.open(img_path))
            # Check against existing hashes (threshold: 8)
            is_dup = False
            for existing_path, existing_hash in hashes.items():
                if h - existing_hash <= 8:
                    duplicates.append((img_path, existing_path))
                    is_dup = True
                    break
            if not is_dup:
                hashes[str(img_path)] = h
        except Exception as e:
            print(f"Error hashing {img_path}: {e}")
    else:
        # Fallback: compare file sizes
        size = img_path.stat().st_size
        if size in hashes.values():
            duplicates.append((img_path, "size-match"))
        else:
            hashes[str(img_path)] = size

# Remove duplicates (keep first occurrence)
for dup_path, original in duplicates:
    print(f"Removing duplicate: {dup_path.name} (matches {Path(original).name if isinstance(original, str) else original})")
    dup_path.unlink()

print(f"Dedup complete: {len(duplicates)} duplicates removed, {len(hashes)} unique images")
EOF
```

STEP 6 - VISUAL VERIFICATION:
- Use Read tool to visually inspect EACH remaining image
- Verify: correct product, high resolution, not blurry
- Delete any wrong images (icons, logos)
- If 0 valid images remain, report FAILURE

STEP 7 - ERROR REPORTING:
If any step fails, write error to state file:
```json
{
  "status": "failed",
  "error": "description of what failed",
  "images_downloaded": 0
}
```

Report back:
- SUCCESS: Number of images, dimensions, file sizes
- FAILURE: What went wrong, suggestions for manual intervention
```

**Output:** `state/agent-0.5b.json`
```json
{
  "source_url": "https://edikted.co.uk/products/...",
  "images_found": 8,
  "images_downloaded": 6,
  "image_files": ["product-01.jpeg", "product-02.jpeg", ...],
  "resolution": "2048x2048",
  "errors": [],
  "status": "complete"
}
```

---

**Wait for both subagents** before proceeding to Phase 1 (Agent 1A depends on prepared images).

---

## PHASE 0.5 ERROR GATE (Mandatory Before Phase 1)

**Before launching Phase 1, verify all conditions are met:**

```bash
# 1. Check Agent 0.5A completed successfully
if [ -f "state/agent-0.5a.json" ]; then
  STATUS_A=$(jq -r '.status' state/agent-0.5a.json)
  ERRORS_A=$(jq '.errors | length' state/agent-0.5a.json)
  if [ "$STATUS_A" = "failed" ] || [ "$ERRORS_A" -gt 0 ]; then
    echo "ERROR: Agent 0.5A failed - check state/agent-0.5a.json"
    exit 1
  fi
fi

# 2. Check Agent 0.5B completed (if PRODUCT_PAGE_URL was provided)
if [ -n "$PRODUCT_PAGE_URL" ]; then
  if [ ! -f "state/agent-0.5b.json" ]; then
    echo "ERROR: Agent 0.5B did not produce output"
    exit 1
  fi
  STATUS_B=$(jq -r '.status' state/agent-0.5b.json)
  IMAGES_B=$(jq '.images_downloaded' state/agent-0.5b.json)
  if [ "$STATUS_B" = "failed" ] || [ "$IMAGES_B" -eq 0 ]; then
    echo "ERROR: Agent 0.5B failed to download images"
    exit 1
  fi
fi

# 3. Verify images actually exist in folders
PRODUCT_COUNT=$(ls -1 "$IMAGES_FOLDER/product/"*.{jpeg,jpg,png,webp} 2>/dev/null | wc -l)
TESTIMONIAL_COUNT=$(ls -1 "$IMAGES_FOLDER/testimonials/"*.{jpeg,jpg,png,webp} 2>/dev/null | wc -l)

if [ "$PRODUCT_COUNT" -eq 0 ]; then
  echo "ERROR: No product images found in $IMAGES_FOLDER/product/"
  echo "Either provide PRODUCT_PAGE_URL or add images manually"
  exit 1
fi

if [ "$TESTIMONIAL_COUNT" -eq 0 ]; then
  echo "WARNING: No testimonial images found in $IMAGES_FOLDER/testimonials/"
  echo "Continuing without testimonial images..."
fi

echo "✓ Phase 0.5 Gate Passed"
echo "  Product images: $PRODUCT_COUNT"
echo "  Testimonial images: $TESTIMONIAL_COUNT"
```

**If gate fails:** STOP execution and request human intervention. Do NOT proceed to Phase 1 with missing images.

---

## CRITICAL SPECS (Hardcoded)

**Button Behavior:**
- `handleAddToCart('primary')` → `processOrder(59)` DIRECT (no popup)
- `handleAddToCart('secondary')` → `showOrderBumpPopup()` → accept=$29, decline=$19

**Cache Headers:** HTML=`max-age=0`, Images=`max-age=31536000`, sw.js=`max-age=0`

**Images:**
- Products: `images/product/product-01.jpeg`, `product-02.jpeg`, etc.
- Testimonials: `images/testimonials/testimonial-01.jpeg`, `testimonial-02.jpeg`, etc.

**Pool Endpoints:** `GET /`, `GET /health`, `POST /buy-now {amountUSD}`, `POST /admin/init-pool`

**Testimonials:**
- Display with **UNCROPPED** circular avatar images from `/testimonials/` folder
- CSS handles circular crop with `border-radius: 50%` - image files stay uncropped
- Preserve full image, no auto-cropping during processing

**SVGs:**
- All custom-designed with **ultrathink** for each icon
- Must match product color palette (extracted from product images)
- Anti-AI: organic curves, asymmetry, hand-drawn feel, varied stroke weights

**Layout:**
- No section exceeds 4 rows without accordion/expand
- Zero horizontal overflow on all viewports (320px-1440px)
- Product description in accordion format (not expanded text blocks)

**Pool Persistence:**
- Render Disk mounted at `/data/` for deploy survival
- Pool file path: `/data/exchange-pool.json`

---

## PHASE 1: PARALLEL FOUNDATION (Launch 7 Agents in ONE Message)

**IMPORTANT: Use Task tool 7 times in a single message. Each agent runs as a subagent with appropriate Claude skills loaded.**

### AGENT 1A: Image Processor

**Subagent Config:** `{subagent_type: "general-purpose"}`

**Product Images (from IMAGES_FOLDER/product/):**
- List files in IMAGES_FOLDER/product/
- Convert to JPEG, rename: product-01.jpeg, product-02.jpeg, etc.
- Copy to OUTPUT_FOLDER/images/product/
- Compress to 800px width, maintain aspect ratio, optimize for web

**Testimonial Images (from IMAGES_FOLDER/testimonials/):**
- List files in IMAGES_FOLDER/testimonials/
- **CRITICAL: Keep images UNCROPPED** - preserve full original image
- Convert to JPEG, rename: testimonial-01.jpeg, testimonial-02.jpeg, etc.
- Copy to OUTPUT_FOLDER/images/testimonials/
- Compress to 400px width but **maintain original aspect ratio**
- Circular avatar display handled in CSS (`border-radius: 50%`), NOT image crop
- Do NOT auto-crop faces or create square crops

**Output:** `state/agent-1a.json`
```json
{
  "product_count": 6,
  "testimonial_count": 20,
  "testimonial_format": "uncropped_preserved",
  "status": "complete"
}
```

---

### AGENT 1B: Content Generator

**Subagent Config:** `{subagent_type: "general-purpose"}`
**Load Skill First:** `~/.claude/plugins/marketplaces/anthropic-agent-skills/copywriting`

- If PRODUCT_URL: fetch and extract details
- Generate 30 testimonials (40% TikTok, 25% IG, 15% FB, 10% Trustpilot, 10% Google)
- Include: 2-3 typos, mixed ratings (70/20/10), specific details
- Generate headlines, CTAs, product copy
- **Integrate market research recommendations** from agent-1f.json if available

**Output:** `state/agent-1b.json`
```json
{
  "testimonials": [...],
  "headlines": [...],
  "product_copy": {...},
  "status": "complete"
}
```

---

### AGENT 1C: Pool Manager

**Subagent Config:** `{subagent_type: "general-purpose"}`

**If existing pool:** Verify at `simpleswap-automation-1.onrender.com`
- Check pools >= 5 each tier ($19, $29, $59)
- If low, init more exchanges

**If new pool deployment, render.yaml MUST include:**
```yaml
services:
  - type: web
    name: $POOL_NAME
    env: node
    buildCommand: npm install
    startCommand: npm start
    disk:
      name: pool-data
      mountPath: /data
      sizeGB: 1
    envVars:
      - key: POOL_FILE_PATH
        value: "/data/exchange-pool.json"
      - key: MERCHANT_WALLET
        value: $MERCHANT_WALLET
      - key: BRD_CUSTOMER_ID
        value: $BRD_CUSTOMER_ID
      - key: BRD_ZONE
        value: $BRD_ZONE
      - key: BRD_PASSWORD
        value: $BRD_PASSWORD
```

**Pool Code Requirement:**
- Must use: `process.env.POOL_FILE_PATH || '/data/exchange-pool.json'`
- This ensures pool data **SURVIVES Render redeploys**

**Deployment Steps (if new):**
1. Clone template: `git clone https://github.com/blinds123/simpleswap-pool`
2. Create .env with Brightdata creds
3. Deploy to Render with disk persistence
4. Init 10x with 30s delays between each

**Output:** `state/agent-1c.json`
```json
{
  "pool_url": "https://...",
  "pool_19": 10,
  "pool_29": 10,
  "pool_59": 10,
  "total": 30,
  "persistence": "render_disk_enabled",
  "status": "complete"
}
```

---

### AGENT 1D: Repository Setup

**Subagent Config:** `{subagent_type: "general-purpose"}`

- `mkdir -p $OUTPUT_FOLDER/state && cd $OUTPUT_FOLDER && git init`
- `gh repo create $SITE_NAME --public --source=. --remote=origin`
- `netlify sites:create --name $SITE_NAME && netlify link`

**Output:** `state/agent-1d.json`
```json
{
  "github_url": "https://github.com/...",
  "netlify_url": "https://...",
  "status": "complete"
}
```

---

### AGENT 1E: Brand & Design Specialist (ULTRATHINK MANDATORY)

**Subagent Config:** `{subagent_type: "general-purpose"}`
**Load Skill First:** `~/.claude/plugins/marketplaces/anthropic-agent-skills/frontend-design`

**Color Palette Extraction (ULTRATHINK):**
1. Analyze product images using vision/image analysis
2. Extract **DOMINANT color** from product images
3. Build entire site color palette around this extracted color:
   - Primary: Dominant product color
   - Secondary: Complementary shade
   - Accent: Highlight variation
   - Background: Neutral that enhances product
   - Text: WCAG AA compliant contrast
4. Generate CSS variables derived from product's main color:
```css
:root {
  --color-primary: /* extracted dominant */;
  --color-secondary: /* derived */;
  --color-accent: /* derived */;
  --color-bg: /* derived */;
  --color-text: /* derived */;
}
```

**SVG Design Protocol (ULTRATHINK MANDATORY for EACH SVG):**

Act as WORLD-CLASS SVG DESIGNER for each icon. Each SVG must be ultrathink designed with:

| Requirement | Specification |
|-------------|---------------|
| Curves | Organic curves only - no perfect circles/squares |
| Details | Micro-details and texture throughout |
| Strokes | Varied stroke weights (1.5-2.5px range) |
| Colors | Use CSS variables from extracted palette |
| Anti-AI | Asymmetry, hand-drawn feel, unique flourishes |

**Required SVGs (ultrathink each):**
1. **Shipping** - "Design a shipping/delivery SVG that looks hand-crafted, premium, matches color palette [colors], suitable for luxury e-commerce, must not look AI-generated"
2. **Star-rating** - Custom star for reviews, organic shape
3. **Checkmark** - Success indicator, premium feel
4. **Heart** - Wishlist/favorite, organic curves
5. **Size-chart** - Measurement icon with ruler elements
6. **Returns** - Return policy icon, circular arrow
7. **Secure-payment** - Lock/shield for trust
8. **Social-proof** - People/community indicator
9. **Accordion-arrow** - Expand/collapse chevron

**Target Audience Analysis:**
- Demographics, color preferences
- TikTok/IG trends for product category

**Mobile Conversion Optimization:**
- Thumb zone CTAs, hero fills viewport
- Price visible without scroll
- Sticky bottom bar, 44px touch targets

**Output:** `state/agent-1e.json`
```json
{
  "color_palette": {
    "extracted_from": "product-01.jpeg",
    "dominant_color": "#...",
    "css_variables": {...}
  },
  "svg_icons": {
    "shipping": "<svg>...</svg>",
    "star_rating": "<svg>...</svg>",
    ...
  },
  "design_tokens": {...},
  "accordion_sections": [...],
  "status": "complete"
}
```

---

### AGENT 1F: Market Research Specialist (NEW)

**Subagent Config:** `{subagent_type: "general-purpose"}`
**Load Skill First:** `~/.claude/plugins/marketplaces/anthropic-agent-skills/copywriting`

**WebFetch COMPETITION_URL and extract:**

| Category | Data Points |
|----------|-------------|
| Pricing Strategy | Price points, discounts, urgency tactics |
| Value Props | Main selling points, unique features highlighted |
| Objection Handling | How they address concerns (returns, quality, shipping) |
| Trust Signals | Reviews, badges, guarantees, social proof placement |
| Social Proof Format | Testimonial style, review layout, UGC presentation |
| CTA Language | Button text, urgency words, action phrases |
| Urgency Tactics | Timers, stock indicators, limited offers |

**Analyze Target Demographic Psychographics:**
- Pain points addressed
- Aspirational messaging
- Emotional triggers used
- Social proof style (influencer vs. customer)

**Generate Sales Copy Recommendations:**
1. **Headlines:** 5 headline variations based on competitor analysis
2. **CTAs:** Primary and secondary button text options
3. **Objection-busters:** Copy for addressing top 3 concerns
4. **Urgency hooks:** Scarcity and time-based messaging
5. **Trust builders:** Badge/guarantee copy

**Output:** `state/agent-1f.json`
```json
{
  "competitor_analysis": {
    "url": "...",
    "pricing": {...},
    "value_props": [...],
    "trust_signals": [...],
    "cta_language": [...]
  },
  "target_demographic": {
    "psychographics": {...},
    "pain_points": [...],
    "emotional_triggers": [...]
  },
  "sales_recommendations": {
    "headlines": [...],
    "ctas": {...},
    "objection_busters": [...],
    "urgency_hooks": [...],
    "trust_builders": [...]
  },
  "conversion_tactics": [...],
  "status": "complete"
}
```

---

### AGENT 1G: Layout & Overflow Guardian (NEW)

**Subagent Config:** `{subagent_type: "general-purpose"}`
**Load Skill First:** `~/.claude/plugins/marketplaces/anthropic-agent-skills/frontend-design`

**Viewport Overflow Enforcement (320px-1440px):**
- Verify `overflow-x: hidden` on body and html
- Check `max-width` constraints on all containers
- Test at breakpoints: 320px, 375px, 414px, 768px, 1024px, 1440px
- **ZERO horizontal scroll allowed on any viewport**

**Accordion Format Enforcement:**
- Product description MUST be in accordion format
- NO expanded text blocks for product details
- Sales copy sections MAX 3-4 rows visible initially
- Rest of content in accordion/expandable sections

**Section Height Limits:**
- No section exceeds 4 visible rows without expand option
- Testimonials in compact grid/carousel, not long vertical list
- Features in card grid, not vertical stack

**Container Requirements:**
```css
body, html {
  overflow-x: hidden;
  max-width: 100vw;
}
.container {
  max-width: min(100%, 1200px);
  padding: 0 16px;
}
img, video {
  max-width: 100%;
  height: auto;
}
```

**Output:** `state/agent-1g.json`
```json
{
  "overflow_checks": {
    "320px": "pass",
    "375px": "pass",
    "414px": "pass",
    "768px": "pass",
    "1024px": "pass",
    "1440px": "pass"
  },
  "accordion_enforced": true,
  "section_heights": {
    "hero": "100vh max",
    "features": "4 rows",
    "testimonials": "carousel",
    "product_details": "accordion"
  },
  "css_overflow_rules": "applied",
  "status": "complete"
}
```

---

### PHASE 1 GATE
Wait for all 7 agents. Verify all `status: complete`. Write `state/PHASE1.md`.

---

## PHASE 2: BUILD (Sequential)

### AGENT 2A: Page Builder

**Subagent Config:** `{subagent_type: "general-purpose"}`
**Load Skill First:** `~/.claude/plugins/marketplaces/anthropic-agent-skills/frontend-design`

1. Clone template: `git clone https://github.com/blinds123/blue-sneaker-lander temp-template`
2. Copy index.html to OUTPUT_FOLDER

**Apply Design System (from agent-1e.json):**
- CSS variables from extracted color palette
- Custom SVG icons (all 9 ultrathink-designed)
- Design tokens for typography and spacing

**Transform Content:**
- Replace product name/tagline
- Inject testimonials from agent-1b.json
- Apply sales copy from agent-1f.json market research
- Update image paths

**Button Behavior (CRITICAL):**
- `#primaryCTA` → `handleAddToCart('primary')` → `processOrder(59)` DIRECT
- `#secondaryCTA` → `handleAddToCart('secondary')` → `showOrderBumpPopup()`

**Product Accordion (MANDATORY - 5 Sections):**
| Section | Icon | Default State |
|---------|------|---------------|
| Description | checkmark | Collapsed (3-4 lines preview) |
| Size Guide | size-chart | Collapsed |
| Shipping Info | shipping | Collapsed |
| Returns Policy | returns | Collapsed |
| Care Instructions | heart | Collapsed |

```html
<div class="accordion">
  <div class="accordion-item">
    <button class="accordion-header">
      <svg><!-- size-chart icon --></svg>
      <span>Size Guide</span>
      <svg class="accordion-arrow"><!-- arrow icon --></svg>
    </button>
    <div class="accordion-content">
      <!-- Content here, collapsed by default -->
    </div>
  </div>
</div>
```

**Layout Rules (from agent-1g.json):**
- NO large text blocks anywhere
- All detailed content in accordions
- Sales copy above fold = punchy, short, scannable
- Testimonials in grid/carousel format
- `overflow-x: hidden` enforced

**Testimonial Avatar CSS:**
```css
.testimonial-avatar {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover; /* CSS handles circular crop */
  /* Image file itself stays UNCROPPED */
}
```

**Mobile-First:**
- 390px viewport priority
- Sticky CTA bar at bottom
- Full-width buttons
- 44px minimum touch targets

**Create Configs:**
- `_headers` - Cache control
- `netlify.toml` - Build settings
- `netlify/functions/buy-now.js` - CORS proxy to pool
- `sw.js` - Service worker

Copy images from agent-1a, clean up temp-template

**Output:** `state/PHASE2.md`
```markdown
## Phase 2 Complete
- Design Applied: [colors, SVGs, tokens]
- Accordion Sections: 5 (all collapsed default)
- Mobile Optimized: [sticky CTA, touch targets, viewport]
- Overflow: Zero horizontal scroll
- Testimonial Avatars: CSS circular crop (uncropped images)
```

---

## PHASE 3: DEPLOY

1. `cd $OUTPUT_FOLDER && git add -A && git commit -m "Initial deployment"`
2. `git push -u origin main && netlify deploy --prod --dir=.`
3. Wait 90s for CDN propagation
4. Verify: `curl -I $NETLIFY_URL`

**Output:** `state/PHASE3.md` with live URLs

---

## PHASE 4: E2E TESTING (Launch 6 Agents in ONE Message, Vision Mode)

**IMPORTANT: Use Task tool 6 times in a single message. All tests run as parallel subagents.**

### TEST A: $59 Direct Flow

**Subagent Config:** `{subagent_type: "general-purpose"}`

- Navigate to site, select size, click #primaryCTA
- **ASSERT:** No popup appears
- **ASSERT:** Redirects to simpleswap.io
- **ASSERT:** Valid exchange_id from pool in URL
- **VERIFY:** Exchange page loads with correct amount

**Output:** `state/test-a.json`
```json
{
  "passed": true,
  "exchange_url": "https://simpleswap.io/exchange?id=...",
  "exchange_id_valid": true
}
```

---

### TEST B: $19 Popup Flow

**Subagent Config:** `{subagent_type: "general-purpose"}`

- Navigate, select size, click #secondaryCTA
- **ASSERT:** Popup appears
- Click decline button
- **ASSERT:** Redirects to simpleswap.io with $19 exchange
- **VERIFY:** Exchange page loads with correct amount

**Output:** `state/test-b.json`
```json
{
  "passed": true,
  "popup_appeared": true,
  "exchange_url": "https://simpleswap.io/exchange?id=...",
  "amount": 19
}
```

---

### TEST C: UI Quality (Vision Mode)

**Subagent Config:** `{subagent_type: "general-purpose"}`

- Check all images load (`naturalHeight > 0`)
- Test accordion open/close (all 5 sections)
- Mobile viewport (390x844): **no horizontal scroll**
- Desktop viewport (1440px): **no horizontal scroll**
- Screenshot analysis: premium design, not AI-looking
- Testimonial avatars: circular display, uncropped appearance
- Accessibility: alt text, button names, contrast, focus order

**Output:** `state/test-c.json`
```json
{
  "broken_images": 0,
  "accordion_works": true,
  "mobile_overflow": false,
  "desktop_overflow": false,
  "testimonial_avatars": "circular_uncropped",
  "a11y_issues": [],
  "passed": true
}
```

---

### TEST D: Pool Integration

**Subagent Config:** `{subagent_type: "general-purpose"}`

- `curl $POOL_URL/health`
- **ASSERT:** $19 pool >= 5 exchanges
- **ASSERT:** $29 pool >= 5 exchanges
- **ASSERT:** $59 pool >= 5 exchanges
- **ASSERT:** Total >= 20 exchanges

**Output:** `state/test-d.json`
```json
{
  "pool_19": 10,
  "pool_29": 10,
  "pool_59": 10,
  "total": 30,
  "passed": true
}
```

---

### TEST E: Performance & Design Audit (Vision Mode)

**Subagent Config:** `{subagent_type: "general-purpose"}`

- Core Web Vitals: LCP < 2.5s, FID < 100ms, CLS < 0.1
- Page weight < 3MB, hero image < 500KB
- Screenshot analysis: anti-AI score, premium feel, conversion optimization, brand consistency
- SVG quality check: organic curves, no perfect geometry
- Color consistency: matches extracted palette
- **ASSERT:** All scores >= 8/10

**Output:** `state/test-e.json`
```json
{
  "vitals": {"LCP": "...", "FID": "...", "CLS": "..."},
  "page_weight": "...",
  "design_scores": {
    "anti_ai": 9,
    "premium_feel": 8,
    "conversion": 9,
    "brand_consistency": 9
  },
  "passed": true
}
```

---

### TEST F: Full Purchase Flow (SimpleSwap Endpoint Verification) (NEW)

**Subagent Config:** `{subagent_type: "general-purpose"}`

**Complete end-to-end purchase verification:**

1. **Click CTA** → Trigger pool consumption
2. **Pool Request** → Verify `POST /buy-now` returns valid exchange
3. **Redirect** → Confirm redirect to `simpleswap.io/exchange?id=...`
4. **Exchange Page** → Verify SimpleSwap page loads with:
   - Correct currency pair (USD → Crypto)
   - Correct amount ($19, $29, or $59)
   - Valid exchange status

**Test all three price points:**
```bash
# Verify pool responds correctly
curl -X POST $POOL_URL/buy-now -d '{"amountUSD": 19}'
curl -X POST $POOL_URL/buy-now -d '{"amountUSD": 29}'
curl -X POST $POOL_URL/buy-now -d '{"amountUSD": 59}'
```

**Output:** `state/test-f.json`
```json
{
  "pool_consumption": {
    "19": {"success": true, "exchange_id": "..."},
    "29": {"success": true, "exchange_id": "..."},
    "59": {"success": true, "exchange_id": "..."}
  },
  "simpleswap_redirect": {
    "19": {"loaded": true, "amount_correct": true},
    "29": {"loaded": true, "amount_correct": true},
    "59": {"loaded": true, "amount_correct": true}
  },
  "passed": true
}
```

---

### PHASE 4 GATE
IF all 6 tests pass → Final Report. ELSE → Auto-Fix Loop.

---

## AUTO-FIX LOOP (Max 3)

For each iteration:
1. Identify failed tests from state/test-*.json
2. Diagnose:
   - Popup issue → fix handleAddToCart function
   - Images broken → fix paths in index.html
   - Pool low → init more exchanges
   - Overflow → add CSS containment
   - Accordion broken → fix JavaScript handlers
   - SimpleSwap redirect fail → check pool endpoint
3. Apply fix to index.html or configs
4. Redeploy: `git add -A && git commit -m "Fix: [issue]" && git push && netlify deploy --prod`
5. Wait 90s, re-run failed tests
6. If all pass: break

If still failing after 3: Write error report, request human intervention.

---

## PHASE 5: FINAL REPORT

Generate `DEPLOYMENT-REPORT.md`:

```markdown
# Deployment Report: [PRODUCT_NAME]

## URLs
- **Live Site:** https://[SITE_NAME].netlify.app
- **GitHub:** https://github.com/[user]/[SITE_NAME]
- **Pool:** https://[pool-url].onrender.com

## Product
- **Name:** [PRODUCT_NAME]
- **Tagline:** [PRODUCT_TAGLINE]
- **Color Palette:** Extracted from product images

## Pool Status
| Tier | Count | Status |
|------|-------|--------|
| $19  | XX    | ✅ |
| $29  | XX    | ✅ |
| $59  | XX    | ✅ |
| **Total** | XX | ✅ |

**Persistence:** Render Disk at /data/exchange-pool.json

## E2E Test Results
| Test | Status |
|------|--------|
| A: $59 Direct | ✅ |
| B: $19 Popup | ✅ |
| C: UI Quality | ✅ |
| D: Pool Integration | ✅ |
| E: Performance | ✅ |
| F: SimpleSwap Flow | ✅ |

## Features Implemented
- [x] Custom color palette from product images
- [x] 9 ultrathink-designed SVG icons
- [x] Product accordion (5 sections)
- [x] Mobile-first responsive design
- [x] CORS proxy for pool requests
- [x] Zero horizontal overflow
- [x] Uncropped testimonial avatars (CSS circular crop)
- [x] Market research integrated sales copy

## Maintenance Commands
```bash
# Refill pool
curl -X POST https://[pool-url].onrender.com/admin/init-pool

# Check pool health
curl https://[pool-url].onrender.com/health
```
```

---

## EXECUTION SUMMARY

| Phase | Agents | Duration |
|-------|--------|----------|
| -2 | Setup | 30s |
| -1 | Prerequisites | 10s |
| 0 | Config (6 questions) | User input |
| 0.5 | Image Prep (2 parallel: 0.5A Collage Splitter + 0.5B Product Scraper) | 30s-1 min |
| 1 | **7 agents parallel** (1A-1G) | 3-4 min |
| 2 | Build (sequential) | 2 min |
| 3 | Deploy | 2 min |
| 4 | **6 test agents parallel** (A-F) | 2 min |
| 5 | Auto-fix if needed | 0-5 min |
| 6 | Final report | 30s |

**Phase 1 Parallel Agents (Launch with Task tool x7 in ONE message):**
- 1A: Image Processor (uncropped testimonials)
- 1B: Content Generator + `copywriting` skill
- 1C: Pool Manager (Render Disk)
- 1D: Repository Setup
- 1E: Brand & Design Specialist + `frontend-design` skill (color extraction, ultrathink SVGs)
- 1F: Market Research Specialist + `copywriting` skill (NEW)
- 1G: Layout & Overflow Guardian + `frontend-design` skill (NEW)

**Phase 4 Parallel Tests (Launch with Task tool x6 in ONE message):**
- A: $59 Direct Flow
- B: $19 Popup Flow
- C: UI Quality
- D: Pool Integration
- E: Performance & Design Audit
- F: Full SimpleSwap Purchase Flow (NEW)

**Rules:**
- All parallel agents launched via Task tool in ONE message
- Load Claude skills at start of subagent prompts when specified
- Delegate heavy work to subagents
- Orchestrator coordinates only
- ULTRATHINK mandatory for all SVGs and color palette

**Target: 10-12 minutes execution, ~22,000 tokens.**
