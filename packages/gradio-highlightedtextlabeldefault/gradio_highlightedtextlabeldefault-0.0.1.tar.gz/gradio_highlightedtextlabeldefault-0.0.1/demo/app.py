
import gradio as gr
from gradio_highlightedtextlabeldefault import HighlightedTextLabelDefault


example = HighlightedTextLabelDefault().example_value()

with gr.Blocks() as demo:
    with gr.Row():
        test_1 = HighlightedTextLabelDefault(value=([("Hello, my name is Slim Shady.", None)]),
                                             label="Double click word to see standard default label", interactive=True)  # default label
        test_2 = HighlightedTextLabelDefault(value=([("Hello, my name is Slim Shady.", None)]), label="Double click word to see modified default label",
                                             interactive=True, default_label="x", color_map={"x": "green"})  # blank component


if __name__ == "__main__":
    demo.launch()
