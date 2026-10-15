import os
import glob

files = glob.glob(r"G:\trading\guias\analisis\*.py")
print(f"Total Python files: {len(files)}")
for f in sorted(files):
    name = os.path.basename(f)
    if "c_" in name.lower() or "lite" in name.lower() or "character" in name.lower() or "obtener" in name.lower():
        print(f"  {name:35s} size: {os.path.getsize(f):6d} bytes")
