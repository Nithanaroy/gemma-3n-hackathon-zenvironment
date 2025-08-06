GEMMA_PATH = "models/gemma-3n-transformers-gemma-3n-e2b-it-v2"

from transformers import AutoProcessor, Gemma3nForConditionalGeneration
from PIL import Image
import requests
import torch
import pprint


model = Gemma3nForConditionalGeneration.from_pretrained(
    GEMMA_PATH, 
    device_map="auto", 
    torch_dtype=torch.bfloat16
).eval()

processor = AutoProcessor.from_pretrained(GEMMA_PATH)

ZEN_IMG_PROMPT = (
    "Guide the user into a mindfulness meditation session by choosing two of 3 activities. "
    "based on the image provided, choose activities from this list - "
    "Mindful breathing, Body Scan, Mindful walking, Mindful eating, Mindful meditation, Mindful listening, "
    "Loving kindness meditation (metta), Mindful journaling, Five senses exercise, Daily mindfulness in routing tasks, "
    "Nature listening walk, Five senses scavenger hunt, Cloud watching, Barefoot walk (if safe), Sit spot / tree time, "
    "Breathing with nature, Gratitude circle, Rock balancing, Tree hugging, Nature mandalas. "
    "Be sure to keep it short and playful, use natural curiosity to lead the user into these kid-friendly activities, "
    "allow silence and stillness. Towards the end of the session, invite reflection: "
    "Ask 'What did you notice?' or 'How did that feel?'"
)
ZEN_IMG_PROMPT_v2 = """
Guide the user into a mindfulness meditation session by choosing two of 3 activities.
based on the image provided, choose activities from <activities> block below

<activities>
1. Mindful breathing
   * **Focus:** Awareness of the breath  
   * **How:** Pay attention to each inhale and exhale. Use breath as an anchor to the present moment.  
   * **Use:** Quick stress relief, grounding, meditation base.  
2. Body Scan  
* **Focus:** Physical sensations in the body  
* **How:** Slowly bring awareness to each part of the body, often from head to toe or vice versa.  
* **Use:** Relaxation, tension awareness, sleep preparation.  
3. Mindful walking  
   * **Focus:** Movement and surroundings  
   * **How:** Walk slowly and notice the sensation of each step, your breath, and what you see/hear.  
   * **Use:** Active mindfulness, stress relief during breaks.  
4. Mindful eating  
   * **Focus:** Taste, texture, and experience of eating  
   * **How:** Eat slowly without distractions. Pay attention to each bite and your hunger/fullness cues.  
   * **Use:** Improve relationship with food, eating disorders, digestion awareness.  
5. Mindful meditation   
* **Focus:** Breath, sounds, sensations, or thoughts  
* **How:** Sit or lie still and observe whatever arises without judgment. Can be guided or unguided.  
* **Use:** Long-term mindfulness practice, emotional regulation.  
6. Mindful listening   
* **Focus:** Sound and presence with others  
* **How:** Give full attention to someone speaking without planning your response. Listen without judgment.  
* **Use:** Improve communication, deepen relationships.  
7. Loving kindness meditation (metta)  
* **Focus:** Cultivating compassion  
* **How:** Silently repeat phrases wishing yourself and others well-being and peace.  
* **Use:** Reduce anger, improve empathy, self-love.  
8. Mindful journaling   
* **Focus:** Thoughts and emotions  
* **How:** Write with full awareness of your feelings, often using prompts.  
* **Use:** Emotional processing, insight development.  
9. Five senses exercise  
* **Focus:** Grounding through the senses  
* **How:** Notice 5 things you can see, 4 you can feel, 3 you can hear, 2 you can smell, 1 you can taste.  
* **Use:** Grounding during anxiety, panic attacks.  
10. Daily mindfulness in routing tasks   
* **Focus:** Everyday moments  
* **How:** Bring full attention to routine activities (e.g., brushing teeth, washing dishes).  
* **Use:** Build habitual mindfulness, integrate it into daily life.  
11. Nature listening walk  
    * **How:** Walk slowly in silence. Ask the kids to listen carefully to the sounds around them (birds, wind, leaves, bugs).  
    * **Goal:** Develop auditory awareness and presence.  
12. Five senses scavenger hunt  
* **How:** Ask them to find:  
  * 5 things they can see  
  * 4 things they can touch  
  * 3 things they can hear  
  * 2 things they can smell  
  * 1 thing they can (safely) taste  
* **Goal:** Grounding, sensory awareness.  
13. Cloud watching   
* **How:** Lie on the grass and watch clouds move. Ask what shapes or images they see.  
* **Goal:** Imagination, relaxation, attention to the present.  
14. Barefoot walk (if safe)  
* **How:** Let kids take off their shoes and walk on grass, sand, or earth, paying attention to how it feels.  
* **Goal:** Tactile awareness, connection with nature.  
15. Sit spot / tree time  
* **How:** Choose a quiet outdoor spot (e.g., under a tree). Sit silently for 5–10 minutes and observe what's happening (bugs, leaves, sounds).  
* **Goal:** Stillness, observation, patience.  
16. Breathing with nature   
* **How:** Find a leaf, feather, or dandelion seed. Hold it and breathe slowly so it moves gently. You can also try "blowing the wind" with deep breaths.  
* **Goal:** Calm breathwork with visual feedback.  
17. Gratitude circle   
* **How:** Sit in a circle and take turns sharing one thing they’re grateful for in nature.  
* **Goal:** Cultivating positive emotions and mindfulness in speech.  
18. Rock balancing  
* **How:** Ask kids to find and balance small rocks on top of each other. It takes still hands and focus.  
* **Goal:** Concentration, patience, body control.  
19. Tree hugging   
* **How:** Have each child hug a tree and feel its bark. Encourage them to close their eyes and breathe deeply.

* **Goal:** Sensory experience and emotional grounding.  
20. Nature mandalas  
* **How:** Collect leaves, twigs, petals, and stones. Create a circular mandala pattern on the ground.  
* **Goal:** Mindful creativity, focus, and appreciation for impermanence.
</activities>

Ensure that all the activities have these characteristics

1. **Keep it short and playful:** Especially for younger kids (5-10 minutes is plenty).
2. **Use natural curiosity:** Let kids lead in observing or describing.
3. **Allow silence and stillness:** Kids may be fidgety at first — that's okay.
4. **Model mindfulness:** Show your own calm presence and curiosity.

**Invite reflection:** Ask "What did you notice?" or "How did that feel?"
"""

def call_gemma(message, image_path=None, conversation_history=[]):

    messages = [
        {
            "role": "system",
            "content": [{"type": "text", "text": "You are a helpful assistant."}]
        },
        {
            "role": "user",
            "content": [
                {"type": "image", "image": image_path},
                {"type": "text", "text": message}
            ]
        }
    ]
    
    print("Calling Gemma with the following messages:")
    pprint(messages)

    inputs = processor.apply_chat_template(
        messages,
        add_generation_prompt=True,
        tokenize=True,
        return_dict=True,
        return_tensors="pt",
    ).to(model.device, dtype=torch.bfloat16)

    input_len = inputs["input_ids"].shape[-1]

    with torch.inference_mode():
        generation = model.generate(**inputs, max_new_tokens=1024, do_sample=False)
        generation = generation[0][input_len:]

    decoded = processor.decode(generation, skip_special_tokens=True)
    
    return decoded