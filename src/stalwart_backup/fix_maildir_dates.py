import os
from pathlib import Path
from datetime import datetime


root = Path("Maildir/new")

for _, _, files in root.walk():
    for bn in files:
        pth = root / bn
        with open(pth, "r") as f:
            for line in f.readlines():
                if line.startswith("Date:"):
                    sdt = line.strip()
                    if sdt.endswith(")"):
                        i = sdt.index(" (")
                        sdt = sdt[:i]

                    sdt = sdt.replace("lun.", "Mon.")
                    sdt = sdt.replace("mar.", "Tue.")
                    sdt = sdt.replace("mer.", "Wed.")
                    sdt = sdt.replace("jeu.", "Thu.")
                    sdt = sdt.replace("ven.", "Fri.")
                    sdt = sdt.replace("sam.", "Sat.")
                    sdt = sdt.replace("dim.", "Sun.")

                    sdt = sdt.replace("janv.", "Jan")
                    sdt = sdt.replace("f=C3=A9vrier", "Feb")
                    sdt = sdt.replace("mars", "Mar")
                    sdt = sdt.replace("avr.", "Apr")
                    sdt = sdt.replace("mai", "Mar")
                    sdt = sdt.replace("juin", "Jun")
                    sdt = sdt.replace("juillet", "Jul")
                    sdt = sdt.replace("ao=C3=BBt", "Aug")
                    sdt = sdt.replace("septembre", "Sep")
                    sdt = sdt.replace("octobre", "Oct")
                    sdt = sdt.replace("novembre", "Nov")
                    sdt = sdt.replace("d=C3=A9c.", "Dec")
                    if "," in sdt:
                        # Date: Fri, 7 Oct 2022 10:27:28 +0200
                        dt = datetime.strptime(sdt, "Date: %a, %d %b %Y %H:%M:%S %z")
                    else:
                        # Date: mar. 28 mai 2024 =C3=A0 12:42
                        dt = datetime.strptime(sdt, "Date: %a. %d %b %Y =C3=A0 %H:%M")

        os.utime(pth, (dt.timestamp(), dt.timestamp()))
