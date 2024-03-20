import json
import re
import requests
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import logging
import connfig as conf
import os

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_last_n_words(text, n):
    """Helperfunc: Extract the last n words from a string."""
    words = text.split()
    return " ".join(words[-n:])


def get_model_response(prompt: str) -> str:
    """Send a prompt to the model and get the response."""
    data = {"top_k": conf.TOP_K, "max_length": conf.MAX_LENGTH, "instances": [prompt]}
    try:
        response = requests.post(conf.MODEL_URL, data=json.dumps(data))
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"An error occurred: {str(e)}")
        return ""
    return response.text


def create_header(name: str, app: dash.Dash) -> dbc.Row:
    """Create header component."""
    title = html.H1(name, style={"margin-top": 5})
    logo = html.Img(
        src=app.get_asset_url("prokube-logo-positive.png"),
        style={"float": "right", "height": 30, "margin-top": 20},
    )
    return dbc.Row([dbc.Col(title, md=8), dbc.Col(logo, md=4)])


def create_textbox(app, text, box="AI"):
    text = text.replace("[INST]", "").replace("[/INST]", "")
    style = {
        "max-width": "60%",
        "width": "max-content",
        "padding": "5px 10px",
        "border-radius": 25,
        "margin-bottom": 20,
    }

    if box == "user":
        style["margin-left"] = "auto"
        style["margin-right"] = 0

        return dbc.Card(text, style=style, body=True, color="primary", inverse=True)

    elif box == "AI":
        style["margin-left"] = 0
        style["margin-right"] = "auto"

        thumbnail = html.Img(
            src=app.get_asset_url("prokube-llama.png"),
            style={
                "border-radius": 50,
                "height": 36,
                "margin-right": 5,
                "float": "left",
            },
        )
        textbox_comp = dbc.Card(
            text, style=style, body=True, color="light", inverse=False
        )

        return html.Div([thumbnail, textbox_comp])


def create_conversation_component() -> html.Div:
    """Create conversation display component."""
    return html.Div(
        html.Div(id="display-conversation"),
        style={
            "overflow-y": "auto",
            "display": "flex",
            "height": "calc(90vh - 132px)",
            "flex-direction": "column-reverse",
        },
    )


def create_controls_component() -> dbc.InputGroup:
    """Create user input controls component."""
    return dbc.InputGroup(
        children=[
            dbc.Input(
                id="user-input", placeholder="Write to the chatbot...", type="text"
            ),
            dbc.Button("Submit", id="submit"),
        ]
    )


def create_app_layout(app: dash.Dash) -> dbc.Container:
    """Create and configure the app layout."""
    return dbc.Container(
        fluid=False,
        children=[
            create_header("Talk to prokube's Llama!", app),
            html.Hr(),
            dcc.Store(id="store-conversation", data=""),
            create_conversation_component(),
            create_controls_component(),
            dbc.Spinner(html.Div(id="loading-component")),
        ],
    )


def register_callbacks(app: dash.Dash) -> None:
    """Register app callbacks."""

    @app.callback(
        Output("display-conversation", "children"),
        [Input("store-conversation", "data")],
    )
    def update_display(chat_history: str):
        return [
            create_textbox(app, x, box="user")
            if i % 2 == 0
            else create_textbox(app, x, box="AI")
            for i, x in enumerate(chat_history.split("<split>")[:-1])
        ]

    @app.callback(
        Output("user-input", "value"),
        [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
    )
    def clear_input(n_clicks, n_submit):
        return ""

    @app.callback(
        [Output("store-conversation", "data"), Output("loading-component", "children")],
        [Input("submit", "n_clicks"), Input("user-input", "n_submit")],
        [State("user-input", "value"), State("store-conversation", "data")],
    )
    def run_chatbot(n_clicks, n_submit, user_input, chat_history):
        if n_clicks == 0 and n_submit is None:
            return "", None

        if user_input is None or user_input == "":
            return chat_history, None

        # add new query to chat history
        chat_history = f"{chat_history} [INST] {user_input} [/INST]<split>"
        # stick together sys prompt and chat history
        model_in = conf.SYSTEM_PROMPT + chat_history.replace("<split>", "\n")
        # reduce to the last 3000 words
        model_in = get_last_n_words(model_in, conf.MAX_HISTORY_WORDS)
        # get resonse from api
        model_answer = get_model_response(model_in)
        model_answer = re.split("]\n", model_answer)[-1]
        # model answer to chat_history
        chat_history = f"{chat_history} {model_answer}<split>"

        return chat_history, None


# Main block
if __name__ == "__main__":
    app_instance = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.BOOTSTRAP],
        url_base_pathname=os.getenv("NB_PREFIX", "") + "/",
        suppress_callback_exceptions=True,
    )
    app_instance.layout = create_app_layout(app_instance)
    register_callbacks(app_instance)
    app_instance.run(debug=True, host="0.0.0.0", port=8888)
