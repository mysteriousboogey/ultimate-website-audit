# Collection, analysis and scoring — version 1.0

## Bounded crawl

Default: up to 50 HTML pages per site, one request at a time per host and at least one second between requests; honor longer applicable crawl delays and back off on 429/503. Follow public internal links and sitemap URLs with bounded sitemap depth/size. Reject non-HTTP(S), credentials in URLs, localhost/private/link-local addresses and redirects into them. Do not follow forms, faceted-query permutations, calendars or downloads unboundedly. Stop on access denial rather than evade it. The cap includes failed HTML attempts; separately record robots/sitemap requests and total requests. Set explicit timeouts and a finite retry budget (one transient retry maximum).

Inspect root robots.txt; record status before parsing (missing, unavailable and disallow are distinct), sitemap declarations and relevant exact agent/path rules. Fetch sitemap or sitemap index only within the same permission/scope boundaries. Inspect the supplied URL even when it is a deep path, subject to robots. Deduplicate fragments and exact duplicate URLs without collapsing meaningful query parameters.

Select homepage, primary hubs, up to three pages per important template (service/product, article, category, location/language), About and relevant contact/policy pages; prioritize input URLs. Record selection reasons and omitted sections. On a site with more pages, this is a sample audit, never claim exhaustive coverage. Crawl all eligible pages only within the budget; request or plan a larger crawl if necessary. Compare sites using equivalent templates, page counts, devices and intent classes.

Capture status/redirect chain, headers including X-Robots-Tag, raw HTML tags (title, description, headings, canonical, robots, hreflang), internal anchors, main text, images/alt and JSON-LD. Inspect schema validity and correspondence with visible facts. Missing descriptions, alt defects, broken resources, unnecessary redirect chains and duplicate metadata are useful findings even when they have no separate scoring deduction. Do not turn character counts, keyword density, word counts or one-H1 rules into ranking requirements.

Render at least one page per primary template at desktop and a recorded mobile viewport (default 390x844); inspect navigation, content visibility and raw/rendered differences. A browser not available means these checks are unknown. Fetch success with a spoofed bot agent is not proof the real bot can access the CDN. Indexability is not indexed status: use authorized Search Console URL Inspection exports for selected canonical/index status, logs for verified bot behavior, and analytics/backlink exports for outcome analysis. Search `site:` is incomplete evidence and cannot prove deindexing or absence of backlinks.

Record PageSpeed/CrUX field values, collection window, device and URL/origin scope when available. Lab Lighthouse diagnostics can identify fixes but are not field CWV. No field data means unknown, not failure. Check HTTPS and variants without changing the website. Review pagination/facets, canonicals, hreflang, image/video discovery, product/local details, accessibility obstructions and spam risks when relevant. Never call E-E-A-T a numeric Google ranking factor or a vendor authority metric a Google score. Off-site authority, search visibility, manual actions and server-log checks without access remain unknown supplementary findings.

## Content sample

Before grading, freeze 5 representative user questions plus 5 natural follow-ups per site (or fewer with an explicit small-site reason), mapped to inspected pages. Use user goals or real query exports where available; otherwise infer from visible offerings. Freeze up to 10 material claims/passages spread across templates, selecting first relevant claims in document order to reduce cherry-picking. Retain exact wording/location. For each judgement failure identify the precise missing answer, qualifier, attribution or contradiction. Another auditor should be able to rerun the same test, even though selecting initial user tasks involves expert judgement.

SEO measures crawl/index eligibility, discovery, relevance and user experience. AEO measures answer availability, extraction, structure, precision and follow-up paths. GEO measures retrieval permission alignment, entity consistency, attributable evidence, reusable context and maintained facts. Their overlap is acknowledged; the same defect may affect several category diagnostics only when it fails different explicit tests. Deduplicate remediation, and do not stack multiple deductions for the same unit/criterion.

