#!/usr/bin/env python3
"""
NL Forward - Politician Registry (January 2026)
All politicians. All parties. All accountable.

CURRENT STATUS:
- PC Majority Government (21 seats) - since October 29, 2025
- Liberal Opposition (15 seats)
- NDP (2 seats)
- Independent (2 seats)

"Red jacket, blue jacket, orange jacket - they've all had their turn."
"""

# =============================================================================
# CURRENT GOVERNMENT - PC (Since October 29, 2025)
# Premier: Tony Wakeham
# =============================================================================

PC_CABINET = [
    {"name": "Tony Wakeham", "role": "Premier", "party": "PC", "twitter": "TonyWakehamNL", "district": "Stephenville-Port au Port", "priority": "high"},
    {"name": "Barry Petten", "role": "Deputy Premier, Transportation & Infrastructure", "party": "PC", "twitter": "BarryPettenNL", "district": "Conception Bay South", "priority": "high"},
    {"name": "Craig Pardy", "role": "Finance Minister", "party": "PC", "twitter": "CraigPardyNL", "district": "Bonavista", "priority": "high"},
    {"name": "Lela Evans", "role": "Health Minister, Labrador Affairs", "party": "PC", "twitter": "LelaEvansNL", "district": "Torngat Mountains", "priority": "high"},
    {"name": "Helen Conway Ottenheimer", "role": "Justice Minister, Attorney General", "party": "PC", "twitter": "HelenConwayO", "district": "Harbour Main", "priority": "high"},
    {"name": "Paul Dinn", "role": "Education Minister", "party": "PC", "twitter": "PaulDinnNL", "district": "Topsail-Paradise", "priority": "medium"},
    {"name": "Lloyd Parrott", "role": "Energy & Mines Minister", "party": "PC", "twitter": "LloydParrottNL", "district": "Terra Nova", "priority": "high"},
    {"name": "Chris Tibbs", "role": "Municipal Affairs, Environment", "party": "PC", "twitter": "ChrisTibbsNL", "district": "Grand Falls-Windsor-Buchans", "priority": "medium"},
    {"name": "Loyola O'Driscoll", "role": "Fisheries & Aquaculture", "party": "PC", "twitter": "LoyolaODriscoll", "district": "Ferryland", "priority": "medium"},
    {"name": "Pleaman Forsey", "role": "Forestry, Agriculture & Lands", "party": "PC", "twitter": "PleamanForsey", "district": "Exploits", "priority": "medium"},
    {"name": "Lin Paddock", "role": "Jobs & Growth, Immigration", "party": "PC", "twitter": "LinPaddockNL", "district": "Baie Verte-Green Bay", "priority": "medium"},
    {"name": "Andrea Barbour", "role": "Tourism, Culture, Arts", "party": "PC", "twitter": "AndreaBarbourNL", "district": "St. Barbe-L'Anse aux Meadows", "priority": "medium"},
    {"name": "Mike Goosney", "role": "Government Services, Labour", "party": "PC", "twitter": "MikeGoosneyNL", "district": "Humber-Gros Morne", "priority": "medium"},
    {"name": "Joedy Wall", "role": "Social Supports, Housing", "party": "PC", "twitter": "JoedyWallNL", "district": "Cape St. Francis", "priority": "medium"},
]

PC_BACKBENCH = [
    {"name": "Jim McKenna", "role": "MHA", "party": "PC", "twitter": "JimMcKennaNL", "district": "Fogo Island-Cape Freels", "priority": "low"},
]

# =============================================================================
# OFFICIAL OPPOSITION - LIBERAL (15 seats)
# =============================================================================

LIBERAL_OPPOSITION = [
    {"name": "John Hogan", "role": "Leader of Opposition", "party": "Liberal", "twitter": "JohnHoganNL", "district": "Windsor Lake", "priority": "high"},
    {"name": "Bernard Davis", "role": "MHA", "party": "Liberal", "twitter": "BernardDavisNL", "district": "Virginia Waters-Pleasantville", "priority": "medium"},
    {"name": "Lisa Dempster", "role": "MHA", "party": "Liberal", "twitter": "LisaDempsterNL", "district": "Cartwright-L'Anse au Clair", "priority": "low"},
    {"name": "Keith White", "role": "MHA", "party": "Liberal", "twitter": "KeithWhiteNL", "district": "St. John's West", "priority": "low"},
    {"name": "Jamie Korab", "role": "MHA", "party": "Liberal", "twitter": "JamieKorabNL", "district": "Waterford Valley", "priority": "low"},
]

