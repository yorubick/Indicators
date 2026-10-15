# Check what branch gives C = 62 in PoiSzn_C_Deterministic_Lab_v4.pine
lines = open('C:/Users/PC/.gemini/antigravity/brain/0d7f3bfd-8524-49c4-8cc4-be41c8fbcb27/scratch/PoiSzn_C_Deterministic_Lab_v4.pine').readlines()

for i, l in enumerate(lines, 1):
    if 'c_auto :=' in l or 'branch_name :=' in l:
        print(f"{i}: {l.strip()}")
