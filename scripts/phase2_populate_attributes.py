# Phase 2: Auto-populate figure attributes from image prompts
# Extracts symbols, generates roles/descriptions from FIGURE_PROMPTS

import re
import json

# Load FIGURE_PROMPTS directly
FIGURE_PROMPTS = {
    "Zeus": {
        "figure_type": "Olympian",
        "prompt": "Zeus: Zeus, King of the Gods and God of Sky and Thunder, depicted as a regal figure in a Renaissance painting, holding a lightning bolt, with majestic robes flowing around him. Symbolism: lightning bolt, eagle, oak tree."
    },
    "Hera": {
        "figure_type": "Olympian",
        "prompt": "Hera: Hera, Queen of the Gods and Goddess of Marriage, depicted as a stately queen in a Renaissance portrait, with a golden crown, peacock feathers, and a scepter. Symbolism: peacock, crown, scepter."
    },
    "Poseidon": {
        "figure_type": "Olympian",
        "prompt": "Poseidon: Poseidon, God of the Sea, depicted as a powerful figure in a Renaissance seascape, holding a trident, with waves crashing in the background. Symbolism: trident, horses, dolphins."
    },
    "Demeter": {
        "figure_type": "Olympian",
        "prompt": "Demeter: Demeter, Goddess of Agriculture and Harvest, depicted as a nurturing woman in a Renaissance pastoral scene, surrounded by wheat sheaves and cornucopias. Symbolism: wheat, cornucopia, torch."
    },
    "Athena": {
        "figure_type": "Olympian",
        "prompt": "Athena: Athena, Goddess of Wisdom and Warfare, depicted as a wise and armored figure in a Renaissance painting, holding a spear and shield, with an owl perched nearby. Symbolism: owl, olive tree, spear."
    },
    "Apollo": {
        "figure_type": "Olympian",
        "prompt": "Apollo: Apollo, God of Music and Poetry, depicted as a radiant young man in a Renaissance portrait, holding a golden lyre, with a laurel wreath on his head. Symbolism: lyre, laurel wreath, sun chariot."
    },
    "Artemis": {
        "figure_type": "Olympian",
        "prompt": "Artemis: Artemis, Goddess of the Hunt, depicted as a swift huntress in a Renaissance forest scene, carrying a silver bow and accompanied by a deer. Symbolism: bow and arrows, crescent moon, deer."
    },
    "Ares": {
        "figure_type": "Olympian",
        "prompt": "Ares: Ares, God of War, depicted as a fierce warrior in a Renaissance battle scene, with armor, a sword, and a war chariot. Symbolism: spear, helmet, vulture."
    },
    "Aphrodite": {
        "figure_type": "Olympian",
        "prompt": "Aphrodite: Aphrodite, Goddess of Love and Beauty, depicted as a graceful figure in a Renaissance painting, emerging from sea foam, with roses and doves surrounding her. Symbolism: roses, doves, scallop shell."
    },
    "Hephaestus": {
        "figure_type": "Olympian",
        "prompt": "Hephaestus: Hephaestus, God of Fire and the Forge, depicted as a skilled blacksmith in a Renaissance workshop, with a hammer and anvil, surrounded by glowing metal. Symbolism: hammer, anvil, fire."
    },
    "Hermes": {
        "figure_type": "Olympian",
        "prompt": "Hermes: Hermes, Messenger of the Gods, depicted as a swift traveler in a Renaissance painting, wearing winged sandals and a winged cap, holding a caduceus. Symbolism: caduceus, winged sandals, traveler's cap."
    },
    "Dionysus": {
        "figure_type": "Olympian",
        "prompt": "Dionysus: Dionysus, God of Wine and Celebration, depicted as a joyful figure in a Renaissance feast scene, crowned with grapevines and holding a wine goblet. Symbolism: grapevines, thyrsus, wine goblet."
    },
    "Hestia": {
        "figure_type": "Olympian",
        "prompt": "Hestia: Hestia, Goddess of the Hearth and Home, depicted as a serene woman in a Renaissance domestic scene, tending a sacred flame, surrounded by warmth and comfort. Symbolism: sacred flame, hearth, modest veil."
    },
    "Hades": {
        "figure_type": "Olympian",
        "prompt": "Hades: Hades, God of the Underworld, depicted as a somber and powerful figure in a Renaissance painting, seated on a dark throne, with Cerberus at his side. Symbolism: helm of invisibility, Cerberus, bident."
    },
    "Persephone": {
        "figure_type": "Olympian",
        "prompt": "Persephone: Persephone, Queen of the Underworld, depicted as a dual figure in a Renaissance painting, holding pomegranate seeds, half surrounded by spring flowers and half by shadows. Symbolism: pomegranate, spring flowers, torch."
    },
    "Hecate": {
        "figure_type": "Olympian",
        "prompt": "Hecate: Hecate, Goddess of Magic and Crossroads, depicted as a mysterious figure in a Renaissance night scene, holding twin torches, with a loyal hound at her side. Symbolism: twin torches, keys, crossroads."
    },
    "Pan": {
        "figure_type": "Minor Deity",
        "prompt": "Pan: Pan, God of the Wild, depicted as a rustic figure in a Renaissance pastoral scene, playing panpipes, with goat-like features and surrounded by nature. Symbolism: panpipes, goat legs, pine wreath."
    },
    "Nike": {
        "figure_type": "Minor Deity",
        "prompt": "Nike: Nike, Goddess of Victory, depicted as a triumphant winged figure in a Renaissance painting, holding a laurel wreath and palm branch, soaring through the clouds. Symbolism: wings, laurel wreath, palm branch."
    },
    "Tyche": {
        "figure_type": "Minor Deity",
        "prompt": "Tyche: Tyche, Goddess of Fortune, depicted as a capricious figure in a Renaissance painting, holding a cornucopia and standing on a wheel, with symbols of both luck and fate. Symbolism: wheel of fortune, cornucopia, rudder."
    },
    "Morpheus": {
        "figure_type": "Minor Deity",
        "prompt": "Morpheus: Morpheus, God of Dreams, depicted as an ethereal figure in a Renaissance painting, emerging from mist and shadows, with dreamlike imagery swirling around him. Symbolism: poppy flowers, wings, dream imagery."
    },
    "Chaos": {
        "figure_type": "Primordial",
        "prompt": "Chaos: Chaos, the Primordial Void, depicted as an abstract swirling mass in a Renaissance painting, with cosmic elements emerging from darkness. Symbolism: void, swirling cosmic matter, primordial darkness."
    },
    "Gaia": {
        "figure_type": "Primordial",
        "prompt": "Gaia: Gaia, the Primordial Earth Mother, depicted as a nurturing figure in a Renaissance painting, cradling the earth, with mountains and forests flowing from her form. Symbolism: earth, mountains, fertile soil."
    },
    "Ouranos": {
        "figure_type": "Primordial",
        "prompt": "Ouranos: Ouranos, the Primordial Sky God, depicted as a vast celestial figure in a Renaissance painting, spanning the heavens, with stars and clouds swirling around him. Symbolism: starry sky, celestial dome, cosmic expanse."
    },
    "Tartarus": {
        "figure_type": "Primordial",
        "prompt": "Tartarus: Tartarus, the Primordial Abyss, depicted as a dark and foreboding chasm in a Renaissance painting, with chains and shadows representing eternal imprisonment. Symbolism: bottomless pit, chains, darkness."
    },
    "Eros": {
        "figure_type": "Primordial",
        "prompt": "Eros: Eros, the Primordial God of Love, depicted as a winged youth in a Renaissance painting, holding a bow and arrow, surrounded by hearts and flowers. Symbolism: bow and arrows, wings, roses."
    },
    "Nyx": {
        "figure_type": "Primordial",
        "prompt": "Nyx: Nyx, the Primordial Goddess of Night, depicted as a dark and mysterious figure in a Renaissance painting, draped in starry robes, with the moon and shadows surrounding her. Symbolism: starry cloak, moon, darkness."
    },
    "Erebus": {
        "figure_type": "Primordial",
        "prompt": "Erebus: Erebus, the Primordial God of Darkness, depicted as a shadowy figure in a Renaissance painting, emerging from deep shadows, with mist and gloom swirling around him. Symbolism: shadows, mist, deep darkness."
    },
    "Chronos": {
        "figure_type": "Primordial",
        "prompt": "Chronos: Chronos, the Primordial God of Time, depicted as an ancient bearded figure in a Renaissance painting, with an hourglass and serpent coiled around him, representing the eternal flow of time. Symbolism: hourglass, serpent, zodiac wheel."
    },
    "Hypnos": {
        "figure_type": "Primordial",
        "prompt": "Hypnos: Hypnos, the God of Sleep, depicted as a peaceful figure in a Renaissance painting, resting on soft clouds with poppy flowers and a sleep-inducing wand. Symbolism: poppy flowers, wings, peaceful slumber."
    },
    "Thanatos": {
        "figure_type": "Primordial",
        "prompt": "Thanatos: Thanatos, the Personification of Death, depicted as a somber winged figure in a Renaissance painting, draped in dark robes with an inverted torch. Symbolism: inverted torch, wings, sword."
    },
    "Kronos": {
        "figure_type": "Titan",
        "prompt": "Kronos: Kronos, the Titan King who ruled during the Golden Age, depicted as a powerful bearded ruler in a Renaissance painting, holding a scythe and hourglass. Symbolism: scythe, hourglass, serpent."
    },
    "Rhea": {
        "figure_type": "Titan",
        "prompt": "Rhea: Rhea, the Titan Goddess of Motherhood, depicted as a nurturing mother figure in a Renaissance painting, cradling an infant, surrounded by lions and natural imagery. Symbolism: lions, swaddled stone, mother's embrace."
    },
    "Oceanus": {
        "figure_type": "Titan",
        "prompt": "Oceanus: Oceanus, the Titan God of the Ocean River, depicted as a bearded god in a Renaissance seascape, with water flowing from his form, fish and sea creatures surrounding him. Symbolism: river streams, sea serpent, fish."
    },
    "Tethys": {
        "figure_type": "Titan",
        "prompt": "Tethys: Tethys, the Titan Goddess of Fresh Water, depicted as a graceful figure in a Renaissance painting, with flowing water and rivers emanating from her hands. Symbolism: flowing rivers, water vessels, aquatic life."
    },
    "Hyperion": {
        "figure_type": "Titan",
        "prompt": "Hyperion: Hyperion, the Titan God of Light, depicted as a radiant figure in a Renaissance painting, with rays of light emanating from his form, surrounded by celestial brightness. Symbolism: sunlight, radiant beams, celestial fire."
    },
    "Theia": {
        "figure_type": "Titan",
        "prompt": "Theia: Theia, the Titan Goddess of Sight and Radiance, depicted as a luminous woman in a Renaissance painting, with gems and precious stones gleaming around her. Symbolism: precious gems, radiant light, shimmering aura."
    },
    "Prometheus": {
        "figure_type": "Titan",
        "prompt": "Prometheus: Prometheus, the Titan who gave fire to humanity, depicted as a noble figure in a Renaissance painting, holding a blazing torch aloft, with a look of compassion and defiance. Symbolism: torch of fire, fennel stalk, eagle."
    },
    "Atlas": {
        "figure_type": "Titan",
        "prompt": "Atlas: Atlas, the Titan condemned to hold up the celestial heavens, depicted as a muscular figure in a Renaissance painting, straining beneath the weight of a massive celestial sphere. Symbolism: celestial sphere, burden of heavens, strength."
    },
    "Coeus": {
        "figure_type": "Titan",
        "prompt": "Coeus: Coeus, the Titan God of Intellect, depicted as a wise scholarly figure in a Renaissance painting, surrounded by scrolls and celestial maps, with stars reflecting in his eyes. Symbolism: scrolls, celestial axis, stars."
    },
    "Cronus": {
        "figure_type": "Titan",
        "prompt": "Cronus: Cronus, the Titan King of the Golden Age, depicted as a powerful bearded ruler in a Renaissance painting, holding a harvesting sickle and an hourglass representing time's passage. Symbolism: sickle, hourglass, golden harvest."
    },
    "Iapetus": {
        "figure_type": "Titan",
        "prompt": "Iapetus: Iapetus, the Titan God of Mortality and Craftsmanship, depicted as a skilled artisan in a Renaissance workshop painting, forging tools with mortal hands alongside celestial elements. Symbolism: spear, crafting tools, mortal essence."
    },
    "Mnemosyne": {
        "figure_type": "Titan",
        "prompt": "Mnemosyne: Mnemosyne, the Titan Goddess of Memory, depicted as a wise woman in a Renaissance painting, holding an open scroll with ancient writing, surrounded by ethereal memory wisps. Symbolism: scrolls, memory pool, written words."
    },
    "Phoebe": {
        "figure_type": "Titan",
        "prompt": "Phoebe: Phoebe, the Titan Goddess of Prophecy, depicted as a mystical figure in a Renaissance painting, gazing into a luminous orb with prophetic visions swirling around her. Symbolism: prophetic orb, silver moon, laurel crown."
    },
    "Themis": {
        "figure_type": "Titan",
        "prompt": "Themis: Themis, the Titan Goddess of Divine Law and Order, depicted as a dignified figure in a Renaissance painting, holding balanced scales and a sword, with a blindfold representing impartial justice. Symbolism: scales of justice, sword, blindfold."
    },
    "Helios": {
        "figure_type": "Titan",
        "prompt": "Helios: Helios, the Titan God of the Sun, depicted as a radiant figure in a Renaissance painting, driving a golden chariot pulled by fiery horses across the sky, with sunbeams radiating outward. Symbolism: sun chariot, radiant crown, golden horses."
    },
    "Selene": {
        "figure_type": "Titan",
        "prompt": "Selene: Selene, the Titan Goddess of the Moon, depicted as a serene figure in a Renaissance night painting, riding a silver chariot pulled by white horses, with moonlight illuminating the landscape. Symbolism: lunar crescent, silver chariot, white horses."
    },
    "Titan": {
        "figure_type": "Titan",
        "prompt": "Titan: An elder Titan, depicted as a primordial giant in a Renaissance painting, with powerful form and ancient wisdom, representing the first generation of divine beings. Symbolism: primordial strength, ancient wisdom, cosmic power."
    },
    "Heracles": {
        "figure_type": "Hero",
        "prompt": "Heracles: Heracles, the greatest of Greek heroes, depicted as a muscular warrior in a Renaissance painting, wearing a lion skin and holding a club, with symbols of his twelve labors around him. Symbolism: Nemean lion skin, club, bow."
    },
    "Achilles": {
        "figure_type": "Hero",
        "prompt": "Achilles: Achilles, the legendary warrior, depicted as a fierce combatant in Renaissance armor, with a spear and shield, radiating invincibility except for a subtle emphasis on his heel. Symbolism: spear, shield, armor."
    },
    "Odysseus": {
        "figure_type": "Hero",
        "prompt": "Odysseus: Odysseus, the cunning hero of the Odyssey, depicted as a weathered traveler in a Renaissance painting, with a thoughtful expression, nautical elements, and symbols of his long journey home. Symbolism: ship, bow, olive wood staff."
    },
    "Perseus": {
        "figure_type": "Hero",
        "prompt": "Perseus: Perseus, the hero who defeated Medusa, depicted as a brave warrior in a Renaissance painting, holding a polished shield and winged sandals, with divine gifts from the gods. Symbolism: polished shield, winged sandals, cap of invisibility."
    },
    "Theseus": {
        "figure_type": "Hero",
        "prompt": "Theseus: Theseus, the Athenian hero, depicted as a noble warrior in a Renaissance painting, holding a sword, with the labyrinth and symbols of his victory over the Minotaur. Symbolism: sword, ball of thread, ship's sail."
    },
    "Jason": {
        "figure_type": "Hero",
        "prompt": "Jason: Jason, the leader of the Argonauts, depicted as an adventurous hero in a Renaissance painting, holding the Golden Fleece, with a ship in the background. Symbolism: Golden Fleece, Argo ship, laurel wreath."
    },
    "Orpheus": {
        "figure_type": "Hero",
        "prompt": "Orpheus: Orpheus, the legendary musician, depicted as a young man in a Renaissance painting, playing a lyre with such beauty that animals and nature gather around him. Symbolism: lyre, laurel wreath, enchanted animals."
    },
    "Medusa": {
        "figure_type": "Mortal",
        "prompt": "Medusa: Medusa, the Gorgon, depicted in a Renaissance painting, with serpentine hair and a haunting beauty, her fearsome power captured in a moment of tragic transformation. Symbolism: serpent hair, petrifying gaze, wings."
    },
    "Cassandra": {
        "figure_type": "Mortal",
        "prompt": "Cassandra: Cassandra, the Trojan prophetess cursed to never be believed, depicted in a Renaissance painting, with a look of anguish and foresight, surrounded by symbols of unheeded warnings. Symbolism: prophetic visions, laurel branch, scroll of warnings."
    },
    "Psyche": {
        "figure_type": "Mortal",
        "prompt": "Psyche: Psyche, the mortal beloved of Eros who became goddess of the soul, depicted as a beautiful maiden in a Renaissance painting, with butterfly wings and a gentle glow, holding a lamp. Symbolism: butterfly wings, lamp, rose."
    },
    "Echo": {
        "figure_type": "Mortal",
        "prompt": "Echo: Echo, the mountain nymph cursed to only repeat others' words, depicted in a Renaissance forest painting as an ethereal figure fading into the landscape, with sound waves visualized around her. Symbolism: mountain peaks, fading voice, reflected sound."
    },
    "Narcissus": {
        "figure_type": "Mortal",
        "prompt": "Narcissus: Narcissus, the beautiful youth who fell in love with his own reflection, depicted in a Renaissance painting gazing into a pool of water, with narcissus flowers blooming around him. Symbolism: pool of water, narcissus flowers, mirror reflection."
    }
}

