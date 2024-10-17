
import gradio as gr
from scripts.voice2voice import get_rvc_models, find_rvc_model_by_name, get_openvoice_refs

# from silero_tts.silero_tts import SileroTTS


from xtts_webui import *

from i18n.i18n import I18nAuto
i18n = I18nAuto()

with gr.Row():
    with gr.Column():
        with gr.Tab(i18n("Text")):
            text = gr.TextArea(label=i18n("Texto de entrada"),
                               placeholder=i18n("Introduzca el texto aquí..."))
        with gr.Tab(i18n("Lote")):
            batch_generation = gr.Files(
                label=i18n("Subir archivos .txt"), file_types=["text"])
            batch_generation_path = gr.Textbox(
                label=i18n("Ruta a la carpeta con archivos .txt, tiene prioridad sobre todos "), value="")
        with gr.Tab(i18n("Subtítulos")):
            batch_sub_generation = gr.Files(
                label=i18n("Subir archivos srt o ass"), file_types=[".ass",".srt"])
            batch_sub_generation_path = gr.Textbox(
                label=i18n("Ruta a la carpeta con srt o ass, tiene prioridad sobre todas"), value="")
            sync_sub_generation = gr.Checkbox(label=i18n("Sincronizar los tiempos de los subtítulos"),value=False)
        
        with gr.Column():
          voice_engine = gr.Radio(label=i18n("Select Voice Engine"), choices=["XTTS", "SILERO"], value="XTTS", visible=False)
          with gr.Tab("XTTS"):    
            language_auto_detect = gr.Checkbox(
                label=i18n("Habilitar detección automática de idioma"), info=i18n("Si su idioma no es compatible o el texto tiene menos de 20 caracteres, esta función no funcionará."))
            languages = gr.Dropdown(
                label=i18n("Idioma"), choices=reversed_supported_languages_list, value="English")
        
            speed = gr.Slider(
                label=i18n("velocidad"),
                minimum=0.1,
                maximum=2,
                step=0.05,
                value=1,
            )
            with gr.Accordion(i18n("Configuración avanzada"), open=False) as acr:
                temperature = gr.Slider(
                    label=i18n("Temperature"),
                    minimum=0.01,
                    maximum=1,
                    step=0.05,
                    value=0.75,
                )
                length_penalty = gr.Slider(
                    label=i18n("Length Penalty"),
                    minimum=-10.0,
                    maximum=10.0,
                    step=0.5,
                    value=1,
                )
                repetition_penalty = gr.Slider(
                    label=i18n("Repetition Penalty"),
                    minimum=1,
                    maximum=10,
                    step=0.5,
                    value=5,
                )
                top_k = gr.Slider(
                    label=i18n("Top K"),
                    minimum=1,
                    maximum=100,
                    step=1,
                    value=50,
                )
                top_p = gr.Slider(
                    label=i18n("Top P"),
                    minimum=0.01,
                    maximum=1,
                    step=0.05,
                    value=0.85,
                )
                sentence_split = gr.Checkbox(
                    label=i18n("Habilitar división de texto"),
                    value=True,
                )

                # infer_type = gr.Radio(["api", "local"], value="local", label="Type of Processing",
                #                       info="Defines how the text will be processed,local gives you more options. Api does not allow you to use advanced settings")

            speakers_list = XTTS.get_speakers()
            speaker_value = ""
            if not speakers_list:
                speakers_list = ["None"]
                speaker_value = "None"
            else:
                speaker_value = speakers_list[0]
                XTTS.speaker_wav = speaker_value

            with gr.Row():
                ref_speaker_list = gr.Dropdown(
                    label=i18n("Speaker de referencia en la carpeta 'speakers'"), value=speaker_value, choices=speakers_list,allow_custom_value=True)
                show_ref_speaker_from_list = gr.Checkbox(
                    value=False, label=i18n("Mostrar muestra de referencia"), info=i18n("Esta opción le permitirá escuchar su muestra de referencia."))
                show_inbuildstudio_speaker = gr.Checkbox(
                    value=False, label=i18n("Mostrar en lista altavoces disponibles altavoces incorporados"), info=i18n("Esta opción te permitirá agregar voces preparadas previamente de coqui-studio a la lista de voces disponibles."))
                update_ref_speaker_list_btn = gr.Button(
                    value=i18n("Actualizar"), elem_classes="speaker-update__btn")
            ref_speaker_example = gr.Audio(
                label=i18n("Muestra de altavoz"), sources="upload", visible=False, interactive=False)

            with gr.Tab(label=i18n("Single")):
                ref_speaker = gr.Audio(
                    label=i18n("Speaker de referencia (mp3, wav, flac)"), editable=False)
            with gr.Tab(label=i18n("Multiple")):
                ref_speakers = gr.Files(
                    label=i18n("Speaker de referencia (mp3, wav, flac)"), file_types=["audio"])

            with gr.Accordion(label=i18n("Reference Speaker settings."), open=False):
                gr.Markdown(
                    value=i18n("**Nota: las configuraciones solo funcionan cuando se suben archivos**"))
                gr.Markdown(
                    value=i18n("Vea cómo crear buenas muestras [here](https://github.com/daswer123/xtts-api-server?tab=readme-ov-file#note-on-creating-samples-for-quality-voice-cloning)"))
                with gr.Row():
                    use_resample = gr.Checkbox(
                        label=i18n("Remuestrear el audio de referencia a 22050Hz"), info=i18n("Esto es para un mejor procesamiento."), value=True)
                    improve_reference_audio = gr.Checkbox(
                        label=i18n("Limpiar el audio de referencia"), info=i18n("Recortar el silencio, utilizar filtros de paso bajo y paso alto"), value=False)
                    improve_reference_resemble = gr.Checkbox(
                        label=i18n("Resemble enhancement (Utiliza 4GB de VRAM adicionales)"), info=i18n("Se puede configurar en la pesaña 'Configuración de salida'"), value=False)
                auto_cut = gr.Slider(
                    label=i18n("Recortar automáticamente el audio hasta x segundos, 0 sin recortar "),
                    minimum=0,
                    maximum=30,
                    step=1,
                    value=0,
                )
                gr.Markdown(
                    value=i18n("Puede guardar los archivos de audio o la grabación del micrófono en una lista compartida, debe establecer un nombre y hacer clic en guardar"))
                speaker_wav_save_name = gr.Textbox(
                    label=i18n("Guardar nombre del Speaker"), value="new_speaker_name")
                save_speaker_btn = gr.Button(
                    value=i18n("Save a single sample for the speaker"), visible=False)
                save_multiple_speaker_btn = gr.Button(
                    value=i18n("Save multiple samples for the speaker"), visible=False)

          with gr.Tab("Silero", render=False):
                with gr.Column():
                    
                    # Get Data
                    silero_avalible_models = list(SILERO.get_available_models()["ru"])
                    silero_avalible_speakers = list(SILERO.get_available_speakers())
                    silero_avalible_sample_rate = list(SILERO.get_available_sample_rates())
                    
                    print(silero_avalible_speakers)
            
                    silero_language = gr.Dropdown(label=i18n("Language Silero"), choices=["ru", "en", "de", "es", "fr", "ba", "xal", "tt", "uz", "ua", "indic"], value="ru")
                    silero_models = gr.Dropdown(label=i18n("Model"), choices=silero_avalible_models, value=silero_avalible_models[0])
                    with gr.Row():
                        silero_speaker = gr.Dropdown(label=i18n("Speaker"), choices=silero_avalible_speakers, value=silero_avalible_speakers[0])
                    # TODO
                    #     siler_show_speaker_sample = gr.Checkbox(label=i18n("Show sample"),info=i18n("This option will allow you to listen to speaker sample"), value=False, interactive=False)
                    # silero_speaker_sample = gr.Audio(label=i18n("Speaker sample"),visible=False, interactive=False)    
                    
                    silero_sample_rate = gr.Radio(label=i18n("Sample rate"), choices=silero_avalible_sample_rate, value=silero_avalible_sample_rate[-1])
                    silero_device = gr.Radio(label=i18n("Device"),info=i18n("Cpu pretty fast"), choices=["cpu", "cuda:0"], value="cpu")

    with gr.Column():
        status_bar = gr.Label(
            label=i18n("Status bar"), value=i18n("Enter text, select language and speaker, then click Generate"))
        video_gr = gr.Video(label=i18n("Waveform Visual"),
                            visible=False, interactive=False)
        audio_gr = gr.Audio(label=i18n("Synthesised Audio"),
                            interactive=False, autoplay=False)
        generate_btn = gr.Button(
            value=i18n("Generate"), size="lg", elem_classes="generate-btn")

        rvc_models = []
        current_rvc_model = ""
        if RVC_ENABLE:
            # Get RVC models
            rvc_models = []
            current_rvc_model = ""
            rvc_models_full = get_rvc_models(this_dir)
            if len(rvc_models_full) > 1:
                current_rvc_model = rvc_models_full[0]["model_name"]
                for rvc_model in rvc_models_full:
                    rvc_models.append(rvc_model["model_name"])
            # print(rvc_models)

        with gr.Accordion(label=i18n("Configuración de salida"), open=True):
            with gr.Column():
                with gr.Row():
                    enable_waveform = gr.Checkbox(
                        label=i18n("Activar Waveform"), info=i18n("Crear vídeo basado en audio en forma de onda"), value=False)
                    improve_output_audio = gr.Checkbox(
                        label=i18n("Mejorar la calidad de salida"), info=i18n("Reduce el ruido y mejora ligeramente el audio."), value=False)
                    improve_output_resemble = gr.Checkbox(
                        label=i18n("Resemble enhancement"), info=i18n("Utiliza Resemble Enhance para mejorar la calidad del sonido a través de redes neuronales. Utiliza 4 GB de VRAM adicionales"), value=False)
                with gr.Row():
                    improve_output_voice2voice = gr.Radio(label=i18n("Utilice RVC o OpenVoice para mejorar el resultado"), visible=RVC_ENABLE,
                                                          info=i18n("Utiliza RVC para cambiar el tono de voz, asegúrate de tener una carpeta del modelo con el archivo pth dentro de la carpeta voice2voice/rvc"), choices=["RVC", "OpenVoice", "None"], value="None")
                with gr.Accordion(label=i18n("Ajustes Resemble Enhancement"), open=False):
                    enhance_resemble_chunk_seconds = gr.Slider(
                        minimum=2, maximum=40, value=8, step=1, label=i18n("Duración de cada fragmento en segundos (cuantos más segundos, mayor uso de VRAM y mayor velocidad de inferencia)"))
                    enhance_resemble_chunk_overlap = gr.Slider(
                        minimum=0.1, maximum=2, value=1, step=0.2, label=i18n("Overlap seconds (Superposición entre fragmentos en segundos.)"))
                    enhance_resemble_solver = gr.Dropdown(label=i18n("Solucionador de ODE de CFM (se recomienda el punto medio)"), choices=[
                                                          "Midpoint", "RK4", "Euler"], value="Midpoint")
                    enhance_resemble_num_funcs = gr.Slider(
                        minimum=1, maximum=128, value=64, step=1, label=i18n("Número de evaluaciones de funciones de CFM (los valores más altos en general producen una mejor calidad pero pueden ser más lentos)"))
                    enhance_resemble_temperature = gr.Slider(
                        minimum=0, maximum=1, value=0.5, step=0.01, label=i18n("Temperatura previa de CFM (valores más altos pueden mejorar la calidad pero pueden reducir la estabilidad)"))
                    enhance_resemble_denoise = gr.Checkbox(
                        value=True, label=i18n("Reducir ruido antes de mejorar (marcar si el audio contiene mucho ruido de fondo)"))

                with gr.Accordion(label=i18n("OpenVoice settings"), visible=RVC_ENABLE, open=False):
                    open_voice_ref_list = get_openvoice_refs(this_dir)
                    if len(open_voice_ref_list) == 0:
                        open_voice_ref_list = ["None"]

                    gr.Markdown(
                        i18n("**Add samples to the voice2voice/openvoice audio files folder or select from the reference speaker list**"))
                    opvoice_ref_list = gr.Dropdown(
                        label=i18n("Reference sample"), value=open_voice_ref_list[0], choices=open_voice_ref_list)
                    opvoice_show_speakers = gr.Checkbox(
                        value=False, label=i18n("Show choises from the speakers folder"))

                with gr.Accordion(label=i18n("Configuración de RVC"), visible=RVC_ENABLE, open=False):
                    # RVC variables
                    with gr.Row():
                        rvc_settings_model_name = gr.Dropdown(
                            label=i18n("RVC Model name"), info=i18n("Cree una carpeta con el nombre de su modelo en la carpeta rvc y coloque .pth y .index allí, .index opcional"), choices=rvc_models)
                        rvc_settings_update_btn = gr.Button(
                            value=i18n("Actulizar"), elem_classes="rvc_update-btn", visible=True)
                    rvc_settings_model_path = gr.Textbox(
                        label=i18n("RVC Model"), value="", visible=True, interactive=False)
                    rvc_settings_index_path = gr.Textbox(
                        label=i18n("Index file"), value="", visible=True, interactive=False)
                    rvc_settings_pitch = gr.Slider(
                        minimum=-24, maximum=24, value=0, step=1, label=i18n("Pitch"))
                    rvc_settings_index_rate = gr.Slider(
                        minimum=0, maximum=1, value=0.75, step=0.01, label=i18n("Index rate"))
                    rvc_settings_protect_voiceless = gr.Slider(
                        minimum=0, maximum=0.5, value=0.33, step=0.01, label=i18n("Protect voiceless"))
                    rvc_settings_method = gr.Radio(
                        ["crepe", "pm", "rmvpe", "harvest"], value="rmvpe", label=i18n("RVC Method"))
                    rvc_settings_filter_radius = gr.Slider(
                        minimum=0, maximum=7, value=3, step=1, label=i18n("Si >=3: aplicar el filtro de mediana a los resultados de tono obtenidos. El valor representa el radio del filtro y puede reducir la respiración."))
                    rvc_settings_resemple_rate = gr.Slider(
                        minimum=0, maximum=48000, value=0, step=1, label=i18n("Remuestrear el audio de salida en el posprocesamiento a la frecuencia de muestreo final. Establezca en 0 para no volver a muestrear"))
                    rvc_settings_envelope_mix = gr.Slider(
                        minimum=0, maximum=1, value=1, step=0.01, label=i18n("Utilice la envolvente de volumen de la entrada para reemplazar o mezclar con la envolvente de volumen de la salida. Cuanto más cercana sea la relación a 1, más se utiliza la envolvente de salida."))
                with gr.Row():
                    output_type = gr.Radio(
                        ["mp3", "wav"], value="wav", label=i18n("Tipo de salida"))
            additional_text_input = gr.Textbox(
                label=i18n("Valor del nombre del archivo"), value="output")

           # Variables
        speaker_value_text = gr.Textbox(
            label=i18n("Reference Speaker Name"), value=speaker_value, visible=False)
        speaker_path_text = gr.Textbox(
            label=i18n("Reference Speaker Path"), value="", visible=False)
        speaker_wav_modifyed = gr.Checkbox(
            i18n("Reference Audio"), visible=False, value=False)
        speaker_ref_wavs = gr.Text(visible=False)
