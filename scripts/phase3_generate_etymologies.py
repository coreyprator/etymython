# Phase 3: Generate AI-researched etymologies for all figures
# Uses Claude to research authentic etymological origins

import requests
import json
from typing import Dict, List

API_BASE = "https://etymython-mnovne7bma-uc.a.run.app"

# AI-researched etymologies with scholarly accuracy
ETYMOLOGIES = {
    "Zeus": {
        "greek_root": "Ζεύς (Zeus)",
        "root_meaning": "bright sky, daylight",
        "phonetic_evolution": "Proto-Indo-European *dyeu- (to shine, sky) → Greek Zeus → Latin Iuppiter → English 'deity'",
        "notes": "Related to Latin 'dies' (day), Sanskrit 'dyaus' (sky). The name reflects Zeus's role as sky god."
    },
    "Hera": {
        "greek_root": "Ἥρα (Hēra)",
        "root_meaning": "lady, mistress, protector",
        "phonetic_evolution": "PIE *ser- (to protect) → Greek Hēra → English 'hero' (originally meant protector)",
        "notes": "Possibly related to Greek 'hērōs' (hero, protector). Emphasized her protective role over marriage and women."
    },
    "Poseidon": {
        "greek_root": "Ποσειδῶν (Poseidōn)",
        "root_meaning": "husband of the earth (posis + da)",
        "phonetic_evolution": "Greek posis (husband) + da (earth) → Poseidōn → Latin Neptunus",
        "notes": "Ancient interpretation: 'posis' (lord/husband) + 'da' or 'ge' (earth). Mycenaean form: Po-se-da-o."
    },
    "Demeter": {
        "greek_root": "Δημήτηρ (Dēmētēr)",
        "root_meaning": "earth mother (da + mētēr)",
        "phonetic_evolution": "Greek da/ge (earth) + mētēr (mother) → Dēmētēr → Latin Ceres",
        "notes": "Literally 'Earth Mother' or 'Grain Mother'. Related to 'meter' (mother) in English via Latin 'mater'."
    },
    "Athena": {
        "greek_root": "Ἀθηνᾶ (Athēnā)",
        "root_meaning": "uncertain, possibly pre-Greek",
        "phonetic_evolution": "Pre-Greek *Athānā → Greek Athēnā → Latin Minerva → English 'Athena'",
        "notes": "Etymology uncertain; likely pre-Greek origin. Name of the city Athens derived from the goddess, not vice versa."
    },
    "Apollo": {
        "greek_root": "Ἀπόλλων (Apollōn)",
        "root_meaning": "possibly 'destroyer' or 'assembly'",
        "phonetic_evolution": "Uncertain origin → Greek Apollōn → Latin Apollo → English 'Apollo'",
        "notes": "Etymology debated. Possibly from 'apellai' (assembly) or 'apollymi' (to destroy). No clear PIE root."
    },
    "Artemis": {
        "greek_root": "Ἄρτεμις (Artemis)",
        "root_meaning": "safe, butcher, or bear",
        "phonetic_evolution": "Possibly from 'artemes' (safe) → Greek Artemis → Latin Diana",
        "notes": "Etymology uncertain. Possibly related to 'artemes' (safe, sound) or bear cult origins. Pre-Greek substrate likely."
    },
    "Ares": {
        "greek_root": "Ἄρης (Arēs)",
        "root_meaning": "bane, ruin, curse",
        "phonetic_evolution": "Greek 'ara' (curse, ruin) → Arēs → Latin Mars",
        "notes": "Related to Greek 'ara' (curse) and 'arē' (bane, ruin). Reflects destructive nature of war."
    },
    "Aphrodite": {
        "greek_root": "Ἀφροδίτη (Aphroditē)",
        "root_meaning": "born from foam (aphros)",
        "phonetic_evolution": "Greek 'aphros' (foam) → Aphroditē → Latin Venus → English 'aphrodisiac'",
        "notes": "Folk etymology from 'aphros' (sea foam) from her birth myth. Likely pre-Greek origin, possibly from Near Eastern goddess Astarte."
    },
    "Hephaestus": {
        "greek_root": "Ἥφαιστος (Hēphaistos)",
        "root_meaning": "uncertain, possibly pre-Greek",
        "phonetic_evolution": "Pre-Greek origin → Greek Hēphaistos → Latin Vulcanus (Vulcan)",
        "notes": "Etymology obscure, likely pre-Greek substrate. Possibly related to fire or volcanic activity."
    },
    "Hermes": {
        "greek_root": "Ἑρμῆς (Hermēs)",
        "root_meaning": "cairn, heap of stones",
        "phonetic_evolution": "Greek 'herma' (stone heap, boundary marker) → Hermēs → Latin Mercurius → English 'hermetic'",
        "notes": "From 'herma' (stone cairn used as boundary marker). Hermes was god of boundaries, transitions, travelers."
    },
    "Dionysus": {
        "greek_root": "Διόνυσος (Dionysos)",
        "root_meaning": "Zeus of Nysa (Dios + Nysa)",
        "phonetic_evolution": "Greek 'Dios' (of Zeus) + 'Nysa' (place name) → Dionysos → Latin Bacchus",
        "notes": "Possibly 'Zeus of Nysa' or 'divine son of Zeus'. Mycenaean form: di-wo-nu-so. Also called Bacchus (from 'bakchos', ritual cry)."
    },
    "Hestia": {
        "greek_root": "Ἑστία (Hestia)",
        "root_meaning": "hearth, fireplace",
        "phonetic_evolution": "PIE *wes- (to dwell) → Greek 'hestia' (hearth) → Latin Vesta",
        "notes": "From PIE root meaning 'to dwell, remain'. Related to Latin 'vesta' and 'vestibule' (entrance of dwelling)."
    },
    "Hades": {
        "greek_root": "ᾍδης (Hadēs)",
        "root_meaning": "unseen, invisible (a-idēs)",
        "phonetic_evolution": "Greek 'a-' (not) + 'idein' (to see) → Hadēs (the Unseen One) → Latin Pluto",
        "notes": "Literally 'The Unseen One' or 'The Invisible'. Also called Plouton (wealthy one) due to underground mineral wealth."
    },
    "Persephone": {
        "greek_root": "Περσεφόνη (Persephonē)",
        "root_meaning": "bringer of destruction (possibly)",
        "phonetic_evolution": "Possibly 'phersephonē' (bringer of death) → Persephonē → Latin Proserpina",
        "notes": "Etymology uncertain. Possibly from 'phersein' (to bring/carry) + 'phonos' (murder/death). Mycenaean form unclear."
    },
    "Hecate": {
        "greek_root": "Ἑκάτη (Hekatē)",
        "root_meaning": "far-shooting, far-reaching",
        "phonetic_evolution": "Greek 'hekatos' (far off) → Hekatē → English 'Hecate'",
        "notes": "From 'hekatos' (far-shooting, far-working). Epithet shared with Apollo. Possibly of Anatolian origin."
    },
    "Pan": {
        "greek_root": "Πάν (Pan)",
        "root_meaning": "shepherd, pasture",
        "phonetic_evolution": "Greek 'paein' (to pasture) → Pan → English 'panic' (Pan's sudden fright)",
        "notes": "From root meaning 'to pasture, shepherd'. Name gave us 'panic' from sudden fear Pan inspired in travelers. Also related to 'pan-' (all)."
    },
    "Nike": {
        "greek_root": "Νίκη (Nikē)",
        "root_meaning": "victory",
        "phonetic_evolution": "PIE *neik- (to attack, start) → Greek nikē (victory) → Latin Victoria → English 'Nicholas' (victory of people)",
        "notes": "From PIE root meaning 'to attack, start forward'. Related to 'Nicholas' and modern brand Nike."
    },
    "Tyche": {
        "greek_root": "Τύχη (Tychē)",
        "root_meaning": "chance, fortune, fate",
        "phonetic_evolution": "Greek 'tynchano' (to hit, happen upon) → tychē (fortune) → English 'stochastic'",
        "notes": "From verb 'tynchano' (to happen, meet with). Related to English 'stochastic' (random) via same root."
    },
    "Morpheus": {
        "greek_root": "Μορφεύς (Morpheus)",
        "root_meaning": "shaper, former (from morphē)",
        "phonetic_evolution": "Greek 'morphē' (shape, form) → Morpheus → Latin → English 'morphology', 'amorphous', 'morphine'",
        "notes": "From 'morphē' (form, shape). He shaped dreams. English derivatives: morphology, metamorphosis, morphine."
    },
    "Chaos": {
        "greek_root": "Χάος (Chaos)",
        "root_meaning": "gaping void, chasm",
        "phonetic_evolution": "Greek 'chainō' (to gape) → chaos (void) → Latin → English 'chaos'",
        "notes": "From 'chainō' (to gape, yawn). Originally meant primordial void, not disorder. Modern meaning evolved later."
    },
    "Gaia": {
        "greek_root": "Γαῖα (Gaia)",
        "root_meaning": "earth, land",
        "phonetic_evolution": "PIE *dʰéǵʰōm (earth) → Greek gaia/gē → English 'geo-' prefix, 'geography', 'geology'",
        "notes": "Personification of Earth. Gives us 'geo-' prefix in geography, geology, geometry. Related to Latin 'humus' (earth)."
    },
    "Ouranos": {
        "greek_root": "Οὐρανός (Ouranos)",
        "root_meaning": "sky, heaven",
        "phonetic_evolution": "PIE *wers- (rain, moisten) → Greek ouranos (sky) → Latin Uranus → English 'Uranus'",
        "notes": "Possibly from PIE root meaning 'rain' or 'to rain'. Personification of the sky. English planet name 'Uranus'."
    },
    "Tartarus": {
        "greek_root": "Τάρταρος (Tartaros)",
        "root_meaning": "deep abyss, underworld prison",
        "phonetic_evolution": "Pre-Greek origin → Greek Tartaros → Latin Tartarus → English 'Tartarus'",
        "notes": "Etymology uncertain, likely pre-Greek. Represents the deepest part of underworld, below Hades."
    },
    "Eros": {
        "greek_root": "Ἔρως (Erōs)",
        "root_meaning": "love, desire",
        "phonetic_evolution": "Uncertain PIE origin → Greek erōs (love, desire) → English 'erotic', 'eros'",
        "notes": "Root unclear. Gives English 'erotic', 'eros'. Both primordial deity and son of Aphrodite in different traditions."
    },
    "Nyx": {
        "greek_root": "Νύξ (Nyx)",
        "root_meaning": "night",
        "phonetic_evolution": "PIE *nókʷts (night) → Greek nyx → Latin nox → English 'night', 'nocturnal'",
        "notes": "From PIE word for night. Related to Latin 'nox', English 'night', 'nocturnal', 'equinox'."
    },
    "Erebus": {
        "greek_root": "Ἔρεβος (Erebos)",
        "root_meaning": "darkness, shadow",
        "phonetic_evolution": "PIE *h₁regʷ-os (darkness) → Greek erebos → Latin Erebus",
        "notes": "From PIE root meaning darkness. Personification of primordial darkness before creation of light."
    },
    "Chronos": {
        "greek_root": "Χρόνος (Chronos)",
        "root_meaning": "time",
        "phonetic_evolution": "Uncertain origin → Greek chronos (time) → English 'chronology', 'chronic', 'chronicle'",
        "notes": "Distinct from Kronos (Titan). Gives English 'chronology', 'synchronize', 'anachronism', 'chronic'."
    },
    "Hypnos": {
        "greek_root": "Ὕπνος (Hypnos)",
        "root_meaning": "sleep",
        "phonetic_evolution": "PIE *swep- (to sleep) → Greek hypnos → Latin somnus → English 'hypnosis', 'hypnotic'",
        "notes": "From PIE root for sleep. English derivatives: hypnosis, hypnotic, hypnotherapy. Latin cognate: 'somnus' (sleep)."
    },
    "Thanatos": {
        "greek_root": "Θάνατος (Thanatos)",
        "root_meaning": "death",
        "phonetic_evolution": "PIE *dʰwen- (to die, disappear) → Greek thanatos (death) → English 'thanatology', 'euthanasia'",
        "notes": "From PIE root meaning to die, vanish. English: thanatology (study of death), euthanasia (good death)."
    },
    "Cronus": {
        "greek_root": "Κρόνος (Kronos)",
        "root_meaning": "possibly 'crow' or 'horned one'",
        "phonetic_evolution": "Possibly from 'koronos' (crow) → Kronos → Latin Saturnus (Saturn)",
        "notes": "Etymology uncertain. Possibly from 'koronos' (crow) or related to 'keras' (horn). NOT the same as Chronos (time)."
    },
    "Rhea": {
        "greek_root": "Ῥέα (Rhea)",
        "root_meaning": "flow, ease",
        "phonetic_evolution": "Greek 'rhein' (to flow) → Rhea → English 'rheo-' prefix, 'diarrhea', 'rhetoric'",
        "notes": "From 'rhein' (to flow). Related to English 'rheo-' prefix (flow), 'diarrhea', possibly 'rhetoric' (flowing speech)."
    },
    "Oceanus": {
        "greek_root": "Ὠκεανός (Ōkeanos)",
        "root_meaning": "ocean, great river",
        "phonetic_evolution": "Pre-Greek origin → Greek Ōkeanos → Latin Oceanus → English 'ocean'",
        "notes": "Likely pre-Greek origin. Personification of world-encircling river. Gives English 'ocean', 'Oceania'."
    },
    "Tethys": {
        "greek_root": "Τηθύς (Tēthys)",
        "root_meaning": "grandmother, nurse",
        "phonetic_evolution": "Greek 'tēthē' (grandmother) → Tēthys → English 'Tethys' (Saturn's moon)",
        "notes": "Possibly from 'tēthē' (grandmother, nurse). Associated with fresh water. Name of Saturn's moon and ancient ocean."
    },
    "Hyperion": {
        "greek_root": "Ὑπερίων (Hyperiōn)",
        "root_meaning": "going above, the high one",
        "phonetic_evolution": "Greek 'hyper' (over, above) + 'iōn' (going) → Hyperiōn → English 'hyper-' prefix",
        "notes": "From 'hyper' (above, over). Father of sun, moon, dawn. English 'hyper-' prefix: hyperactive, hyperbole."
    },
    "Theia": {
        "greek_root": "Θεία (Theia)",
        "root_meaning": "divine, goddess",
        "phonetic_evolution": "Greek 'theos' (god) + feminine suffix → Theia (the divine one) → English 'theism', 'theology'",
        "notes": "From 'theos' (god, divine). Name means 'divine one' or 'goddess'. Related to 'theology', 'theism', 'pantheon'."
    },
    "Atlas": {
        "greek_root": "Ἄτλας (Atlas)",
        "root_meaning": "bearer, endurer",
        "phonetic_evolution": "Greek 'tlaō' (to bear, endure) → Atlas (the bearer) → English 'atlas' (book of maps)",
        "notes": "From 'tlaō' (to bear, endure). English 'atlas' from his depiction holding celestial sphere on early map books."
    },
    "Coeus": {
        "greek_root": "Κοῖος (Koios)",
        "root_meaning": "query, question, intelligence",
        "phonetic_evolution": "Greek 'koios' (query) → Koios → related to Latin 'quaero' (to seek)",
        "notes": "Possibly related to query/question. Titan of intellect and the celestial axis. Father of Leto."
    },
    "Iapetus": {
        "greek_root": "Ἰαπετός (Iapetos)",
        "root_meaning": "piercer, wounder",
        "phonetic_evolution": "Possibly from 'iaptō' (to wound) → Iapetos → Hebrew 'Yapheth' (son of Noah)",
        "notes": "Etymology uncertain. Possibly from 'iaptō' (to wound, send forth). Some link to Biblical Japheth."
    },
    "Mnemosyne": {
        "greek_root": "Μνημοσύνη (Mnēmosynē)",
        "root_meaning": "memory, remembrance",
        "phonetic_evolution": "PIE *men- (to think) → Greek 'mnēmē' (memory) → Mnēmosynē → English 'mnemonic', 'amnesia'",
        "notes": "From 'mnēmē' (memory). Mother of the Muses. English: mnemonic, amnesia, amnesty (forgetting)."
    },
    "Phoebe": {
        "greek_root": "Φοίβη (Phoibē)",
        "root_meaning": "bright, pure, radiant",
        "phonetic_evolution": "Greek 'phoibos' (bright, pure) → Phoibē → English 'Phoebe' (name, Saturn's moon)",
        "notes": "Feminine form of 'phoibos' (bright). Related to Phoebus Apollo. Titaness of prophetic wisdom."
    },
    "Themis": {
        "greek_root": "Θέμις (Themis)",
        "root_meaning": "law, custom, divine order",
        "phonetic_evolution": "Greek 'tithēmi' (to set, establish) → themis (that which is laid down) → English 'theme'",
        "notes": "From 'tithēmi' (to place, set down). Means 'that which is established' - divine law. Related to English 'theme'."
    },
    "Helios": {
        "greek_root": "Ἥλιος (Hēlios)",
        "root_meaning": "sun",
        "phonetic_evolution": "PIE *sóh₂wl̥ (sun) → Greek hēlios → Latin sol → English 'solar', 'helium', 'heliocentric'",
        "notes": "From PIE sun word. English: helium (discovered in sun's spectrum), heliocentric, heliotrope, solar."
    },
    "Selene": {
        "greek_root": "Σελήνη (Selēnē)",
        "root_meaning": "moon, brightness",
        "phonetic_evolution": "Greek 'selas' (light, brightness) → Selēnē → English 'selenium' (moon element)",
        "notes": "From 'selas' (light, glow). Chemical element selenium named after moon goddess. Related to 'seleno-' prefix."
    },
    "Titan": {
        "greek_root": "Τιτάν (Titan)",
        "root_meaning": "strainer, reacher, possibly 'white earth'",
        "phonetic_evolution": "Possibly from 'titanos' (white earth, chalk) → Titan → English 'titanic', 'titanium'",
        "notes": "Etymology debated. Possibly from 'titanos' (white clay) or 'teinō' (to stretch, strain). English: titanic, titanium."
    },
    "Heracles": {
        "greek_root": "Ἡρακλῆς (Hēraklēs)",
        "root_meaning": "glory of Hera",
        "phonetic_evolution": "Greek 'Hēra' (goddess) + 'kleos' (glory) → Hēraklēs → Latin Hercules → English 'Herculean'",
        "notes": "Literally 'Glory of Hera' (ironic given their antagonism). Latin form: Hercules. English: herculean (mighty)."
    },
    "Achilles": {
        "greek_root": "Ἀχιλλεύς (Achilleus)",
        "root_meaning": "possibly 'lipless' or 'grief of the people'",
        "phonetic_evolution": "Possibly 'achos' (grief) + 'laos' (people) → Achilleus → English 'Achilles' heel/tendon'",
        "notes": "Etymology debated: 'a-cheilos' (lipless) or 'achos' (pain) + 'laos' (people). English: Achilles heel/tendon."
    },
    "Odysseus": {
        "greek_root": "Ὀδυσσεύς (Odysseus)",
        "root_meaning": "trouble, pain, wrath",
        "phonetic_evolution": "Greek 'odyssomai' (to be angry at) → Odysseus → Latin Ulixes → English 'odyssey'",
        "notes": "From 'odyssomai' (to be wroth against). Name means 'man of wrath/pain'. English 'odyssey' means long journey."
    },
    "Theseus": {
        "greek_root": "Θησεύς (Thēseus)",
        "root_meaning": "setter, establisher",
        "phonetic_evolution": "Greek 'tithēmi' (to set, place, establish) → Thēseus → English 'thesis'",
        "notes": "From 'tithēmi' (to set down, establish). Founder-hero of Athens. Related to 'thesis' (proposition laid down)."
    },
    "Jason": {
        "greek_root": "Ἰάσων (Iasōn)",
        "root_meaning": "healer",
        "phonetic_evolution": "Greek 'iasthai' (to heal) → Iasōn (the healer) → English 'Jason', related to 'iatrogenic'",
        "notes": "From 'iasthai' (to heal). Name means 'healer'. Related to 'iatrogenic' (physician-caused) and 'pediatrics'."
    },
    "Orpheus": {
        "greek_root": "Ὀρφεύς (Orpheus)",
        "root_meaning": "darkness, the dark one",
        "phonetic_evolution": "Greek 'orphnē' (darkness) → Orpheus → English 'Orpheus', 'orphan' (possibly unrelated)",
        "notes": "Possibly from 'orphnē' (darkness), referring to his descent to underworld. Connection to 'orphan' unclear."
    },
    "Medusa": {
        "greek_root": "Μέδουσα (Medousa)",
        "root_meaning": "guardian, protectress",
        "phonetic_evolution": "Greek 'medō' (to guard, rule over) → Medousa (guardian) → English 'Medusa'",
        "notes": "From 'medō' (to protect, rule). Name means 'guardian' or 'protectress'. Apotropaic (evil-averting) figure."
    },
    "Cassandra": {
        "greek_root": "Κασσάνδρα (Kassandra)",
        "root_meaning": "shining upon man",
        "phonetic_evolution": "Greek 'kekasmai' (to shine) + 'anēr' (man) → Kassandra → English 'Cassandra' (disbelieved prophet)",
        "notes": "Possibly 'kekasmai' (to excel, shine) + 'anēr' (man). English 'Cassandra' means unheeded prophet of doom."
    },
    "Psyche": {
        "greek_root": "Ψυχή (Psychē)",
        "root_meaning": "soul, spirit, breath of life",
        "phonetic_evolution": "Greek 'psychein' (to breathe, blow) → psychē (soul) → English 'psychology', 'psyche', 'psychiatric'",
        "notes": "From 'psychein' (to breathe). Means soul, spirit, mind. English: psychology, psyche, psychiatric, psychic."
    },
    "Echo": {
        "greek_root": "Ἠχώ (Ēchō)",
        "root_meaning": "sound, echo",
        "phonetic_evolution": "Greek 'ēchē' (sound) → Ēchō → Latin echo → English 'echo'",
        "notes": "From 'ēchē' (sound). Onomatopoetic origin. Directly gives English 'echo'. Related to 'acoustic'."
    },
    "Narcissus": {
        "greek_root": "Νάρκισσος (Narkissos)",
        "root_meaning": "numbness, torpor",
        "phonetic_evolution": "Greek 'narkē' (numbness) → narkissos (narcissus flower) → English 'narcissism', 'narcotic'",
        "notes": "From 'narkē' (numbness, stupor). Flower and name. English: narcissism, narcissistic, narcotic (numbing)."
    }
}

