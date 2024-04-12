
import gradio as gr
from app import demo as app
import os

_docs = {'HighlightedTextLabelDefault': {'description': 'Displays text that contains spans that are highlighted by category or numerical value.\n', 'members': {'__init__': {'value': {'type': 'list[tuple[str, str | float | None]]\n    | dict\n    | Callable\n    | None', 'default': 'None', 'description': 'Default value to show. If callable, the function will be called whenever the app loads to set the initial value of the component.'}, 'color_map': {'type': 'dict[str, str] | None', 'default': 'None', 'description': 'A dictionary mapping labels to colors. The colors may be specified as hex codes or by their names. For example: {"person": "red", "location": "#FFEE22"}'}, 'show_legend': {'type': 'bool', 'default': 'False', 'description': 'whether to show span categories in a separate legend or inline.'}, 'combine_adjacent': {'type': 'bool', 'default': 'False', 'description': 'If True, will merge the labels of adjacent tokens belonging to the same category.'}, 'adjacent_separator': {'type': 'str', 'default': '""', 'description': 'Specifies the separator to be used between tokens if combine_adjacent is True.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component. Appears above the component and is also used as the header if there are a table of examples for this component. If None and used in a `gr.Interface`, the label will be the name of the parameter this component is assigned to.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open. Has no effect otherwise. The event can be accessed (e.g. to cancel it) via this component's .load_event attribute."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative size compared to adjacent Components. For example if Components A and B are in a Row, and A has scale=2, and B has scale=1, A will be twice as wide as B. Should be an integer. scale applies in Rows, and to top-level Components in Blocks where fill_height=True.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value. If a certain scale value results in this Component being narrower than min_width, the min_width parameter will be respected first.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM. Can be used for targeting CSS styles.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context. Should be used if the intention is to assign event listeners now but render the component later.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'If True, the component will be editable, and allow user to select spans of text and label them.'}, 'default_label': {'type': 'str | None', 'default': 'None', 'description': None}}, 'postprocess': {'value': {'type': 'list[tuple[str, str | float | None]] | dict | None', 'description': 'Expects a list of (word, category) tuples, or a dictionary of two keys: "text", and "entities", which itself is a list of dictionaries, each of which have the keys: "entity" (or "entity_group"), "start", and "end"'}}, 'preprocess': {'return': {'type': 'list[tuple[str, str | float | None]] | None', 'description': 'Passes the value as a list of tuples as a `list[tuple]` into the function. Each `tuple` consists of a `str` substring of the text (so the entire text is included) and `str | float | None` label, which is the category or confidence of that substring.'}, 'value': None}}, 'events': {'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the HighlightedTextLabelDefault changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the HighlightedTextLabelDefault. Uses event data gradio.SelectData to carry `value` referring to the label of the HighlightedTextLabelDefault, and `selected` to refer to state of the HighlightedTextLabelDefault. See EventData documentation on how to use this event data'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'HighlightedTextLabelDefault': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_highlightedtextlabeldefault`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.0.1%20-%20orange">  
</div>

Modify the default label when selecting a word in the interactive HighlightedText component.
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_highlightedtextlabeldefault
```

## Usage

```python

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

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `HighlightedTextLabelDefault`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["HighlightedTextLabelDefault"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["HighlightedTextLabelDefault"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes the value as a list of tuples as a `list[tuple]` into the function. Each `tuple` consists of a `str` substring of the text (so the entire text is included) and `str | float | None` label, which is the category or confidence of that substring.
- **As output:** Should return, expects a list of (word, category) tuples, or a dictionary of two keys: "text", and "entities", which itself is a list of dictionaries, each of which have the keys: "entity" (or "entity_group"), "start", and "end".

 ```python
def predict(
    value: list[tuple[str, str | float | None]] | None
) -> list[tuple[str, str | float | None]] | dict | None:
    return value
```
""", elem_classes=["md-custom", "HighlightedTextLabelDefault-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          HighlightedTextLabelDefault: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
