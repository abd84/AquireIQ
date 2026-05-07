# NAICS prefix → (ebitda_multiple, is_fragmented, is_asset_light)
INDUSTRY_PROFILES: dict[str, tuple[float, bool, bool]] = {
    "2382": (5.5, True, True),   # Plumbing, heating, AC
    "2381": (5.0, True, True),   # Foundation, structure, building exterior
    "5617": (6.0, True, True),   # Services to buildings (pest, lawn)
    "6211": (7.0, True, True),   # Physician offices
    "6212": (8.0, True, True),   # Dental offices
    "6213": (7.5, True, True),   # Optometrists
    "5412": (5.5, True, True),   # Accounting services
    "5411": (5.0, True, True),   # Legal services
    "5241": (9.0, True, True),   # Insurance agencies
    "5621": (4.0, True, False),  # Clothing stores
    "4411": (3.5, True, False),  # Auto dealers
    "8111": (4.0, True, False),  # Auto repair
    "4812": (5.0, True, False),  # Air transport
    "5611": (4.5, True, True),   # Management consulting
    "3340": (4.0, False, False), # Computer/electronic manufacturing
    "3360": (3.5, False, False), # Transportation equipment
    "5629": (7.0, True, True),   # Waste management
}

DEFAULT_PROFILE = (4.2, False, False)

# Keyword → (ebitda_multiple, is_fragmented, is_asset_light)
# Matched against Google Places primaryTypeDisplayName (case-insensitive)
KEYWORD_PROFILES: list[tuple[list[str], tuple[float, bool, bool]]] = [
    (["plumb", "hvac", "heating", "cooling", "air condition"],  (5.5, True, True)),
    (["dental", "dentist", "orthodont"],                        (8.0, True, True)),
    (["physician", "doctor", "medical clinic", "urgent care"],  (7.0, True, True)),
    (["optom", "eye care", "vision"],                           (7.5, True, True)),
    (["accounti", "bookkeep", "cpa", "tax"],                    (5.5, True, True)),
    (["law firm", "legal", "attorney"],                         (5.0, True, True)),
    (["insurance"],                                             (9.0, True, True)),
    (["pest control", "lawn", "landscap", "tree service"],      (6.0, True, True)),
    (["waste", "junk removal", "hauling"],                      (7.0, True, True)),
    (["consult"],                                               (4.5, True, True)),
    (["auto repair", "mechanic", "body shop"],                  (4.0, True, False)),
    (["roofing", "gutter", "siding", "window install"],         (5.0, True, True)),
    (["electrician", "electrical"],                             (5.5, True, True)),
    (["physical therap", "chiropract"],                         (6.5, True, True)),
    (["veterinar", "animal hospital", "pet clinic"],            (6.0, True, True)),
    (["restaurant", "diner", "cafe", "food"],                   (3.5, True, False)),
    (["retail", "clothing", "boutique"],                        (4.0, True, False)),
    (["manufact", "fabricat"],                                  (3.8, False, False)),
]


def get_industry_profile(naics_code: str | None, industry_description: str | None = None) -> tuple[float, bool, bool]:
    """Return (ebitda_multiple, is_fragmented, is_asset_light).

    Falls back to keyword matching on industry_description when naics_code is absent,
    which is the common case when sourcing from Google Places.
    """
    if naics_code:
        for prefix_len in [4, 3, 2]:
            prefix = naics_code[:prefix_len]
            if prefix in INDUSTRY_PROFILES:
                return INDUSTRY_PROFILES[prefix]

    if industry_description:
        lower = industry_description.lower()
        for keywords, profile in KEYWORD_PROFILES:
            if any(kw in lower for kw in keywords):
                return profile

    return DEFAULT_PROFILE


def multiple_to_score(multiple: float) -> int:
    if multiple >= 8.0:
        return 8
    elif multiple >= 6.0:
        return 6
    elif multiple >= 4.5:
        return 4
    else:
        return 2