# API base URL (update to your deployed URL if needed)
API_BASE = "https://etymython-mnovne7bma-uc.a.run.app"

def extract_symbols(prompt_text):
    """Extract symbols from prompt text."""
    # Find the Symbolism: section
    match = re.search(r'Symbolism:\s*([^.]+\.)', prompt_text)
    if match:
        symbols_text = match.group(1)
        # Remove the trailing period and clean up
        symbols_text = symbols_text.rstrip('.')
        # Extract individual symbols (comma-separated phrases)
        symbols = [s.strip() for s in symbols_text.split(',')]
        # Join back but remove articles and clean up
        clean_symbols = []
        for s in symbols:
            s = re.sub(r'\b(the|a|an)\b\s*', '', s, flags=re.IGNORECASE).strip()
            if s:
                clean_symbols.append(s)
        return ', '.join(clean_symbols)
    return ""

def generate_role(figure_name, figure_type, prompt_text):
    """Generate role from figure type and prompt context."""
    roles = {
        "Zeus": "King of the Gods, God of Sky and Thunder",
        "Hera": "Queen of the Gods, Goddess of Marriage",
        "Poseidon": "God of the Sea, Earthquakes, and Horses",
        "Demeter": "Goddess of Agriculture and Harvest",
        "Athena": "Goddess of Wisdom, Strategy, and Warfare",
        "Apollo": "God of Music, Poetry, Light, and Prophecy",
        "Artemis": "Goddess of the Hunt, Wilderness, and Moon",
        "Ares": "God of War and Violence",
        "Aphrodite": "Goddess of Love, Beauty, and Passion",
        "Hephaestus": "God of Fire, Metalwork, and Craftsmanship",
        "Hermes": "Messenger of the Gods, God of Trade and Travel",
        "Dionysus": "God of Wine, Revelry, and Theater",
        "Hestia": "Goddess of the Hearth and Home",
        "Hades": "God of the Underworld and the Dead",
        "Persephone": "Queen of the Underworld, Goddess of Spring",
        "Hecate": "Goddess of Magic, Crossroads, and Ghosts",
        "Pan": "God of the Wild, Shepherds, and Rustic Music",
        "Nike": "Goddess of Victory",
        "Tyche": "Goddess of Fortune and Chance",
        "Morpheus": "God of Dreams",
        "Chaos": "Primordial Void of Creation",
        "Gaia": "Primordial Earth Mother",
        "Ouranos": "Primordial Sky God",
        "Tartarus": "Primordial Abyss",
        "Eros": "Primordial God of Love",
        "Nyx": "Primordial Goddess of Night",
        "Erebus": "Primordial God of Darkness",
        "Chronos": "Primordial God of Time",
        "Hypnos": "God of Sleep",
        "Thanatos": "Personification of Death",
        "Kronos": "Titan King, Lord of Time",
        "Rhea": "Titan Goddess of Motherhood",
        "Oceanus": "Titan God of the Ocean River",
        "Tethys": "Titan Goddess of Fresh Water",
        "Hyperion": "Titan God of Light",
        "Theia": "Titan Goddess of Sight and Radiance",
        "Prometheus": "Titan Champion of Humanity, Giver of Fire",
        "Atlas": "Titan Bearer of the Heavens",
        "Coeus": "Titan God of Intellect",
        "Cronus": "Titan King of the Golden Age",
        "Iapetus": "Titan God of Mortality and Craftsmanship",
        "Mnemosyne": "Titan Goddess of Memory",
        "Phoebe": "Titan Goddess of Prophecy",
        "Themis": "Titan Goddess of Divine Law and Order",
        "Helios": "Titan God of the Sun",
        "Selene": "Titan Goddess of the Moon",
        "Titan": "Elder Primordial God",
        "Heracles": "Greatest of Greek Heroes",
        "Achilles": "Legendary Warrior of the Trojan War",
        "Odysseus": "Hero of the Odyssey, King of Ithaca",
        "Perseus": "Hero Slayer of Medusa",
        "Theseus": "Hero Founder of Athens",
        "Jason": "Leader of the Argonauts",
        "Orpheus": "Legendary Musician and Poet",
        "Medusa": "Gorgon with Petrifying Gaze",
        "Cassandra": "Trojan Prophetess",
        "Psyche": "Mortal Beloved of Eros, Goddess of the Soul",
        "Echo": "Mountain Nymph",
        "Narcissus": "Beautiful Youth"
    }
    
    return roles.get(figure_name, f"{figure_type} Figure")

