import os
import subprocess

import pandas as pd
import numpy as np


class RPEventGen:

    def __init__(self):
        SHEET_ID = '134iAr6fepLq1cBAhyAyNkX3RCvbDwclhHsMx_tVtgtY'
        SHEET_NAME = 'DATA'
        url = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}'
        df = pd.read_csv(url)

        self.max_id = int(max(df['slot id'].tolist()))
        self.max_event_pages = (self.max_id // 30) + 1

        self.track_list = list(dict.fromkeys(df['track file'].tolist()))

        self.slots = []
        entries = []
        for i in range(len(df)):
            if np.isnan(df.at[i, 'volume (%)']):
                break

            if not np.isnan(df.at[i, 'slot id']) and i > 0:
                self.slots.append(entries)
                entries = []

            track_file = df.at[i, 'track file']
            volume = int(df.at[i, 'volume (%)'])
            speed = int(df.at[i, 'speed (%)'])
            if not np.isnan(df.at[i, 'Unlock skill']):
                condition = "record misc:%d" % (int(df.at[i, 'Unlock skill']))
            elif not np.isnan(df.at[i, 'Map id']):
                condition = "map progress:%d" % (int(df.at[i, 'Map id']))
            else:
                condition = "no condition"

            entries.append([condition, track_file, volume, speed])

        if len(entries) > 0:
            self.slots.append(entries)

        self.header = ""
        with open("emu_data/header.txt", "r") as fd:
            self.header = ''.join(fd.readlines())

        self.footer = ""
        with open("emu_data/footer.txt", "r") as fd:
            self.footer = ''.join(fd.readlines())

        self.play_event_header = ""
        with open("emu_data/play_event_header.txt", "r") as fd:
            self.play_event_header = ''.join(fd.readlines())

        self.play_event_footer = ""
        with open("emu_data/play_event_footer.txt", "r") as fd:
            self.play_event_footer = ''.join(fd.readlines())

        self.condition_clause_base = []
        with open("emu_data/condition_clause.txt", "r") as fd:
            self.condition_clause_base = fd.readlines()

        self.play_clause_base = []
        with open("emu_data/play_clause.txt", "r") as fd:
            self.play_clause_base = fd.readlines()

        self.play_clause_footer = ""
        with open("emu_data/play_clause_footer.txt", "r") as fd:
            self.play_clause_footer = ''.join(fd.readlines())

        self.slot_update_header = ""
        with open("emu_data/slot_update_header.txt", "r") as fd:
            self.slot_update_header = ''.join(fd.readlines())

        self.slot_update_footer = ""
        with open("emu_data/slot_update_footer.txt", "r") as fd:
            self.slot_update_footer = ''.join(fd.readlines())

        self.slot_update_clause = []
        with open("emu_data/slot_update_clause.txt", "r") as fd:
            self.slot_update_clause = fd.readlines()

        self.preloading_header = ""
        with open("emu_data/preloading_header.txt", "r") as fd:
            self.preloading_header = ''.join(fd.readlines())

        self.track_loading = ""
        with open("emu_data/track_loading.txt", "r") as fd:
            self.track_loading = ''.join(fd.readlines())

        self.preloading_footer = ""
        with open("emu_data/preloading_footer.txt", "r") as fd:
            self.preloading_footer = ''.join(fd.readlines())

        self.picture_loading = ""
        with open("emu_data/picture_loading.txt", "r") as fd:
            self.picture_loading = ''.join(fd.readlines())

        self.preloading_middle = ""
        with open("emu_data/preloading_middle.txt", "r") as fd:
            self.preloading_middle = ''.join(fd.readlines())

        self.track_unlock_header = ""
        with open("emu_data/track_unlock_header.txt", "r") as fd:
            self.track_unlock_header = ''.join(fd.readlines())

        self.track_unlock_footer = ""
        with open("emu_data/track_unlock_footer.txt", "r") as fd:
            self.track_unlock_footer = ''.join(fd.readlines())

        self.track_unlock_clause = []
        with open("emu_data/track_unlock_clause.txt", "r") as fd:
            self.track_unlock_clause = fd.readlines()

        self.play_sorted_header = ""
        with open("emu_data/play_sorted_header.txt", "r") as fd:
            self.play_sorted_header = ''.join(fd.readlines())

        self.play_sorted_clause = ""
        with open("emu_data/play_sorted_clause.txt", "r") as fd:
            self.play_sorted_clause = ''.join(fd.readlines())

        self.wait_0 = ""
        with open("emu_data/wait_0.txt", "r") as fd:
            self.wait_0 = ''.join(fd.readlines())

    def play_slot(self, index):
        if index >= len(self.slots):
            return ""

        slot_id = index
        event = "       <EventCommand>\n        <code>12010</code>\n        <indent>0</indent>\n        " \
                "<string></string>\n        <parameters>1 1 0 %d 0 0</parameters>\n       </EventCommand>\n" % (slot_id)

        slot = self.slots[index]

        last_entry = slot[len(slot) - 1]
        condition = last_entry[0].split(':')
        condition_value = condition[1]
        cond_number = 2
        if condition[0] == "map progress":
            cond_number = 2
        elif condition[0] == "record misc":
            cond_number = 3
        elif condition[0] == "no condition":
            condition_value = 1

        has_unconditional = False
        for entry in slot:
            if entry[0].split(':')[0] == "no condition":
                has_unconditional = True
                break

        condition_clause = ""
        indent = len(slot)
        if not has_unconditional:
            condition_clause = ''.join(self.condition_clause_base) % (
                indent, cond_number, int(condition_value), indent + 1, indent, indent + 1, indent + 1, indent)
            condition_clause += "\n"

            condition_up = ''.join(self.condition_clause_base[:18])
            condition_down = ''.join(self.condition_clause_base[24:])

            for entry_idx in reversed(range(0, len(slot) - 1)):
                entry = slot[entry_idx]

                condition = entry[0].split(':')
                cond_number = 2
                condition_value = 1
                if condition[0] != "no condition":
                    if condition[0] == "map progress":
                        cond_number = 2
                    elif condition[0] == "record misc":
                        cond_number = 3
                    condition_value = int(condition[1])

                indent = entry_idx + 1  # must be 1 in the last loop

                old_condition_clause = condition_clause
                condition_clause = condition_up % (indent, cond_number, int(condition_value), indent + 1, indent)
                condition_clause += old_condition_clause
                condition_clause += condition_down % (indent + 1, indent)
                condition_clause += "\n"

            event += condition_clause

        event += "       <EventCommand>\n        <code>12410</code>\n        <indent>1</indent>\n        " \
                 "<string>----------------</string>\n        <parameters></parameters>\n       </EventCommand>\n"

        event += ''.join(self.play_clause_base[:12]) % (len(slot))

        def play_clause(stack):
            if stack >= len(slot):
                return ""

            [filename, volume, speed] = slot[stack][1:4]
            entry_condition = slot[stack][0].split(':')
            condition_value = 1
            condition_category = entry_condition[0]
            cond_number_stack = 2
            if condition_category != "no condition":
                if condition_category == "map progress":
                    cond_number_stack = 2
                elif condition_category == "record misc":
                    cond_number_stack = 3
                condition_value = int(entry_condition[1])

            indent_ = stack + 1

            result = ''.join(self.play_clause_base[12:24]) % (indent_, stack, indent_ + 1)

            if stack == 0:
                result += ''.join(self.play_clause_base[24:36]) % (indent_ + 1, indent_ + 1)

            result += ''.join(self.play_clause_base[36:42]) % (indent_ + 1)

            if condition_category != "no condition":
                result += ''.join(self.play_clause_base[42:84]) % (
                    indent_ + 1, cond_number_stack, condition_value, indent_ + 2, filename, int(volume), int(speed),
                    indent_ + 2, indent_ + 1, indent_ + 2, indent_ + 2, indent_ + 1)
            else:
                result += ''.join(self.play_clause_base[48:54]) % (indent_ + 1, filename, int(volume), int(speed))

            result += ''.join(self.play_clause_base[84:96]) % (indent_ + 1, indent_)

            # self.play_clause_base % (len(slot), indent, stack, indent + 1, indent + 1,  indent + 1,  indent + 1,
            # indent + 1, condition[0], condition[1], indent + 2 (+1 only if no condition), filename, volume, speed,
            # indent + 2, indent + 1, indent + 2, indent + 2, indent + 1, indent + 1, indent, indent + 1, indent + 1,
            # indent)

            result += play_clause(stack + 1)

            result += ''.join(self.play_clause_base[102:]) % (indent_ + 1, indent_)
            result += "\n"

            return result

        event += play_clause(0)

        event += self.play_clause_footer
        event += "\n"

        return event

    def slot_update(self, it):
        if it > self.max_event_pages:
            return ""

        indent = it + 3
        result = ''.join(self.slot_update_clause[:24]) % (indent, it * 30, indent + 1, it, indent + 1, indent)

        result += self.slot_update(it + 1)

        result += ''.join(self.slot_update_clause[30:]) % (indent + 1, indent)
        result += "\n"

        return result

    def preloading(self):
        result = self.preloading_header
        result += "\n"

        index = 0
        space_between_waits = (len(self.slots) // 100) + 1

        for track in self.track_list:
            if index % space_between_waits == 0:
                result += self.wait_0
                result += "\n"

            index += 1

            result += self.track_loading % (track)
            result += "\n"

        result += "       <EventCommand>\n        <code>12410</code>\n        <indent>0</indent>\n        " \
                  "<string>---------------------------</string>\n        <parameters></parameters>\n       " \
                  "</EventCommand>\n"

        for x in range(len(self.slots)):
            for y in range(len(self.slots[x])):
                if index % space_between_waits == 0:
                    result += self.wait_0
                    result += "\n"

                index += 1

                string_id = str(1000000 + (x * 100 + y))[1:]
                result += self.picture_loading % ("background", string_id, "0")
                result += "\n"

        result += self.preloading_middle
        result += "\n"

        for x in range(len(self.slots)):
            for y in range(len(self.slots[x])):
                if index % space_between_waits == 0:
                    result += self.wait_0
                    result += "\n"

                index += 1

                string_id = str(1000000 + (x * 100 + y))[1:]
                result += self.picture_loading % ("description", string_id, "1")
                result += "\n"

        result += self.preloading_footer
        result += "\n"

        return result

    def track_unlock_slot(self, index):
        if index >= len(self.slots):
            return ""

        result = ''.join(self.track_unlock_clause[:6]) % (index)

        entries = self.slots[index]
        for entry in entries:
            condition = entry[0].split(':')
            cond_number = 0
            if condition[0] == "map progress":
                cond_number = 2
            elif condition[0] == "record misc":
                cond_number = 3

            if cond_number == 0:
                result += ''.join(self.track_unlock_clause[12:18])
            else:
                result += ''.join(self.track_unlock_clause[6:48]) % (cond_number, int(condition[1]))

        result += ''.join(self.track_unlock_clause[48:])
        result += "\n"

        return result

    def generate(self, filename):
        if os.path.exists(filename):
            os.remove(filename)

        with open(filename, "w") as fd:
            contents = self.header % (self.max_id)
            contents += "\n"

            # play event
            contents += "   <Event id=\"0007\">\n    <name>play</name>\n    <x>0</x>\n    <y>2</y>\n    <pages>\n"

            for page in range(1, self.max_event_pages + 1):
                contents += self.play_event_header % (str(page + 10000)[1::], (page - 1) * 30, (page * 30) - 1)
                contents += "\n"

                for slot_idx in range((page - 1) * 30, page * 30):
                    contents += self.play_slot(slot_idx)

                contents += self.play_event_footer
                contents += "\n"

            contents += "    </pages>\n   </Event>\n"

            # slot update event
            contents += self.slot_update_header
            contents += "\n"

            contents += self.slot_update(1)

            contents += self.slot_update_footer
            contents += "\n"

            # preloading
            contents += self.preloading()

            # track unlock check
            contents += "<Event id=\"0018\">\n    <name>Track unlock check</name>\n    <x>0</x>\n    <y>7</y>\n    " \
                        "<pages>"

            for page in range(1, self.max_event_pages + 1):
                contents += self.track_unlock_header % (str(page + 10000)[1::], (page - 1) * 30, (page * 30) - 1)
                contents += "\n"

                for slot_idx in range((page - 1) * 30, page * 30):
                    contents += self.track_unlock_slot(slot_idx)

                contents += self.track_unlock_footer
                contents += "\n"

            contents += "    </pages>\n   </Event>\n"

            # play sorted
            contents += self.play_sorted_header
            contents += "\n"

            for i in range(1, self.max_event_pages + 1):
                contents += self.play_sorted_clause % (i * 30, i)
                contents += "\n"

            contents += "      </event_commands>\n    </EventPage>\n    </pages>\n   </Event>\n"

            # remaining
            contents += self.footer

            fd.seek(0)
            fd.writelines(contents)

        lmu_path = filename[:-3]
        lmu_path += "lmu"

        print(lmu_path)

        if os.path.exists(lmu_path):
            os.remove(lmu_path)

        subprocess.call(["lcf2xml.exe", filename])


generator = RPEventGen()
generator.generate("Map0007.emu")

#%%
