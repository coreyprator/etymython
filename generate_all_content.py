"""Generate content for all 56 mythological figures."""
import requests
import time
import json
from datetime import datetime

SERVICE_URL = "https://etymython-mnovne7bma-uc.a.run.app"

def check_status():
    """Check current content status."""
    response = requests.get(f"{SERVICE_URL}/api/v1/content/status")
    return response.json()

def generate_content_for_figure(figure_id):
    """Generate both origin story and fun facts for a figure."""
    results = {"figure_id": figure_id, "origin_story": "skipped", "fun_facts": "skipped"}
    
    try:
        # Try origin story
        response = requests.post(
            f"{SERVICE_URL}/api/v1/content/generate-origin-story/{figure_id}",
            timeout=120
        )
        if response.status_code == 200:
            data = response.json()
            results["origin_story"] = "generated"
            results["figure_name"] = data.get("figure_name", f"Figure {figure_id}")
        elif response.status_code == 400:
            results["origin_story"] = "exists"
        else:
            results["origin_story"] = f"error_{response.status_code}"
    except requests.exceptions.Timeout:
        results["origin_story"] = "timeout"
    except Exception as e:
        results["origin_story"] = f"error: {str(e)[:50]}"
    
    try:
        # Try fun facts
        response = requests.post(
            f"{SERVICE_URL}/api/v1/content/generate-fun-facts/{figure_id}",
            timeout=120
        )
        if response.status_code == 200:
            data = response.json()
            results["fun_facts"] = f"generated_{data.get('facts_created', 4)}"
        elif response.status_code == 400:
            results["fun_facts"] = "exists"
        else:
            results["fun_facts"] = f"error_{response.status_code}"
    except requests.exceptions.Timeout:
        results["fun_facts"] = "timeout"
    except Exception as e:
        results["fun_facts"] = f"error: {str(e)[:50]}"
    
    return results

def main():
    print("="*70)
    print("🚀 CONTENT GENERATION FOR ALL 56 FIGURES")
    print("="*70)
    print(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # Check initial status
    status = check_status()
    print(f"📊 Initial Status:")
    print(f"   Total figures: {status['total_figures']}")
    print(f"   Origin stories: {status['with_origin_stories']}/{status['total_figures']} ({status['origin_story_percentage']}%)")
    print(f"   Fun facts: {status['total_fun_facts']} total")
    print(f"   Figures with facts: {status['figures_with_fun_facts']}")
    print(f"\n⏱️  Estimated time: ~3-5 minutes")
    print(f"💰 Estimated cost: ~$0.73 for new content\n")
    
    # Generate for all figures
    results = []
    generated_stories = 0
    generated_facts = 0
    errors = 0
    
    for figure_id in range(1, 57):  # 1-56
        print(f"[{figure_id}/56] ", end="", flush=True)
        
        result = generate_content_for_figure(figure_id)
        results.append(result)
        
        # Track stats
        if result["origin_story"] == "generated":
            generated_stories += 1
            print(f"✅ {result.get('figure_name', f'Figure {figure_id}')} - Story + Facts")
        elif result["origin_story"] == "exists":
            print(f"⏭️  Figure {figure_id} - Already complete")
        else:
            errors += 1
            print(f"❌ Figure {figure_id} - {result['origin_story']}")
        
        if result["fun_facts"].startswith("generated"):
            generated_facts += int(result["fun_facts"].split("_")[1])
        
        # Small delay to avoid rate limits
        time.sleep(1)
    
    # Final status
    print(f"\n" + "="*70)
    final_status = check_status()
    print(f"📊 Final Status:")
    print(f"   Origin stories: {final_status['with_origin_stories']}/{final_status['total_figures']} ({final_status['origin_story_percentage']}%)")
    print(f"   Fun facts: {final_status['total_fun_facts']} total")
    print(f"   Avg facts/figure: {final_status['avg_facts_per_figure']}")
    
    print(f"\n📈 This Session:")
    print(f"   New origin stories: {generated_stories}")
    print(f"   New fun facts: {generated_facts}")
    print(f"   Errors: {errors}")
    
    print(f"\nCompleted: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*70)
    
    # Save detailed results
    with open("content_generation_results.json", "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "initial_status": status,
            "final_status": final_status,
            "details": results
        }, f, indent=2)
    
    print(f"\n💾 Detailed results saved to: content_generation_results.json")

if __name__ == "__main__":
    main()
