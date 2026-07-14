def get_advice(scan_results):
    skin = scan_results.get("skin", {})
    acne = scan_results.get("acne", {})
    hair = scan_results.get("hair_texture", {})
    dark = scan_results.get("dark_circles", {})

    tone = skin.get("tone", "")  # fitzpatrick_1 to fitzpatrick_6
    undertone = skin.get("undertone", "")  # warm / cool / neutral
    acne_severity = acne.get("overall_severity", "").lower()  # mild / moderate / severe
    hair_type = hair.get("type", "")  # straight / wavy / curly / coily
    dark_severity = dark.get("severity", "")  # none / mild / severe

    routine_am = []
    routine_pm = []
    lifestyle = []
    colors = []
    hair_advice = []
    eye_advice = []

    # ── Fitzpatrick type ──────────────────────────────────────────
    tone = skin.get("tone", "").lower()

    if "very light" in tone or ("light" in tone and "medium" not in tone):
            routine_am.append("SPF 50+ sunscreen — your skin burns easily, this is non-negotiable")
            lifestyle.append("Reapply sunscreen every 2 hours outdoors")
            lifestyle.append("Niacinamide serum helps with redness and barrier repair")
    elif "light-medium" in tone or "medium" == tone:
            routine_am.append("SPF 30–50 sunscreen daily")
            lifestyle.append("Introduce retinoids and acids gradually")
            lifestyle.append("Vitamin C serum in AM helps prevent early pigmentation")
    elif "medium-dark" in tone or "dark" in tone:
            routine_am.append("Daily SPF is critical — unprotected sun exposure darkens acne marks significantly")
            lifestyle.append("Introduce all actives slowly — irritation triggers hyperpigmentation in deeper skin tones")
            lifestyle.append("Azelaic acid is your best friend for fading dark marks safely")
            lifestyle.append("Avoid inflammation at all costs — it directly causes pigmentation")
    # ── Acne severity ─────────────────────────────────────────────
    if acne_severity == "mild":
        routine_am.append("Salicylic acid cleanser (0.5–2%) to keep pores clear")
        routine_am.append("Niacinamide serum (2–5%) to regulate oil and reduce minor inflammation")
        routine_pm.append("Salicylic acid toner or BHA leave-on to dissolve sebum overnight")
        routine_pm.append("Azelaic acid gel (5–10%) to prevent clogging and even out skin tone")
        routine_pm.append("Optional: low-dose adapalene gel 2–3x per week to prevent microcomedones")
        lifestyle.append("Change pillowcase every 3 days")
        lifestyle.append("Avoid touching your face — transfers bacteria to pores")

    elif acne_severity == "moderate":
        routine_am.append("Salicylic acid cleanser to keep pores clear")
        routine_am.append("Niacinamide serum for barrier repair and oil control")
        routine_am.append("Benzoyl peroxide (2.5–5%) spot treatment on active pimples")
        routine_pm.append("Adapalene gel (retinoid) — start 2x per week, build up slowly")
        routine_pm.append("Azelaic acid (10–20%) for post-acne marks and inflammation")
        routine_pm.append("Ceramide moisturizer to buffer retinoid irritation")
        lifestyle.append("Do not pop or squeeze pimples — causes scarring and deeper infection")
        lifestyle.append("Reduce dairy and high-glycemic foods if possible — linked to acne flares")
        lifestyle.append("Change pillowcase every 2–3 days")

    elif acne_severity == "severe":
        routine_am.append("Gentle non-foaming cleanser — avoid stripping already inflamed skin")
        routine_am.append("Ceramide moisturizer to protect skin barrier")
        routine_am.append("SPF — sun exposure darkens acne scars significantly")
        routine_pm.append("Low-frequency benzoyl peroxide wash to control surface bacteria")
        routine_pm.append("Ceramide or barrier repair moisturizer")
        lifestyle.append("See a dermatologist — severe acne requires prescription treatment (isotretinoin or oral antibiotics)")
        lifestyle.append("Do not self-treat with multiple actives — this will worsen inflammation")
        lifestyle.append("Avoid makeup that clogs pores on active lesions")

    # ── Dark circles ──────────────────────────────────────────────
    if dark_severity == "mild":
        routine_am.append("Caffeine eye serum in the morning — constricts blood vessels, reduces puffiness")
        routine_pm.append("Niacinamide eye cream at night for under-eye pigmentation")
        routine_pm.append("Low-strength retinol eye cream 2–3x per week — thickens under-eye skin over time")

    elif dark_severity == "severe":
        routine_am.append("Caffeine + Vitamin C eye serum — brightens pigmentation and reduces vascular darkening")
        routine_pm.append("Retinol eye cream at night — improves skin thickness gradually")
        lifestyle.append("Always apply sunscreen near the orbital (eye) area — prevents worsening pigmentation")
        lifestyle.append("Note: topical products have limited effect on structural hollowing or deep genetic circles — dermal fillers or laser therapy may be needed for full correction")

    # ── Hair texture ──────────────────────────────────────────────
    if hair_type == "straight":
        hair_advice.append("Use lightweight shampoo and cleanse frequently — sebum travels fast on straight hair")
        hair_advice.append("Apply conditioner mid-length to ends only — avoid roots or hair looks greasy")
        hair_advice.append("Use dry shampoo between washes for volume")
        hair_advice.append("Avoid heavy oils on scalp")

    elif hair_type == "wavy":
        hair_advice.append("Use balanced hydration shampoo — wavy hair is prone to both dryness and frizz")
        hair_advice.append("Apply light leave-in conditioner for wave definition")
        hair_advice.append("Sea salt spray enhances natural wave texture")
        hair_advice.append("Never brush dry — scrunch instead to avoid frizz")

    elif hair_type == "curly":
        hair_advice.append("Use sulfate-free gentle cleanser — sulfates strip moisture from curls")
        hair_advice.append("Deep condition once a week — curly hair loses moisture fast")
        hair_advice.append("Apply leave-in conditioner + curl cream while hair is soaking wet")
        hair_advice.append("Try the squish-to-condish technique for better curl formation")
        hair_advice.append("Avoid heat styling and harsh brushing")

    elif hair_type == "coily":
        hair_advice.append("Use the LOC method — Layer Liquid (water), Oil (light), Cream (butter/thick) for moisture retention")
        hair_advice.append("Co-wash or use very gentle shampoo — coily hair needs maximum moisture")
        hair_advice.append("Protective styles (braids, twists) reduce breakage significantly")
        hair_advice.append("Use low-manipulation styles — coily hair is fragile and prone to breakage")
        hair_advice.append("Avoid frequent heat and aggressive detangling")

    # ── Undertone color recommendations ───────────────────────────
    if undertone == "warm":
        colors.append("Your warm undertone suits earth tones best — mustard yellow, brick red, coral, olive green, orange, cream")
        colors.append("Avoid icy blue, cool gray, and bluish pastels — they wash out warm skin")

    elif undertone == "cool":
        colors.append("Your cool undertone suits jewel tones — emerald green, sapphire blue, ruby red, lavender, berry, wine")
        colors.append("Pure white and charcoal gray look great on you")
        colors.append("Avoid heavy orange and yellow-based earth tones")

    elif undertone == "neutral":
        colors.append("Lucky you — neutral undertones can wear both warm and cool colors")
        colors.append("Best bets: blush pink, teal, sage green, true red, navy, taupe")

    return {
        "routine_am": routine_am,
        "routine_pm": routine_pm,
        "lifestyle": lifestyle,
        "colors": colors,
        "hair": hair_advice,
        "eye_care": eye_advice
    }