# =============================================================================
# NDP (2 seats)
# =============================================================================

NDP_CAUCUS = [
    {"name": "Jim Dinn", "role": "NDP Leader", "party": "NDP", "twitter": "JimDinnNL", "district": "St. John's Centre", "priority": "medium"},
    {"name": "Sheilagh O'Leary", "role": "MHA", "party": "NDP", "twitter": "SheilaghOLeary", "district": "St. John's East-Quidi Vidi", "priority": "low"},
]

# =============================================================================
# INDEPENDENTS (2 seats)
# =============================================================================

INDEPENDENTS = [
    {"name": "Alison Coffin", "role": "Independent", "party": "Independent", "twitter": "AlisonCoffinNL", "district": "TBD", "priority": "low"},
]

# =============================================================================
# FORMER LIBERAL CABINET (2015-2025) - Track their legacy
# =============================================================================

FORMER_LIBERALS = [
    {"name": "Andrew Furey", "role": "Former Premier (2020-2025)", "party": "Liberal", "twitter": "AndrewFureyNL", "status": "resigned"},
    {"name": "Siobhan Coady", "role": "Former Finance Minister", "party": "Liberal", "twitter": "SiobhanCoady", "status": "retired"},
    {"name": "John Haggie", "role": "Former Health Minister", "party": "Liberal", "twitter": "JohnHaggieNL", "status": "retired"},
]

# =============================================================================
# FEDERAL MPs
# =============================================================================

FEDERAL_MPS = [
    {"name": "Gudie Hutchings", "role": "MP", "party": "Liberal", "twitter": "GudieHutchings", "riding": "Long Range Mountains", "priority": "medium"},
    {"name": "Seamus O'Regan", "role": "MP", "party": "Liberal", "twitter": "SeijOReganNL", "riding": "St. John's South-Mount Pearl", "priority": "medium"},
    {"name": "Clifford Small", "role": "MP", "party": "Conservative", "twitter": "CliffordSmallNL", "riding": "Coast of Bays-Central-Notre Dame", "priority": "low"},
    {"name": "Ken McDonald", "role": "MP", "party": "Liberal", "twitter": "KenMcDonaldNL", "riding": "Avalon", "priority": "low"},
    {"name": "Joanne Thompson", "role": "MP", "party": "Liberal", "twitter": "JoanneThompson", "riding": "St. John's East", "priority": "low"},
    {"name": "Churence Rogers", "role": "MP", "party": "Liberal", "twitter": "ChurenceRogers", "riding": "Bonavista-Burin-Trinity", "priority": "low"},
    {"name": "Yvonne Jones", "role": "MP", "party": "Liberal", "twitter": "YvonneJonesNL", "riding": "Labrador", "priority": "low"},
]

# =============================================================================
# MUNICIPAL
# =============================================================================

MUNICIPAL_LEADERS = [
    {"name": "Danny Breen", "role": "Mayor of St. John's", "party": "None", "twitter": "DannyBreenNL", "priority": "medium"},
]

# =============================================================================
# OFFICIAL ACCOUNTS
# =============================================================================

OFFICIAL_ACCOUNTS = [
    {"name": "Government of NL", "type": "government", "twitter": "GovNL", "priority": "high"},
    {"name": "NL Health Services", "type": "government", "twitter": "NLHealthServices", "priority": "high"},
    {"name": "House of Assembly", "type": "government", "twitter": "NLHouseAssembly", "priority": "medium"},
]

PARTY_ACCOUNTS = [
    {"name": "NL PC Party", "type": "party", "party": "PC", "twitter": "PCNL", "priority": "high"},
    {"name": "NL Liberal Party", "type": "party", "party": "Liberal", "twitter": "LiberalNL", "priority": "medium"},
    {"name": "NL NDP", "type": "party", "party": "NDP", "twitter": "NL_NDP", "priority": "medium"},
]

# =============================================================================
# COMBINED LISTS
# =============================================================================

