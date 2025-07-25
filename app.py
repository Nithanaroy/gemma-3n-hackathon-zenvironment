import gradio as gr

def echo_message(message):
    """
    Simple function that returns the same message that was sent
    """
    return message

# Create the Gradio interface
def create_interface():
    with gr.Blocks(
        title="Echo Server",
        theme=gr.themes.Soft(),
        css="""
        .container {
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }
        .input-container {
            margin-bottom: 20px;
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin: 20px 0;
        }
        .output-container {
            margin-top: 20px;
        }
        @media (max-width: 768px) {
            .container {
                padding: 10px;
                max-width: 100%;
            }
        }
        """
    ) as demo:
        
        gr.Markdown(
            """
            # 🔄 Echo Server
            ### A simple responsive UI that echoes back your message
            Enter any text below and click the button to see it echoed back!
            """
        )
        
        with gr.Column(elem_classes="container"):
            with gr.Row(elem_classes="input-container"):
                textbox = gr.Textbox(
                    label="Enter your message",
                    placeholder="Type something here...",
                    lines=2,
                    max_lines=5,
                    scale=4
                )
            
            with gr.Row(elem_classes="button-container"):
                submit_btn = gr.Button(
                    "Echo Message",
                    variant="primary",
                    size="lg",
                    scale=1
                )
            
            with gr.Row(elem_classes="output-container"):
                output = gr.Textbox(
                    label="Server Response",
                    interactive=False,
                    lines=2,
                    max_lines=5
                )
        
        # Set up the event handler
        submit_btn.click(
            fn=echo_message,
            inputs=[textbox],
            outputs=[output],
            api_name="echo"
        )
        
        # Also allow Enter key to trigger the echo
        textbox.submit(
            fn=echo_message,
            inputs=[textbox],
            outputs=[output]
        )
    
    return demo

if __name__ == "__main__":
    # Create the interface
    demo = create_interface()
    
    # Launch the app with settings for LAN/WAN access
    demo.launch(
        server_name="0.0.0.0",  # This allows access from other devices on the network
        server_port=7860,       # Default Gradio port
        share=False,            # Set to True if you want a public tunnel via gradio.live
        inbrowser=True,         # Automatically open in browser
        show_error=True,        # Show errors in the interface
        quiet=False             # Show launch messages
    )
