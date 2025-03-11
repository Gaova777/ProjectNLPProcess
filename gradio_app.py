import gradio as gr
import pandas as pd
from theme_classifier import ThemeClassifier
from character_network import NamedEntityRecognizer, CharacterNetworkGenerator

def get_themes(theme_list, subtitles_path, save_path):
    theme_list = theme_list.split(",")
    theme_classifier = ThemeClassifier(theme_list)
    output_df = theme_classifier.get_theme(subtitles_path, save_path)

    # Remover "dialogue" de la lista de temas
    theme_list = [theme for theme in theme_list if theme != "dialogue"]
    output_df = output_df[theme_list]

    output_df = output_df.sum().reset_index()
    output_df.columns = ["Theme", "Score"]

    print(output_df.head())  

    return output_df

def get_character_network(subtitles_path, ner_path):
    ner = NamedEntityRecognizer()
    ner_df = ner.get_ners(subtitles_path, ner_path)

    character_network_generator = CharacterNetworkGenerator()
    relationship_df = character_network_generator.generate_character_network(ner_df)
    html = character_network_generator.draw_network_graph(relationship_df)

    return html

def main():
    with gr.Blocks() as iface:
        #Theme Classifier Section
        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Theme Classifier</h1>")
                with gr.Row():
                    with gr.Column():
                        plot = gr.BarPlot(
                                x="Theme",
                                y="Score",
                                title="Series Themes",
                                tooltip=["Theme", "Score"],
                                width=500,
                                height=300,
                                color="Theme",
                                grid=True
                            )

                    with gr.Column():
                        theme_list = gr.Textbox(label="Theme List")
                        subtitles_path = gr.Textbox(label="Subtitles or Script Path")
                        save_path = gr.Textbox(label="Save Path")
                        get_themes_button = gr.Button("Get Themes")

                        get_themes_button.click(
                            get_themes, 
                            inputs=[theme_list, subtitles_path, save_path], 
                            outputs=[plot]
                        )

        #Character Network Section

        with gr.Row():
            with gr.Column():
                gr.HTML("<h1>Character Network (NERs and Graph)</h1>")
                with gr.Row():
                    with gr.Column():
                       network_html = gr.HTML()
                    with gr.Column():
                        subtitles_path = gr.Textbox(label="Subtitle or Script Path")
                        ner_path = gr.Textbox(label="NER Path")
                        get_network_graph_button = gr.Button("Get Network Graph")
                        get_network_graph_button.click(
                            get_character_network, 
                            inputs=[subtitles_path, ner_path], 
                            outputs=[network_html]
                        )

    iface.launch(share=True) 

if __name__ == "__main__":
    main()