Supplement with live AI/SERP observations only when tools exist: freeze engine/model, exact prompts, locale, date and repetitions; record response, citation URL, factual accuracy and referral outcomes. These observations are volatile, are not universal visibility, and do not enter the readiness score. Training permissions and search/grounding permissions must be distinguished using each provider's current official documentation. For Google, check the current Search Console generative AI inclusion setting and Generative AI performance report when authorized access exists; public HTML alone cannot verify account-level inclusion. Prior older documentation describes different reporting, so refresh the current guide. Missing llms.txt, special AI schema, FAQ markup, IndexNow or permissive training access is never an automatic failure.

## Evidence and prioritization

Confirmed: direct page/header/tool observation establishes the defect for a stated intended use. Potential: plausible but unverified; no deduction. Unknown: no sufficient observation, record the next verification needed. NA: demonstrably irrelevant, with a reason; never use NA to hide a blocked or inconvenient test. Passing checks need evidence too.

Every finding: stable ID, criterion ID(s), URL/location, observation timestamp, tool and raw/rendered mode, minimal observation/snippet, status, category, severity, affected sample count, why it matters, concrete fix and recheck. A 403/timeout against the audit client alone cannot establish real crawler blocking. If owner intent is uncertain, a noindex/private section is potential, not confirmed accidental exclusion.

High: confirmed access/index loss on intended key pages, material misinformation or broken core user task. Medium: confirmed answer/discovery/relevance/usability impairment with a working route. Low: limited presentation or maintenance opportunity. Prioritize severity, then affected intended pages, then owner business priority; use effort as a tie-breaker. No speculative revenue or traffic uplift estimates.

## Scoring input

`score.py` reads UTF-8 JSON:

```json
{
  "rubric_version": "1.0",
  "sites": [{
    "url": "https://example.com",
    "checks": {
      "S1": [{"unit":"https://example.com/", "status":"pass", "evidence":"ledger.md#response-1"}],
      "S2": [{"unit":"https://example.com/", "status":"unknown", "evidence":"robots retrieval failed; retry needed"}]
    }
  }]
}
```

Include every criterion from rubric.json in production inputs. An omitted criterion becomes one unknown unit automatically, never a pass. Multiple units have equal weight inside a criterion. For site-level checks use one named unit. For claims/questions use their frozen IDs. Keep the planned unit population fixed; omitted failed pages must appear unknown. All units require nonempty evidence/reason. Distinguish complete NA criteria from partially unknown ones.

For criterion weight w and P/F/U applicable unit counts, earned = w * P/(P+F+U), verified = w * (P+F)/(P+F+U). NA units are removed. An all-NA criterion is removed from applicable weight. Category score = 100 * sum(earned)/sum(verified); coverage = 100 * sum(verified)/sum(applicable weights). This equals verified pass rates weighted by observed share, without penalizing unknowns as failures or giving them credit. No verified evidence -> score null. No applicable checks -> coverage null. Retain unrounded values internally, round final numbers to one decimal; classify on unrounded scores. This is a designed audit rubric, not an empirically calibrated ranking model.

Overall = .50 SEO + .25 AEO + .25 GEO using unrounded scores. If any category is undefined, overall is undefined; do not change category weights. Overall coverage uses the same fixed weights, with absent coverage treated as zero. Any incomplete coverage makes the result provisional; below 80% coverage explicitly say insufficient coverage for a confident assessment, even if the observed score is Good. Coverage is not a statistical confidence interval. A confirmed high-severity blocker remains prominently flagged even if the arithmetic score is Good; do not secretly cap or alter the score.

For comparisons use equal sampling protocols and report coverage. Where tested criteria differ materially, compute an additional common-criteria view (same criterion IDs and comparable unit types) using the same calculator, clearly labeled; never replace the individual full audit scores. If scopes or remaining unknowns can change the apparent winner, no definitive overall winner. Preserve input and rubric version to reproduce arithmetic. Human classification and changing websites limit repeatability; never promise identical future scores.
