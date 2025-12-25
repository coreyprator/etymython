"""
Etymython Figure Image Generation - Renaissance Portrait Prompts
Custom prompts for each mythological figure with symbolic attributes.
"""

FIGURE_PROMPTS = {
    # PRIMORDIALS
    "Chaos": {
        "figure_type": "Primordial",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Chaos, the primordial void from which all creation emerged, depicted as a swirling abstract presence of darkness and light intermingling, in neutral backdrop, dramatic Rembrandt lighting, centered composition filling 70% of frame. Symbolism: swirling mists, void darkness meeting dawn light, cosmic egg fragmenting, formless essence. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Gaia": {
        "figure_type": "Primordial",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Gaia, the primordial Earth Mother and personification of the Earth itself, depicted as a nurturing maternal figure with earthy presence, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: grain wreath crown, fertile soil, mountain silhouette, verdant leaves, roots. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Ouranos": {
        "figure_type": "Primordial",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Ouranos, the primordial sky god and personification of the heavens, depicted as an ethereal celestial figure gazing upward, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: star-studded cloak, constellation patterns, celestial sphere, dawn breaking. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Tartarus": {
        "figure_type": "Primordial",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Tartarus, the primordial abyss and deepest dungeon beneath the underworld, depicted as a dark imposing figure emerging from shadows, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: chains, deep chasm, bronze gates, darkness absolute, imprisonment. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Eros": {
        "figure_type": "Primordial",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Eros, the primordial god of love and procreation, depicted as a beautiful youthful figure with captivating allure, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: golden arrows, heart flames, roses blooming, cosmic union, desire. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Nyx": {
        "figure_type": "Primordial",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Nyx, the primordial goddess of night, depicted as a hauntingly beautiful woman cloaked in star-studded darkness, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: cloak of night sky with stars, crescent moon diadem, owl feathers, poppies for sleep. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Erebus": {
        "figure_type": "Primordial",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Erebus, the primordial deity of darkness and shadow, depicted as a mysterious figure shrouded in deep shadows, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: impenetrable darkness, shadow tendrils, moonless night, cave depths. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    
    # TITANS
    "Kronos": {
        "figure_type": "Titan",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Kronos, the Titan lord of time who devoured his children, depicted as an ancient powerful figure with world-weary eyes, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: scythe of time, hourglass, ouroboros, harvest sickle, temporal gears. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Rhea": {
        "figure_type": "Titan",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Rhea, the Titan goddess of motherhood and fertility, depicted as a protective maternal figure with regal bearing, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: lion companion, mountain crown, fertile earth, swaddling stone, maternal strength. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Oceanus": {
        "figure_type": "Titan",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Oceanus, the Titan god of the world-encircling river, depicted as a bearded aquatic figure with flowing presence, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: serpentine river, crab-claw horns, flowing water, global stream, fish. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Tethys": {
        "figure_type": "Titan",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Tethys, the Titan goddess of fresh water and nursing, depicted as a serene aquatic maternal figure, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: spring waters, river tributaries, nurturing streams, water vessel, pearl adornments. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Hyperion": {
        "figure_type": "Titan",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Hyperion, the Titan god of light and watchfulness, depicted as a radiant vigilant figure, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: solar crown, golden rays, all-seeing eyes, celestial light, dawn breaking. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Theia": {
        "figure_type": "Titan",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Theia, the Titan goddess of sight and shining light, depicted as a luminous elegant figure, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: precious gems, gold and silver, radiant eyes, crystal prism, light refraction. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Prometheus": {
        "figure_type": "Titan",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Prometheus, the Titan champion of humanity who stole fire, depicted as a defiant noble figure bearing suffering with dignity, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: torch of stolen fire, chain marks, eagle, fennel stalk, foresight wisdom. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Atlas": {
        "figure_type": "Titan",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Atlas, the Titan condemned to bear the heavens on his shoulders, depicted as a muscular strained figure with cosmic burden, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: celestial sphere, star-map, shoulders bearing weight, mountain strength, endurance. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    
    # OLYMPIANS - PRIMARY DEITIES
    "Zeus": {
        "figure_type": "Olympian",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Zeus, the king of the Olympian gods and ruler of sky and thunder, depicted as a powerful regal figure with commanding presence, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: lightning bolt, eagle, oak wreath crown, royal scepter, storm clouds. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Hera": {
        "figure_type": "Olympian",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Hera, queen of the gods and goddess of marriage and family, depicted as a majestic royal woman with dignified bearing, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: golden diadem, peacock feathers, pomegranate, royal scepter, wedding veil. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Poseidon": {
        "figure_type": "Olympian",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Poseidon, god of the sea, earthquakes, and horses, depicted as a powerful bearded figure with oceanic majesty, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: trident, dolphin, horse, coral crown, wave patterns, ship. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Demeter": {
        "figure_type": "Olympian",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Demeter, goddess of harvest, agriculture, and fertility, depicted as a nurturing maternal figure with agricultural abundance, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: wheat sheaf crown, cornucopia, torch, poppies, sickle, ripe grain. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Athena": {
        "figure_type": "Olympian",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Athena, goddess of wisdom, warfare, and crafts, depicted as a wise warrior with intelligent gaze and armor, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: owl companion, Medusa aegis shield, olive branch, helmet with crest, spear, wisdom. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Apollo": {
        "figure_type": "Olympian",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Apollo, god of sun, music, prophecy, and healing, depicted as a radiant youthful figure with artistic grace, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: golden lyre, laurel wreath, sun rays, silver bow, python, healing staff. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Artemis": {
        "figure_type": "Olympian",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Artemis, goddess of the hunt, wilderness, and moon, depicted as a fierce independent huntress with wild beauty, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: silver bow and arrows, crescent moon diadem, deer companion, hunting dog, cypress trees. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Ares": {
        "figure_type": "Olympian",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Ares, god of war and bloodshed, depicted as a fierce warrior with battle-hardened intensity, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: bronze helmet, blood-red plume, spear and shield, war chariot, vulture, flames of battle. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Aphrodite": {
        "figure_type": "Olympian",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Aphrodite, goddess of love, beauty, and desire, depicted as an exquisitely beautiful figure with captivating allure, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: seashell, dove, rose, myrtle wreath, golden apple, swan, mirror. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Hephaestus": {
        "figure_type": "Olympian",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Hephaestus, god of fire, metalworking, and crafts, depicted as a powerful craftsman with creative intensity, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: hammer and anvil, forge flames, mechanical automatons, golden leg brace, tongs, bronze. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Hermes": {
        "figure_type": "Olympian",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Hermes, messenger of the gods and god of travelers, commerce, and thieves, depicted as a swift clever youth with mischievous intelligence, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: winged sandals, caduceus staff with serpents, petasos traveler's hat, tortoise, ram. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Dionysus": {
        "figure_type": "Olympian",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Dionysus, god of wine, ecstasy, and theater, depicted as an androgynous youthful figure with wild joyous energy, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: ivy crown, thyrsus staff with pinecone, wine goblet, grape clusters, leopard, theatrical mask. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Hestia": {
        "figure_type": "Olympian",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Hestia, goddess of the hearth, home, and sacred fire, depicted as a gentle serene figure with warm presence, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: eternal flame, hearthfire, veil of modesty, kettle, home altar, domestic peace. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    
    # MAJOR DEITIES
    "Hades": {
        "figure_type": "Deity",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Hades, god of the underworld and lord of the dead, depicted as a dark imposing figure with regal solemnity, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: bident scepter, helm of invisibility, Cerberus, cypress, narcissus flower, keys to underworld. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Persephone": {
        "figure_type": "Deity",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Persephone, queen of the underworld and goddess of spring, depicted as a dual-nature figure showing both maiden and queen, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: pomegranate seeds, spring flowers meeting shadows, torch, duality of light and dark, crown of life and death. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Hecate": {
        "figure_type": "Deity",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Hecate, goddess of magic, crossroads, and ghosts, depicted as a mysterious triple-formed figure with arcane power, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: twin torches, key, dagger, black dogs, yew tree, crossroads, moon phases. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Pan": {
        "figure_type": "Deity",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Pan, god of the wild, shepherds, and rustic music, depicted as a rustic half-goat figure with wild untamed energy, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: pan pipes (syrinx), goat horns, shepherd's crook, pine wreath, wild nature, panic. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Nike": {
        "figure_type": "Deity",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Nike, goddess of victory, depicted as a triumphant winged figure with dynamic energy, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: large feathered wings, laurel wreath, palm branch, victory trumpet, athletic grace, triumph. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Tyche": {
        "figure_type": "Deity",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Tyche, goddess of fortune and chance, depicted as an enigmatic figure balancing fate, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: wheel of fortune, cornucopia, rudder of fate, mural crown, dice, changing expression. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    
    # HEROES & MORTALS
    "Heracles": {
        "figure_type": "Hero",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Heracles, the greatest of Greek heroes known for his strength, depicted as a powerfully muscular figure with heroic bearing, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: lion skin headdress, wooden club, bow and arrows, twelve labors symbols, olive wreath. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Achilles": {
        "figure_type": "Hero",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Achilles, the invulnerable warrior hero of the Trojan War, depicted as a fierce noble warrior with tragic intensity, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: golden armor, spear, heel exposed, myrmidons ant motif, grief and glory, warrior's laurel. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Odysseus": {
        "figure_type": "Hero",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Odysseus, the cunning hero of the Odyssey known for his intelligence, depicted as a weathered clever figure with wise eyes, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: ship and oar, Trojan horse miniature, odyssey compass, olive wood bow, traveler's cloak. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Perseus": {
        "figure_type": "Hero",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Perseus, the hero who slew Medusa, depicted as a youthful triumphant figure with divine favor, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: mirrored shield, winged sandals, kibisis pouch, Medusa head reflection, harpe sword, starry constellation. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Theseus": {
        "figure_type": "Hero",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Theseus, the hero who defeated the Minotaur, depicted as a courageous noble youth with kingly bearing, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: Ariadne's thread spool, labyrinth pattern, sword, Minotaur horn, Athenian ship. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Jason": {
        "figure_type": "Hero",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Jason, leader of the Argonauts who sought the Golden Fleece, depicted as an adventurous leader with determined gaze, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: golden fleece draped, Argo ship model, dragon teeth, lost sandal, Argonaut helm. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Orpheus": {
        "figure_type": "Hero",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Orpheus, the legendary musician who descended to the underworld, depicted as a melancholic poetic figure with artistic soul, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: golden lyre, musical notes, looking back pose, poplar leaves, Eurydice's shadow, broken strings. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Medusa": {
        "figure_type": "Mortal",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Medusa, the gorgon whose gaze turns mortals to stone, depicted as a tragically beautiful woman with serpentine features, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: living serpent hair, petrifying stare, grief and rage, stone statues, Athena's curse, transformation. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
    "Cassandra": {
        "figure_type": "Mortal",
        "prompt": "Studio portrait photography styled like a Renaissance allegory: Cassandra, the tragic prophetess cursed never to be believed, depicted as a desperate impassioned figure with knowing eyes, in neutral backdrop, dramatic Rembrandt lighting, centered bust composition filling 70% of frame. Symbolism: laurel crown, prophetic visions, flames of Troy, unheeded warnings, tragic knowledge, Apollo's curse. Ultra sharp, museum-quality, high contrast for thumbnail visibility, no text."
    },
}

# Helper function to get all figure names
def get_all_figure_names():
    """Return list of all figure names that have prompts."""
    return list(FIGURE_PROMPTS.keys())

# Helper function to get prompts by type
def get_prompts_by_type(figure_type: str):
    """Return all prompts for a specific figure type."""
    return {
        name: data for name, data in FIGURE_PROMPTS.items() 
        if data["figure_type"] == figure_type
    }

# Get figure types
def get_figure_types():
    """Return list of unique figure types."""
    return list(set(data["figure_type"] for data in FIGURE_PROMPTS.values()))
