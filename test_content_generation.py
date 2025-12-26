"""Test content generation with progress tracking."""
import requests
import time
import json

SERVICE_URL = "https://etymython-mnovne7bma-uc.a.run.app"

def check_status():
    """Check current content status."""
    response = requests.get(f"{SERVICE_URL}/api/v1/content/status")
    return response.json()

def generate_single_figure(figure_id):
    """Generate content for a single figure."""
    print(f"\n🔨 Generating content for figure {figure_id}...")
    
    try:
        # Generate origin story
        print(f"  📝 Generating origin story...")
        response = requests.post(
            f"{SERVICE_URL}/api/v1/content/generate-origin-story/{figure_id}",
            timeout=120
        )
        story_result = response.json()
        print(f"  ✅ Origin story: {story_result.get('message', 'done')}")
        
        # Generate fun facts
        print(f"  🎯 Generating fun facts...")
        response = requests.post(
            f"{SERVICE_URL}/api/v1/content/generate-fun-facts/{figure_id}",
            timeout=120
        )
        facts_result = response.json()
        print(f"  ✅ Fun facts: {facts_result.get('message', 'done')}")
        
        return True
    except requests.exceptions.Timeout:
        print(f"  ⏱️ Timeout for figure {figure_id}")
        return False
    except Exception as e:
        print(f"  ❌ Error: {str(e)}")
        return False

def main():
    print("🚀 Starting content generation\n")
    
    # Check initial status
    status = check_status()
    print(f"📊 Initial Status:")
    print(f"   Total figures: {status['total_figures']}")
    print(f"   With origin stories: {status['with_origin_stories']}")
    print(f"   With fun facts: {status['figures_with_fun_facts']}")
    
    # Generate for first 5 figures as test
    print(f"\n🎯 Generating content for first 5 figures (test batch)...")
    
    success_count = 0
    for figure_id in range(1, 6):
        if generate_single_figure(figure_id):
            success_count += 1
        time.sleep(2)  # Brief pause between figures
    
    # Check final status
    print(f"\n" + "="*60)
    status = check_status()
    print(f"📊 Final Status:")
    print(f"   Origin stories: {status['with_origin_stories']}/{status['total_figures']}")
    print(f"   Fun facts: {status['total_fun_facts']} total")
    print(f"   Success rate: {success_count}/5 figures")
    
    if success_count == 5:
        print(f"\n✅ Test successful! Ready to generate all 56 figures.")
        print(f"💡 Run: python generate_all_content.py")
    else:
        print(f"\n⚠️ Some failures occurred. Check logs.")

if __name__ == "__main__":
    main()
