"""Display generated content examples."""
import requests
import json

SERVICE_URL = "https://etymython-mnovne7bma-uc.a.run.app"

def display_figure_content(figure_id):
    """Display all content for a figure."""
    # Get figure details
    response = requests.get(f"{SERVICE_URL}/api/v1/figures/{figure_id}")
    figure = response.json()
    
    print("\n" + "="*70)
    print(f"📖 {figure['english_name']} ({figure['greek_name']})")
    print("="*70)
    
    print(f"\n🎭 Role: {figure.get('role', 'N/A')}")
    print(f"🏛️  Domain: {figure.get('domain', 'N/A')}")
    print(f"⚡ Symbols: {figure.get('symbols', 'N/A')}")
    
    # Origin story
    if figure.get('origin_story'):
        print(f"\n📜 ORIGIN STORY:")
        print("-" * 70)
        print(figure['origin_story'])
    else:
        print(f"\n📜 ORIGIN STORY: Not generated yet")
    
    # Fun facts
    response = requests.get(f"{SERVICE_URL}/api/v1/figures/{figure_id}/facts")
    if response.status_code == 200:
        facts = response.json()
        if facts:
            print(f"\n🎯 FUN FACTS ({len(facts)} total):")
            print("-" * 70)
            for i, fact in enumerate(facts, 1):
                print(f"\n  {i}. [{fact['category'].upper()}] ⭐ {fact['surprise_factor']}/5")
                print(f"     {fact['content']}")
        else:
            print(f"\n🎯 FUN FACTS: None yet")
    
    print("\n" + "="*70)

def main():
    print("\n🌟 ETYMYTHON GENERATED CONTENT EXAMPLES")
    
    # Show status
    status = requests.get(f"{SERVICE_URL}/api/v1/content/status").json()
    print(f"\n📊 Current Status:")
    print(f"   Origin Stories: {status['with_origin_stories']}/{status['total_figures']}")
    print(f"   Fun Facts: {status['total_fun_facts']} total")
    
    # Show examples from different figure types
    examples = [
        (1, "Olympian goddess"),
        (5, "Olympian goddess"),
        (3, "Olympian god"),
        (15, "Titan"),
        (20, "Primordial deity")
    ]
    
    for figure_id, description in examples:
        display_figure_content(figure_id)
        input(f"\n⏎ Press Enter to see next example ({description})...")

if __name__ == "__main__":
    main()