ALL_PROVINCIAL = PC_CABINET + PC_BACKBENCH + LIBERAL_OPPOSITION + NDP_CAUCUS + INDEPENDENTS
ALL_POLITICIANS = ALL_PROVINCIAL + FEDERAL_MPS + MUNICIPAL_LEADERS
ALL_ACCOUNTS = ALL_POLITICIANS + OFFICIAL_ACCOUNTS + PARTY_ACCOUNTS

HIGH_PRIORITY_ACCOUNTS = [p["twitter"] for p in ALL_ACCOUNTS if p.get("priority") == "high" and p.get("twitter")]
ALL_TWITTER_HANDLES = [p["twitter"] for p in ALL_ACCOUNTS if p.get("twitter")]

# =============================================================================
# PARTY CONTEXT FOR RESPONSES
# =============================================================================

RESPONSE_CONTEXT = {
    "PC": {
        "status": "CURRENT GOVERNMENT (since Oct 29, 2025)",
        "in_power_since": 2025,
        "previous_term": "2003-2015",
        "promises": ["Better healthcare", "Lower taxes", "Safer communities", "Churchill Falls referendum"],
        "key_question": "You're in government now. No more blaming Liberals. Show us results."
    },
    "Liberal": {
        "status": "OFFICIAL OPPOSITION",
        "in_power": "2015-2025 (10 years)",
        "reports": ["Greene Report", "Health Accord NL", "DAME Report"],
        "failures": ["$50M+ on reports", "~15% implemented", "Wait times worsened"],
        "key_question": "You had 10 years. You commissioned the reports. Why didn't you implement them?"
    },
    "NDP": {
        "status": "Third Party (2 seats)",
        "key_question": "Which specific policies do you commit to implementing?"
    }
}

# =============================================================================
# KEYWORDS
# =============================================================================

PLATFORM_KEYWORDS = {
    "healthcare": ["wait time", "MRI", "surgery", "hospital", "nurse", "Health Accord", "Lela Evans"],
    "fiscal": ["budget", "deficit", "debt", "Muskrat Falls", "Craig Pardy"],
    "energy": ["Churchill Falls", "Gull Island", "referendum", "Lloyd Parrott"],
    "youth": ["youth", "graduates", "brain drain", "leaving", "population"],
    "municipal": ["municipal", "amalgamation", "consolidation", "Chris Tibbs"],
    "housing": ["housing", "affordable", "rent", "Joedy Wall"],
}

ALL_KEYWORDS = [kw for keywords in PLATFORM_KEYWORDS.values() for kw in keywords]

HIGH_PRIORITY_TRIGGERS = [
    "announcing", "commitment", "promise", "new funding",
    "wait time", "MRI", "Churchill Falls", "referendum"
]

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_politician_by_twitter(handle):
    handle = handle.lower().replace("@", "")
    for p in ALL_ACCOUNTS:
        if p.get("twitter", "").lower() == handle:
            return p
    return None

def get_party_context(party):
    return RESPONSE_CONTEXT.get(party, {})

def is_high_priority(handle):
    return handle in HIGH_PRIORITY_ACCOUNTS

def get_relevant_keywords(text):
    text_lower = text.lower()
    found = []
    for category, keywords in PLATFORM_KEYWORDS.items():
        for kw in keywords:
            if kw.lower() in text_lower:
                found.append({"category": category, "keyword": kw})
    return found


# =============================================================================
# ACCOUNTABILITY MESSAGES
# =============================================================================

ACCOUNTABILITY_MESSAGES = {
    "PC": "You're in government now. No more opposition. DELIVER on your promises.",
    "Liberal": "You had 10 years and $50M in reports. You don't get to complain now.",
    "NDP": "Show us a real plan with specifics, not just criticism.",
    "ALL": "Red jacket, blue jacket, orange jacket - we're tracking ALL of you."
}


if __name__ == "__main__":
    print("NL Forward Politician Registry - January 2026")
    print("=" * 50)
    print("GOVERNMENT: PC Majority (21 seats)")
    print("Premier: Tony Wakeham")
    print("=" * 50)
    print(f"Monitoring: {len(ALL_TWITTER_HANDLES)} accounts")
    print(f"High priority: {len(HIGH_PRIORITY_ACCOUNTS)} accounts")
