import gradio as gr
from xtts_webui import *

from i18n.i18n import I18nAuto
i18n = I18nAuto()

with gr.Tab(i18n("Translate")):
    with gr.Row():
        with gr.Column():
            with gr.Tab(i18n("Single")):
                translate_audio_single = gr.Audio(
                    label=i18n("Single file"), value=None)
            # LATER
            with gr.Tab(i18n("Batch")):
                gr.Markdown(i18n("Work in progress..."))
                with gr.Column(visible=False):
                    translate_audio_batch = gr.File(
                        file_count="multiple", label=i18n("Batch files"), file_types=["audio"])
                    translate_audio_batch_path = gr.Textbox(
                        label=i18n("Path to folder with audio files (High priority)"), value=None)
            with gr.Column():
                translate_whisper_model = gr.Dropdown(label=i18n("Whisper Model"), choices=[
                                                      "small", "medium", "large-v2", "large-v3"], value="large-v3")
                translate_audio_mode = gr.Radio(label=i18n("Mode"), choices=[
                                                1, 2,3], value=2, info=i18n("Mode Desk"))
                translate_translator = gr.Radio(label=i18n("Translator"), choices=[
                                                "google", "bing", "baidu"], value="google")
                
                deepl_auth_key_textbox = gr.Textbox(label="Deepl API Key", value="",type="password",visible=False)
                
                with gr.Row():
                    translate_num_sent = gr.Slider(label=i18n("Número de oraciones que se expresarán a la vez"),minimum=1,maximum=6,step=1,visible=True)
                    translate_max_reference_seconds= gr.Slider(label=i18n("Número de segundos de referencia que se utilizarán"),minimum=10,maximum=600,value=20,step=1,visible=True)
                with gr.Row():
                    sync_with_original_checkbox = gr.Checkbox(label=i18n("Sincronización de tiempo con el original (precisión ~ 80 - 90%)"), value=False)
                with gr.Accordion(label=i18n("Configuración de subtítulos")):
                    with gr.Row():
                        max_width_sub_v2v = gr.Slider(label=i18n("Ancho máximo por línea"), minimum=1, maximum=100, value=40, step=1)
                        max_line_sub_v2v = gr.Slider(label=i18n("Línea máxima"),visible=True, minimum=1, maximum=20, value=2, step=1)
                    with gr.Row():
                        highlight_words_v2v = gr.Checkbox(label=i18n("Resaltar palabras"),visible=False, value=False)
                # speakers_list = XTTS.get_speakers()
                # speaker_value = ""
                # if not speakers_list:
                #     speakers_list = ["None"]
                #     speaker_value = "None"
                # else:
                #     speaker_value = speakers_list[0]
                #     XTTS.speaker_wav = speaker_value

                # translate_ref_speaker_list = gr.Dropdown(
                #     label=i18n("Reference Speaker from folder 'speakers'"), value=speaker_value, choices=speakers_list)
                # translate_show_ref_speaker_from_list = gr.Checkbox(
                #     value=False, label=i18n("Show reference sample"), info=i18n("This option will allow you to listen to your reference sample"))
                # translate_update_ref_speaker_list_btn = gr.Button(
                #         value=i18n("Update"), elem_classes="speaker-update__btn")
                # translate_ref_speaker_example = gr.Audio(
                #     label=i18n("speaker sample"), sources="upload", visible=False, interactive=False)
                
                with gr.Column():
                    with gr.Row():
                        translate_ref_speaker_list = gr.Dropdown(
                            label=i18n("Reference Speaker from folder 'speakers'"), visible=False)
                        translate_show_ref_speaker_from_list = gr.Checkbox(
                            value=False, label=i18n("Show reference sample"),visible=False, info=i18n("This option will allow you to listen to your reference sample"))
                        translate_update_ref_speaker_list_btn = gr.Button(
                                value=i18n("Update"),visible=False, elem_classes="speaker-update__btn")
                    translate_ref_speaker_example = gr.Audio(
                        label=i18n("speaker sample"), sources="upload", visible=False, interactive=False)
                
                with gr.Row():
                    translate_source_lang = gr.Text(
                        value="auto", label=i18n("Ingrese el código de idioma del idioma de origen, si desea definirlo automáticamente, escriba 'auto'"))
                    translate_target_lang = gr.Dropdown(
                        label=i18n("Idioma de destino"), choices=supported_languages_list, value="ru")
                    translate_speaker_lang = gr.Dropdown(
                        label=i18n("Acento del Speaker "), choices=supported_languages_list, value="ru")
                with gr.Column():
                    with gr.Accordion("Whisper settings",open=False):
                        with gr.Row():
                            # translate_whisper_model = gr.Dropdown(label=i18n("Whisper Model"), choices=["small", "medium", "large-v2", "large-v3"], value="medium")
                            translate_whisper_compute_time = gr.Radio(label="Compute Type",choices=["int8","float16"],value="float16",info="Cambie a 'int8' si tiene poca memoria en la GPU (puede reducir la precisión)")
                            translate_whisper_device = gr.Radio(label="Device",choices=["cuda","cpu"],value="cuda",info="Cambie a 'CPU' si no tiene GPU con CUDA (puede reducir la precisión)")
                        with gr.Row():
                            translate_whisper_batch_size = gr.Slider(label="Batch Size", minimum=1, maximum=32, value=8, step=1,info="reducir si hay poca memoria")
                            translate_whisper_aline = gr.Checkbox(value=True,label="Alinear la salida del whisper")
                with gr.Column():
                  with gr.Accordion(i18n("XTTS settings"), open=False,visible=True):
                    translate_speed = gr.Slider(
                        label=i18n("Speed"),
                        minimum=0.5,
                        maximum=2,
                        step=0.01,
                        value=1,
                    )
                    translate_temperature = gr.Slider(
                        label=i18n("Temperature"),
                        minimum=0.01,
                        maximum=1,
                        step=0.05,
                        value=0.75,
                    )
                    translate_length_penalty = gr.Slider(
                        label=i18n("Length Penalty"),
                        minimum=-10.0,
                        maximum=10.0,
                        step=0.5,
                        value=1,
                    )
                    translate_repetition_penalty = gr.Slider(
                        label=i18n("Repetition Penalty"),
                        minimum=1,
                        maximum=10,
                        step=0.5,
                        value=5,
                    )
                    translate_top_k = gr.Slider(
                        label=i18n("Top K"),
                        minimum=1,
                        maximum=100,
                        step=1,
                        value=50,
                    )
                    translate_top_p = gr.Slider(
                        label=i18n("Top P"),
                        minimum=0.01,
                        maximum=1,
                        step=0.05,
                        value=0.85,
                    )
                    translate_sentence_split = gr.Checkbox(
                        label=i18n("Habilitar división de texto"),
                        value=False,
                    )
                    
        with gr.Column():
            translate_status_bar = gr.Label(
                value=i18n("Seleccione el idioma de destino, el modo y cargue el audio, luego presione el botón traducir."))
            translate_video_output = gr.Video(
                label=i18n("Mp4 Translate"), value=None, interactive=False,visible=False)
            translate_voice_output = gr.Audio(
                label=i18n("Result"), value=None, interactive=False)
            translate_files_output = gr.Files(label=i18n("Subtitles"),interactive=False)
            with gr.Accordion(i18n("Modo traducir")):
              with gr.Tab(i18n("Modo simple")):
                translate_btn = gr.Button(value=i18n("Translate"))
              with gr.Tab(i18n("Modo avanzado")):
                translate_advance_stage1_btn = gr.Button(value=i18n("Paso 1 – Transcribir, traducir y editar el texto"))
                translate_advance_stage1_text = gr.TextArea(label=i18n("Texto traducido"),value=None,visible=False)
                translate_advance_stage2_btn = gr.Button(value=i18n("Etapa 2 - Texto de voz"),visible=False)
                transalte_advance_markdown = gr.Markdown(i18n("Trabajo en progreso..."),visible=False)

