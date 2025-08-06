import gradio as gr
import time

from gemma_server import call_gemma, ZEN_IMG_PROMPT, ZEN_IMG_PROMPT_v2

def generate_mindfulness_activities(description, audio, image):
    if image:
        if description:
            message = f"""{description}\n\n{ZEN_IMG_PROMPT_v2}"""
        else:
            message = ZEN_IMG_PROMPT_v2
    elif description:
        message = description
    else:
        raise ValueError("Please provide at least a description or an image.")
    
    response = call_gemma(
        message=message,
        image_path=image,
        conversation_history=[]
    )
    
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
    demo.launch(server_name="0.0.0.0", server_port=7860)
