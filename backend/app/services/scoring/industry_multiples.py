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

def get_industry_profile(naics_code: str | None) -> tuple[float, bool, bool]:
    if not naics_code:
        return DEFAULT_PROFILE
    for prefix_len in [4, 3, 2]:
        prefix = naics_code[:prefix_len]
        if prefix in INDUSTRY_PROFILES:
            return INDUSTRY_PROFILES[prefix]
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