if RVC_ENABLE:
  with gr.Tab("RVC"):
    with gr.Row():
        with gr.Column():
            with gr.Tab(i18n("Single")):
                rvc_audio_single = gr.Audio(
                    label=i18n("Single file"), value=None)
            with gr.Tab(i18n("Batch")):
                rvc_audio_batch = gr.File(
                    file_count="multiple", label=i18n("Batch files"), file_types=["audio"])
                rvc_audio_batch_path = gr.Textbox(
                    label=i18n("Path to folder with audio files (High priority)"), value=None)
            with gr.Column():
                with gr.Row():
                    rvc_voice_settings_output_type = gr.Radio(
                        ["wav", "mp3"], value="wav", label=i18n("Output type"))
                    rvc_voice_settings_model_name = gr.Dropdown(
                        label=i18n("RVC Model name"), info=i18n("Create a folder with your model name in the rvc folder and put .pth and .index there , .index optional"), choices=rvc_models)
                    rvc_voice_settings_update_btn = gr.Button(
                        value=i18n("Update"), elem_classes="rvc_update-btn", visible=True)
                rvc_voice_settings_model_path = gr.Textbox(
                    label=i18n("RVC Model"), value="", visible=True, interactive=False)
                rvc_voice_settings_index_path = gr.Textbox(
                    label=i18n("Index file"), value="", visible=True, interactive=False)
                rvc_voice_settings_pitch = gr.Slider(
                    minimum=-24, maximum=24, value=0, step=1, label=i18n("Pitch"))
                rvc_voice_settings_index_rate = gr.Slider(
                    minimum=0, maximum=1, value=0.75, step=0.01, label=i18n("Index rate"))
                rvc_voice_settings_protect_voiceless = gr.Slider(
                    minimum=0, maximum=0.5, value=0.33, step=0.01, label=i18n("Protect voiceless"))
                rvc_voice_settings_method = gr.Radio(
                    ["crepe", "pm", "rmvpe", "harvest"], value="rmvpe", label=i18n("RVC Method"))
                rvc_voice_filter_radius = gr.Slider(
                    minimum=0, maximum=7, value=3, step=1, label=i18n("If >=3: apply median filtering to the harvested pitch results. The value represents the filter radius and can reduce breathiness."))
                rvc_voice_resemple_rate = gr.Slider(
                    minimum=0, maximum=48000, value=0, step=1, label=i18n("Resample the output audio in post-processing to the final sample rate. Set to 0 for no resampling"))
                rvc_voice_envelope_mix = gr.Slider(
                    minimum=0, maximum=1, value=1, step=0.01, label=i18n("Use the volume envelope of the input to replace or mix with the volume envelope of the output. The closer the ratio is to 1, the more the output envelope is used"))
        with gr.Column():
            rvc_voice_status_bar = gr.Label(
                value=i18n("Choose model and click Infer button"))
            rvc_video_output = gr.Video(
                label=i18n("Waveform RVC"), value=None, interactive=False, visible=False)
            rvc_voice_output = gr.Audio(
                label=i18n("Result"), value=None, interactive=False)
            rvc_voice_infer_btn = gr.Button(value=i18n("Infer"))

