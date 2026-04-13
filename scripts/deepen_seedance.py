"""Insert a deepening block into each existing Seedance post before the
'When to use something else' section. Adds a Step-by-step walkthrough,
a troubleshooting table, and a cross-link to the new Seedance 2.0 cluster.
"""
import os, re

BLOG = os.path.join(os.path.dirname(__file__), '..', 'public', 'blog')

def block(step_title, steps_html, trouble_rows, hub_line):
    rows = ''.join(f'<tr><td>{s}</td><td>{c}</td><td>{fx}</td></tr>' for s,c,fx in trouble_rows)
    return (
        f'<h2>{step_title}</h2>'
        f'<ol>{steps_html}</ol>'
        f'<h2>Troubleshooting table</h2>'
        f'<table><thead><tr><th>Symptom</th><th>Likely cause</th><th>Fix</th></tr></thead>'
        f'<tbody>{rows}</tbody></table>'
        f'<p>{hub_line}</p>'
    )

def steps(*items):
    return ''.join(f'<li>{i}</li>' for i in items)

POSTS = {
'better-prompts-seedance.html': block(
    'Step by step: build a Seedance prompt that works',
    steps(
        '<strong>Write one subject sentence.</strong> "A red fox walks through tall grass at dawn." Keep it under 15 words. No adjectives yet.',
        '<strong>Add one camera instruction.</strong> "Camera slowly dollies left as the fox moves forward." One camera move per clip.',
        '<strong>Add one lighting line.</strong> "Warm golden-hour backlight, long shadows, soft haze." Lighting sells the shot more than detail words.',
        '<strong>Add one motion-intensity cue.</strong> "Gentle motion, natural pace." Tells Seedance not to overdrive the scene.',
        '<strong>Generate at low resolution first.</strong> Use draft quality to test the idea. Only re-render at full quality once the shot looks right.',
        '<strong>Revise one element at a time.</strong> If lighting is wrong, only change the lighting line. Changing three things at once makes it impossible to tell what helped.',
    ),
    [
        ('Subject drifts or morphs mid-clip', 'Prompt has too many competing descriptors', 'Cut to one subject sentence. Move style details to a separate style line.'),
        ('Camera moves too fast', 'Generic camera verb without qualifier', 'Use "slowly dollies" or "gently pans" — add a speed word.'),
        ('Scene feels flat', 'No lighting direction', 'Add time of day + light source ("late afternoon side light").'),
        ('Output is overly busy', 'Too many objects in the prompt', 'Remove background elements. Seedance handles 1-2 subjects well, 5+ badly.'),
    ],
    'For the full beginner workflow, read the <a href="/blog/seedance-2-tutorial-beginner">Seedance 2.0 beginner tutorial</a>. For motion-specific fixes, see <a href="/blog/seedance-2-motion-intensity-settings">motion intensity settings</a>.'
),

'consistent-characters-seedance.html': block(
    'Step by step: keep a character consistent across clips',
    steps(
        '<strong>Build one reference sheet first.</strong> Use Midjourney or Dreamina to create a front, 3/4, and side view of the character on a neutral background.',
        '<strong>Upload the cleanest view as the reference image.</strong> 3/4 angle usually works best — it carries face and body proportions.',
        '<strong>Write a short character description.</strong> "Woman, late 20s, shoulder-length black hair, grey linen jacket." Reuse this exact string across every clip prompt.',
        '<strong>Generate each shot in the same session.</strong> Seedance holds some context across one session. Opening a new tab resets it.',
        '<strong>Check the first frame.</strong> If the character looks right at frame 1, the rest of the clip usually holds. If frame 1 is already wrong, regenerate — do not wait.',
        '<strong>Lock lighting across clips.</strong> "Soft overcast daylight" used in every prompt gives more visual continuity than changing light per shot.',
    ),
    [
        ('Face changes between clips', 'Reference image not uploaded on the second clip', 'Re-upload the same reference for every new generation.'),
        ('Outfit colour shifts', 'Colour word is vague ("dark jacket")', 'Name the exact colour ("charcoal grey jacket").'),
        ('Character ages or changes gender', 'Description missing key anchor words', 'Always include age range and one distinctive feature.'),
        ('Same prompt gives different faces', 'Seed varies each run', 'Lock the seed if your interface exposes it. Otherwise generate 3 takes and pick the closest.'),
    ],
    'For reference-image prep, read <a href="/blog/consistent-characters-seedance">Seedance reference images for characters</a>. For the full lip-sync workflow on a consistent character, see <a href="/blog/seedance-2-lip-sync-talking-head">Seedance 2.0 lip-sync and talking heads</a>.'
),

'fix-bad-motion-seedance.html': block(
    'Step by step: diagnose bad motion in one minute',
    steps(
        '<strong>Watch the clip at 0.25x speed.</strong> Most motion problems are invisible at full speed. Slow it down and the glitch becomes obvious.',
        '<strong>Name the problem in one word.</strong> Jitter, warp, drift, stutter, or overshoot. Each has a different fix.',
        '<strong>Check motion intensity first.</strong> If it is above 60, drop to 35-45. Most "bad motion" is just too much motion.',
        '<strong>Read your prompt for verbs.</strong> "Runs, leaps, spins" all stack. Keep one action verb per clip.',
        '<strong>Shorten the clip.</strong> 5 seconds is more stable than 10. Seedance drifts on longer clips — cut and concatenate instead.',
        '<strong>Re-generate with the same prompt.</strong> Seedance is non-deterministic. Sometimes the fix is just another seed.',
    ),
    [
        ('Subject jitters frame-to-frame', 'Motion intensity too high for the scene', 'Drop intensity to 25-40 for talking heads, 40-60 for walking.'),
        ('Face warps mid-clip', 'No reference image or unclear face', 'Add a reference image. Cap motion intensity at 35.'),
        ('Background drifts unrealistically', 'Camera move not specified', 'Add "static camera" or "locked camera" to the prompt.'),
        ('Limbs duplicate or merge', 'Prompt has multiple action verbs', 'Use one verb. Generate a second clip for the second action.'),
    ],
    'For motion intensity reference, see <a href="/blog/seedance-2-motion-intensity-settings">motion intensity 0-100 explained</a>. For the full beginner workflow, read the <a href="/blog/seedance-2-tutorial-beginner">Seedance 2.0 beginner tutorial</a>.'
),

'seedance-anime-video.html': block(
    'Step by step: generate clean anime-style clips',
    steps(
        '<strong>Start the prompt with a style tag.</strong> "Anime style, cel-shaded, 2D animation look" — Seedance needs this upfront.',
        '<strong>Name a specific aesthetic.</strong> "Studio Ghibli warmth" or "90s shonen" beats a generic "anime". The model locks onto named styles better.',
        '<strong>Keep the scene simple.</strong> One or two characters, one action, one background. Anime models drift fast with crowded scenes.',
        '<strong>Limit camera motion.</strong> Anime sequences use held frames and pans, not complex dolly moves. "Slow pan right" is usually enough.',
        '<strong>Use 24 fps, 5 seconds.</strong> Anime feels wrong at 30+ fps. Short clips let you assemble a real sequence in an editor.',
        '<strong>Stack two clips for dialogue.</strong> Generate one clip per speaker. Cut in an editor instead of asking Seedance for two talking characters.',
    ),
    [
        ('Output looks 3D not 2D', 'Style tag missing or too vague', 'Lead with "cel-shaded 2D anime, flat colour".'),
        ('Face has too much realism', 'Reference image is photo-real', 'Use an anime reference sheet or skip references entirely.'),
        ('Lines flicker between frames', 'High motion intensity', 'Drop to 25-35. Anime tolerates less motion than live-action.'),
        ('Colours wash out', 'No colour direction in prompt', 'Add "saturated colours, strong contrast".'),
    ],
    'For the full Seedance workflow, start with the <a href="/blog/seedance-2-tutorial-beginner">beginner tutorial</a>. For export settings that suit anime, see <a href="/blog/seedance-2-resolution-export-settings">resolution and export settings</a>.'
),

'seedance-audio-prompts.html': block(
    'Step by step: write audio-aware prompts',
    steps(
        '<strong>Separate the audio line from the visual line.</strong> "Visual: a chef slicing vegetables. Audio: rhythmic knife chops, kitchen ambience." Seedance handles split prompts better than blended ones.',
        '<strong>Name one ambient layer.</strong> "Coffee shop hum" or "rain on window". One layer is clean; three layers fight each other.',
        '<strong>Name one foreground sound.</strong> Footsteps, a bell, a laugh — the sound the viewer should notice.',
        '<strong>Avoid dialogue in the prompt.</strong> Seedance does not generate clean speech. Generate the visual and add dialogue in post.',
        '<strong>Match sound timing to motion.</strong> If the clip is 5 seconds, describe a 5-second audio event ("a single door slam at the 3-second mark").',
        '<strong>Export at 48kHz for editing.</strong> Keeps sync accurate when you layer in extra audio later.',
    ),
    [
        ('Audio feels disconnected from visual', 'Prompt described visual only', 'Add an explicit audio line.'),
        ('Ambient sound drowns out the action', 'Ambient layer too dominant in prompt', 'Describe ambient as "quiet" or "low". Foreground sound should be the main descriptor.'),
        ('Dialogue sounds garbled', 'Seedance cannot do clean dialogue', 'Record voiceover separately and layer in an editor.'),
        ('Sync drifts by the end of the clip', 'Clip length above 8 seconds', 'Keep clips to 5-6 seconds.'),
    ],
    'For the beginner workflow, start with the <a href="/blog/seedance-2-tutorial-beginner">Seedance 2.0 tutorial</a>. For lip-sync specifically, see <a href="/blog/seedance-2-lip-sync-talking-head">lip-sync and talking heads</a>.'
),

'seedance-cinematic-camera-movement.html': block(
    'Step by step: direct the camera like a cinematographer',
    steps(
        '<strong>Pick one camera move per clip.</strong> Dolly, pan, tilt, orbit, push-in, pull-out — never combine.',
        '<strong>Add a speed word.</strong> "Slowly dollies in" works. Just "dollies in" runs too fast.',
        '<strong>Name the subject of the move.</strong> "Camera orbits the subject clockwise" — Seedance needs to know what to circle.',
        '<strong>Specify the start and end framing.</strong> "Starts on a wide shot, ends on a medium close-up." The model uses this to plan the motion arc.',
        '<strong>Keep subject motion low during camera moves.</strong> A running character plus a fast dolly becomes chaos. Pin one element still.',
        '<strong>Generate 3 takes.</strong> Camera moves vary run to run. Pick the cleanest and re-render at full quality.',
    ),
    [
        ('Camera jitters during the move', 'Motion intensity too high', 'Drop to 30-45 for camera-led clips.'),
        ('Move goes the wrong direction', 'Ambiguous direction word', 'Use "left-to-right" or "clockwise" — not just "across".'),
        ('Subject goes off-frame mid-move', 'No end-frame direction', 'Tell the model where to end ("ends with subject centred in frame").'),
        ('Move is too fast to read', 'No speed qualifier', 'Add "slowly" or "gradually" to every camera verb.'),
    ],
    'For a broader look at motion settings, see <a href="/blog/seedance-2-motion-intensity-settings">motion intensity 0-100 explained</a>. To start from scratch, read the <a href="/blog/seedance-2-tutorial-beginner">beginner tutorial</a>.'
),

'seedance-dreamina-guide.html': block(
    'Step by step: generate your first clip in Dreamina',
    steps(
        '<strong>Sign in at dreamina.capcut.com.</strong> Free tier gives you a credit pool to test.',
        '<strong>Click "Video" in the top nav.</strong> Dreamina separates Image and Video tools — Seedance lives under Video.',
        '<strong>Open the model dropdown.</strong> Select "Seedance 2.0". If you see only "Seedance 1", your region may not have 2.0 yet — wait a day and retry.',
        '<strong>Paste a prompt and pick aspect ratio.</strong> 16:9 for YouTube, 9:16 for Reels/Shorts, 1:1 for feed posts.',
        '<strong>Set duration and motion intensity.</strong> Start at 5 seconds and intensity 40 for your first clip.',
        '<strong>Click Generate and wait.</strong> Expect 60-90 seconds per clip. Do not refresh — Dreamina resumes in the background if you close the tab.',
    ),
    [
        ('Seedance 2.0 not in the dropdown', 'Regional rollout', 'Refresh, check again in 24h. Fall back to Seedance 1 for now.'),
        ('Credits deplete too fast', 'Generating at full quality for every test', 'Test at draft quality first, re-render at full only for final takes.'),
        ('Generation fails silently', 'Prompt flagged by content filter', 'Remove brand names, real people, and graphic descriptors.'),
        ('Video downloads without audio', 'Audio was not enabled in settings', 'Toggle "Include audio" before generating.'),
    ],
    'For the full beginner workflow, read the <a href="/blog/seedance-2-tutorial-beginner">Seedance 2.0 tutorial</a>. For account and first-run setup, see <a href="/blog/how-to-setup-seedance">how to set up Seedance</a>.'
),

'seedance-image-to-video.html': block(
    'Step by step: turn one image into a clean video',
    steps(
        '<strong>Pick a source image with clear focal depth.</strong> A portrait with soft background works better than a flat landscape.',
        '<strong>Crop to your target aspect ratio before uploading.</strong> 16:9 for YouTube, 9:16 for Shorts. Seedance will not recrop cleanly.',
        '<strong>Upload as the reference image.</strong> In Dreamina, drag into the "Reference" slot — not the prompt box.',
        '<strong>Write a motion prompt, not a scene prompt.</strong> "The woman slowly turns her head to the left" beats re-describing the whole image.',
        '<strong>Cap motion intensity at 40.</strong> Image-to-video is most stable below 50. Above 60, faces warp.',
        '<strong>Generate 5 seconds first.</strong> Longer clips drift further from the reference.',
    ),
    [
        ('Output looks nothing like the reference', 'Reference slot not used', 'Make sure the image went into the reference slot, not the prompt.'),
        ('Face warps halfway through', 'Motion intensity too high', 'Drop to 30-35 for face-centric clips.'),
        ('Background moves but subject stands still', 'Prompt described scene, not subject motion', 'Rewrite prompt to describe what the subject does.'),
        ('Aspect ratio changes unexpectedly', 'Uploaded a different ratio', 'Pre-crop the image to match your target ratio.'),
    ],
    'For aspect ratio and export rules, see <a href="/blog/seedance-2-resolution-export-settings">resolution and export settings</a>. For character consistency across multiple clips, see <a href="/blog/consistent-characters-seedance">reference images for characters</a>.'
),

'seedance-marketing-videos.html': block(
    'Step by step: produce a 15-second marketing clip',
    steps(
        '<strong>Write the hook first.</strong> The opening 2 seconds need to stop the scroll. "Your coffee is lying to you." — specific, surprising.',
        '<strong>Describe the product shot.</strong> One clean clip of the product. "Close-up of a matte black coffee bag rotating slowly on a marble surface, soft side light."',
        '<strong>Describe the benefit shot.</strong> One clip of the payoff. "A person pours coffee into a white cup, steam rising, warm morning window light."',
        '<strong>Keep each clip 5 seconds.</strong> Three 5-second clips edit cleanly into a 15-second ad.',
        '<strong>Generate each clip separately.</strong> Do not ask Seedance for a 3-shot sequence in one prompt — it will blur the shots.',
        '<strong>Cut in an editor with one text overlay and one CTA.</strong> Hook, product, CTA — nothing else.',
    ),
    [
        ('Ad feels generic', 'Prompt described product without context', 'Add a specific setting and lighting direction.'),
        ('Product looks fake or plasticky', 'No material word in prompt', 'Name the material ("matte paper", "brushed metal").'),
        ('Motion distracts from the product', 'Intensity above 50', 'Drop to 25-35 for product shots.'),
        ('CTA gets ignored', 'Too much motion in the final clip', 'End on a held frame — Seedance will hold if you add "final frame static".'),
    ],
    'For a product-ad-specific walkthrough, see <a href="/blog/seedance-product-ad-videos">Seedance product ad videos</a>. For the pricing breakdown of running weekly ads, see <a href="/blog/seedance-2-pricing-credits">Seedance 2.0 pricing and credits</a>.'
),

'seedance-product-ad-videos.html': block(
    'Step by step: shoot a product in Seedance',
    steps(
        '<strong>Pick one hero angle.</strong> 3/4 front works for most products. Profile for bottles, top-down for food.',
        '<strong>Describe the surface.</strong> "Polished concrete", "weathered oak", "white seamless" — surface sells context.',
        '<strong>Name the light source.</strong> "Soft key light from camera left, subtle rim light from behind." This is the single biggest quality lever.',
        '<strong>Pick one slow camera move.</strong> Orbit, push-in, or reveal. Not all three.',
        '<strong>Hold for the last second.</strong> Add "final frame static, product centred" so the clip ends on a clean hero shot.',
        '<strong>Generate 3 takes and pick the sharpest.</strong> Product shots live or die on sharpness; always A/B.',
    ),
    [
        ('Product looks toy-like', 'No scale reference', 'Add a hand, a surface detail, or a lit-by-light description.'),
        ('Labels look garbled', 'Seedance struggles with text', 'Add label in post. Do not expect clean product text from the model.'),
        ('Reflections look wrong', 'No environment description', 'Add "reflects a soft studio environment" or similar.'),
        ('Background upstages the product', 'Background too busy in prompt', 'Use "clean seamless background" or "shallow depth of field".'),
    ],
    'For broader ad production, see <a href="/blog/seedance-marketing-videos">Seedance marketing videos</a>. For resolution and export settings, see <a href="/blog/seedance-2-resolution-export-settings">export settings</a>.'
),

'consistent-characters-seedance.html': block(
    'Step by step: build a reference image a model can actually use',
    steps(
        '<strong>Shoot or generate three angles.</strong> Front, 3/4, side. Same lighting, same background, same clothes.',
        '<strong>Use a neutral background.</strong> Grey or off-white. Busy backgrounds leak into the generated scene.',
        '<strong>Crop tight on the character.</strong> The model latches onto the subject, not the frame.',
        '<strong>Save at 1024x1024 or 1024x1536.</strong> Larger is not better — Seedance downsamples anyway.',
        '<strong>Upload the 3/4 angle as the primary reference.</strong> It carries the most information about face and body.',
        '<strong>Reuse the exact same reference for every clip in the series.</strong> New reference = new character. Continuity dies the moment you swap.',
    ),
    [
        ('Character changes between clips', 'Swapped reference or uploaded nothing', 'Always reuse the same 3/4 reference.'),
        ('Outfit drifts', 'Outfit not described in prompt', 'Reuse the exact outfit description string across every clip.'),
        ('Face softens over the clip', 'Motion intensity above 45', 'Cap at 35 for face-forward shots.'),
        ('Reference image is ignored', 'Uploaded into prompt box instead of reference slot', 'Always use the dedicated reference slot.'),
    ],
    'For the consistency-across-clips workflow, see <a href="/blog/consistent-characters-seedance">consistent characters in Seedance</a>. For lip-sync on a consistent character, see <a href="/blog/seedance-2-lip-sync-talking-head">lip-sync and talking heads</a>.'
),

'seedance-vs-kling.html': block(
    'Step by step: decide between Seedance 2.0 and Kling',
    steps(
        '<strong>Pick your primary use case.</strong> Talking heads: Seedance. Wide cinematic establishing shots: Kling.',
        '<strong>Test the same prompt on both.</strong> Use a fixed prompt and compare the first generation from each. Do not cherry-pick.',
        '<strong>Check credit cost per 5s clip.</strong> Seedance 2.0 is usually cheaper per clip for the same resolution.',
        '<strong>Check motion handling.</strong> Kling tends to produce larger camera moves; Seedance holds subjects more stable.',
        '<strong>Check aspect ratio support.</strong> Both do 16:9 and 9:16 cleanly. 1:1 varies — test before committing.',
        '<strong>Pick one and stick with it for a week.</strong> Switching tools mid-project wastes more time than either tool saves.',
    ),
    [
        ('Kling output too shaky', 'Kling default motion too high', 'Drop intensity or switch to Seedance for that clip.'),
        ('Seedance subject feels locked', 'Seedance prefers stability', 'Add explicit motion words or switch to Kling for wide dynamic shots.'),
        ('Burning credits too fast', 'Testing at full quality', 'Always test at draft quality first.'),
        ('Cannot pick', 'Both are close on your use case', 'Pick the cheaper one for that month. Revisit next month.'),
    ],
    'For a full pricing breakdown on Seedance, see <a href="/blog/seedance-2-pricing-credits">Seedance 2.0 pricing and credits</a>. For the full beginner workflow, read the <a href="/blog/seedance-2-tutorial-beginner">beginner tutorial</a>.'
),

'seedance-vs-sora-2.html': block(
    'Step by step: decide between Seedance 2.0 and Sora 2',
    steps(
        '<strong>Check access.</strong> Sora 2 is gated behind ChatGPT Pro/Plus in many regions. Seedance is open via Dreamina.',
        '<strong>Check cost per clip.</strong> Sora 2 is bundled into a Pro sub. Seedance is credit-based. For heavy use, Sora can be cheaper; for light use, Seedance is.',
        '<strong>Check physical realism.</strong> Sora 2 still leads on physics (water, cloth, crowds). Seedance closes the gap on portraits and product shots.',
        '<strong>Check prompt control.</strong> Seedance responds more predictably to direct camera instructions. Sora interprets more loosely.',
        '<strong>Test one hard prompt on both.</strong> Something with motion, lighting, and a subject. Compare the first unedited take.',
        '<strong>Pick based on which failed less.</strong> Not which looked best on cherry-picked demos.',
    ),
    [
        ('Sora output feels overproduced', 'Prompt was generic', 'Add constraints: aspect, lighting, one action.'),
        ('Seedance looks flatter than Sora', 'No lighting direction in prompt', 'Add time-of-day and light-source direction.'),
        ('Credit burn too high on Seedance', 'Generating at full quality repeatedly', 'Draft first, final only once.'),
        ('Cannot decide', 'Use case overlaps both', 'Pick the one you already have access to. Switching tools wastes a week.'),
    ],
    'For the pricing and credits breakdown, see <a href="/blog/seedance-2-pricing-credits">Seedance 2.0 pricing and credits</a>. For the beginner workflow, read the <a href="/blog/seedance-2-tutorial-beginner">beginner tutorial</a>.'
),

'seedance-vs-veo-3.html': block(
    'Step by step: decide between Seedance 2.0 and Veo 3',
    steps(
        '<strong>Check audio needs.</strong> Veo 3 generates synced audio. Seedance audio is improving but still behind. If audio matters, start with Veo 3.',
        '<strong>Check access and cost.</strong> Veo 3 runs via Google (Vertex, Flow). Seedance runs via Dreamina. Pricing models differ — compare per finished minute, not per generation.',
        '<strong>Check prompt specificity.</strong> Seedance honours explicit camera and lighting instructions more literally. Veo 3 interprets more creatively.',
        '<strong>Run a same-prompt test.</strong> Pick a prompt with a subject, a light source, and a camera move. Compare both outputs unedited.',
        '<strong>Measure revision count.</strong> The tool that needs fewer re-rolls wins for that use case, even if each individual clip looks worse.',
        '<strong>Commit for a month.</strong> Switching tools every other project costs more than the quality gap.',
    ),
    [
        ('Veo audio drowns out the visual', 'Prompt was audio-heavy', 'Rewrite with visual direction first, audio as a short line.'),
        ('Seedance clip has no audio', 'Audio not enabled', 'Toggle audio in Dreamina generation settings.'),
        ('Veo over-interprets the prompt', 'Too vague', 'Add constraints: aspect, duration, lighting, camera.'),
        ('Hit a cost wall', 'Testing at full fidelity', 'Always start at draft quality.'),
    ],
    'For the pricing breakdown, see <a href="/blog/seedance-2-pricing-credits">Seedance 2.0 pricing and credits</a>. For the audio-side of Seedance, see <a href="/blog/seedance-audio-prompts">Seedance audio prompts</a>.'
),

'seedance-youtube-shorts.html': block(
    'Step by step: ship a Seedance-made YouTube Short',
    steps(
        '<strong>Set aspect to 9:16 from the start.</strong> Generating in 16:9 and cropping loses the subject off-frame.',
        '<strong>Hook in the first 1.5 seconds.</strong> The clip needs to start with motion, not a held frame. "A red door swings open" beats "a red door".',
        '<strong>Keep each clip 5 seconds.</strong> Three 5-second clips edit into a 15-second Short cleanly.',
        '<strong>Design for sound-off.</strong> Most Shorts play muted. Make sure the visual tells the story alone.',
        '<strong>Add one-line captions per clip.</strong> Use your editor, not Seedance. Seedance text rendering is unreliable.',
        '<strong>End on a held frame with a CTA overlay.</strong> "Follow for more" on a clean final frame converts better than a CTA mid-motion.',
    ),
    [
        ('Subject gets cropped in the middle', 'Generated in 16:9, cropped to 9:16', 'Always generate in 9:16 directly.'),
        ('Scroll-through rate is bad', 'Opening frame is static', 'Start every clip with motion.'),
        ('Audio is out of sync after editing', 'Clips at different frame rates', 'Lock all clips to 24 fps or 30 fps.'),
        ('CTA gets ignored', 'Moved during CTA frame', 'End with "final frame static".'),
    ],
    'For the full export and aspect reference, see <a href="/blog/seedance-2-resolution-export-settings">resolution and export settings</a>. For the beginner workflow, read the <a href="/blog/seedance-2-tutorial-beginner">tutorial</a>.'
),
}

ANCHOR = '<h2>When to use something else</h2>'

def main():
    for slug, content in POSTS.items():
        path = os.path.join(BLOG, slug)
        html = open(path, encoding='utf-8').read()
        if content in html:
            print(f'SKIP {slug}: already inserted')
            continue
        if ANCHOR not in html:
            print(f'MISS {slug}: anchor not found')
            continue
        new_html = html.replace(ANCHOR, content + ANCHOR, 1)
        open(path, 'w', encoding='utf-8').write(new_html)
        print(f'OK   {slug}')

if __name__ == '__main__':
    main()
