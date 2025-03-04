import gradio as gr
import pandas as pd
from theme_classifier import ThemeClassifier

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

def main():
    with gr.Blocks() as iface:
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

    iface.launch(share=True) 

if __name__ == "__main__":
    main()
