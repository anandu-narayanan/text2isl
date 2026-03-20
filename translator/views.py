from django.shortcuts import render
from django.http import JsonResponse
import json
import os
import re
from django.conf import settings
from .nlp_utils import process_text_to_isl

def get_glossary_mapping():
    words_dir = os.path.join(settings.BASE_DIR, 'static', 'sign_assets', 'words')
    glossary_mapping = {}
    if os.path.exists(words_dir):
        for filename in os.listdir(words_dir):
            if filename.endswith(".mp4"):
                base = filename.rsplit('.', 1)[0]
                base_clean = re.sub(r'\(.*?\)', '', base)
                parts = [p.strip().lower() for p in base_clean.split(',')]
                for p in parts:
                    if p:
                        glossary_mapping[p] = filename
    return glossary_mapping

def index(request):
    return render(request, 'translator/index.html')

def dictionary(request):
    mapping = get_glossary_mapping()
    # Unique videos, distinct by filename
    videos_dict = {}
    for word, file in mapping.items():
        if file not in videos_dict:
            videos_dict[file] = []
        videos_dict[file].append(word)
    
    # Sort for display
    sorted_videos = []
    for f in sorted(videos_dict.keys()):
        words = ", ".join(videos_dict[f])
        sorted_videos.append({'file': f, 'words': words, 'url': f'/static/sign_assets/words/{f}'})
        
    return render(request, 'translator/dictionary.html', {'videos': sorted_videos})

def translate_api(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            text = data.get('text', '')
            fallback = data.get('fallback', 'skip')
            use_ai = data.get('use_ai', False)
            
            if not text:
                return JsonResponse({'error': 'No text provided'}, status=400)
                
            glosses = process_text_to_isl(text, use_ai=use_ai)
            
            # Map glosses to assets
            assets = []
            
            # Target directories where assets are stored
            words_dir = os.path.join(settings.BASE_DIR, 'static', 'sign_assets', 'words')
            letters_dir = os.path.join(settings.BASE_DIR, 'static', 'sign_assets', 'letters')
            
            # Use shared helper function to get mapping
            glossary_mapping = get_glossary_mapping()
            
            for gloss in glosses:
                gloss_lower = gloss.lower()
                found = False
                
                # Further fallback: maybe gloss matches exactly
                if gloss_lower in glossary_mapping:
                    assets.append({
                        'type': 'word',
                        'gloss': gloss,
                        'url': f'/static/sign_assets/words/{glossary_mapping[gloss_lower]}'
                    })
                    found = True
                else:
                    # Partial match e.g. gloss="you" and key="you, your"
                    for key, filename in glossary_mapping.items():
                        if key == gloss_lower:
                            assets.append({
                                'type': 'word',
                                'gloss': gloss,
                                'url': f'/static/sign_assets/words/{filename}'
                            })
                            found = True
                            break
                            
                if not found:
                    if fallback == 'spell':
                        spelled = []
                        for char in gloss:
                            if char.isalpha():
                                char_lower = char.lower()
                                spelled.append({
                                    'type': 'letter',
                                    'char': char_lower,
                                    'url': f'/static/sign_assets/letters/{char_lower}.png'
                                })
                        if spelled:
                            assets.append({
                                'type': 'spelled',
                                'gloss': gloss,
                                'letters': spelled
                            })
                    elif fallback == 'message':
                        assets.append({
                            'type': 'message',
                            'gloss': gloss,
                            'message': f'"{gloss.capitalize()}" is missing from the dataset.'
                        })
                    
            return JsonResponse({'glosses': glosses, 'assets': assets})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
            
    return JsonResponse({'error': 'Invalid request method'}, status=405)
