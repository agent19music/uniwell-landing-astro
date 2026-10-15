# AppDrop → Astro / EmDash

Source project: https://framer.com/projects/AppDrop-Mobile-App-Template-copy--XKgUzZBkEagoC9Qek9EI-79Bf8?node=augiA20Il

Published reference: https://physical-routine-484648.framer.app/

## Source capture

Read-only Framer Agent session captured the Home page, layout template, 16 reusable component definitions, styles, variables, and desktop/tablet/phone variants. Original raster artwork and available vector layers are in `public/appdrop/`. Solar Duotone icons and the Phosphor rating star reproduce the source icon families. No Framer project changes were made.

## Mapping

| Framer section | CMS block | Astro renderer |
| --- | --- | --- |
| Hero | `marketing_hero` | `Hero.astro` + `Device.astro` + `StoreButtons.astro` |
| The Challenge | `marketing_statement` | `Statement.astro` |
| Key benefits | `marketing_benefits` | `Benefits.astro` |
| Features | `marketing_features` | `Features.astro` |
| Intelligence Powered | `marketing_intelligence` | `Intelligence.astro` |
| Connect | `marketing_integrations` | `Integrations.astro` |
| Reviews | `marketing_testimonials` | `Testimonials.astro` |
| Pricing | `marketing_pricing` | `Pricing.astro` |
| FAQs | `marketing_faq` | `FAQ.astro` |
| Download | `marketing_download` | `Download.astro` |
| Layout navigation / footer | EmDash menus + site settings | `Header.astro` / `Footer.astro` |

`src/styles/theme.css` holds source colors, typography, device positions/masks, card layouts, and the 810px / 1200px breakpoints. Inter is the main typeface; DM Sans is used for the rating. Native Astro/DOM components replace Framer runtime components: navigation, review controls, billing toggle, exclusive FAQ disclosure, entry motion and the integration orbit. Reduced motion and keyboard navigation are supported.

All ten Home sections are stored in the local CMS and in `seed/seed.json`; editors can add, edit, duplicate and reorder these blocks. `src/data/appdrop.json` records the imported Home content; the live page queries EmDash. Pricing and Contact remain CMS-rendered routes with the shared design system. The reference has no dedicated Pricing/Contact pages, so these routes reuse the source pricing/FAQ blocks and a minimal contact introduction.

`scripts/import-appdrop-reference.py` converts the captured Framer JSON plus its asset manifest into the repeatable seed. The read-only capture and asset mapping are retained in `reference/appdrop/`; run `python3 scripts/import-appdrop-reference.py` to regenerate the import.

## Scope and handoff

This is the AppDrop template, including its original copy, example metrics, testimonials, pricing and outbound destinations, as requested for the faithful port. These are reference content, not Uniwell product claims. App-store / purchase buttons retain the source template destinations. The template's own remix card and author credit are preserved. Framer's hosting-injected badge/editor chrome are not application layers and are not represented as Astro hosting claims.

No deployment, test execution or autonomous UI testing was performed. Visual acceptance and interaction testing remain with Sean. The project directory has no initialized Git repository, so no commit or PR was created.
