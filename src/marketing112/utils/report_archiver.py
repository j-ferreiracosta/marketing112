import os
import shutil
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def archive_old_reports(project_root: str):
    """
    Checks for reports in the 'reports' directory and moves them to a sequentially
    numbered folder within 'OldReports'. Creates 'OldReports' if it doesn't exist.
    """
    reports_dir = os.path.join(project_root, "reports")
    old_reports_dir = os.path.join(project_root, "OldReports")

    try:
        # 1. Ensure OldReports directory exists
        os.makedirs(old_reports_dir, exist_ok=True)
        logging.info(f"Ensured 'OldReports' directory exists at: {old_reports_dir}")

        # Check if reports_dir exists and is a directory
        if not os.path.isdir(reports_dir):
            logging.warning(f"'reports' directory not found at: {reports_dir}. Skipping archiving.")
            return

        # 2. Check if there are files in the reports directory
        files_to_move = [f for f in os.listdir(reports_dir) if os.path.isfile(os.path.join(reports_dir, f))]

        if not files_to_move:
            logging.info(f"No files found in '{reports_dir}'. No archiving needed.")
            return

        logging.info(f"Found {len(files_to_move)} files in '{reports_dir}' to archive.")

        # 4. Determine the next folder number in OldReports
        next_folder_num = 1
        try:
            existing_folders = [d for d in os.listdir(old_reports_dir) if os.path.isdir(os.path.join(old_reports_dir, d))]
            numeric_folders = [int(f) for f in existing_folders if f.isdigit()]
            if numeric_folders:
                next_folder_num = max(numeric_folders) + 1
        except Exception as e:
            logging.error(f"Error determining next folder number in '{old_reports_dir}': {e}")
            # Fallback or decide how to handle - perhaps default to 1 or raise error
            # For now, we'll proceed with 1 if error occurs

        target_subdir = os.path.join(old_reports_dir, str(next_folder_num))
        os.makedirs(target_subdir, exist_ok=True)
        logging.info(f"Created target archive subfolder: {target_subdir}")

        # 3. Move files
        for filename in files_to_move:
            source_path = os.path.join(reports_dir, filename)
            destination_path = os.path.join(target_subdir, filename)
            try:
                shutil.move(source_path, destination_path)
                logging.info(f"Moved '{filename}' to '{target_subdir}'")
            except Exception as e:
                logging.error(f"Failed to move '{filename}' from '{reports_dir}' to '{target_subdir}': {e}")

        logging.info("Report archiving process completed.")

    except Exception as e:
        logging.error(f"An error occurred during the report archiving process: {e}")

# Example usage (if run directly, though it's meant to be imported)
if __name__ == '__main__':
    # Assuming the script is in src/marketing112/utils
    # Go up three levels to get the project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(script_dir)))
    print(f"Detected Project Root for standalone test: {project_root_path}")
    archive_old_reports(project_root_path)
