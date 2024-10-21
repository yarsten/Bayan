import os
import pandas as pd
from datasets import load_dataset, Audio

def load_datasets():
    # Load AR dataset
    ar_data_dir = '/kaggle/input/data-ar/AR'
    newar_data = []

    for file_name in os.listdir(ar_data_dir):
        if file_name.endswith('.wav'):
            base_name = os.path.splitext(file_name)[0]
            wav_path = os.path.join(ar_data_dir, file_name)
            txt_path = os.path.join(ar_data_dir, f"{base_name}.txt")
            with open(txt_path, 'r', encoding='utf-8') as f:
                sentence = f.read().strip()  
            newar_data.append({
                'Audio Path': wav_path,
                'Sentence': sentence
            })

    df_ar_data = pd.DataFrame(newar_data)
    print("AR Dataset created successfully.")

    # Load Mozilla dataset
    commonvoice_eval = load_dataset("mozilla-foundation/common_voice_11_0", "ar", split="all", trust_remote_code=True)
    commonvoice_eval = commonvoice_eval.cast_column("audio", Audio(sampling_rate=16000))

    selected_data = []
    for sample in commonvoice_eval:
        audio_array = sample['audio']['array']  
        sampling_rate = sample['audio']['sampling_rate']  
        selected_data.append({
            'Audio Path': sample['audio']['path'], 
            'Sentence': sample.get('sentence', None)  
        })

    df_selected = pd.DataFrame(selected_data)
    print("Mozilla Dataset created successfully.")

    df_combined = pd.concat([df_selected, df_ar_data], ignore_index=True)

    # Load SADA dataset
    sada_data_dir = '/kaggle/input/sada2022'
    train_df = pd.read_csv(os.path.join(sada_data_dir, 'train.csv'))
    test_df = pd.read_csv(os.path.join(sada_data_dir, 'test.csv'))
    valid_df = pd.read_csv(os.path.join(sada_data_dir, 'valid.csv'))

    df_sada = pd.concat([train_df, test_df, valid_df], ignore_index=True)

    df_sada_selected = df_sada[['ProcessedText']].copy()
    df_sada_selected.rename(columns={'ProcessedText': 'Sentence'}, inplace=True)
    df_sada_selected.reset_index(drop=True, inplace=True)
    df_sada_selected['Index'] = df_sada_selected.index

    directory_path = '/kaggle/input/new-sada-roaa/new_sada'

    filenames = os.listdir(directory_path)

    df_filenames = pd.DataFrame({
        'Audio Path': [os.path.join(directory_path, filename) for filename in filenames]
    })

    df_filenames['Index'] = df_filenames['Audio Path'].apply(lambda x: int(x.split('/')[-1].split('_')[0]))

    df_filenames.head() 

    df_sada_selected['Index'] = df_sada_selected['Index'].astype(int)

    merged_df = pd.merge(df_sada_selected, df_filenames, on='Index', how='left')
    merged_df = merged_df.drop(columns='Index')

    merged_df.head()

    Final_df = pd.concat([df_combined, merged_df], ignore_index=True)

    return Final_df