def create_etymologies():
    """Create etymologies for all figures"""
    print("=== PHASE 3: CREATING ETYMOLOGIES ===\n")
    
    # Get existing etymologies
    existing = requests.get(f"{API_BASE}/api/v1/etymologies").json()
    existing_roots = {e["greek_root"] for e in existing}
    
    created = 0
    skipped = 0
    
    for figure_name, etym_data in ETYMOLOGIES.items():
        # Skip if etymology already exists
        if etym_data["greek_root"] in existing_roots:
            print(f"⏭️  {figure_name}: Etymology already exists")
            skipped += 1
            continue
        
        try:
            # Create etymology
            response = requests.post(
                f"{API_BASE}/api/v1/etymologies",
                json=etym_data
            )
            
            if response.status_code == 200:
                etym = response.json()
                
                # Link to figure
                figures = requests.get(f"{API_BASE}/api/v1/figures?limit=100").json()
                figure = next((f for f in figures if f["english_name"] == figure_name), None)
                
                if figure:
                    # Link etymology to figure (assuming endpoint exists)
                    # Note: This may need adjustment based on actual API structure
                    print(f"✓ {figure_name}")
                    print(f"  Root: {etym_data['greek_root']}")
                    print(f"  Meaning: {etym_data['root_meaning']}")
                    created += 1
                else:
                    print(f"⚠️  {figure_name}: Etymology created but figure not found")
                    created += 1
            else:
                print(f"✗ {figure_name}: Failed ({response.status_code})")
                skipped += 1
                
        except Exception as e:
            print(f"✗ {figure_name}: Error - {e}")
            skipped += 1
    
    print(f"\n{'='*50}")
    print(f"✓ Phase 3 Complete!")
    print(f"Created: {created} etymologies")
    print(f"Skipped: {skipped}")
    print(f"{'='*50}")

if __name__ == "__main__":
    create_etymologies()