if RVC_ENABLE:
  with gr.Tab("OpenVoice"):
    with gr.Row():
        with gr.Column():
            with gr.Tab(i18n("Single")):
                openvoice_audio_single = gr.Audio(
                    label="Single file", value=None)
            with gr.Tab(i18n("Batch")):
                openvoice_audio_batch = gr.File(
                    file_count="multiple", label=i18n("Batch files"), file_types=["audio"])
                openvoice_audio_batch_path = gr.Textbox(
                    label=i18n("Path to folder with audio files (High priority)"), value=None)
            with gr.Column():
                openvoice_voice_ref_list = get_openvoice_refs(this_dir)

                if len(openvoice_voice_ref_list) == 0:
                    openvoice_voice_ref_list = ["None"]

                gr.Markdown(
                    i18n("**Add samples to the voice2voice/openvoice audio files folder or select from the reference speaker list**"))
                with gr.Row():
                    opvoice_voice_ref_list = gr.Dropdown(
                        label=i18n("Reference sample"), value=openvoice_voice_ref_list[0], choices=openvoice_voice_ref_list)
                    opvoice_voice_show_speakers = gr.Checkbox(
                        value=False, label=i18n("Show choises from the speakers folder"))
        with gr.Column():
            openvoice_status_bar = gr.Label(
                value=i18n("Choose reference and click Infer button"))
            openvoice_video_output = gr.Video(
                label=i18n("Waveform OpenVoice"), value=None, interactive=False, visible=False)
            openvoice_voice_output = gr.Audio(
                label=i18n("Result"), value=None, interactive=False)
            openvoice_voice_infer_btn = gr.Button(value=i18n("Infer"))