def generate_description(figure_name, prompt_text):
    """Generate 1-2 sentence description from prompt."""
    # Extract the main descriptive clause from prompt
    match = re.search(r':\s*([^,]+),\s*([^,]+),\s*depicted as\s+([^,]+)', prompt_text)
    if match:
        name = match.group(1)
        title = match.group(2)
        depiction = match.group(3)
        return f"{name}, {title}, depicted as {depiction} in Greek mythology."
    
    # Fallback
    return f"{figure_name} from Greek mythology."

def update_figure_attributes():
    """Update all figures with extracted data from prompts."""
    import requests
    
    updated_count = 0
    skipped_count = 0
    
    # Get all figures first
    response = requests.get(f"{API_BASE}/api/v1/figures?limit=100")
    if response.status_code != 200:
        print(f"Error fetching figures: {response.status_code}")
        return
    
    figures = response.json()
    
    for figure_name, data in FIGURE_PROMPTS.items():
        # Find figure in API response
        figure = next((f for f in figures if f["english_name"] == figure_name), None)
        
        if not figure:
            print(f"⚠️  {figure_name}: Not found in database")
            skipped_count += 1
            continue
        
        prompt = data["prompt"]
        
        # Extract data
        symbols = extract_symbols(prompt)
        role = generate_role(figure_name, data["figure_type"], prompt)
        description = generate_description(figure_name, prompt)
        
        # Prepare update payload (only update if current value is None/empty)
        updates = {}
        if not figure.get("symbols"):
            updates["symbols"] = symbols
        if not figure.get("role"):
            updates["role"] = role
        if not figure.get("description"):
            updates["description"] = description
        
        # Skip if nothing to update
        if not updates:
            print(f"⏭️  {figure_name}: Already complete")
            skipped_count += 1
            continue
        
        # Update via API
        update_response = requests.put(
            f"{API_BASE}/api/v1/figures/{figure['id']}",
            json=updates
        )
        
        if update_response.status_code == 200:
            updated_count += 1
            print(f"✓ {figure_name}")
            if "role" in updates:
                print(f"  Role: {role}")
            if "symbols" in updates:
                print(f"  Symbols: {symbols[:60]}{'...' if len(symbols) > 60 else ''}")
        else:
            print(f"✗ {figure_name}: Update failed ({update_response.status_code})")
            skipped_count += 1
    
    print(f"\n{'='*50}")
    print(f"✓ Phase 2 Complete!")
    print(f"Updated: {updated_count} figures")
    print(f"Skipped: {skipped_count} figures")
    print(f"{'='*50}")

if __name__ == "__main__":
    update_figure_attributes()
