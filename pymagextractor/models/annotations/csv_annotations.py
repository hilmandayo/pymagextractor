import pandas as pd
import pathlib

# TODO: do not use pandas???
class CSVAnnotations:
    def __init__(self, csv_file: str, anns_type="bb"):
        self.csv_file = pathlib.Path(csv_file)
        self.anns_type = anns_type

        if not csv_file.exists():
            header = "frame_id object_id x1, y1, x2, y2"
            csv_file.write_text(f"{header}\n")

    def save(args):
        pass  # save everything into file
