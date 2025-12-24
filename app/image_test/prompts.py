"""
Etymython Image Style Test - Prompt Library
All prompts organized by category for systematic DALL-E 3 testing.
"""

PROMPTS = {
    # ============================================================
    # 1) ART-HISTORICAL MOVEMENTS
    # ============================================================
    "1A_baroque_caravaggio": {
        "category": "Art Historical",
        "style": "Baroque (Caravaggio tenebrism)",
        "prompt": 'Oil painting in the style of Caravaggio tenebrism: CHRONOS (Χρόνος), primordial personification of eternal Time, as a towering human-like figure emerging from darkness. Single centered silhouette, dramatic chiaroscuro spotlight, deep blacks. Symbolism: a glowing hourglass in one hand, a faint ouroboros circle behind his head like a halo, dust motes and candle smoke suggesting decay. Minimal background, museum-grade realism, no text.'
    },
    "1A_baroque_rubens": {
        "category": "Art Historical",
        "style": "High Baroque (Rubens-era)",
        "prompt": 'High Baroque allegory (Rubens-era): CHRONOS as a colossal figure with swirling cloth like a galaxy, central composition, bold light–dark contrast. Symbolism: celestial clockwork (gears as constellations), a waning-to-waxing moon arc above, subtle cracks and gold leaf highlights. Rich oil textures, dynamic brushwork, no text.'
    },
    "1B_romanticism_turner": {
        "category": "Art Historical",
        "style": "Romanticism (Turner sublime)",
        "prompt": 'Romantic sublime painting: CHRONOS as a luminous, semi-abstract figure standing in a storm of cosmic clouds, center-framed. Symbolism: spiral nebula as a time vortex, tiny ruined columns dissolving into mist (entropy), distant sunrise (renewal). Soft edges but strong central value contrast, no text.'
    },
    "1B_romanticism_friedrich": {
        "category": "Art Historical",
        "style": "Romanticism (Caspar David Friedrich)",
        "prompt": 'Caspar David Friedrich atmosphere: CHRONOS as a lone monumental silhouette on a cliff above a sea of fog, central. Symbolism: seasonal ring of trees faintly encircling him, stars forming a clock face, subdued palette, no text.'
    },
    "1C_cubism_analytic": {
        "category": "Art Historical",
        "style": "Analytic Cubism",
        "prompt": 'Analytic Cubism: CHRONOS built from interlocking geometric planes, centered bust with strong contour. Symbolism: fragmented clock hands, repeated hourglass triangles, an ouroboros broken into facets. Limited palette, crisp edges, high contrast, no text.'
    },
    "1C_cubism_synthetic": {
        "category": "Art Historical",
        "style": "Synthetic Cubism",
        "prompt": 'Synthetic Cubism collage: CHRONOS as a central emblem made of layered paper textures, faux newsprint (abstract, unreadable), metallic foil shapes for gears, bold silhouette. Symbolism: circular time loop, seasons as color bands. No legible letters, no text.'
    },
    "1D_futurism_balla": {
        "category": "Art Historical",
        "style": "Italian Futurism",
        "prompt": 'Italian Futurism: CHRONOS as a central figure made of speed lines and repeated forms, radiating motion. Symbolism: clock numerals suggested as shapes (not readable), orbiting planets as rhythmic arcs, metallic sheen. Strong center contrast, no text.'
    },
    "1D_futurism_boccioni": {
        "category": "Art Historical",
        "style": "Futurism (Boccioni sculptural)",
        "prompt": 'Boccioni-inspired sculptural Futurism painting: CHRONOS as a bronze-like form exploding into temporal ripples, centered, bold silhouette. Symbolism: concentric rings = time waves, no text.'
    },
    "1E_abstract_rothko": {
        "category": "Art Historical",
        "style": "Abstract Expressionism (Rothko)",
        "prompt": 'Rothko-like luminous fields: CHRONOS implied as a single central totem silhouette inside glowing stacked color rectangles, subtle ouroboros ring as a soft circle. Minimal elements, intense color depth, no text.'
    },
    "1E_abstract_dekooning": {
        "category": "Art Historical",
        "style": "Abstract Expressionism (de Kooning)",
        "prompt": 'De Kooning gestural: CHRONOS as a central figure formed by sweeping brushstrokes, violent contrast, paint drips like sand in an hourglass. Symbolism: cycles hinted by circular strokes, no text.'
    },

    # ============================================================
    # 2) TRADITIONAL MEDIUMS
    # ============================================================
    "2A_fresco_renaissance": {
        "category": "Traditional Medium",
        "style": "Buon Fresco (Renaissance)",
        "prompt": 'Buon fresco mural: CHRONOS as an allegorical central figure on cracked plaster, pigments slightly faded. Symbolism: hourglass, zodiac ring, vines sprouting through cracks (renewal). Strong silhouette, no text.'
    },
    "2A_fresco_pompeian": {
        "category": "Traditional Medium",
        "style": "Pompeian Fresco",
        "prompt": 'Pompeian-style fresco realism: CHRONOS centered against a flat architectural backdrop, warm earth pigments, subtle trompe-l\'oeil frame. Symbolism: ouroboros medallion, sundial shadow, no text.'
    },
    "2B_mosaic_byzantine": {
        "category": "Traditional Medium",
        "style": "Byzantine Gold Mosaic",
        "prompt": 'Gold tesserae mosaic: CHRONOS front-facing, iconic, centered, bold outline. Background: shimmering gold. Symbolism: circular ouroboros border, hourglass as gem-inlaid icon, star ring. High contrast for thumbnails, no text.'
    },
    "2B_mosaic_roman": {
        "category": "Traditional Medium",
        "style": "Ancient Stone Mosaic",
        "prompt": 'Ancient stone mosaic: limited palette, chunky tesserae, CHRONOS as a central emblem with clear contour. Symbolism: seasons as four corner motifs, no text.'
    },
    "2C_stained_glass_gothic": {
        "category": "Traditional Medium",
        "style": "Gothic Stained Glass",
        "prompt": 'Cathedral stained glass: CHRONOS as a central stained-glass saint-like figure but cosmic, thick black lead lines, saturated colors. Symbolism: hourglass, zodiac wheel, ouroboros halo. No text, no letters, strong central icon.'
    },
    "2C_stained_glass_nouveau": {
        "category": "Traditional Medium",
        "style": "Art Nouveau Stained Glass",
        "prompt": 'Art Nouveau stained glass (Mucha-adjacent): flowing curves, CHRONOS as central figure with orbiting celestial motifs, bold outline, no text.'
    },
    "2D_ink_sumi": {
        "category": "Traditional Medium",
        "style": "Sumi-e Ink Wash",
        "prompt": 'Sumi-e ink wash: CHRONOS as a single bold brushstroke figure, centered, lots of negative space. Symbolism: one circular brushstroke (ensō) as ouroboros, dripping ink as sand/time, no text.'
    },
    "2D_ink_chinese": {
        "category": "Traditional Medium",
        "style": "Chinese Ink Landscape",
        "prompt": 'Chinese ink landscape + figure: CHRONOS as a central ink silhouette in mist, tiny crumbling pagoda/ruin below, moon phases as small marks. Strong center contrast, no text.'
    },
    "2E_woodcut_german": {
        "category": "Traditional Medium",
        "style": "German Expressionist Woodcut",
        "prompt": 'German Expressionist woodcut: CHRONOS as a stark central black figure, carved lines, heavy contrast. Symbolism: hourglass, ouroboros, sun/moon. Perfect for tiny thumbnails, no text.'
    },
    "2E_woodcut_japanese": {
        "category": "Traditional Medium",
        "style": "Japanese Linocut",
        "prompt": 'Japanese-inspired linocut: flat colors, bold outlines, CHRONOS centered with wave-like time ribbons, no text.'
    },

    # ============================================================
    # 3) CULTURAL ART TRADITIONS
    # ============================================================
    "3A_byzantine_icon": {
        "category": "Cultural Tradition",
        "style": "Byzantine Icon",
        "prompt": 'Byzantine icon painting: CHRONOS front-facing, symmetrical, gold leaf background, strong outline. Symbolism: ouroboros halo, hourglass held like a sacred object, star ring. No text, no Greek letters.'
    },
    "3A_orthodox_icon": {
        "category": "Cultural Tradition",
        "style": "Orthodox Icon (Cosmic)",
        "prompt": 'Orthodox icon + cosmic allegory: CHRONOS as a central icon with celestial mandorla, cracked varnish patina, no text.'
    },
    "3B_ukiyo_hokusai": {
        "category": "Cultural Tradition",
        "style": "Ukiyo-e (Hokusai)",
        "prompt": 'Ukiyo-e woodblock print: CHRONOS as a central stylized figure emerging from swirling waves that resemble clock spirals, limited palette, crisp outline. Symbolism: moon phases arc, hourglass motif simplified. No text.'
    },
    "3B_ukiyo_night": {
        "category": "Cultural Tradition",
        "style": "Ukiyo-e Night Sky",
        "prompt": 'Ukiyo-e night sky: CHRONOS centered, constellations as pattern, ouroboros circle behind, no text.'
    },
    "3C_persian_miniature": {
        "category": "Cultural Tradition",
        "style": "Persian Miniature",
        "prompt": 'Persian miniature illumination: CHRONOS centered on a flat patterned background, intricate borders, jewel tones. Symbolism: celestial spheres, hourglass, ouroboros. Keep main figure large and central, avoid crowding, no text.'
    },
    "3C_timurid_miniature": {
        "category": "Cultural Tradition",
        "style": "Timurid Miniature",
        "prompt": 'Timurid-style miniature: CHRONOS as a central cosmic elder, swirling clouds, fine linework, no text.'
    },
    "3D_art_deco_erte": {
        "category": "Cultural Tradition",
        "style": "Art Deco (Erté)",
        "prompt": 'Art Deco (Erté / 1920s): CHRONOS as a central geometric figure with symmetrical rays, metallic gold and deep navy. Symbolism: stylized hourglass, concentric circles like clockwork. No text, no lettering.'
    },
    "3D_art_deco_streamline": {
        "category": "Cultural Tradition",
        "style": "Streamline Moderne",
        "prompt": 'Streamline Moderne Deco: CHRONOS as a sleek central silhouette, bold sunburst, minimal forms, no text.'
    },
    "3E_constructivist": {
        "category": "Cultural Tradition",
        "style": "Soviet Constructivist",
        "prompt": 'Propaganda-style graphic illustration (constructivist composition): CHRONOS as a monumental central figure with bold diagonal shapes and limited palette. Symbolism: clock gears, rising sun for renewal. No text, no slogans.'
    },
    "3E_constructivist_montage": {
        "category": "Cultural Tradition",
        "style": "Constructivist Photomontage",
        "prompt": 'Constructivist photomontage look: CHRONOS centered, abstract geometry + cosmic elements, strong contrast, no text.'
    },

    # ============================================================
    # 4) PHOTOREALISTIC APPROACHES
    # ============================================================
    "4A_cinematic_epic": {
        "category": "Photorealistic",
        "style": "Cinematic Film Still (Epic)",
        "prompt": 'Cinematic film still: CHRONOS as a towering cosmic humanoid in a dark void, centered, rim-lit. Symbolism: floating hourglass with glowing sand, planets orbiting like clock gears, decayed marble fragments drifting. Ultra-detailed, high contrast, no text, no UI.'
    },
    "4A_cinematic_imax": {
        "category": "Photorealistic",
        "style": "IMAX Cosmic Close-up",
        "prompt": "IMAX cosmic close-up: CHRONOS' face implied in nebulae, central, intense eyes as star clusters, ouroboros halo faint, no text."
    },
    "4B_portrait_renaissance": {
        "category": "Photorealistic",
        "style": "Renaissance Studio Portrait",
        "prompt": 'Studio portrait photography styled like a Renaissance allegory: CHRONOS as an ageless figure in neutral backdrop, dramatic Rembrandt lighting, centered bust. Symbolism: hourglass, antique astrolabe, subtle decay (wilted leaves) and renewal (sprout). Ultra sharp, no text.'
    },
    "4B_portrait_editorial": {
        "category": "Photorealistic",
        "style": "High-Fashion Editorial",
        "prompt": 'High-fashion editorial portrait: CHRONOS as a modern cosmic entity, centered, strong silhouette, minimal props: single hourglass + ouroboros bracelet, hard light, no text.'
    },

    # ============================================================
    # 5) 3D AND SCULPTURAL
    # ============================================================
    "5A_marble_classical": {
        "category": "Sculptural",
        "style": "Greco-Roman Marble",
        "prompt": 'Greco-Roman marble statue: CHRONOS as a colossal classical statue, centered, shallow depth of field, dramatic museum lighting. Symbolism: carved ouroboros ring, hourglass relief, subtle cracks with moss (renewal). High contrast, no text.'
    },
    "5A_marble_hellenistic": {
        "category": "Sculptural",
        "style": "Hellenistic Fragment",
        "prompt": 'Hellenistic sculpture fragment: CHRONOS as a broken but powerful bust on pedestal, cosmic starfield background, hourglass motif carved, no text.'
    },
    "5B_bronze_patina": {
        "category": "Sculptural",
        "style": "Bronze with Verdigris",
        "prompt": 'Bronze statue with verdigris patina: CHRONOS as a central totem, gears and celestial rings integrated, moody lighting, no text.'
    },
    "5B_terracotta": {
        "category": "Sculptural",
        "style": "Terracotta Ritual Figure",
        "prompt": 'Terracotta ritual figure: CHRONOS as ancient figurine, centered, earthy tones, incised hourglass and spiral motifs, no text.'
    },
    "5C_holographic_glass": {
        "category": "Sculptural",
        "style": "Holographic Glass Sculpture",
        "prompt": 'Iridescent glass hologram sculpture: CHRONOS as a central translucent figure refracting light into spectral rings, ouroboros as a light loop, hourglass as internal glow. Clean background, high contrast, no text.'
    },

    # ============================================================
    # 6) DIGITAL / CONTEMPORARY
    # ============================================================
    "6A_concept_art_aaa": {
        "category": "Digital",
        "style": "AAA Concept Art",
        "prompt": 'AAA concept art: CHRONOS as an epic cosmic entity, centered, sharp silhouette, massive time halo of rotating astrolabe rings. Symbolism: hourglass core, decaying stars turning into newborn stars. Painterly realism, no text.'
    },
    "6A_matte_painting": {
        "category": "Digital",
        "style": "Matte Painting",
        "prompt": 'Matte painting style: CHRONOS as a colossal figure in a cosmic cathedral of time, centered, strong foreground silhouette, no text.'
    },
    "6B_graphic_novel": {
        "category": "Digital",
        "style": "Graphic Novel Cover",
        "prompt": 'Graphic novel cover art (ink + flat color): CHRONOS centered with thick inks, bold shapes, high contrast. Symbolism: ouroboros halo, hourglass, clockwork planets. No text.'
    },
    "6B_bande_dessinee": {
        "category": "Digital",
        "style": "European Bande Dessinée",
        "prompt": 'European bande dessinée: clean line, limited palette, CHRONOS as central emblem, no text.'
    },
    "6C_synthwave": {
        "category": "Digital",
        "style": "Synthwave",
        "prompt": 'Synthwave digital art: CHRONOS as a central neon silhouette, grid horizon, sun as clock face, ouroboros as neon ring, hourglass glowing. High contrast, no text.'
    },

    # ============================================================
    # 7) ANCIENT / ARCHAEOLOGICAL
    # ============================================================
    "7A_greek_redfigure": {
        "category": "Archaeological",
        "style": "Greek Red-Figure Vase",
        "prompt": 'Attic red-figure vase painting: CHRONOS as a central black-figure-like silhouette on terracotta, simplified but iconic. Symbolism: meander border shaped like time cycle, hourglass motif, ouroboros ring. No text, no inscriptions.'
    },
    "7A_greek_blackfigure": {
        "category": "Archaeological",
        "style": "Greek Black-Figure Amphora",
        "prompt": 'Black-figure amphora style: CHRONOS centered, bold silhouette, minimal scene elements, no text.'
    },
    "7B_egyptian_papyrus": {
        "category": "Archaeological",
        "style": "Egyptian Papyrus",
        "prompt": 'Ancient papyrus illustration: CHRONOS as a central deity-like figure rendered in flat profile style, symbolic hourglass and sun disk cycles, aged papyrus texture. Strong outline, no text.'
    },
    "7C_minoan_fresco": {
        "category": "Archaeological",
        "style": "Minoan Fresco",
        "prompt": 'Minoan fresco style: CHRONOS as a central flowing figure with curvilinear forms, sea-blue and ochre palette, spiral motifs = time, no text.'
    },

    # ============================================================
    # 8) EXPERIMENTAL / HYBRID
    # ============================================================
    "8A_double_exposure": {
        "category": "Experimental",
        "style": "Double Exposure Portrait",
        "prompt": 'Double exposure portrait: CHRONOS as a centered silhouette; inside the silhouette are layered time symbols: star trails, decaying leaves, blooming flowers, hourglass sand, lunar phases. Clean outer edges, high contrast, no text.'
    },
    "8A_star_trails": {
        "category": "Experimental",
        "style": "Long-Exposure Star Trails",
        "prompt": 'Long-exposure star trails: CHRONOS implied as a central negative-space figure formed by star trails and light arcs, ouroboros circle, no text.'
    },
    "8B_glitch_art": {
        "category": "Experimental",
        "style": "High-End Glitch Art",
        "prompt": 'High-end glitch art: CHRONOS as a central statue image subtly fragmented by temporal distortion bands, RGB shifts controlled, hourglass core intact, clean background, no text.'
    },
    "8C_sacred_geometry": {
        "category": "Experimental",
        "style": "Generative Sacred Geometry",
        "prompt": 'Generative sacred geometry: CHRONOS as a central abstract totem made of interlocking circles, spirals, and clockwork mandalas. Clear silhouette, strong contrast, minimal palette, no text.'
    },
    "8C_mixed_media": {
        "category": "Experimental",
        "style": "Mixed Media Collage",
        "prompt": 'Mixed media collage: CHRONOS centered, layered textures of marble, parchment, gold leaf, starfield; hourglass and ouroboros as primary shapes; no text.'
    },
}

# Convenience: Get all prompt IDs
def get_all_prompt_ids():
    return list(PROMPTS.keys())

# Get prompts by category
def get_prompts_by_category(category: str):
    return {k: v for k, v in PROMPTS.items() if v["category"] == category}

# Get all categories
def get_categories():
    return list(set(p["category"] for p in PROMPTS.values()))
