import os
import hashlib

def generate_addons_xml():
    addons_xml = u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<addons>\n"

    for addon in sorted(os.listdir("./addons")):
        if not os.path.isdir(os.path.join("./addons", addon)):
            continue

        try:
            addon_xml_path = os.path.join("./addons", addon, "addon.xml")
            with open(addon_xml_path, "r", encoding="UTF-8") as f:
                addon_xml = f.read().strip()

            # Remove the XML declaration if it exists
            if addon_xml.startswith('<?xml'):
                addon_xml = addon_xml.split("?>", 1)[1].strip()

        except Exception as e:
            print(f"Excluding {addon} for error: {e}")
            continue

        addons_xml += f"{addon_xml}\n\n"

    addons_xml = addons_xml.strip() + u"\n</addons>\n"

    with open("addons.xml", "w", encoding="UTF-8") as f:
        f.write(addons_xml)

    md5_hash = hashlib.md5(addons_xml.encode("UTF-8")).hexdigest()
    with open("addons.xml.md5", "w", encoding="UTF-8") as f:
        f.write(md5_hash)

if __name__ == "__main__":
    generate_addons_xml()
