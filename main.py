import os
import engine

sigs_folder = "sigs"
include_folder = os.path.join(sigs_folder, "include")
output_folder = "output"
img_folder = "imgs"

os.makedirs(output_folder, exist_ok=True)

files = [f for f in os.listdir(sigs_folder) if os.path.isfile(os.path.join(sigs_folder, f))]

for file in files:
    filepath = os.path.join(sigs_folder, file)   
    engine.build_sig(file, sigs_folder, include_folder, output_folder, img_folder)

