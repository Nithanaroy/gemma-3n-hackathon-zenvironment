import gradio as gr

# from gemma_server import call_gemma

def generate_mindfulness_activities(description, audio, image):
    """
    Stub method that processes user inputs and generates personalized
    mindfulness activities. In the future, this will call the actual Gemma model.
    """
    # Process inputs
    inputs_info = []
    
    if description and description.strip():
        inputs_info.append(f"Text description: {description}")
    
    if audio:
        inputs_info.append(f"Audio file uploaded: {audio}")
    
    if image:
        inputs_info.append(f"Image uploaded: {image}")
    
    # Generate stub response based on inputs
    response = "### 🌟 Personalized Mindfulness Session\n\n"
    
    if inputs_info:
        response += "Based on your inputs:\n"
        for info in inputs_info:
            response += f"- {info}\n"
        response += "\n"
    
    response += """### 🧘‍♀️ Let's start with mindful breathing
- Take a moment to settle into your current environment
- Bring awareness to your body and breath
- Pay attention to each inhale and exhale
- Continue this for a few more breaths

### 🔍 Nature connection exercise
- Look around and observe the natural elements you mentioned
- Find 4 things that you can touch and feel safely
- Listen for 3 different sounds in your environment
- Notice 2 different scents around you
- If safe, find 1 thing you can taste (like fresh air or mint)

### 🎯 Reflection moment
- How does this environment make you feel?
- What do you appreciate most about this moment?
- Take three deep breaths before completing the session"""
    
    return response



def create_input_screen():
    with gr.Column(visible=True, elem_id="input_row") as input_row:
        gr.Markdown("*Welcome to Zenvironment, a place to recharge in nature with your family.*")
        gr.Markdown("Tell me about your surroundings and how you would like to recharge.")

        description = gr.Textbox(
            placeholder="Share a photo / audio / text description to start your mindfulness session...",
            label="Description"
        )
        with gr.Row():
            audio = gr.Audio(type="filepath", label="Upload Audio (Optional)")
            image = gr.Image(type="filepath", label="Upload Image (Optional)")

        start_button = gr.Button("Start Session")

    return input_row, description, audio, image, start_button


def create_activities_screen():
    with gr.Column(visible=False, elem_id="activity_column") as activity_column:
        activities_content = gr.Markdown("""
        ### 🧘‍♀️ We will start with some mindful breathing
        - Bring awareness to your body and breath
        - Pay attention to each inhale and exhale
        - Continue this for a few more breaths

        ### 🔍 Next, we will perform the 5 senses scavenger hunt
        - Observe the creations of nature that you see around you
        - Find 4 things that you can touch and feel
        - Find 3 things you can hear
        - 2 things that you can smell
        - 1 thing that you can taste safely
        """)

        complete_button = gr.Button("Activities complete")

    return activity_column, activities_content, complete_button


def create_feedback_drawer():
    with gr.Column(visible=False, elem_id="feedback_drawer") as feedback_drawer:
        gr.Markdown("### ✅ Session complete\nHow do you feel after this session?")
        with gr.Row():
            better_btn = gr.Button("😊 I feel better", variant="primary")
            same_btn = gr.Button("🥱 I feel the same or no better")

    return feedback_drawer, better_btn, same_btn


def start_session(description, audio, image):
    # Generate personalized activities using the stub method
    activities_response = generate_mindfulness_activities(
        description, audio, image
    )
    
    return (
        gr.update(visible=False),  # hide input
        gr.update(visible=True),   # show activities
        gr.update(value=activities_response)  # update activities content
    )


def complete_activities():
    return gr.update(visible=True)  # show feedback drawer


def record_feedback():
    print("✅ Feedback recorded")
    return


with gr.Blocks(title="Time to Recharge") as demo:
    gr.Markdown("## 🌱 Time to recharge")

    with gr.Tabs() as tabs:
        with gr.TabItem("Recharge activities", id="tab_recharge"):
            (input_row, description, audio, image,
             start_button) = create_input_screen()
            (activity_column, activities_content,
             complete_button) = create_activities_screen()
            feedback_drawer, better_btn, same_btn = create_feedback_drawer()

            # Bind session start
            start_button.click(
                fn=start_session,
                inputs=[description, audio, image],
                outputs=[input_row, activity_column, activities_content]
            )

            # Bind activity complete
            complete_button.click(
                lambda: gr.update(visible=True),
                outputs=feedback_drawer
            )

            # Feedback buttons route back to home
            better_btn.click(fn=record_feedback, inputs=[], outputs=[])
            better_btn.click(lambda: [
                gr.update(visible=True),         # show input row
                gr.update(visible=False),        # hide feedback drawer
                gr.update(visible=False),        # hide activity column
                gr.update(selected="tab_recharge")
            ], outputs=[input_row, feedback_drawer, activity_column, tabs])

            same_btn.click(fn=record_feedback, inputs=[], outputs=[])
            same_btn.click(lambda: [
                gr.update(visible=True),
                gr.update(visible=False),
                gr.update(visible=False),
                gr.update(selected="tab_recharge")
            ], outputs=[input_row, feedback_drawer, activity_column, tabs])

        with gr.TabItem("History"):
            gr.Markdown("_No past sessions yet._")

        with gr.TabItem("Favorites"):
            gr.Markdown("_Your favorite activities will appear here._")

# Dev mode launcher
if __name__ == "__main__":
    demo.launch()
