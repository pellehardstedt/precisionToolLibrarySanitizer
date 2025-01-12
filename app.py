import os
import shutil
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def load_env():
    env_path = os.path.join(os.path.dirname(__file__), '.env')
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

def process_folder(folder_path):
    logging.info(f"Processing folder: {folder_path}")
    
    subs_folder = os.path.join(folder_path, 'Subs')
    if os.path.exists(subs_folder):
        for item in os.listdir(subs_folder):
            s = os.path.join(subs_folder, item)
            d = os.path.join(folder_path, item)
            if os.path.isfile(s):
                shutil.move(s, d)
                logging.info(f"Moved file: {s} to {d}")
        
        shutil.rmtree(subs_folder)
        logging.info(f"Removed folder: {subs_folder}")

    extensions = ['.exe', '.txt', '.jpg', '.png', '.nfo']
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    logging.info(f"Deleted file: {file_path}")
                except Exception as e:
                    logging.error(f"Error deleting file {file_path}: {e}")

    for root, dirs, files in os.walk(folder_path):
        for dir in dirs:
            if dir.lower() in ['sample', 'extras', 'screens']:
                dir_path = os.path.join(root, dir)
                try:
                    shutil.rmtree(dir_path)
                    logging.info(f"Removed folder: {dir_path}")
                except Exception as e:
                    logging.error(f"Error deleting folder {dir_path}: {e}")

    video_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.mp4', '.mkv', '.avi'))]
    video_file_basenames = [os.path.splitext(vf)[0].lower() for vf in video_files]
    
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.lower().endswith('.srt'):
                file_basename = os.path.splitext(file)[0].lower()
                if not (file_basename in video_file_basenames or
                        file.lower().startswith('english') or 
                        file.lower().startswith('eng') or 
                        file.lower().startswith('swedish') or 
                        file.lower().startswith('swe') or 
                        file.lower().startswith('svenska')):
                    file_path = os.path.join(root, file)
                    try:
                        os.remove(file_path)
                        logging.info(f"Deleted .srt file: {file_path}")
                    except Exception as e:
                        logging.error(f"Error deleting .srt file {file_path}: {e}")

def main():
    load_env()
    parent_folders = os.getenv('PARENT_FOLDERS')
    if not parent_folders:
        logging.error("Environment variable PARENT_FOLDERS is not set")
        return

    parent_folders = parent_folders.split(';')
    for parent_folder in parent_folders:
        for root, dirs, files in os.walk(parent_folder):
            for dir in dirs:
                process_folder(os.path.join(root, dir))

if __name__ == "__main__":
    main()