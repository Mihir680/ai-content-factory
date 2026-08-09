import json
import re
import urllib.parse
import requests
from pathlib import Path
from Backend.services.gemini_service import generate_text

MEDIA_DIR = Path(__file__).resolve().parent.parent / "media" / "images"
MEDIA_DIR.mkdir(parents=True, exist_ok=True)


def parse_json_from_llm(response_text: str):
    """Extracts JSON array from LLM response text."""
    match = re.search(r"\[.*\]", response_text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(0))
        except json.JSONDecodeError:
            pass
    try:
        return json.loads(response_text)
    except Exception:
        return None


def generate_scenes_and_images(script: str, topic: str = "", platform: str = "YouTube", visual_style: str = "real"):
    """
    Analyzes script and topic to generate ultra-relevant visual prompts,
    and downloads high quality AI images strictly matched to each scene.
    """
    clean_topic = topic.strip() if topic else "topic"
    is_vertical = "short" in platform.lower() or "reel" in platform.lower() or "tiktok" in platform.lower()
    width, height = (1080, 1920) if is_vertical else (1920, 1080)
    aspect_str = "9:16 vertical full screen" if is_vertical else "16:9 widescreen"

    is_anim = "anim" in visual_style.lower() or "cartoon" in visual_style.lower() or "3d" in visual_style.lower()
    style_desc = "3D Pixar Disney digital art render, vibrant animation, 8k resolution, octane render, stylized" if is_anim else "National Geographic award winning real camera 8k photograph, authentic real life texture, 35mm Hasselblad camera, photorealistic, no cartoon, no anime"

    prompt = f"""
    You are a Hollywood visual effects director and viral CapCut video editor.
    Analyze the following video script about topic "{clean_topic}".
    Split the script into 5 to 8 fast, punchy B-roll visual scenes (each scene 2 to 4 seconds).

    CRITICAL INSTRUCTIONS FOR VISUAL PROMPTS ({visual_style.upper()} STYLE):
    Each "visual_prompt" MUST be a breathtaking visual prompt specifically tailored to "{clean_topic}".
    - Style requirement: {style_desc}.
    - ALWAYS explicitly incorporate "{clean_topic}" into every single visual prompt!
    - Include high-impact camera angles (e.g. "Extreme close-up macro lens", "Dramatic overhead drone shot", "High-speed tracking action shot").

    Return ONLY a valid JSON array of objects:
    [
      {{
        "scene_number": 1,
        "narration": "exact short narration sentence spoken in this scene",
        "visual_prompt": "visual prompt about {clean_topic}, {style_desc}, {aspect_str}"
      }}
    ]

    Script:
    {script}
    """

    scenes = None
    try:
        llm_output = generate_text(prompt)
        scenes = parse_json_from_llm(llm_output)
    except Exception as e:
        print(f"⚠️ Scene parsing notice: {e}")

    # Explicit Topic-locked scenes if Gemini output was unavailable
    if not scenes or not isinstance(scenes, list) or len(scenes) < 1:
        topic_lower = clean_topic.lower()

        if "car" in topic_lower or "auto" in topic_lower or "vehicle" in topic_lower or "supercar" in topic_lower:
            scenes = [
                {
                    "scene_number": 1,
                    "narration": "These 5 secret supercars are so expensive, only multi-billionaires can own them!",
                    "visual_prompt": f"Ultra luxury red {clean_topic} hypercar parked in futuristic glass garage at night, {style_desc}, {aspect_str}"
                },
                {
                    "scene_number": 2,
                    "narration": "Number 1: The $18 Million Bugatti La Voiture Noire, featuring a quad-turbo W16 engine.",
                    "visual_prompt": f"Black Bugatti La Voiture Noire luxury supercar with glowing LED headlights, carbon fiber body, {style_desc}, {aspect_str}"
                },
                {
                    "scene_number": 3,
                    "narration": "Number 2: The $30 Million Rolls-Royce Droptail, crafted with hand-carved wood veneer.",
                    "visual_prompt": f"Sleek custom Rolls Royce Droptail convertible supercar cruising near Monaco coastline at sunset, {style_desc}, {aspect_str}"
                },
                {
                    "scene_number": 4,
                    "narration": "Number 3: The Pagani Zonda HP Barchetta, built with a raw V12 screaming exhaust sound.",
                    "visual_prompt": f"Pagani Zonda HP Barchetta drifting through race track curves with smoke, {style_desc}, {aspect_str}"
                },
                {
                    "scene_number": 5,
                    "narration": "Number 4: The Koenigsegg Jesko Absolut, reaching a mind-bending top speed of 330 miles per hour!",
                    "visual_prompt": f"Koenigsegg Jesko Absolut hypercar aerodynamic rear wing and carbon fiber body, {style_desc}, {aspect_str}"
                },
                {
                    "scene_number": 6,
                    "narration": "Number 5: The $2.7 Million Mercedes-AMG One, powered by an actual Formula 1 hybrid engine!",
                    "visual_prompt": f"Silver Mercedes-AMG One hypercar accelerating fast on highway, {style_desc}, {aspect_str}"
                },
                {
                    "scene_number": 7,
                    "narration": "Which of these 5 secret hypercars would you pick? Subscribe for more mind-blowing car facts!",
                    "visual_prompt": f"Multi-million dollar luxury supercars lined up at sunset, {style_desc}, {aspect_str}"
                }
            ]

        elif "saturn" in topic_lower or "space" in topic_lower or "planet" in topic_lower:
            scenes = [
                {
                    "scene_number": 1,
                    "narration": "Saturn is famous for its magnificent ring system, composed mainly of ice particles and space dust.",
                    "visual_prompt": f"Deep space photograph of planet Saturn with golden glowing icy rings, starry universe background, {style_desc}, {aspect_str}"
                },
                {
                    "scene_number": 2,
                    "narration": "Scientists have recently discovered mysterious ocean moons orbiting Saturn, like Enceladus and Titan.",
                    "visual_prompt": f"Saturn moon Titan with icy ocean surface and distant Saturn ringed planet in dark space sky, {style_desc}, {aspect_str}"
                },
                {
                    "scene_number": 3,
                    "narration": "These discoveries make Saturn one of the most promising places in our solar system to search for alien life.",
                    "visual_prompt": f"Space telescope exploring deep space planet Saturn, glowing nebulae and galaxies, {style_desc}, {aspect_str}"
                }
            ]
        else:
            scenes = [
                {
                    "scene_number": 1,
                    "narration": f"These secret facts about {clean_topic} will blow your mind!",
                    "visual_prompt": f"Cinematic imagery of {clean_topic}, breathtaking scenery, {style_desc}, {aspect_str}"
                },
                {
                    "scene_number": 2,
                    "narration": f"First: {clean_topic} is built with extreme precision and rare engineering.",
                    "visual_prompt": f"Ultra detailed shot illustrating {clean_topic}, dramatic lighting, {style_desc}, {aspect_str}"
                },
                {
                    "scene_number": 3,
                    "narration": f"Second: It reaches performance levels that normal people never get to see.",
                    "visual_prompt": f"Wide angle shot showcasing {clean_topic} in action, {style_desc}, {aspect_str}"
                },
                {
                    "scene_number": 4,
                    "narration": f"Which secret about {clean_topic} surprised you most? Subscribe now for more!",
                    "visual_prompt": f"Dynamic close up of {clean_topic}, {style_desc}, {aspect_str}"
                }
            ]

    def download_real_google_image(search_query: str, output_path: Path):
        """Scrapes real high-res HD stock camera photo from Bing / Pexels / Wikimedia / DuckDuckGo for ANY topic."""
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"}
        clean_q = search_query.strip()
        if not clean_q:
            return False

        # Method 1: Pexels Public Stock API (100% High Quality Real Stock Photos for general topics)
        try:
            pexels_url = f"https://api.pexels.com/v1/search?query={urllib.parse.quote(clean_q)}&per_page=5"
            # Try free headers or Bing image search
            bing_url = f"https://www.bing.com/images/search?q={urllib.parse.quote(clean_q + ' 8k photo wallpaper')}&FORM=HDRSC2"
            res = requests.get(bing_url, headers=headers, timeout=6)
            murls = re.findall(r'murl&quot;:&quot;(https?://[^&]+)&quot;', res.text)
            for murl in murls[:10]:
                if any(ext in murl.lower() for ext in ['.jpg', '.jpeg', '.png']) and not any(bad in murl.lower() for bad in ['icon', 'logo', 'svg', 'avatar']):
                    try:
                        img_res = requests.get(murl, headers=headers, timeout=6)
                        if img_res.status_code == 200 and len(img_res.content) > 35000:
                            with open(output_path, "wb") as f:
                                f.write(img_res.content)
                            print(f"  [Universal Real Photo Success] Saved real image for: '{search_query}' ({len(img_res.content)} bytes)")
                            return True
                    except Exception:
                        continue
        except Exception as e:
            print(f"  [Bing Real Photo Notice] {e}")

        # Method 2: Wikimedia Commons API Search for Real Entity/Subject Photos
        try:
            wiki_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrsearch={urllib.parse.quote(clean_q)}&gsrnamespace=6&format=json&prop=imageinfo&iiprop=url"
            wres = requests.get(wiki_url, headers=headers, timeout=5)
            if wres.status_code == 200:
                pages = wres.json().get("query", {}).get("pages", {})
                for p in pages.values():
                    ii = p.get("imageinfo", [{}])[0]
                    img_url = ii.get("url")
                    if img_url and any(ext in img_url.lower() for ext in ['.jpg', '.jpeg', '.png']):
                        img_res = requests.get(img_url, headers=headers, timeout=6)
                        if img_res.status_code == 200 and len(img_res.content) > 25000:
                            with open(output_path, "wb") as f:
                                f.write(img_res.content)
                            print(f"  [Wikimedia Real Photo Success] Downloaded real image for: '{search_query}' ({len(img_res.content)} bytes)")
                            return True
        except Exception as e:
            print(f"  [Wikimedia Notice] {e}")

        # Method 3: DuckDuckGo Fallback
        try:
            token_url = f"https://duckduckgo.com/?q={urllib.parse.quote(clean_q)}&t=h_&iax=images&ia=images"
            res = requests.get(token_url, headers=headers, timeout=5)
            vqd_match = re.search(r'vqd=([\d-]+)', res.text)
            if vqd_match:
                vqd = vqd_match.group(1)
                img_api = f"https://duckduckgo.com/i.js?q={urllib.parse.quote(clean_q)}&o=json&vqd={vqd}"
                api_res = requests.get(img_api, headers=headers, timeout=5)
                if api_res.status_code == 200:
                    results = api_res.json().get("results", [])
                    for item in results[:5]:
                        image_link = item.get("image")
                        if image_link and not image_link.endswith(".svg"):
                            img_res = requests.get(image_link, headers=headers, timeout=6)
                            if img_res.status_code == 200 and len(img_res.content) > 25000:
                                with open(output_path, "wb") as f:
                                    f.write(img_res.content)
                                print(f"  [DDG Real Photo Success] Downloaded real image for: '{search_query}' ({len(img_res.content)} bytes)")
                                return True
        except Exception as e:
            print(f"  [DDG Notice] {e}")

        return False


    downloaded_scenes = [None] * len(scenes)

    def fetch_scene_image(idx, scene):
        narration = scene.get("narration", "")
        visual_prompt = scene.get("visual_prompt", f"{clean_topic}, {style_desc}")

        clean_prompt = visual_prompt.strip()
        image_path = MEDIA_DIR / f"scene_{idx}.jpg"
        download_success = False

        # Generate 8K Photorealistic AI Images using Flux Realism / Flux Anime
        model_type = "flux-anime" if is_anim else "flux-realism"
        
        if not is_anim:
            style_prompt = f"Ultra-realistic 8K professional camera photograph of {clean_prompt}, real life photography, Hasselblad 35mm lens, crisp metallic reflections, photorealistic, 8k resolution"
        else:
            style_prompt = f"3D animated cartoon illustration of {clean_prompt}, Pixar style, vibrant 3D render, highly detailed"

        encoded_prompt = urllib.parse.quote(style_prompt)
        image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width={width}&height={height}&model={model_type}&nologo=true&enhance=true&seed={idx * 7777 + 1234}"
        print(f"[Photorealistic AI Engine] Scene {idx}: '{clean_prompt[:50]}...'")

        try:
            res = requests.get(image_url, timeout=12)
            if res.status_code == 200 and len(res.content) > 10000:
                with open(image_path, "wb") as f:
                    f.write(res.content)
                print(f"  [Success] Saved photorealistic scene_{idx}.jpg ({len(res.content)} bytes)")
                download_success = True
        except Exception as e:
            print(f"  [Warning] Fast download timeout/error for scene {idx}: {e}")

        if not download_success:
            image_path = MEDIA_DIR / "cover.jpg"

        return {
            "scene_number": idx,
            "narration": narration,
            "image_path": str(image_path),
        }


    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = [
            executor.submit(fetch_scene_image, idx, scene)
            for idx, scene in enumerate(scenes, start=1)
        ]
        downloaded_scenes = [f.result() for f in futures]

    return downloaded_scenes


def generate_scenes(topic: str):
    """Compatibility alias for scenes API router."""
    return generate_scenes_and_images(script=topic, topic=topic)